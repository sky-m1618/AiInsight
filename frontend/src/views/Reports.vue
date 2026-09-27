<!-- src/views/Reports.vue -->
<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Reports</h2>
        <p class="text-sm text-gray-500">View and download your generated reports</p>
      </div>
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Generate Report
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="report in reports" :key="report.title" class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
        <div>
          <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          </div>
          <h3 class="font-semibold text-gray-800">{{ report.title }}</h3>
          <p class="text-xs text-gray-500 mt-1">{{ report.dataset }}</p>
        </div>
        <div class="flex justify-between items-center mt-6 pt-4 border-t border-gray-100">
          <p class="text-xs text-gray-400">{{ report.date }} · {{ report.size }}</p>
          <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref ,onMounted} from 'vue';

const reports = ref([
  { title: 'Sales Analysis Report', dataset: 'sales_data.csv', date: 'May 18, 2024', size: '2.4 MB' },
  { title: 'Churn Prediction Report', dataset: 'customer_churn.xlsx', date: 'May 18, 2024', size: '1.8 MB' },
  { title: 'Marketing Insights Report', dataset: 'marketing_data.csv', date: 'May 16, 2024', size: '2.1 MB' },
  { title: 'Forecast Report', dataset: 'sales_data.csv', date: 'May 15, 2024', size: '1.7 MB' },
  { title: 'Anomaly Detection Report', dataset: 'transactions.csv', date: 'May 14, 2024', size: '1.9 MB' },
  { title: 'Inventory Analysis Report', dataset: 'inventory_data.xlsx', date: 'May 12, 2024', size: '2.0 MB' },
]);


const edaData = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    // Fetch the latest generated EDA entry record from your database
    const response = await fetch('http://127.0.0.1:5000/api/ml/analyze');
    const data = await response.json();
    
    edaData.value = data.eda_summary;
    const message = data.message;
    console.log(message)
    console.log(edaData)
    // Map edaData.value to your ApexCharts / Chart.js series configurations here!
  } catch (error) {
    console.error("Failed loading data metric reports:", error);
  } finally {
    loading.value = false;
  }
});
</script>

