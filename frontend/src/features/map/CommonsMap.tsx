import { useMemo, useState } from 'react';

import '../../styles/commons-map.css';
import type { Asset, LayerKey, Role, Selection } from '../../lib/types';
import { zoneMetrics } from '../../lib/metrics';
import {
  useAssets, useCreateZone, useDeleteAsset, useFloorPlan, useFloorPlans, useUpdateAsset,
} from '../../lib/hooks';
import { TopBar } from './TopBar';
import { LayerDock } from './LayerDock';
import { MapStage } from './MapStage';
import { CartographerPalette } from './CartographerPalette';
import { Inspector } from './Inspector';
import { Legend } from './Legend';
import { StatusChips } from './StatusChips';
import { ZoomCluster } from './ZoomCluster';

const RESTRICTED: LayerKey[] = ['occupancy', 'devices'];

export function CommonsMap() {
  const [role, setRole] = useState<Role>('guest');
  const [pickedFloorId, setPickedFloorId] = useState<string | null>(null);
  const [layer, setLayer] = useState<LayerKey>('heatmap');
  const [selected, setSelected] = useState<Selection>(null);
  const [query, setQuery] = useState('');
  const [zoom, setZoom] = useState(1);
  const [hint, setHint] = useState<string | null>(null);
  const isCart = role === 'cartographer';

  const floorsQ = useFloorPlans();
  // Derive the active floor rather than syncing it via an effect: the picked
  // floor wins, otherwise fall back to the first one once floors load.
  const activeFloorId = pickedFloorId ?? floorsQ.data?.[0]?.id ?? null;
  const fpQ = useFloorPlan(activeFloorId);
  const assetsQ = useAssets();

  const createZone = useCreateZone(activeFloorId ?? '');
  const updateAsset = useUpdateAsset();
  const deleteAsset = useDeleteAsset();

  const fp = fpQ.data;
  const floorAssets = useMemo<Asset[]>(
    () => (assetsQ.data ?? []).filter((a) => a.last_floor_id === activeFloorId),
    [assetsQ.data, activeFloorId],
  );

  const switchRole = (r: Role) => {
    setRole(r);
    setSelected(null);
    if (r === 'guest' && RESTRICTED.includes(layer)) setLayer('heatmap');
  };

  const flash = (msg: string) => {
    setHint(msg);
    window.setTimeout(() => setHint((h) => (h === msg ? null : h)), 2600);
  };
  const onStub = (label: string) => flash(`“${label}” isn’t wired up yet — design stub.`);

  const onNewZone = () => {
    if (!fp || createZone.isPending) return;
    const cx = fp.width / 2, cy = fp.height / 2, h = Math.min(fp.width, fp.height) * 0.12;
    createZone.mutate({
      name: 'New Zone',
      zone_type: 'general',
      polygon: [[cx - h, cy - h], [cx + h, cy - h], [cx + h, cy + h], [cx - h, cy + h]],
    });
  };

  const onEditAsset = (a: Asset) => {
    const name = window.prompt('Rename asset', a.name);
    if (name && name !== a.name) updateAsset.mutate({ id: a.id, name });
  };
  const onDeleteAsset = (a: Asset) => {
    if (window.confirm(`Remove “${a.name}”?`)) {
      deleteAsset.mutate(a.id);
      setSelected(null);
    }
  };

  const statusChips = useMemo<[string, string][]>(() => {
    const zones = fp?.zones ?? [];
    if (isCart) {
      const agg = zones.reduce(
        (acc, z) => {
          const m = zoneMetrics(z.id);
          return { occ: acc.occ + m.occPct, dev: acc.dev + m.devices };
        },
        { occ: 0, dev: 0 },
      );
      const avgOcc = zones.length ? Math.round(agg.occ / zones.length) : 0;
      return [
        ['Occ.', `${avgOcc}%`], ['Devices', String(agg.dev)],
        ['APs', String(fp?.access_points.length ?? 0)], ['Zones', String(zones.length)],
        ['Assets', String(floorAssets.length)], ['Sync', 'live'],
      ];
    }
    return [
      ['Zones', String(zones.length)], ['Assets', String(floorAssets.length)],
      ['Floor', fp?.floor ?? '—'], ['Sync', 'live'],
    ];
  }, [isCart, fp, floorAssets.length]);

  // ---- top-level states ----
  if (floorsQ.isLoading) {
    return <div className="cx-root"><div className="cx-empty"><div className="small">Loading…</div></div></div>;
  }
  if (floorsQ.error) {
    return (
      <div className="cx-root">
        <div className="cx-empty">
          <div className="big">Can’t reach the API</div>
          <div className="small">{String(floorsQ.error)}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="cx-root">
      {/* FULL-BLEED MAP */}
      {fp ? (
        <MapStage
          fp={fp} assets={floorAssets} layer={layer} isCart={isCart}
          selected={selected} query={query} zoom={zoom} onSelect={setSelected}
        />
      ) : (
        <div className="cx-map">
          <div className="cx-empty">
            {floorsQ.data?.length ? (
              <div className="small">Loading floor…</div>
            ) : (
              <>
                <div className="big">No floor plans yet</div>
                <div className="small">Create a floor plan via the API (POST /api/v1/maps) and it’ll appear here as a floor tab.</div>
              </>
            )}
          </div>
        </div>
      )}

      <TopBar
        floors={floorsQ.data ?? []} activeFloorId={activeFloorId}
        onSelectFloor={(id) => { setPickedFloorId(id); setSelected(null); }}
        role={role} onSwitchRole={switchRole} query={query} onQuery={setQuery}
      />

      {isCart && fp && (
        <CartographerPalette onNewZone={onNewZone} onStub={onStub} creating={createZone.isPending} />
      )}

      {hint ? (
        <div className="cx-hint">{hint}</div>
      ) : (!selected && !isCart && fp ? (
        <div className="cx-hint">Select a zone or asset to inspect it</div>
      ) : null)}

      {/* Occupancy/heatmap/people/AP-stats are demo values (see metrics.ts). */}
      <div className="cx-demobadge" title="Occupancy, heatmap, people and AP stats are placeholder data">Sample metrics</div>

      {fp && <LayerDock layer={layer} role={role} onLayer={setLayer} />}
      {fp && <Legend />}
      {fp && <StatusChips chips={statusChips} />}
      {fp && (
        <ZoomCluster
          zoom={zoom}
          onZoomIn={() => setZoom((z) => Math.min(2, +(z + 0.25).toFixed(2)))}
          onZoomOut={() => setZoom((z) => Math.max(0.5, +(z - 0.25).toFixed(2)))}
          onFit={() => setZoom(1)}
        />
      )}

      {fp && (
        <Inspector
          selection={selected} fp={fp} assets={floorAssets} isCart={isCart}
          onClose={() => setSelected(null)} onEditAsset={onEditAsset}
          onDeleteAsset={onDeleteAsset} onStub={onStub}
        />
      )}
    </div>
  );
}
