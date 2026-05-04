import asyncio
import aiohttp
import ssl
import certifi
import logging
import os
import json
import io
from datetime import datetime, timezone, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN     = os.getenv("BOT_TOKEN", "")
MAKER_FEE     = float(os.getenv("MAKER_FEE", "0.0002"))   # 0.02% MEXC
TAKER_FEE     = float(os.getenv("TAKER_FEE", "0.0006"))   # 0.06% MEXC
SPOT_FEE      = float(os.getenv("SPOT_FEE", "0.001"))     # 0.1% spot moyen
SLIPPAGE      = float(os.getenv("SLIPPAGE", "0.0005"))    # 0.05% slippage estimé
# ──────────────────────────────────────────────────────────────────────────────


def _ssl_ctx():
    return ssl.create_default_context(cafile=certifi.where())


async def fetch_funding_history(session, symbol: str, days: int) -> list[dict]:
    """Récupère l'historique funding MEXC pour N jours."""
    url = f"https://contract.mexc.com/api/v1/contract/funding_rate/history"
    all_data = []
    page = 1
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    while True:
        params = {"symbol": symbol, "page_num": page, "page_size": 100}
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as r:
            data = await r.json()

        rows = data.get("data", {}).get("resultList", [])
        if not rows:
            break

        for row in rows:
            ts = int(row.get("settleTime") or row.get("collectTime"))
            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
            if dt < cutoff:
                return all_data
            all_data.append({
                "time": dt,
                "rate": float(row["fundingRate"]),
                "symbol": symbol,
            })

        if len(rows) < 100:
            break
        page += 1
        if page > 50:  # safety
            break

    return all_data


async def fetch_price_history(session, symbol: str, days: int) -> list[dict]:
    """Récupère les klines pour calculer drawdown / liquidation risk."""
    url = "https://contract.mexc.com/api/v1/contract/kline"
    end = int(datetime.now(timezone.utc).timestamp())
    start = end - days * 86400
    params = {
        "symbol": symbol,
        "interval": "Hour1",
        "start": start,
        "end": end,
    }
    async with session.get(f"{url}/{symbol}", params={"interval": "Hour1", "start": start, "end": end},
                           timeout=aiohttp.ClientTimeout(total=15)) as r:
        data = await r.json()
    if not data.get("success"):
        return []
    d = data.get("data", {})
    times = d.get("time", [])
    closes = d.get("close", [])
    return [{"time": datetime.fromtimestamp(t, tz=timezone.utc), "close": float(c)}
            for t, c in zip(times, closes)]


def backtest_cash_and_carry(funding_data: list[dict], threshold: float = 0.005) -> dict:
    """
    Stratégie : à chaque settlement où |funding| > threshold,
    on simule une position cash&carry et on encaisse le funding net des frais.

    Frais par settlement actif :
      - Ouverture : 1× taker (perp) + 1× spot fee
      - Clôture   : 1× taker (perp) + 1× spot fee
      - Slippage  : 2× slippage
    Pour un trade qui dure 1 settlement.

    On suppose qu'on tient la position uniquement pendant le settlement (entrée/sortie).
    """
    trades = []
    total_pnl = 0.0
    equity = [0.0]
    times = []

    if not funding_data:
        return {"trades": [], "total_pnl": 0, "equity": [0], "times": [],
                "n_trades": 0, "win_rate": 0, "avg_pnl": 0,
                "max_drawdown": 0, "sharpe": 0}

    funding_data = sorted(funding_data, key=lambda x: x["time"])

    for row in funding_data:
        rate = row["rate"]
        if abs(rate) >= threshold:
            # Si funding négatif → short perp, on reçoit |rate|
            # Si funding positif → long perp, on reçoit rate (mais on est short spot, donc inversion)
            # Stratégie: on parie toujours dans le sens contraire au funding pour l'encaisser
            gross = abs(rate)

            # Frais : open + close du perp (taker) + open + close du spot
            fees = 2 * TAKER_FEE + 2 * SPOT_FEE + 2 * SLIPPAGE

            net = gross - fees
            total_pnl += net
            equity.append(total_pnl)
            times.append(row["time"])
            trades.append({
                "time": row["time"],
                "rate": rate,
                "gross": gross,
                "fees": fees,
                "net": net,
            })

    if not trades:
        return {"trades": [], "total_pnl": 0, "equity": [0], "times": [],
                "n_trades": 0, "win_rate": 0, "avg_pnl": 0,
                "max_drawdown": 0, "sharpe": 0}

    n = len(trades)
    wins = sum(1 for t in trades if t["net"] > 0)
    win_rate = wins / n
    avg_pnl = total_pnl / n

    # Max drawdown
    peak = equity[0]
    max_dd = 0
    for v in equity:
        if v > peak:
            peak = v
        dd = peak - v
        if dd > max_dd:
            max_dd = dd

    # Sharpe sur returns par trade
    rets = [t["net"] for t in trades]
    if len(rets) > 1:
        mean_r = sum(rets) / len(rets)
        var = sum((r - mean_r) ** 2 for r in rets) / len(rets)
        std = var ** 0.5
        sharpe = (mean_r / std) * (n ** 0.5) if std > 0 else 0
    else:
        sharpe = 0

    return {
        "trades": trades,
        "total_pnl": total_pnl,
        "equity": equity,
        "times": times,
        "n_trades": n,
        "win_rate": win_rate,
        "avg_pnl": avg_pnl,
        "max_drawdown": max_dd,
        "sharpe": sharpe,
    }


def build_equity_chart(result: dict, symbol: str, days: int, threshold: float) -> io.BytesIO:
    BG, GRID, TEXT, ACCENT, GREEN, RED = "#0d1117", "#1c2333", "#e6edf3", "#58a6ff", "#00c897", "#ff4d6d"

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    if result["times"]:
        times = [result["times"][0]] + result["times"]
        equity_pct = [v * 100 for v in result["equity"]]
        ax.plot(times, equity_pct, color=ACCENT, linewidth=2)
        ax.fill_between(times, 0, equity_pct,
                        color=GREEN if result["total_pnl"] > 0 else RED, alpha=0.15)

    ax.axhline(0, color=TEXT, linewidth=0.5, linestyle="--")
    ax.set_ylabel("Cumulative Return (%)", color=TEXT, fontsize=10)
    ax.tick_params(colors=TEXT, labelsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:+.2f}%"))

    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(True, color=GRID, linewidth=0.7, zorder=0)

    title = (f"Backtest Cash & Carry — {symbol}\n"
             f"{days}j  |  seuil ±{threshold*100:.2f}%  |  {result['n_trades']} trades")
    ax.set_title(title, color=ACCENT, fontsize=12, fontweight="bold", pad=14)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return buf


def format_results(symbol: str, days: int, threshold: float, result: dict) -> str:
    pnl_color = "🟢" if result["total_pnl"] > 0 else "🔴"
    return (
        f"📈 *Backtest Cash & Carry*\n"
        f"{'─'*30}\n"
        f"Symbole : `{symbol}`\n"
        f"Période : {days} jours\n"
        f"Seuil   : ±{threshold*100:.2f}%\n\n"
        f"{pnl_color} *PnL total : {result['total_pnl']*100:+.2f}%*\n\n"
        f"📊 Trades         : {result['n_trades']}\n"
        f"✅ Win rate       : {result['win_rate']*100:.1f}%\n"
        f"💰 PnL moyen      : {result['avg_pnl']*100:+.4f}%\n"
        f"📉 Max drawdown   : -{result['max_drawdown']*100:.2f}%\n"
        f"⚡ Sharpe (trade) : {result['sharpe']:.2f}\n\n"
        f"_Frais inclus : taker 0.06%, spot 0.1%, slippage 0.05%_"
    )


# ─── COMMANDES ────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 *Bot Backtest Funding Rates*\n\n"
        "Stratégie *Cash & Carry* simulée sur l'historique MEXC.\n\n"
        "*Commandes :*\n"
        "• `/backtest SYMBOL JOURS [SEUIL%]`\n"
        "    ex : `/backtest B3_USDT 30 0.5`\n"
        "• `/topfunding JOURS` — top opportunités sur N jours\n"
        "• `/help` — aide détaillée",
        parse_mode="Markdown"
    )


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Aide*\n\n"
        "*Backtest d'une paire :*\n"
        "`/backtest SYMBOL JOURS [SEUIL%]`\n"
        "  - SYMBOL : ex `B3_USDT`, `BLAST_USDT`, `BTC_USDT`\n"
        "  - JOURS  : période historique (ex 30, 90, 180)\n"
        "  - SEUIL  : seuil d'entrée en % (défaut 0.5)\n\n"
        "*Exemples :*\n"
        "`/backtest B3_USDT 30`\n"
        "`/backtest BLAST_USDT 90 0.3`\n\n"
        "*Stratégie testée :*\n"
        "À chaque settlement où |funding| ≥ seuil :\n"
        "→ On ouvre une position delta-neutre (long spot + short perp ou inverse)\n"
        "→ On encaisse le funding\n"
        "→ On déduit les frais (taker, spot, slippage)\n",
        parse_mode="Markdown"
    )


async def cmd_backtest(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    if not args:
        await update.message.reply_text(
            "❌ Usage : `/backtest SYMBOL JOURS [SEUIL%]`\nEx : `/backtest B3_USDT 30 0.5`",
            parse_mode="Markdown"
        )
        return

    symbol = args[0].upper()
    if "_" not in symbol:
        symbol = symbol.replace("USDT", "_USDT") if symbol.endswith("USDT") else symbol + "_USDT"

    try:
        days = int(args[1]) if len(args) > 1 else 30
    except ValueError:
        await update.message.reply_text("❌ JOURS doit être un nombre entier.")
        return

    try:
        threshold_pct = float(args[2]) if len(args) > 2 else 0.5
    except ValueError:
        await update.message.reply_text("❌ SEUIL doit être un nombre (en %).")
        return

    threshold = threshold_pct / 100  # convert % to decimal

    if days < 1 or days > 365:
        await update.message.reply_text("❌ JOURS doit être entre 1 et 365.")
        return

    msg = await update.message.reply_text(
        f"⏳ Backtest `{symbol}` sur {days}j (seuil ±{threshold_pct}%)...",
        parse_mode="Markdown"
    )

    connector = aiohttp.TCPConnector(ssl=_ssl_ctx())
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            funding = await fetch_funding_history(session, symbol, days)
    except Exception as e:
        await msg.edit_text(f"❌ Erreur récupération données : {e}")
        return

    if not funding:
        await msg.edit_text(f"❌ Aucune donnée trouvée pour `{symbol}`.", parse_mode="Markdown")
        return

    result = backtest_cash_and_carry(funding, threshold=threshold)

    caption = format_results(symbol, days, threshold, result)
    chart = build_equity_chart(result, symbol, days, threshold)

    await msg.delete()
    await ctx.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=InputFile(chart, filename="backtest.png"),
        caption=caption,
        parse_mode="Markdown"
    )


async def cmd_topfunding(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Liste les paires MEXC avec le plus gros funding cumulé sur N jours."""
    args = ctx.args
    try:
        days = int(args[0]) if args else 7
    except ValueError:
        await update.message.reply_text("❌ Usage : `/topfunding JOURS`", parse_mode="Markdown")
        return

    if days < 1 or days > 90:
        await update.message.reply_text("❌ JOURS doit être entre 1 et 90.")
        return

    msg = await update.message.reply_text(
        f"⏳ Recherche des top opportunités sur {days}j (peut prendre 1-2 min)..."
    )

    connector = aiohttp.TCPConnector(ssl=_ssl_ctx())
    async with aiohttp.ClientSession(connector=connector) as session:
        # 1. Récupère la liste des paires MEXC
        async with session.get(
            "https://contract.mexc.com/api/v1/contract/ticker",
            timeout=aiohttp.ClientTimeout(total=15)
        ) as r:
            tickers = await r.json()

        # On garde les paires USDT uniquement, par volume décroissant (top 50)
        symbols = sorted(
            [d for d in tickers["data"] if d["symbol"].endswith("_USDT")],
            key=lambda x: float(x.get("amount24", 0)),
            reverse=True
        )[:50]

        # 2. Pour chaque paire, calcule le funding cumulé absolu
        results = []
        for sym in symbols:
            try:
                hist = await fetch_funding_history(session, sym["symbol"], days)
                if hist:
                    cumul_abs = sum(abs(h["rate"]) for h in hist)
                    n = len(hist)
                    results.append({
                        "symbol": sym["symbol"],
                        "cumul": cumul_abs,
                        "settlements": n,
                        "avg": cumul_abs / n if n else 0,
                    })
            except Exception:
                continue

        results.sort(key=lambda x: x["cumul"], reverse=True)

    if not results:
        await msg.edit_text("❌ Aucune donnée récupérée.")
        return

    lines = [f"🏆 *Top funding cumulé sur {days}j*\n"]
    for i, r in enumerate(results[:15], 1):
        lines.append(
            f"{i}. `{r['symbol']}` — *{r['cumul']*100:.2f}%* "
            f"({r['settlements']} settl., moy {r['avg']*100:.4f}%)"
        )

    await msg.edit_text("\n".join(lines), parse_mode="Markdown")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN manquant")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",      cmd_start))
    app.add_handler(CommandHandler("help",       cmd_help))
    app.add_handler(CommandHandler("backtest",   cmd_backtest))
    app.add_handler(CommandHandler("topfunding", cmd_topfunding))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
