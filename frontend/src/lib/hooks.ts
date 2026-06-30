import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from './api';
import type { Asset, FloorPlanDetail, FloorPlanSummary } from './types';

export function useFloorPlans() {
  return useQuery({
    queryKey: ['floor-plans'],
    // Trailing slash is canonical; without it FastAPI 307-redirects to the
    // absolute backend URL, which would bypass the dev proxy and hit CORS.
    queryFn: async () => (await api.get<FloorPlanSummary[]>('/api/v1/maps/')).data,
  });
}

export function useFloorPlan(mapId: string | null) {
  return useQuery({
    queryKey: ['floor-plan', mapId],
    enabled: !!mapId,
    queryFn: async () => (await api.get<FloorPlanDetail>(`/api/v1/maps/${mapId}`)).data,
  });
}

export function useAssets() {
  return useQuery({
    queryKey: ['assets'],
    queryFn: async () => (await api.get<Asset[]>('/api/v1/assets/')).data,
  });
}

// ---- Mutations (only the endpoints the backend currently exposes) ----

interface CreateZoneInput {
  name: string;
  zone_type?: string;
  polygon: number[][];
}

export function useCreateZone(mapId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: CreateZoneInput) =>
      (await api.post(`/api/v1/maps/${mapId}/zones`, input)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['floor-plan', mapId] }),
  });
}

interface UpdateZoneInput {
  id: string;
  name?: string;
  zone_type?: string;
  polygon?: number[][];
}

export function useUpdateZone(mapId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...patch }: UpdateZoneInput) =>
      (await api.put(`/api/v1/maps/${mapId}/zones/${id}`, patch)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['floor-plan', mapId] }),
  });
}

export function useDeleteZone(mapId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => (await api.delete(`/api/v1/maps/${mapId}/zones/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['floor-plan', mapId] }),
  });
}

interface CreateApInput {
  mac_address: string;
  name?: string | null;
  x: number;
  y: number;
}

export function useCreateAccessPoint(mapId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: CreateApInput) =>
      (await api.post(`/api/v1/maps/${mapId}/aps`, input)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['floor-plan', mapId] }),
  });
}

interface UpdateApInput {
  id: string;
  mac_address?: string;
  name?: string | null;
  x?: number;
  y?: number;
}

export function useUpdateAccessPoint(mapId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...patch }: UpdateApInput) =>
      (await api.put(`/api/v1/maps/${mapId}/aps/${id}`, patch)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['floor-plan', mapId] }),
  });
}

export function useDeleteAccessPoint(mapId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => (await api.delete(`/api/v1/maps/${mapId}/aps/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['floor-plan', mapId] }),
  });
}

export function useUpdateAsset() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...patch }: { id: string; name?: string; asset_type?: string }) =>
      (await api.put(`/api/v1/assets/${id}`, patch)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['assets'] }),
  });
}

export function useDeleteAsset() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => (await api.delete(`/api/v1/assets/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['assets'] }),
  });
}
