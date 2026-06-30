import { Box, Pencil, Plus, Radio, Square, UploadCloud } from 'lucide-react';

interface Props {
  onNewZone: () => void;
  onStub: (label: string) => void;
  creating: boolean;
}

// Per DESIGN_HANDOFF, these tools are stubs (no real interaction/backend yet):
// draw-dots canvas, preset shapes, WAP coverage simulation, connect-asset
// search, and plan upload. They stay present and clickable but announce that
// they're not wired. "New zone" is the one wired action — it hits the real
// POST /maps/{id}/zones endpoint with a default square the cartographer can
// later reshape (reshape itself is still a stub).
export function CartographerPalette({ onNewZone, onStub, creating }: Props) {
  return (
    <div className="cx-float cx-palette">
      <button className="cx-pal-btn primary" onClick={onNewZone} disabled={creating}>
        <Plus size={14} /> {creating ? 'Adding…' : 'New zone'}
      </button>
      <button className="cx-pal-btn" onClick={() => onStub('Draw zone (dots)')}><Pencil size={14} /> Draw dots</button>
      <button className="cx-pal-btn" onClick={() => onStub('Preset shapes')}><Square size={14} /> Shapes</button>
      <div className="cx-pal-sep" />
      <button className="cx-pal-btn" onClick={() => onStub('Simulate WAP')}><Radio size={14} /> Simulate WAP</button>
      <button className="cx-pal-btn" onClick={() => onStub('Connect asset')}><Box size={14} /> Connect asset</button>
      <div className="cx-pal-sep" />
      <button className="cx-pal-btn" onClick={() => onStub('Upload plan')}><UploadCloud size={14} /> Upload plan</button>
    </div>
  );
}
