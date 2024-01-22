import { createApp } from 'vue'
import App from './App.vue'
import './css/app.scss'

import { Quasar } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

import router from './routers/index.js'

const app = createApp(App)

app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
})
app.use(router)

app.mount('#app')
