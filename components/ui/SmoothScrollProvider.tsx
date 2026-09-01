"use client";

import { useEffect, type ReactNode } from "react";
import Lenis from "lenis";
import { getGsap } from "@/lib/gsap";
import { prefersReducedMotion } from "@/lib/utils";

export function SmoothScrollProvider({ children }: { children: ReactNode }) {
  useEffect(() => {
    if (prefersReducedMotion()) return;

    const { gsap, ScrollTrigger } = getGsap();
    const lenis = new Lenis({
      duration: 1.1,
      smoothWheel: true,
    });

    lenis.on("scroll", ScrollTrigger.update);

    const update = (time: number) => {
      lenis.raf(time * 1000);
    };

    gsap.ticker.add(update);
    gsap.ticker.lagSmoothing(0);

    return () => {
      lenis.destroy();
      gsap.ticker.remove(update);
    };
  }, []);

  return <>{children}</>;
}
