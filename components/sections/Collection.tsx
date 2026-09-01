"use client";

import { useState } from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { products, productMacro, type Product } from "@/data/products";
import { formatPrice } from "@/lib/utils";
import { QuickViewModal } from "@/components/ui/QuickViewModal";

export function Collection() {
  const [selected, setSelected] = useState<Product | null>(null);

  return (
    <section id="collection" className="mx-auto max-w-7xl px-6 py-28 md:px-10">
      <header className="mb-16 max-w-xl">
        <p className="eyebrow text-[var(--color-accent)]">La collection</p>
        <h2 className="fluid-h2 font-serif mt-3">Neuf cadrans, un seul calibre.</h2>
      </header>

      <div className="grid grid-cols-1 gap-x-8 gap-y-16 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((product, i) => (
          <motion.button
            key={product.slug}
            onClick={() => setSelected(product)}
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-10%" }}
            transition={{ duration: 0.6, delay: (i % 3) * 0.08, ease: [0.22, 1, 0.36, 1] }}
            className="group text-left"
          >
            <div className="relative aspect-[3/4] overflow-hidden bg-[var(--color-paper-dim)]">
              <Image
                src={product.image}
                alt={`Montre Meridian ${product.name}`}
                fill
                sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                unoptimized
                className="object-cover transition-opacity duration-500 group-hover:opacity-0"
              />
              <Image
                src={productMacro(product)}
                alt={`Plan macro du cadran ${product.name}`}
                fill
                sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                unoptimized
                aria-hidden="true"
                className="object-cover scale-[1.04] opacity-0 transition-opacity duration-500 group-hover:opacity-100"
              />
              <span className="eyebrow absolute left-4 top-4 bg-[var(--color-paper)]/90 px-2 py-1 text-[var(--color-ink)]">
                Réf. {product.ref}
              </span>
            </div>
            <div className="mt-4 flex items-start justify-between gap-4">
              <div>
                <h3 className="font-serif text-xl">{product.name}</h3>
                <p className="mt-1 text-sm text-[var(--color-stone)]">{product.dialType}</p>
              </div>
              <p className="mono-num shrink-0 text-sm">{formatPrice(product.price)}</p>
            </div>
          </motion.button>
        ))}
      </div>

      <QuickViewModal product={selected} onClose={() => setSelected(null)} />
    </section>
  );
}
