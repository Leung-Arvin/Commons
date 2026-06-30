import type { Asset, FloorPlanDetail, LayerKey, Selection } from '../../lib/types';
import { OCC, occBar, occHeat, occTint, zoneMetrics } from '../../lib/metrics';

interface Props {
  fp: FloorPlanDetail;
  assets: Asset[];
  layer: LayerKey;
  isCart: boolean;
  selected: Selection;
  query: string;
  zoom: number;
  onSelect: (sel: Selection) => void;
}

const centroid = (poly: number[][]): [number, number] => {
  const n = poly.length || 1;
  const sx = poly.reduce((a, [x]) => a + x, 0);
  const sy = poly.reduce((a, [, y]) => a + y, 0);
  return [sx / n, sy / n];
};

export function MapStage({ fp, assets, layer, isCart, selected, query, zoom, onSelect }: Props) {
  // Floor coords can be meters (e.g. 50×30) or pixels (1040×600); derive every
  // visual size from the smaller dimension so it scales the same either way.
  const U = Math.max(Math.min(fp.width, fp.height), 1);
  const strokeW = U * 0.005;
  const fontZone = U * 0.04;
  const fontCount = U * 0.045;
  const apCore = U * 0.014;
  const apRing = U * 0.06;
  const assetSize = U * 0.032;
  const q = query.trim().toLowerCase();

  const dim = (name: string) => q.length > 0 && !name.toLowerCase().includes(q);
  const heat = layer === 'heatmap';

  return (
    <div className="cx-map">
      <svg
        className="cx-svg" viewBox={`0 0 ${fp.width} ${fp.height}`} preserveAspectRatio="xMidYMid meet"
        style={{ transform: `scale(${zoom})`, transition: 'transform .18s ease' }}
      >
        {/* Zones */}
        {fp.zones.map((z) => {
          if (!z.polygon?.length) return null;
          const m = zoneMetrics(z.id);
          const sel = selected?.type === 'zone' && selected.id === z.id;
          const pts = z.polygon.map(([x, y]) => `${x},${y}`).join(' ');
          const [cx, cy] = centroid(z.polygon);
          return (
            <g key={z.id} opacity={dim(z.name) ? 0.25 : 1}>
              <polygon
                className={`cx-svg-zone ${sel ? 'sel' : ''}`}
                points={pts}
                fill={heat ? occHeat(m.level, m.fill) : occTint(m.level)}
                stroke={sel ? 'var(--teal)' : occBar(m.level)}
                strokeWidth={sel ? strokeW * 1.8 : strokeW}
                onClick={() => onSelect({ type: 'zone', id: z.id })}
              />
              <text
                className="cx-svg-zonelabel" x={cx} y={heat ? cy : cy - fontCount * 0.6}
                fontSize={fontZone} fill="var(--ink)" textAnchor="middle" dominantBaseline="middle"
              >
                {z.name}
              </text>
              {!heat && (
                <text
                  className="cx-svg-count" x={cx} y={cy + fontZone * 0.7}
                  fontSize={fontCount} fill={OCC[m.level].text} textAnchor="middle" dominantBaseline="middle"
                >
                  {m.people}
                </text>
              )}
              {layer === 'occupancy' && (
                <circle cx={cx} cy={cy} r={apCore} fill="var(--teal)">
                  <animate attributeName="opacity" values="0.9;0.3;0.9" dur="2.2s" repeatCount="indefinite" />
                </circle>
              )}
            </g>
          );
        })}

        {/* Access points — Cartographer-only, Devices layer */}
        {isCart && layer === 'devices' && fp.access_points.map((ap) => {
          const sel = selected?.type === 'ap' && selected.id === ap.id;
          return (
            <g key={ap.id} className="cx-svg-ap" onClick={() => onSelect({ type: 'ap', id: ap.id })}>
              <circle cx={ap.x} cy={ap.y} fill="none" stroke="var(--teal)" strokeWidth={strokeW} opacity={0.5}>
                <animate attributeName="r" values={`${apCore};${apRing}`} dur="2.2s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.5;0" dur="2.2s" repeatCount="indefinite" />
              </circle>
              <circle cx={ap.x} cy={ap.y} r={sel ? apCore * 1.4 : apCore} fill="var(--teal)"
                stroke={sel ? 'var(--ink)' : 'none'} strokeWidth={strokeW} />
            </g>
          );
        })}

        {/* Assets — Devices or Assets layer; only those with a known position */}
        {(layer === 'devices' || layer === 'assets') && assets.map((a) => {
          if (a.last_x == null || a.last_y == null) return null;
          const sel = selected?.type === 'asset' && selected.id === a.id;
          return (
            <rect
              key={a.id} className="cx-svg-asset"
              x={a.last_x - assetSize / 2} y={a.last_y - assetSize / 2}
              width={assetSize} height={assetSize} rx={assetSize * 0.28}
              fill="var(--occ-mod)" stroke={sel ? 'var(--ink)' : 'var(--bg-deep)'} strokeWidth={strokeW}
              onClick={() => onSelect({ type: 'asset', id: a.id })}
            />
          );
        })}
      </svg>
    </div>
  );
}
