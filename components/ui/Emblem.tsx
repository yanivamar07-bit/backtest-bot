type EmblemProps = {
  className?: string;
  color?: string;
};

/**
 * MERIDIAN emblem: an archer-angel mounted on a striding lion, reduced to
 * monoweight linework — a horological seal, not an illustration.
 * `Free` is the unframed mark (header, large use); `Seal` sits it inside a
 * fine circle for favicon / embossing use at small sizes.
 */
export function EmblemFree({ className, color = "currentColor" }: EmblemProps) {
  return (
    <svg
      viewBox="0 0 120 90"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label="Emblème Meridian"
    >
      <g stroke={color} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        {/* Lion body, profile, striding */}
        <path d="M10 66c3-9 10-14 20-14 6 0 9 2 13 6 5-6 12-9 20-8 9 1 15 7 17 15" />
        {/* Lion head */}
        <path d="M10 66c-4-1-7-4-7-9 0-4 3-7 7-7 3 0 5 1 6 4" />
        {/* Lion mane, geometric strokes */}
        <path d="M14 50c1-3 4-5 7-5M18 47c1-3 4-4 7-3M23 46c2-2 5-3 8-2" />
        {/* Lion legs */}
        <path d="M22 66v10M34 66v10M55 68v9M68 66v10" />
        {/* Lion tail, curled */}
        <path d="M78 65c6 0 10-4 9-9-1-4-5-5-7-2" />
        {/* Ange: torso seated on lion back */}
        <path d="M46 52c0-8 5-14 12-14s12 6 12 14" />
        <circle cx="58" cy="30" r="5.5" />
        {/* Wings, stylised geometric feathers */}
        <path d="M46 44c-8-2-14-8-16-16 6 1 12 5 16 11" />
        <path d="M40 40c-6-1-10-5-12-10M43 47c-7 0-12-3-15-8" />
        <path d="M70 44c8-2 14-8 16-16-6 1-12 5-16 11" />
        <path d="M76 40c6-1 10-5 12-10M73 47c7 0 12-3 15-8" />
        {/* Bow, drawn vertical, held in front */}
        <path d="M60 20c5 2 8 8 8 16s-3 14-8 16" />
        <path d="M68 20v32" />
        {/* Arrow nocked, diagonal */}
        <path d="M50 30l20 6" />
      </g>
    </svg>
  );
}

export function EmblemSeal({ className, color = "currentColor" }: EmblemProps) {
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label="Sceau Meridian"
    >
      <circle cx="50" cy="50" r="47" stroke={color} strokeWidth="1.4" />
      <circle cx="50" cy="50" r="42" stroke={color} strokeWidth="0.6" />
      <g stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 63c2.5-7 8-11 16-11 5 0 7.5 1.5 10.5 5 4-5 9.5-7 16-6.5 7 0.8 12 5.5 13.5 12" />
        <path d="M20 63c-3-0.8-5.5-3-5.5-7 0-3.2 2.4-5.6 5.5-5.6 2.4 0 4 0.8 4.8 3.2" />
        <path d="M23 51c0.8-2.4 3.2-4 5.6-4M26.5 48.8c0.8-2.4 3.2-3.2 5.6-2.4" />
        <path d="M29 63v7M38 63v7M56 64.5v6.5M66 63v7" />
        <path d="M73 62c4.8 0 8-3.2 7.2-7-0.8-3.2-4-4-5.6-1.6" />
        <path d="M45 55c0-6.4 4-11.2 9.6-11.2S64.2 48.6 64.2 55" />
        <circle cx="54.6" cy="37" r="4.4" />
        <path d="M45 49c-6.4-1.6-11.2-6.4-12.8-12.8 4.8 0.8 9.6 4 12.8 8.8" />
        <path d="M40.6 46c-4.8-0.8-8-4-9.6-8" />
        <path d="M64.2 49c6.4-1.6 11.2-6.4 12.8-12.8-4.8 0.8-9.6 4-12.8 8.8" />
        <path d="M68.6 46c4.8-0.8 8-4 9.6-8" />
        <path d="M57.4 29c4 1.6 6.4 6.4 6.4 12.8s-2.4 11.2-6.4 12.8" />
        <path d="M63.8 29v25.6" />
        <path d="M50 37l16 4.8" />
      </g>
    </svg>
  );
}
