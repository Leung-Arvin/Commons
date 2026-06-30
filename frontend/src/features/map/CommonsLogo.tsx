// Brand logomark, ported from the design handoff (the inline <svg> in the
// prototype top bar). Rendered on the teal gradient tile in TopBar.
export function CommonsLogomark({ size = 26 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 128 128" aria-hidden="true">
      <g opacity="0.95">
        <rect x="18" y="28" width="31" height="72" rx="4" fill="#04201E" fillOpacity="0.18" />
        <rect x="49" y="24" width="30" height="80" rx="4" fill="#04201E" fillOpacity="0.06" />
        <rect x="79" y="28" width="31" height="72" rx="4" fill="#04201E" fillOpacity="0.24" />
      </g>
      <line x1="49.5" y1="24" x2="49.5" y2="104" stroke="#04201E" strokeOpacity="0.42" strokeWidth="3.5" />
      <line x1="78.5" y1="24" x2="78.5" y2="104" stroke="#04201E" strokeOpacity="0.42" strokeWidth="3.5" />
      <path
        d="M22 80 C34 66, 40 90, 50 74 S66 48, 79 62 S98 82, 106 56"
        fill="none" stroke="#04201E" strokeOpacity="0.6" strokeWidth="5.5"
        strokeLinecap="round" strokeLinejoin="round"
      />
      <g transform="translate(64,70)">
        <path d="M0,-15 C8,-15 14,-9 14,-2 C14,7 0,19 0,19 C0,19 -14,7 -14,-2 C-14,-9 -8,-15 0,-15 Z" fill="#04201E" />
        <circle r="4.6" cy="-2" fill="#3FE8D2" />
      </g>
    </svg>
  );
}
