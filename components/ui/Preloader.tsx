"use client";

import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { prefersReducedMotion } from "@/lib/utils";

const STORAGE_KEY = "meridian-preloader-seen";

export function Preloader() {
  // Always render the same thing on the server and on first client paint —
  // sessionStorage is only consulted after mount, never in the initializer,
  // so SSR and the first client render can never disagree (no hydration
  // mismatch).
  const [done, setDone] = useState(false);
  const [skip, setSkip] = useState(false);
  const [percent, setPercent] = useState(0);
  const rafRef = useRef<number>();

  useLayoutEffect(() => {
    try {
      if (sessionStorage.getItem(STORAGE_KEY)) {
        setSkip(true);
        setDone(true);
      }
    } catch {
      // sessionStorage unavailable (private mode, etc.) — just run the preloader.
    }
  }, []);

  useEffect(() => {
    if (skip || done) return;

    if (prefersReducedMotion()) {
      setPercent(100);
      finish();
      return;
    }

    const start = performance.now();
    const duration = 2000;

    function tick(now: number) {
      const elapsed = now - start;
      const pct = Math.min(100, Math.round((elapsed / duration) * 100));
      setPercent(pct);
      if (pct < 100) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        finish();
      }
    }

    rafRef.current = requestAnimationFrame(tick);

    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [skip]);

  function finish() {
    try {
      sessionStorage.setItem(STORAGE_KEY, "1");
    } catch {
      // ignore
    }
    window.setTimeout(() => setDone(true), 400);
  }

  return (
    <AnimatePresence>
      {!done && (
        <motion.div
          exit={{ opacity: 0 }}
          transition={{ duration: 0.6, ease: "easeInOut" }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-[var(--color-ink)] on-dark"
        >
          <video
            autoPlay
            muted
            loop
            playsInline
            className="absolute inset-0 h-full w-full object-cover opacity-30"
            poster="/images/movement.svg"
          >
            <source src="/videos/movement-macro.mp4" type="video/mp4" />
          </video>
          <div className="relative z-10 font-serif text-[clamp(3rem,12vw,7rem)] text-[var(--color-paper)]">
            {percent}
            <span className="align-top text-[0.35em]">%</span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
