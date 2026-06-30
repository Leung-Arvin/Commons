import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy API calls to the backend so the browser stays same-origin (no CORS).
    // Override the target with VITE_PROXY_TARGET if the backend runs elsewhere.
    proxy: {
      '/api': {
        target: process.env.VITE_PROXY_TARGET ?? 'http://localhost:8003',
        changeOrigin: true,
      },
    },
  },
})
