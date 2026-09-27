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

const routes = [
  { path: '/', name: 'Overview', component: Overview },
  { path: '/datasets', name: 'Datasets', component: Datasets },
  { path: '/eda', name: 'EDA Explorer', component: EdaExplorer },
  { path: '/models', name: 'ML Models', component: MlModels },
  { path: '/predictions', name: 'Predictions', component: Predictions },
  { path: '/reports', name: 'Reports', component: Reports },
  { path: '/deployments', name: 'Deployments', component: Deployments },
  { path: '/settings', name: 'Settings', component: Settings },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;