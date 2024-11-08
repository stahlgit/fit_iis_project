import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import { createVuetify } from 'vuetify'
import 'vuetify/dist/vuetify.css'

// creating vuetify instance
const vuetify = createVuetify({
    // all your configurations of vuetify
})

const app = createApp(App)
app.use(vuetify)
app.mount('#app')