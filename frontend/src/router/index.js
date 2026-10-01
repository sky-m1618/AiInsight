import { createRouter, createWebHistory } from 'vue-router';

// Import Views
import Overview from '../views/Overview.vue';
import Datasets from '../views/Datasets.vue';
import EdaExplorer from '../views/EdaExplorer.vue';
import MlModels from '../views/MlModels.vue';
import Predictions from '../views/Predictions.vue';
import Reports from '../views/Reports.vue';
import Deployments from '../views/Deployments.vue';
import Settings from '../views/Settings.vue';
import Landing from '../views/Landing.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashBoard from '../views/AdminDashBoard.vue';

const routes = [
  { path: '/', name: 'Landing', component: Landing ,meta:{layout:'public'}},
  { path: '/login', name: 'Login', component: Login ,meta:{layout:'public'}},
  { path: '/register', name: 'Register', component: Register ,meta:{layout:'public'}},
  // { path: '/admin', name: 'Admin', component: Admin ,meta:{layout:'public'}},
  { path: '/overview', name: 'Overview', component: Overview,meta:{layout:'dashboard'} },
  { path: '/datasets', name: 'Datasets', component: Datasets ,meta:{layout:'dashboard'}},
  { path: '/eda', name: 'EDA Explorer', component: EdaExplorer ,meta:{layout:'dashboard'}},
  { path: '/models', name: 'ML Models', component: MlModels,meta:{layout:'dashboard'} },
  { path: '/predictions', name: 'Predictions', component: Predictions ,meta:{layout:'dashboard'}},
  { path: '/reports', name: 'Reports', component: Reports,meta:{layout:'dashboard'} },
  { path: '/deployments', name: 'Deployments', component: Deployments,meta:{layout:'dashboard'} },
  { path: '/settings', name: 'Settings', component: Settings,meta:{layout:'dashboard'} },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;