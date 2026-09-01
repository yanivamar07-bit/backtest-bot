"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";
import { getGsap } from "@/lib/gsap";
import { prefersReducedMotion } from "@/lib/utils";

const LABELS = [
  { id: "balancier", title: "Balancier-spiral", detail: "18 000 alternances / heure", top: "18%", left: "62%" },
  { id: "pont", title: "Pont de finissage", detail: "Anglage adouci à la main", top: "38%", left: "20%" },
  { id: "rouage", title: "Rouage de finissage", detail: "Rubis synthétiques, 21 pierres", top: "60%", left: "68%" },
  { id: "barillet", title: "Barillet", detail: "Réserve de marche 42 heures", top: "72%", left: "28%" },
];

export function Movement() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (prefersReducedMotion() || !sectionRef.current) return;
    const { gsap, ScrollTrigger } = getGsap();

    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>(".movement-label").forEach((el, i) => {
        gsap.fromTo(
          el,
          { opacity: 0, x: -12 },
          {
            opacity: 1,
            x: 0,
            duration: 0.6,
            ease: "power2.out",
            scrollTrigger: {
              trigger: sectionRef.current,
              start: `top+=${i * 80} center`,
              toggleActions: "play none none reverse",
            },
          }
        );
      });
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section id="mouvement" ref={sectionRef} className="on-dark relative bg-[var(--color-ink)] px-6 py-32 text-[var(--color-paper)] md:px-14">
      <div className="mx-auto max-w-6xl">
        <p className="eyebrow text-[var(--color-accent-soft)]">Le calibre M.01</p>
        <h2 className="fluid-h2 font-serif mt-3 mb-16 max-w-2xl">
          La précision se voit dans ce qu&apos;on ne montre jamais.
        </h2>

        <div className="relative mx-auto aspect-square w-full max-w-2xl">
          <Image
            src="/images/movement.svg"
            alt="Calibre M.01 à nu"
            fill
            sizes="(min-width: 768px) 42rem, 100vw"
            unoptimized
            className="object-cover"
          />
          {LABELS.map((label) => (
            <div
              key={label.id}
              className="movement-label absolute max-w-[10rem] opacity-0"
              style={{ top: label.top, left: label.left }}
            >
              <div className="mb-2 h-px w-6 bg-[var(--color-accent-soft)]" />
              <p className="eyebrow text-[var(--color-accent-soft)]">{label.title}</p>
              <p className="mono-num mt-1 text-xs text-[var(--color-stone-light)]">{label.detail}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
