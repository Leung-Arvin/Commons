import { useQuery } from '@tanstack/react-query';
import { api, API_BASE_URL } from '../lib/api';

interface FloorPlan {
  id: string;
  name: string;
  building: string;
  floor: string;
  svg_url: string | null;
  image_url: string | null;
  width: number;
  height: number;
  zones: Array<{
    id: string;
    name: string;
    zone_type: string;
    polygon: number[][];
  }>;
  access_points: Array<{
    id: string;
    mac_address: string;
    name: string | null;
    x: number;
    y: number;
  }>;
}

const ZONE_COLORS: Record<string, string> = {
  meeting_room: '#3b82f6',  // blue
  desk_area: '#10b981',     // green
  general: '#f59e0b',       // amber
};

export function FloorMap({ mapId }: { mapId: string }) {
  const { data: fp, isLoading, error } = useQuery({
    queryKey: ['floor-plan', mapId],
    queryFn: async () => {
      const { data } = await api.get<FloorPlan>(`/api/v1/maps/${mapId}`);
      return data;
    },
  });

  if (isLoading) return <div className="p-6">Loading map...</div>;
  if (error || !fp) return <div className="p-6 text-red-600">Error loading map</div>;

  const imageUrl = fp.svg_url || fp.image_url;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2">{fp.name}</h1>
      <p className="text-gray-600 mb-4">{fp.building} · Floor {fp.floor}</p>

      <div 
        className="relative border rounded overflow-hidden bg-white"
        style={{ width: '100%', maxWidth: fp.width, aspectRatio: `${fp.width}/${fp.height}` }}
      >
        {/* Floor plan image */}
        {imageUrl && (
          <img
            src={`${API_BASE_URL}${imageUrl}`}
            alt={fp.name}
            className="absolute inset-0 w-full h-full object-contain"
          />
        )}

        {/* SVG overlay for zones */}
        <svg
          viewBox={`0 0 ${fp.width} ${fp.height}`}
          className="absolute inset-0 w-full h-full"
          style={{ pointerEvents: 'none' }}
        >
          {/* Zone polygons */}
          {fp.zones.map((zone) => {
            const points = zone.polygon.map(([x, y]) => `${x},${y}`).join(' ');
            const color = ZONE_COLORS[zone.zone_type] || '#6b7280';
            return (
              <g key={zone.id}>
                <polygon
                  points={points}
                  fill={color}
                  fillOpacity={0.25}
                  stroke={color}
                  strokeWidth={2}
                  style={{ pointerEvents: 'auto', cursor: 'pointer' }}
                >
                  <title>{zone.name}</title>
                </polygon>
                {/* Zone label */}
                <text
                  x={zone.polygon[0][0] + 10}
                  y={zone.polygon[0][1] + 20}
                  fontSize={14}
                  fill={color}
                  fontWeight="bold"
                  style={{ pointerEvents: 'none' }}
                >
                  {zone.name}
                </text>
              </g>
            );
          })}

          {/* Access points */}
          {fp.access_points.map((ap) => (
            <g key={ap.id}>
              <circle
                cx={ap.x}
                cy={ap.y}
                r={8}
                fill="#ef4444"
                stroke="white"
                strokeWidth={2}
              >
                <title>{ap.name || ap.mac_address}</title>
              </circle>
              <text
                x={ap.x + 12}
                y={ap.y + 4}
                fontSize={12}
                fill="#ef4444"
                fontWeight="bold"
              >
                {ap.name || 'AP'}
              </text>
            </g>
          ))}
        </svg>
      </div>

      {/* Legend */}
      <div className="mt-4 flex gap-4 text-sm">
        {Object.entries(ZONE_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: color, opacity: 0.5 }} />
            <span className="capitalize">{type.replace('_', ' ')}</span>
          </div>
        ))}
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-red-500" />
          <span>Access Point</span>
        </div>
      </div>
    </div>
  );
}