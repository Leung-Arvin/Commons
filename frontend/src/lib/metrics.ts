import type { OccLevel } from './types';

/* ------------------------------------------------------------------ *
 * PLACEHOLDER METRICS — NOT REAL DATA.
 *
 * The backend stores zones as (name, type, polygon) and APs as
 * (mac, name, x, y). It has NO occupancy %, people counts, device
 * counts, signal heatmap, or AP client/dBm stats. The design calls for
 * all of those, so until a real telemetry source exists we synthesize
 * stable, deterministic placeholders from each entity's id.
 *
 * TODO(backend): replace every export here with real readings once the
 * occupancy/signal data layer exists. Anything importing this module is
 * showing demo data — the UI surfaces a "sample metrics" badge for it.
 * ------------------------------------------------------------------ */

// Visual ramp — kept intentionally distinct from the teal accent so occupancy
// never collides with "active/selected" state (see handoff color notes).
export const OCC: Record<OccLevel, { label: string; text: string }> = {
  vacant: { label: 'VACANT', text: '#8DA0A8' },
  low: { label: 'LOW', text: '#5BD49A' },
  moderate: { label: 'MODERATE', text: '#E6C264' },
  high: { label: 'HIGH', text: '#F09A66' },
  full: { label: 'FULL', text: '#F0859A' },
};

export const occBar = (l: OccLevel): string =>
  ({ vacant: '#3A4A52', low: '#2FB573', moderate: '#D9A93A', high: '#E07B3E', full: '#E0556B' })[l];

export const occTint = (l: OccLevel): string =>
  ({
    vacant: 'rgba(58,74,82,.18)', low: 'rgba(47,181,115,.16)', moderate: 'rgba(217,169,58,.16)',
    high: 'rgba(224,123,62,.20)', full: 'rgba(224,85,107,.20)',
  })[l];

export const occHeat = (l: OccLevel, fill: number): string => {
  const rgb = {
    vacant: '58,74,82', low: '47,181,115', moderate: '217,169,58', high: '224,123,62', full: '224,85,107',
  }[l];
  return `rgba(${rgb},${(0.18 + fill * 0.5).toFixed(2)})`;
};

const levelFor = (pct: number): OccLevel =>
  pct === 0 ? 'vacant' : pct < 50 ? 'low' : pct < 70 ? 'moderate' : pct < 90 ? 'high' : 'full';

// Stable hash so a given id always yields the same demo numbers across renders.
const hash = (s: string): number => {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return h;
};

export interface ZoneMetrics {
  level: OccLevel;
  occPct: number;
  fill: number; // 0..1
  people: string; // "11/14"
  devices: number;
}

export function zoneMetrics(zoneId: string): ZoneMetrics {
  const h = hash(zoneId);
  const cap = 8 + (h % 28); // 8..35 capacity
  const occPct = h % 101; // 0..100
  const present = Math.round((occPct / 100) * cap);
  return {
    level: levelFor(occPct),
    occPct,
    fill: occPct / 100,
    people: `${present}/${cap}`,
    devices: (h >> 3) % (cap + 2),
  };
}

// Placeholder AP activity line, e.g. "12 clients · -41 dBm".
export function apActivity(apId: string): string {
  const h = hash(apId);
  const clients = h % 36;
  const dbm = -(34 + (h % 24));
  return `${clients} clients · ${dbm} dBm`;
}
