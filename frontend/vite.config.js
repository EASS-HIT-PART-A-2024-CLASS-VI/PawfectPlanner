import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 3000,  // ✅ Force the correct port
    strictPort: true,  // ✅ Prevent auto-switching to 3001+
    proxy: {
      "/api": {
        target: "http://pawfect-planner-backend:8000",
        changeOrigin: true
      }
    }
  },
  optimizeDeps: {
    include: ["ics"],
  },
});