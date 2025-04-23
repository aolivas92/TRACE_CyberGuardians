// vitest.config.js
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom'
  },
  resolve: {
    alias: {
      $lib: path.resolve('./src/lib'),
      $test: path.resolve('./src/test'),
      $app: path.resolve('./.svelte-kit/types/app'),
    }
  }
});