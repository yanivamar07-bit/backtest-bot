"use client";

import { useRef } from "react";
import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";

export function Editorial() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], ["-8%", "8%"]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [1.1, 1, 1.1]);

  return (
    <section ref={ref} className="relative h-[100svh] overflow-hidden">
      <motion.div style={{ y, scale }} className="absolute inset-0">
        <Image
          src="/images/editorial.svg"
          alt="Lumière naturelle sur un boîtier Meridian"
          fill
          sizes="100vw"
          unoptimized
          className="object-cover"
        />
      </motion.div>
      <div className="absolute inset-0 bg-gradient-to-t from-[var(--color-ink)]/80 via-transparent to-transparent" />
      <div className="absolute inset-x-6 bottom-14 md:inset-x-14">
        <h2 className="fluid-h2 font-serif max-w-2xl text-[var(--color-paper)]">
          Fabriquée pour durer plus longtemps que les modes.
        </h2>
      </div>
    </section>
  );
}
