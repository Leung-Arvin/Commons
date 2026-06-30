import { Activity, Box, Hexagon, Users, Wifi } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

import type { LayerKey, Role } from '../../lib/types';

const GUEST_LAYERS: [LayerKey, LucideIcon, string][] = [
  ['heatmap', Activity, 'Heatmap'],
  ['zones', Hexagon, 'Zones'],
  ['assets', Box, 'Assets'],
];

const CART_LAYERS: [LayerKey, LucideIcon, string][] = [
  ['occupancy', Users, 'Occupancy'],
  ['devices', Wifi, 'Devices'],
  ...GUEST_LAYERS,
];

export function LayerDock({ layer, role, onLayer }: { layer: LayerKey; role: Role; onLayer: (l: LayerKey) => void }) {
  const layers = role === 'cartographer' ? CART_LAYERS : GUEST_LAYERS;
  return (
    <div className="cx-float cx-dock-left">
      <div className="cx-dock-label">Layers</div>
      {layers.map(([key, Icon, label]) => (
        <button key={key} className={`cx-dockbtn ${layer === key ? 'active' : ''}`} onClick={() => onLayer(key)}>
          <Icon size={17} /> <span className="lab">{label}</span>
        </button>
      ))}
    </div>
  );
}
