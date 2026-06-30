import { Box, Hexagon, Move, Pencil, Radio, Trash2, X } from 'lucide-react';

import type { AccessPoint, Asset, FloorPlanDetail, Selection, Zone } from '../../lib/types';
import { OCC, apActivity, occBar, zoneMetrics } from '../../lib/metrics';

interface Props {
  selection: Selection;
  fp: FloorPlanDetail;
  assets: Asset[];
  isCart: boolean;
  onClose: () => void;
  onEditAsset: (a: Asset) => void;
  onDeleteAsset: (a: Asset) => void;
  onEditZone: (z: Zone) => void;
  onDeleteZone: (z: Zone) => void;
  onEditAccessPoint: (ap: AccessPoint) => void;
  onDeleteAccessPoint: (ap: AccessPoint) => void;
  onStub: (label: string) => void;
}

function relativeTime(iso: string | null): string {
  if (!iso) return 'never';
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return '—';
  const secs = Math.max(0, Math.round((Date.now() - then) / 1000));
  if (secs < 60) return `${secs}s ago`;
  if (secs < 3600) return `${Math.round(secs / 60)} min ago`;
  if (secs < 86400) return `${Math.round(secs / 3600)} h ago`;
  return `${Math.round(secs / 86400)} d ago`;
}

export function Inspector({
  selection, fp, assets, isCart, onClose, onEditAsset, onDeleteAsset,
  onEditZone, onDeleteZone, onEditAccessPoint, onDeleteAccessPoint, onStub,
}: Props) {
  if (!selection) return null;

  if (selection.type === 'zone') {
    const z = fp.zones.find((x) => x.id === selection.id);
    if (!z) return null;
    const m = zoneMetrics(z.id);
    return (
      <div className="cx-float cx-inspect">
        <div className="cx-ins-head">
          <div className="ic"><Hexagon size={16} color="var(--teal)" /></div>
          <div>
            <div className="nm">{z.name}</div>
            <div className="sub">Zone · {z.zone_type}</div>
          </div>
          <button className="cx-ins-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="cx-ins-body">
          <div className="cx-kv"><span className="k">Occupancy</span><span className="v">{m.people} · {m.occPct}%</span></div>
          <div className="cx-kv"><span className="k">Devices</span><span className="v">{m.devices}</span></div>
          <div className="cx-kv"><span className="k">Status</span><span className="v" style={{ color: OCC[m.level].text }}>{OCC[m.level].label}</span></div>
          <div className="cx-occbar"><div className="f" style={{ width: `${m.occPct}%`, background: occBar(m.level) }} /></div>
        </div>
        {isCart && (
          <div className="cx-crud">
            {/* Edit/Delete are live; Reshape needs canvas polygon editing, still a stub. */}
            <button onClick={() => onEditZone(z)}><Pencil size={12} /> Edit</button>
            <button onClick={() => onStub('Reshape zone')}><Move size={12} /> Reshape</button>
            <button className="danger" onClick={() => onDeleteZone(z)}><Trash2 size={12} /> Delete</button>
          </div>
        )}
      </div>
    );
  }

  if (selection.type === 'ap') {
    const ap = fp.access_points.find((x) => x.id === selection.id);
    if (!ap) return null;
    return (
      <div className="cx-float cx-inspect">
        <div className="cx-ins-head">
          <div className="ic"><Radio size={16} color="var(--teal)" /></div>
          <div>
            <div className="nm">{ap.name || ap.mac_address}</div>
            <div className="sub">Access point</div>
          </div>
          <button className="cx-ins-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="cx-ins-body">
          <div className="cx-kv"><span className="k">MAC</span><span className="v">{ap.mac_address}</span></div>
          <div className="cx-kv"><span className="k">Position</span><span className="v">{ap.x.toFixed(1)}, {ap.y.toFixed(1)}</span></div>
          <div className="cx-kv"><span className="k">Activity</span><span className="v">{apActivity(ap.id)}</span></div>
        </div>
        {isCart && (
          <div className="cx-crud">
            {/* Edit/Remove are live; Move needs canvas drag-to-position, still a stub. */}
            <button onClick={() => onEditAccessPoint(ap)}><Pencil size={12} /> Edit</button>
            <button onClick={() => onStub('Move AP')}><Move size={12} /> Move</button>
            <button className="danger" onClick={() => onDeleteAccessPoint(ap)}><Trash2 size={12} /> Remove</button>
          </div>
        )}
      </div>
    );
  }

  // asset
  const a = assets.find((x) => x.id === selection.id);
  if (!a) return null;
  const pos = a.last_x != null && a.last_y != null ? `${a.last_x.toFixed(1)}, ${a.last_y.toFixed(1)}` : 'unknown';
  return (
    <div className="cx-float cx-inspect">
      <div className="cx-ins-head">
        <div className="ic"><Box size={16} color="var(--occ-mod)" /></div>
        <div>
          <div className="nm">{a.name}</div>
          <div className="sub">Asset · {a.asset_type}</div>
        </div>
        <button className="cx-ins-close" onClick={onClose}><X size={16} /></button>
      </div>
      <div className="cx-ins-body">
        <div className="cx-kv"><span className="k">Position</span><span className="v">{pos}</span></div>
        <div className="cx-kv"><span className="k">MAC</span><span className="v">{a.mac_address}</span></div>
        <div className="cx-kv"><span className="k">Last seen</span><span className="v">{relativeTime(a.last_seen_at)}</span></div>
      </div>
      {isCart && (
        <div className="cx-crud">
          {/* Assets have full backend CRUD — these are live. */}
          <button onClick={() => onEditAsset(a)}><Pencil size={12} /> Edit</button>
          <button onClick={() => onStub('Move asset')}><Move size={12} /> Move</button>
          <button className="danger" onClick={() => onDeleteAsset(a)}><Trash2 size={12} /> Remove</button>
        </div>
      )}
    </div>
  );
}
