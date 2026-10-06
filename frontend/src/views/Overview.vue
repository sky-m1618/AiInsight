<!-- src/views/Overview.vue -->
<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-bold text-gray-800">Overview</h2>
    </div>
    
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <p class="text-sm font-medium text-gray-500">Datasets</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">12</p>
        <p class="text-xs text-gray-400 mt-1">Total uploaded datasets</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <p class="text-sm font-medium text-gray-500">Models Trained</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">18</p>
        <p class="text-xs text-gray-400 mt-1">Total trained models</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <p class="text-sm font-medium text-gray-500">Predictions Made</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">1,248</p>
        <p class="text-xs text-gray-400 mt-1">Total predictions</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <p class="text-sm font-medium text-gray-500">Reports Generated</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">24</p>
        <p class="text-xs text-gray-400 mt-1">Total reports</p>
      </div>
    </div>

    <!-- Tables Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Datasets -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="font-semibold text-gray-800">Recent Datasets</h3>
          <router-link to="/datasets" class="text-sm text-blue-600 hover:text-blue-700 font-medium">View all datasets →</router-link>
        </div>
        <table class="w-full text-left text-sm text-gray-600">
          <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              <th class="px-5 py-3 font-medium">Name</th>
              <th class="px-5 py-3 font-medium">Rows</th>
              <th class="px-5 py-3 font-medium">Columns</th>
              <th class="px-5 py-3 font-medium">Uploaded</th>
              <th class="px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="ds in datasets" :key="ds.name" class="hover:bg-gray-50">
              <td class="px-5 py-3 font-medium text-gray-900">{{ ds.name }}</td>
              <td class="px-5 py-3">{{ ds.rows }}</td>
              <td class="px-5 py-3">{{ ds.cols }}</td>
              <td class="px-5 py-3">{{ ds.date }}</td>
              <td class="px-5 py-3">
                <span class="flex items-center gap-1.5 text-green-600 text-xs font-medium">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span> {{ ds.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Recent Model Runs -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="font-semibold text-gray-800">Recent Model Runs</h3>
          <router-link to="/models" class="text-sm text-blue-600 hover:text-blue-700 font-medium">View all models →</router-link>
        </div>
        <table class="w-full text-left text-sm text-gray-600">
          <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              <th class="px-5 py-3 font-medium">Model Name</th>
              <th class="px-5 py-3 font-medium">Task Type</th>
              <th class="px-5 py-3 font-medium">Best Score</th>
              <th class="px-5 py-3 font-medium">Run At</th>
              <th class="px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="run in modelRuns" :key="run.name" class="hover:bg-gray-50">
              <td class="px-5 py-3 font-medium text-gray-900">{{ run.name }}</td>
              <td class="px-5 py-3">{{ run.task }}</td>
              <td class="px-5 py-3">{{ run.score }}</td>
              <td class="px-5 py-3">{{ run.date }}</td>
              <td class="px-5 py-3">
                <span class="flex items-center gap-1.5 text-green-600 text-xs font-medium">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span> {{ run.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Bottom Charts Area -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
       <div class="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 class="font-semibold text-gray-800 mb-4">Model Performance (Last 7 Runs)</h3>
          <!-- Placeholder for Chart -->
          <div class="h-48 flex items-end justify-between gap-2 pt-4 border-b border-l border-gray-200 p-2">
             <div class="w-full bg-blue-100 rounded-t h-1/2"></div>
             <div class="w-full bg-blue-100 rounded-t h-2/3"></div>
             <div class="w-full bg-blue-100 rounded-t h-1/3"></div>
             <div class="w-full bg-blue-100 rounded-t h-3/4"></div>
             <div class="w-full bg-blue-100 rounded-t h-1/2"></div>
             <div class="w-full bg-blue-100 rounded-t h-4/5"></div>
             <div class="w-full bg-blue-100 rounded-t h-2/3"></div>
          </div>
       </div>
       <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col items-center justify-center">
          <h3 class="font-semibold text-gray-800 mb-4 self-start">Task Distribution</h3>
          <!-- Donut Chart Placeholder -->
          <div class="w-32 h-32 rounded-full border-8 border-blue-500 border-r-gray-200 border-b-gray-200 border-l-gray-200 flex items-center justify-center relative">
             <div class="absolute right-0 top-0 w-1/2 h-1/2 bg-white"></div>
          </div>
          <div class="mt-4 space-y-1 w-full text-xs text-gray-600">
             <div class="flex justify-between"><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-gray-200"></span>Regression</span> <span>35%</span></div>
             <div class="flex justify-between"><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-blue-500"></span>Classification</span> <span>30%</span></div>
             <div class="flex justify-between"><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-gray-400"></span>Forecasting</span> <span>15%</span></div>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import {api} from '../api/api.js';


const datasets = ref([]);
const modelRuns = ref([]);

onMounted(async () => {
  // Mocked Axios calls
  const mockData = await new Promise(resolve => setTimeout(() => resolve({
    datasets: [
      { name: 'sales_data.csv', rows: '24,532', cols: 18, date: 'May 19, 2024', status: 'Processed' },
      { name: 'customer_churn.xlsx', rows: '10,345', cols: 15, date: 'May 18, 2024', status: 'Processed' },
      { name: 'marketing_data.csv', rows: '8,765', cols: 21, date: 'May 16, 2024', status: 'Processed' },
      { name: 'transactions.csv', rows: '152,324', cols: 12, date: 'May 14, 2024', status: 'Processed' },
      { name: 'inventory_data.xlsx', rows: '5,324', cols: 16, date: 'May 12, 2024', status: 'Processed' },
    ],
    modelRuns: [
      { name: 'XGBoost Regressor', task: 'Regression', score: '0.92 (R²)', date: 'May 19, 2024', status: 'Completed' },
      { name: 'Random Forest', task: 'Classification', score: '0.89 (F1)', date: 'May 18, 2024', status: 'Completed' },
      { name: 'Prophet', task: 'Forecasting', score: '0.91 (MAE)', date: 'May 17, 2024', status: 'Completed' },
      { name: 'Isolation Forest', task: 'Anomaly Detection', score: '0.95 (AUC)', date: 'May 16, 2024', status: 'Completed' },
      { name: 'KMeans', task: 'Clustering', score: '0.72 (Silhouette)', date: 'May 15, 2024', status: 'Completed' },
    ]
  }), 500));
  
  datasets.value = mockData.datasets;
  modelRuns.value = mockData.modelRuns;
});

onMounted( async() =>{
  const response = await api.user.overviewdata('/overview')

  if (response.status == 200){
    console.log(response.data)
  }
  else{
    console.log(response.data)
  }
})
</script>