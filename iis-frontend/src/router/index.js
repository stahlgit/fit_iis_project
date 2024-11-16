// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Root from '../components/HelloWorld.vue'
import axios from 'axios'

const routes = [
  {
    path: '/',
    name: 'Root',
    component: Root
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/RegisterView.vue')
  }
  ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation guard to check for authentication
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('authToken')
  if (to.name !== 'Login' && to.name !== 'Register' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

// Function to log in the user and set JWT in local storage
async function login(username, password) {
  try {
    const response = await axios.post('/api/login', { username, password })
    const token = response.data.token
    localStorage.setItem('authToken', token)
    return true
  } catch (error) {
    console.error('Login failed:', error)
    return false
  }
}

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
