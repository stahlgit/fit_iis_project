// Composables
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import { setUserRole } from '@/services/utils';

export const API_BASE_URL = 'http://164.92.232.11:8000/'

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['Authorization']= `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// interceptor to refresh token on 401 error
axiosInstance.interceptors.response.use(response => {
  return response;
}, async error => {
  if (error.response.status === 401) {
    localStorage.removeItem('authToken');
    await router.push('/login');
  }
});

const authentiatedAxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
  },
});


export { axiosInstance, authentiatedAxiosInstance };

async function refreshUserSession() {
  try {
    axiosInstance.get('user/me')
  } catch (error) {
    localStorage.removeItem('authToken')
    await router.push('/login')
  }
}

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
    redirect: '/main/tickets',
    children: [
      {
        path: 'conferences',
        name: 'Konference',
        component: () => import('../components/ConferencesView.vue')
      },
      {
        path: 'rooms',
        name: 'Místnosti',
        component: () => import('../components/RoomsView.vue')
      },
      {
        path: 'users',
        name: 'Uživatelé',
        component: () => import('../components/UsersView.vue')
      },
      {
        path: 'reservations',
        name: 'Rezervace',
        component: () => import('../components/ReservationsView.vue')
      },
      {
        path: 'tickets',
        name: 'Vstupenky',
        component: () => import('../components/TicketsView.vue')
      },
      {
        path: 'voting',
        name: 'Hlasování',
        component: () => import('../components/VotingView.vue')
      },
      {
        path: 'presentations',
        name: 'Prezentace',
        component: () => import('../components/PresentationsView.vue')
      }
    ]
  },
  {
    path: '/public',
    name: 'Public',
    component: () => import('../components/PublicView.vue')
  },
  {
    path: '/public/conference/:id',
    name: 'PublicDetail',
    component: () => import('../components/PublicDetailView.vue'),
    props: true
  }
  ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation guard to check for authentication
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('authToken')
  if (to.name !== 'Login' && to.name !== 'Register' && to.name !== 'Public' && to.name !== 'PublicDetail' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export async function register(username, email,password) {
  const url = API_BASE_URL + 'user/register';

  const userData = {
    name: username,
    email: email,
    password: password,
    role: "registered"
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
  const url = API_BASE_URL + 'user/token';

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
    setUserRole(response.data.role);
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

export function isLoggedIn() {
  return localStorage.getItem('authToken') != null
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
