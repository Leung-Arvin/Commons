import axios from 'axios';

// Base URL for the backend API. Override via `VITE_API_BASE_URL` in a .env
// file; defaults to the local backend exposed by docker-compose.
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});
