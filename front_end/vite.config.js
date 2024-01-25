// FILE: vite.config.js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        transformAssetUrls
      }
    }),

    quasar({
      sassVariables: 'src/css/quasar-variables.sass'
    })
  ],
    server: {
      host: '0.0.0.0',
      port:  80,
    }
})
