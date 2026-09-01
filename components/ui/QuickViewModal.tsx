"use client";

import { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";
import { productGallery, type Product } from "@/data/products";
import { formatPrice } from "@/lib/utils";

type QuickViewModalProps = {
  product: Product | null;
  onClose: () => void;
};

type AddState = "idle" | "loading" | "success";

export function QuickViewModal({ product, onClose }: QuickViewModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const galleryRef = useRef<HTMLDivElement>(null);
  const slideRefs = useRef<(HTMLDivElement | null)[]>([]);
  const [addState, setAddState] = useState<AddState>("idle");
  const [activeSlide, setActiveSlide] = useState(0);

  useEffect(() => {
    if (!product) return;

    setAddState("idle");
    setActiveSlide(0);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        onClose();
        return;
      }
      if (e.key === "Tab" && dialogRef.current) {
        const focusable = dialogRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }

    document.addEventListener("keydown", onKeyDown);
    dialogRef.current?.focus();

    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [product, onClose]);

  useEffect(() => {
    const container = galleryRef.current;
    if (!container || !product) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = slideRefs.current.findIndex((el) => el === entry.target);
            if (index !== -1) setActiveSlide(index);
          }
        });
      },
      { root: container, threshold: 0.6 }
    );

    slideRefs.current.forEach((el) => el && observer.observe(el));
    return () => observer.disconnect();
  }, [product]);

  function scrollToSlide(index: number) {
    slideRefs.current[index]?.scrollIntoView({ behavior: "smooth", inline: "start", block: "nearest" });
  }

  async function handleAddToCart() {
    setAddState("loading");
    await new Promise((resolve) => setTimeout(resolve, 900));
    setAddState("success");
    window.setTimeout(() => setAddState("idle"), 2200);
  }

  return (
    <AnimatePresence>
      {product && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[90] flex items-center justify-center bg-[var(--color-ink)]/70 backdrop-blur-sm"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) onClose();
          }}
        >
          <motion.div
            ref={dialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby="quickview-title"
            tabIndex={-1}
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 24 }}
            transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
            className="relative grid max-h-[90vh] w-[min(1100px,92vw)] grid-cols-1 overflow-y-auto bg-[var(--color-paper)] md:grid-cols-2"
          >
            <button
              onClick={onClose}
              aria-label="Fermer"
              className="absolute right-5 top-5 z-10 h-9 w-9 border border-[var(--color-hairline)] text-lg"
            >
              &times;
            </button>

            <div className="flex flex-col bg-[var(--color-paper-dim)]">
              <div
                ref={galleryRef}
                className="flex aspect-square snap-x snap-mandatory overflow-x-auto md:aspect-auto md:h-full"
              >
                {productGallery(product).map((slide, i) => (
                  <div
                    key={slide.src}
                    ref={(el) => {
                      slideRefs.current[i] = el;
                    }}
                    className="relative aspect-square w-full shrink-0 snap-start md:h-full md:w-full"
                  >
                    <Image
                      src={slide.src}
                      alt={`${slide.label} — ${product.name}`}
                      fill
                      sizes="(min-width: 768px) 50vw, 100vw"
                      unoptimized
                      className="object-cover"
                    />
                  </div>
                ))}
              </div>

              <div className="flex gap-2 p-4">
                {productGallery(product).map((slide, i) => (
                  <button
                    key={slide.src}
                    onClick={() => scrollToSlide(i)}
                    aria-label={`Voir : ${slide.label}`}
                    aria-current={activeSlide === i}
                    className={`relative aspect-square w-14 shrink-0 overflow-hidden border transition-colors ${
                      activeSlide === i ? "border-[var(--color-accent)]" : "border-[var(--color-hairline)]"
                    }`}
                  >
                    <Image
                      src={slide.src}
                      alt=""
                      fill
                      sizes="56px"
                      unoptimized
                      aria-hidden="true"
                      className="object-cover"
                    />
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-col gap-6 p-8 md:p-12">
              <div>
                <p className="eyebrow text-[var(--color-stone)]">Réf. {product.ref}</p>
                <h3 id="quickview-title" className="fluid-h2 font-serif mt-2">
                  {product.name}
                </h3>
                <p className="mono-num mt-3 text-lg">{formatPrice(product.price)}</p>
              </div>

              <dl className="grid grid-cols-2 gap-4 border-y border-[var(--color-hairline)] py-6 text-sm">
                <Spec label="Boîtier" value={product.caseMaterial} />
                <Spec label="Cadran" value={product.dialType} />
                <Spec label="Diamètre" value={product.diameter} />
                <Spec label="Réserve de marche" value={product.powerReserve} />
                <Spec label="Étanchéité" value={product.waterResistance} />
                <Spec label="Verre" value={product.glass} />
                {product.complication && (
                  <Spec label="Complication" value={product.complication} />
                )}
              </dl>

              <button
                onClick={handleAddToCart}
                disabled={addState === "loading"}
                className="eyebrow relative flex h-14 items-center justify-center border border-[var(--color-ink)] bg-[var(--color-ink)] text-[var(--color-paper)] transition-opacity disabled:opacity-70"
              >
                {addState === "idle" && "Ajouter au panier"}
                {addState === "loading" && "Ajout en cours…"}
                {addState === "success" && "Ajouté ✓"}
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function Spec({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="eyebrow text-[var(--color-stone)]">{label}</dt>
      <dd className="mono-num mt-1 text-[var(--color-ink)]">{value}</dd>
    </div>
  );
}
