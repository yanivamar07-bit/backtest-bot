"use client";

import { useRef, type ReactNode, type MouseEvent } from "react";
import { motion, useSpring, type HTMLMotionProps } from "framer-motion";
import { prefersReducedMotion } from "@/lib/utils";

type MagneticButtonProps = HTMLMotionProps<"button"> & {
  children: ReactNode;
};

export function MagneticButton({ children, className, ...props }: MagneticButtonProps) {
  const ref = useRef<HTMLButtonElement>(null);
  const x = useSpring(0, { stiffness: 200, damping: 15, mass: 0.3 });
  const y = useSpring(0, { stiffness: 200, damping: 15, mass: 0.3 });

  function handleMove(e: MouseEvent<HTMLButtonElement>) {
    if (prefersReducedMotion() || !ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const relX = e.clientX - rect.left - rect.width / 2;
    const relY = e.clientY - rect.top - rect.height / 2;
    x.set(relX * 0.35);
    y.set(relY * 0.35);
  }

  function handleLeave() {
    x.set(0);
    y.set(0);
  }

  return (
    <motion.button
      ref={ref}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
      style={{ x, y }}
      className={className}
      {...props}
    >
      {children}
    </motion.button>
  );
}
