"use client";

import Image from "next/image";
import { MagneticButton } from "@/components/ui/MagneticButton";

export function Hero() {
  return (
    <section id="top" className="relative grid min-h-[100svh] grid-cols-1 md:grid-cols-2">
      <div className="relative z-10 flex flex-col justify-center gap-8 px-6 py-32 md:px-14 md:py-0">
        <div className="absolute inset-0 -z-10 md:hidden">
          <Image
            src="/images/hero.svg"
            alt=""
            fill
            sizes="100vw"
            unoptimized
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[var(--color-ink)] via-[var(--color-ink)]/40 to-transparent" />
        </div>

        <p className="eyebrow text-[var(--color-stone)] md:text-[var(--color-stone)]">
          Manufacture indépendante — Réf. 01 à 09
        </p>

        <h1 className="fluid-h1 font-serif text-[var(--color-ink)] md:text-[var(--color-ink)]">
          L&apos;heure,
          <br />
          <em className="text-[var(--color-accent)] not-italic font-serif italic">rien de plus.</em>
        </h1>

        <p className="max-w-md text-[var(--color-stone)] md:text-[var(--color-ink)]/70">
          Un seul mouvement mécanique, pensé une fois pour être juste, remonté à la main
          et décliné en neuf cadrans. Pas de collaboration, pas de nouvelle référence chaque
          année — un geste manufacturier que nous répétons jusqu&apos;à l&apos;exactitude.
        </p>

        <MagneticButton
          className="eyebrow w-fit border border-[var(--color-ink)] px-8 py-4"
          onClick={() => document.querySelector("#collection")?.scrollIntoView({ behavior: "smooth" })}
        >
          Découvrir la collection
        </MagneticButton>
      </div>

      <div className="relative hidden md:block">
        <Image
          src="/images/hero.svg"
          alt="Lumière rasante sur un cadran Meridian"
          fill
          sizes="50vw"
          unoptimized
          priority
          className="object-cover"
        />
      </div>
    </section>
  );
}
