import axios from 'axios';

// Centralized client. Defaults to same-origin so the Vite dev proxy (see
// vite.config.ts) can forward /api to the backend without CORS. In production,
// set VITE_API_URL to the backend origin (or front it with a reverse proxy).
export const API_BASE = import.meta.env.VITE_API_URL ?? '';

export const api = axios.create({ baseURL: API_BASE });
