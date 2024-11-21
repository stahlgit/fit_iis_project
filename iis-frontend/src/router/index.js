// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Root from '../components/HelloWorld.vue'
import axios from 'axios'
import { ca } from 'vuetify/locale'

const API_BASE_URL = 'http://localhost:8000/'

const routes = [
  {
    path: '/',
    name: 'Root',
    redirect: '/public'
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
  },
  {
    path: '/main',
    name: 'Main',
    component: () => import('../components/MainView.vue'),
    children: [
      {
        path: 'conferences',
        name: 'Conferences',
        component: () => import('../components/ConferencesView.vue')
      },
      {
        path: 'rooms',
        name: 'Rooms',
        component: () => import('../components/RoomsView.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../components/UsersView.vue')
      },
      {
        path: 'reservations',
        name: 'Reservations',
        component: () => import('../components/ReservationsView.vue')
      },
      {
        path: 'tickets',
        name: 'Tickets',
        component: () => import('../components/TicketsView.vue')
      },
      {
        path: 'voting',
        name: 'Voting',
        component: () => import('../components/VotingView.vue')
      }
    ]
  },
  {
    path: '/public',
    name: 'Public',
    component: () => import('../components/PublicView.vue'),
  }
  ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation guard to check for authentication
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('authToken')
  console.log('Token:', token)
  if (to.name !== 'Login' && to.name !== 'Register' && to.name !== 'Public' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export async function register(username, email,password) {
  const url = 'http://localhost:8000/user/register';

  const userData = {
    name: username,
    email: email,
    password: password,
  };

  try {
    const response = await axios.post(url, userData, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    });

    console.log('Registration successful:', response.data);

    const loginSuccess = await login(email, password);
    if(loginSuccess) {
      await router.push('/main');
      return true;
    }
    else {
      console.error('Login failed:', error.response ? error.response.data : error.message);
      return false;
    }

  } catch (error) {
    if (error.response) {
      const errorMessage = error.response.data.detail || 'An error occurred';
      console.error('Registration failed:', errorMessage);
      alert(errorMessage); // Display error message to the user
    } else if (error.request) {
      console.error('No response received:', error.request);
      alert('No response from the server. Please try again later.');
    } else {
      console.error('Error:', error.message);
      alert('An unexpected error occurred. Please try again.');
    }
    return null;
  }
}


export async function login(username, password) {
  const url = 'http://localhost:8000/user/token';

  // Form data as a URL-encoded string
  const formData = new URLSearchParams();
  formData.append('grant_type', 'password');
  formData.append('username', username);
  formData.append('password', password);
  formData.append('scope', '');
  formData.append('client_id', 'string'); // Use the correct client ID
  formData.append('client_secret', 'string'); // Use the correct client secret

  try {
    const response = await axios.post(url, formData, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      }

    });

    localStorage.setItem('authToken', response.data.access_token);
    await router.push('/main');
    return true;
  } catch (error) {
    console.error('Login failed:', error.response ? error.response.data : error.message);
    return null; // Handle error appropriately
  }
}

export async function logout() {
  localStorage.removeItem('authToken')
  await router.push('/')
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
