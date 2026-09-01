export function GrainOverlay() {
  return (
    <svg className="grain-overlay" aria-hidden="true">
      <filter id="meridian-grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch" />
        <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.9 0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#meridian-grain)" />
    </svg>
  );
}
