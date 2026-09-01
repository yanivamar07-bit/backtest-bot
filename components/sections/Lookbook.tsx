"use client";

import { useCallback, useEffect, useState } from "react";
import Image from "next/image";
import useEmblaCarousel from "embla-carousel-react";

const SLIDES = Array.from({ length: 6 }, (_, i) => ({
  id: i + 1,
  src: `/images/lookbook-${i + 1}.svg`,
}));

export function Lookbook() {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    dragFree: true,
    containScroll: "trimSnaps",
  });
  const [selected, setSelected] = useState(0);

  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setSelected(emblaApi.selectedScrollSnap());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on("select", onSelect);
    return () => {
      emblaApi.off("select", onSelect);
    };
  }, [emblaApi, onSelect]);

  return (
    <section className="py-28">
      <header className="mx-auto mb-10 max-w-7xl px-6 md:px-10">
        <p className="eyebrow text-[var(--color-accent)]">Lookbook</p>
        <h2 className="fluid-h2 font-serif mt-3">Portée au quotidien.</h2>
      </header>

      <div className="overflow-hidden pl-6 md:pl-10" ref={emblaRef}>
        <div className="flex gap-6">
          {SLIDES.map((slide) => (
            <div key={slide.id} className="relative aspect-[4/5] w-[70vw] shrink-0 md:w-[32vw]">
              <Image
                src={slide.src}
                alt={`Meridian portée, look ${slide.id}`}
                fill
                sizes="(min-width: 768px) 32vw, 70vw"
                unoptimized
                className="object-cover"
              />
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 flex justify-center gap-2">
        {SLIDES.map((slide, i) => (
          <button
            key={slide.id}
            aria-label={`Aller à l'image ${i + 1}`}
            onClick={() => emblaApi?.scrollTo(i)}
            className={`h-1.5 w-6 transition-colors ${
              selected === i ? "bg-[var(--color-accent)]" : "bg-[var(--color-hairline)]"
            }`}
          />
        ))}
      </div>
    </section>
  );
}
