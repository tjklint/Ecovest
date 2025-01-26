import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';
import { sveltePreprocess } from 'svelte-preprocess';

export default defineConfig({
  plugins: [
    svelte({
      preprocess: sveltePreprocess({
        typescript: true 
      }),
      compilerOptions: {
        compatibility: {
          componentApi: 4
        }
      }
    })  ],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
        analytics: path.resolve(__dirname, 'analytics.html')
      }
    }
  }
});
