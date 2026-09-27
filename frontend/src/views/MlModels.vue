<!-- src/views/MlModels.vue -->
<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-bold text-gray-800">Model Runs</h2>
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        New Model Run
      </button>
    </div>

    <!-- Create New Run Form -->
    <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
      <h3 class="font-semibold text-gray-800 mb-4">Create New Run</h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Select Dataset</label>
          <select class="w-full border border-gray-300 rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>sales_data.csv</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Select Task Type</label>
          <select class="w-full border border-gray-300 rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Regression</option>
            <option>Classification</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Target Variable</label>
          <select class="w-full border border-gray-300 rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Sales</option>
          </select>
        </div>
        <button class="w-full py-2 bg-gray-800 text-white rounded-lg text-sm font-medium hover:bg-gray-900 transition-colors">Configure & Train</button>
      </div>
    </div>

    <!-- Model Comparison Chart Placeholder -->
    <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
      <h3 class="font-semibold text-gray-800 mb-4">Model Comparison</h3>
      <div class="space-y-4">
        <div v-for="model in comparison" :key="model.name" class="grid grid-cols-12 gap-4 items-center text-sm">
          <div class="col-span-3 font-medium text-gray-800">{{ model.name }}</div>
          <div class="col-span-1 text-gray-500">{{ model.r2 }}</div>
          <div class="col-span-1 text-gray-500">{{ model.rmse }}</div>
          <div class="col-span-1 text-gray-500">{{ model.mae }}</div>
          <div class="col-span-1 text-gray-500">{{ model.time }}</div>
          <div class="col-span-5">
             <div class="w-full bg-gray-100 rounded-full h-2">
                <div class="bg-blue-500 h-2 rounded-full" :style="{ width: (model.r2 * 100) + '%' }"></div>
             </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Runs Table -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-800">Recent Runs</h3>
      </div>
      <table class="w-full text-left text-sm text-gray-600">
        <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
          <tr>
            <th class="px-5 py-3 font-medium">Model Name</th>
            <th class="px-5 py-3 font-medium">Task Type</th>
            <th class="px-5 py-3 font-medium">Dataset</th>
            <th class="px-5 py-3 font-medium">Best Score</th>
            <th class="px-5 py-3 font-medium">Run At</th>
            <th class="px-5 py-3 font-medium">Status</th>
            <th class="px-5 py-3 font-medium">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="run in recentRuns" :key="run.name" class="hover:bg-gray-50">
            <td class="px-5 py-3 font-medium text-gray-900">{{ run.name }}</td>
            <td class="px-5 py-3">{{ run.task }}</td>
            <td class="px-5 py-3">{{ run.dataset }}</td>
            <td class="px-5 py-3">{{ run.score }}</td>
            <td class="px-5 py-3">{{ run.date }}</td>
            <td class="px-5 py-3">
              <span class="flex items-center gap-1.5 text-green-600 text-xs font-medium">
                <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span> {{ run.status }}
              </span>
            </td>
            <td class="px-5 py-3">
               <button class="text-blue-600 hover:text-blue-800 text-xs font-medium">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const comparison = ref([
  { name: 'XGBoost Regressor', r2: 0.92, rmse: 2.34, mae: 1.45, time: '00:01:23' },
  { name: 'Random Forest', r2: 0.88, rmse: 2.67, mae: 1.78, time: '00:01:10' },
  { name: 'LightGBM', r2: 0.91, rmse: 2.45, mae: 1.52, time: '00:00:58' },
  { name: 'Linear Regression', r2: 0.78, rmse: 3.45, mae: 2.34, time: '00:00:05' },
]);

const recentRuns = ref([
  { name: 'XGBoost Regressor', task: 'Regression', dataset: 'sales_data.csv', score: '0.92 (R²)', date: 'May 19, 2024', status: 'Completed' },
  { name: 'Random Forest', task: 'Classification', dataset: 'customer_churn.xlsx', score: '0.89 (F1)', date: 'May 18, 2024', status: 'Completed' },
  { name: 'Prophet', task: 'Forecasting', dataset: 'sales_data.csv', score: '0.91 (MAE)', date: 'May 17, 2024', status: 'Completed' },
  { name: 'Linear Regression', task: 'Regression', dataset: 'marketing_data.csv', score: '0.78 (R²)', date: 'May 16, 2024', status: 'Completed' },
  { name: 'Isolation Forest', task: 'Anomaly Detection', dataset: 'transactions.csv', score: '0.95 (AUC)', date: 'May 16, 2024', status: 'Completed' },
]);
</script>