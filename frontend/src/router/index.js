import { createRouter, createWebHistory } from 'vue-router'

// Import Views
import Overview from '../views/Overview.vue'
import Datasets from '../views/Datasets.vue'
import EdaExplorer from '../views/EdaExplorer.vue'
import MlModels from '../views/MlModels.vue'
import Predictions from '../views/Predictions.vue'
import Reports from '../views/Reports.vue'
import Deployments from '../views/Deployments.vue'
import Settings from '../views/Settings.vue'
import Landing from '../views/Landing.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashBoard from '../views/AdminDashBoard.vue'

const routes = [
  { path: '/', name: 'Landing', component: Landing, meta: { layout: 'public' } },
  { path: '/login', name: 'Login', component: Login, meta: { layout: 'public' } },
  { path: '/register', name: 'Register', component: Register, meta: { layout: 'public' } },
  { path: '/admin', name: 'Admin', component: AdminDashBoard, meta: { layout: 'admin', requiresAuth: true, requiresAdmin: true } },
  { path: '/overview', name: 'Overview', component: Overview, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/datasets', name: 'Datasets', component: Datasets, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/eda', name: 'EDA Explorer', component: EdaExplorer, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/models', name: 'ML Models', component: MlModels, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/predictions', name: 'Predictions', component: Predictions, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/reports', name: 'Reports', component: Reports, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/deployments', name: 'Deployments', component: Deployments, meta: { layout: 'dashboard', requiresAuth: true } },
  { path: '/settings', name: 'Settings', component: Settings, meta: { layout: 'dashboard', requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard — protect dashboard and admin routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')
  const role = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    return next({ name: 'Login' })
  }
  if (to.meta.requiresAdmin && role !== 'ADMIN') {
    return next({ name: 'Overview' })
  }
  // Redirect logged-in users away from login/register
  if ((to.name === 'Login' || to.name === 'Register') && token) {
    if (role === 'ADMIN') return next({ name: 'Admin' })
    return next({ name: 'Overview' })
  }
  next()
})

export default router