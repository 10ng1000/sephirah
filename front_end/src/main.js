import { createApp } from 'vue'
import App from './App.vue'
import './css/app.css'
import './css/variables.css'
import router from './routers/index.js'
import { createPinia } from 'pinia'
import axios from 'axios'

const pinia = createPinia()
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL
axios.defaults.withCredentials = true

createApp(App).use(pinia).use(router).mount('#app')
