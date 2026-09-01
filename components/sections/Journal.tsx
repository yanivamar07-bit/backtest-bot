"use client";

import { useState, type FormEvent } from "react";

type Status = "idle" | "loading" | "success" | "error";

export function Journal() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setMessage("");

    try {
      const res = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Une erreur est survenue.");
      }

      setStatus("success");
      setMessage("Vous recevrez notre prochaine lettre.");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMessage(err instanceof Error ? err.message : "Une erreur est survenue.");
    }
  }

  return (
    <section id="journal" className="on-dark bg-[var(--color-ink)] px-6 py-32 text-[var(--color-paper)] md:px-14">
      <div className="mx-auto max-w-2xl text-center">
        <p className="eyebrow text-[var(--color-accent-soft)]">Journal</p>
        <h2 className="fluid-h2 font-serif mt-3">
          Ceux qui savent recevront l&apos;information avant les autres.
        </h2>

        <form onSubmit={handleSubmit} className="mx-auto mt-10 flex max-w-md flex-col gap-3 sm:flex-row">
          <label htmlFor="newsletter-email" className="sr-only">
            Adresse email
          </label>
          <input
            id="newsletter-email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="vous@exemple.com"
            className="h-14 flex-1 border border-[var(--color-hairline-dark)] bg-transparent px-4 text-[var(--color-paper)] placeholder:text-[var(--color-stone)] focus:border-[var(--color-accent-soft)] focus:outline-none"
          />
          <button
            type="submit"
            disabled={status === "loading"}
            className="eyebrow h-14 border border-[var(--color-paper)] px-8 disabled:opacity-60"
          >
            {status === "loading" ? "Envoi…" : "S'inscrire"}
          </button>
        </form>

        {message && (
          <p
            role="status"
            className={`mt-4 text-sm ${status === "error" ? "text-red-400" : "text-[var(--color-accent-soft)]"}`}
          >
            {message}
          </p>
        )}
      </div>
    </section>
  );
}
