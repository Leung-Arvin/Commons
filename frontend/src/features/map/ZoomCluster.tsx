import { Maximize2, ZoomIn, ZoomOut } from 'lucide-react';

interface Props {
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFit: () => void;
}

export function ZoomCluster({ zoom, onZoomIn, onZoomOut, onFit }: Props) {
  return (
    <div className="cx-float cx-zoom">
      <button onClick={onZoomIn} title="Zoom in"><ZoomIn size={16} /></button>
      <div className="lvl">{Math.round(zoom * 100)}%</div>
      <button onClick={onZoomOut} title="Zoom out"><ZoomOut size={16} /></button>
      <button onClick={onFit} title="Fit to view"><Maximize2 size={15} /></button>
    </div>
  );
}
