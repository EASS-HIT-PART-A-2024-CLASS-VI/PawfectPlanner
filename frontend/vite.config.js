import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",  // ✅ Allow external access
    port: 3000,  // ✅ Enforce correct port
    strictPort: true,
    proxy: {
      "/api": {
        target: "http://pawfect-planner-backend:8000", // ✅ Redirect API calls
        changeOrigin: true
      }
    }
  },
  optimizeDeps: {
    include: ["ics"],
  },
});
