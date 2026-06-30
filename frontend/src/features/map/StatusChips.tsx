export function StatusChips({ chips }: { chips: [string, string][] }) {
  return (
    <div className="cx-float cx-status">
      {chips.map(([k, v]) => (
        <div className="cx-chip" key={k}>
          <span className="ck">{k}</span><span className="cv">{v}</span>
        </div>
      ))}
    </div>
  );
}
