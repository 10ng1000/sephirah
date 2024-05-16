import { createApp } from 'vue'
import App from './App.vue'
import './css/app.css'
import './css/variables.css'
import router from './routers/index.js'
import { createPinia } from 'pinia'
import axios from 'axios'
import { createAuth0 } from '@auth0/auth0-vue';

const pinia = createPinia()
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL
axios.defaults.withCredentials = true


// createApp(App).use(pinia).use(router).use(
//   createAuth0({
//     domain: "dev-uhy8wfnt8jw8hxtk.us.auth0.com",
//     clientId: "r9aMvtmuhRE4aOqf5rDlroXIvzAtOKhX",
//     authorizationParams: {
//       redirect_uri: window.location.origin
//     }
//   })
// ).mount('#app')

createApp(App).use(pinia).use(router).mount('#app')