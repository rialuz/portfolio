import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'
import nextTs from 'eslint-config-next/typescript'

export default defineConfig([
  ...nextVitals,
  ...nextTs,
  globalIgnores([
    '.next/**',
    'out/**',
    'dist/**',
    'next-env.d.ts',
    'pixel-assets/**',
    'playwright-report/**',
    'test-results/**',
    // The Vue site this replaced, kept for reference.
    'legacy/**',
  ]),
])
