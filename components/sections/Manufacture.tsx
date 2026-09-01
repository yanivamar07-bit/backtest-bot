"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

const CHAPTERS = [
  {
    numeral: "I",
    title: "Le mouvement",
    body: "Un seul calibre, conçu une fois et jamais remplacé. Nous ne cherchons pas la nouveauté mécanique chaque saison — nous cherchons la justesse, année après année.",
  },
  {
    numeral: "II",
    title: "L'atelier",
    body: "Chaque mouvement est remonté, réglé et emboîté à la main, dans un atelier où l'on compte les gestes, pas les cadences.",
  },
  {
    numeral: "III",
    title: "La réserve",
    body: "Une montre Meridian ne se remplace pas, elle se transmet. Le calibre est garanti à vie et réparable pour toujours par nos soins.",
  },
];

export function Manufacture() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start 0.8", "end 0.4"] });
  const scaleY = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <section
      id="manufacture"
      ref={ref}
      className="on-dark relative overflow-hidden bg-[var(--color-ink)] px-6 py-32 text-[var(--color-paper)] md:px-14"
    >
      <video
        autoPlay
        muted
        loop
        playsInline
        preload="none"
        className="absolute inset-0 h-full w-full object-cover opacity-[0.07]"
      >
        <source src="/videos/atelier-ambient.mp4" type="video/mp4" />
      </video>

      <div className="relative mx-auto max-w-4xl">
        <p className="eyebrow text-[var(--color-accent-soft)]">Manufacture</p>
        <h2 className="fluid-h2 font-serif mt-3 mb-20">Trois chapitres, un seul métier.</h2>

        <div className="relative grid grid-cols-[2rem_1fr] gap-x-8 md:grid-cols-[3rem_1fr]">
          <div className="relative">
            <div className="absolute left-1/2 top-0 h-full w-px -translate-x-1/2 bg-[var(--color-hairline-dark)]" />
            <motion.div
              style={{ scaleY }}
              className="absolute left-1/2 top-0 h-full w-px origin-top -translate-x-1/2 bg-[var(--color-accent-soft)]"
            />
          </div>

          <div className="flex flex-col gap-24">
            {CHAPTERS.map((chapter) => (
              <motion.div
                key={chapter.numeral}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-20%" }}
                transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
              >
                <p className="eyebrow text-[var(--color-accent-soft)]">{chapter.numeral}</p>
                <h3 className="fluid-h2 font-serif mt-2" style={{ fontSize: "clamp(1.6rem, 1.2rem + 2vw, 3rem)" }}>
                  {chapter.title}
                </h3>
                <p className="mt-4 max-w-lg text-[var(--color-stone-light)]">{chapter.body}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
