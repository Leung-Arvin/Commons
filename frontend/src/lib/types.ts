// Types mirror the backend responses defined in shared/openapi/map.yaml.

export interface FloorPlanSummary {
  id: string;
  name: string;
  building: string;
  floor: string;
}

export interface Zone {
  id: string;
  floor_plan_id: string;
  name: string;
  zone_type: string;
  polygon: number[][]; // [[x, y], ...] in floor-plan coordinates
}

export interface AccessPoint {
  id: string;
  floor_plan_id: string;
  mac_address: string;
  name: string | null;
  x: number;
  y: number;
}

export interface FloorPlanDetail {
  id: string;
  name: string;
  building: string;
  floor: string;
  svg_url: string | null;
  image_url: string | null;
  width: number;
  height: number;
  zones: Zone[];
  access_points: AccessPoint[];
}

export interface Asset {
  id: string;
  name: string;
  mac_address: string;
  asset_type: string;
  last_x: number | null;
  last_y: number | null;
  last_floor_id: string | null;
  last_seen_at: string | null;
  created_at: string;
}

export type Role = 'guest' | 'cartographer';
export type LayerKey = 'occupancy' | 'devices' | 'heatmap' | 'zones' | 'assets';
export type OccLevel = 'vacant' | 'low' | 'moderate' | 'high' | 'full';

export type Selection =
  | { type: 'zone'; id: string }
  | { type: 'ap'; id: string }
  | { type: 'asset'; id: string }
  | null;
