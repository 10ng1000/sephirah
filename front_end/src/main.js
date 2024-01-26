import { createApp } from 'vue'
import App from './App.vue'
import './css/app.css'
import './css/variables.css'
import router from './routers/index.js'


createApp(App).use(router).mount('#app')
