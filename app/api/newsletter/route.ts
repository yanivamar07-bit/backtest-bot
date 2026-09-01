import { NextResponse } from "next/server";

export const runtime = "nodejs";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Requête invalide." }, { status: 400 });
  }

  const email = typeof body === "object" && body !== null && "email" in body ? (body as { email: unknown }).email : undefined;

  if (typeof email !== "string" || !EMAIL_RE.test(email)) {
    return NextResponse.json({ error: "Adresse email invalide." }, { status: 400 });
  }

  const apiKey = process.env.RESEND_API_KEY;

  if (apiKey) {
    try {
      const { Resend } = await import("resend");
      const resend = new Resend(apiKey);
      await resend.emails.send({
        from: process.env.NEWSLETTER_FROM || "Meridian <journal@meridian-watches.ch>",
        to: process.env.NEWSLETTER_TO || email,
        subject: "Nouvelle inscription au Journal Meridian",
        text: `Nouvelle inscription : ${email}`,
      });
    } catch (error) {
      console.error("[newsletter] Resend delivery failed", error);
      return NextResponse.json({ error: "Envoi impossible pour le moment." }, { status: 502 });
    }
  } else {
    console.log(`[newsletter] (dev fallback, no RESEND_API_KEY) new subscriber: ${email}`);
  }

  return NextResponse.json({ ok: true });
}
