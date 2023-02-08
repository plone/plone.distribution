import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/++theme++barceloneta': 'http://localhost:8080',
      '/++resource++plone-admin-ui.css': 'http://localhost:8080',
      '/++resource++plone-logo.svg': 'http://localhost:8080',
      '/@@plone-addsite': 'http://localhost:8080',
      '/@sites': 'http://localhost:8080',
      '/@login': 'http://localhost:8080',
      '/@@ploneAddSite': 'http://localhost:8080',
    },
  },
  build: {
    chunkSizeWarningLimit: 800,
    assetsDir: '',
    rollupOptions: {
      input: 'src/main.tsx',
      output: {
        entryFileNames: 'plone-overview.min.js',
        assetFileNames: 'plone-overview.min.css',
      },
    },
  },
});
