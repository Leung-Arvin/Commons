import type { OccLevel } from '../../lib/types';
import { occBar } from '../../lib/metrics';

const ROWS: [OccLevel, string][] = [
  ['vacant', 'Vacant'],
  ['low', 'Low < 50%'],
  ['moderate', 'Moderate'],
  ['high', 'High > 75%'],
  ['full', 'Full'],
];

export function Legend() {
  return (
    <div className="cx-float cx-legend">
      <div className="ttl">Occupancy</div>
      {ROWS.map(([level, label]) => (
        <div className="cx-legend-row" key={level}>
          <span className="sw" style={{ background: occBar(level) }} />
          {label}
        </div>
      ))}
    </div>
  );
}
