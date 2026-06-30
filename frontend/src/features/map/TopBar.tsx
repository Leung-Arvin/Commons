import { useEffect, useState } from 'react';
import { Bell, Search, Settings } from 'lucide-react';

import type { FloorPlanSummary, Role } from '../../lib/types';
import { CommonsLogomark } from './CommonsLogo';

interface Props {
  floors: FloorPlanSummary[];
  activeFloorId: string | null;
  onSelectFloor: (id: string) => void;
  role: Role;
  onSwitchRole: (r: Role) => void;
  query: string;
  onQuery: (q: string) => void;
}

function LiveClock() {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);
  return <>{now.toLocaleTimeString([], { hour12: false })}</>;
}

export function TopBar({ floors, activeFloorId, onSelectFloor, role, onSwitchRole, query, onQuery }: Props) {
  const isCart = role === 'cartographer';
  return (
    <div className="cx-float cx-top">
      <div className="cx-brand">
        <div className="cx-mark"><CommonsLogomark size={26} /></div>
        <span className="cx-brand-name cx-display">Commons</span>
        <span className="cx-tag">MVP</span>
      </div>
      <div className="cx-grip" />
      <div className="cx-floors">
        {floors.map((f) => (
          <button
            key={f.id} className={`cx-floor ${activeFloorId === f.id ? 'active' : ''}`}
            title={`${f.building} · ${f.name}`} onClick={() => onSelectFloor(f.id)}
          >
            {f.floor}
          </button>
        ))}
      </div>
      <div className="cx-top-right">
        <div className="cx-search">
          <Search size={13} />
          <input
            value={query} onChange={(e) => onQuery(e.target.value)}
            placeholder={isCart ? 'Search zones, APs…' : 'Search zones, assets…'}
          />
        </div>
        <div className="cx-clock"><span className="live" /> <LiveClock /></div>
        <div className="cx-roles">
          <button className={!isCart ? 'active' : ''} onClick={() => onSwitchRole('guest')}>Guest</button>
          <button className={isCart ? 'active' : ''} onClick={() => onSwitchRole('cartographer')}>Cartographer</button>
        </div>
        <button className="cx-ibtn" title="Notifications"><Bell size={15} /></button>
        <button className="cx-ibtn" title="Settings"><Settings size={15} /></button>
      </div>
    </div>
  );
}
