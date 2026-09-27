<!-- src/views/Datasets.vue -->
<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <div>
      <h2 class="text-xl font-bold text-gray-800">Upload Dataset</h2>
      <p class="text-sm text-gray-500">Upload your dataset to get started with automated analysis and ML.</p>
    </div>

    <!-- Upload Area -->
    <div class="bg-white p-8 rounded-xl border-2 border-dashed border-gray-300 flex flex-col items-center justify-center text-center hover:bg-gray-50 transition-colors cursor-pointer">
      <svg class="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
      <p class="text-gray-700 font-medium">Drag & Drop your file here</p>
      <p class="text-sm text-gray-500 mb-4">or</p>
      <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors">Browse files</button>
      <p class="text-xs text-gray-400 mt-4">Supports: CSV, XLSX (Max size: 200MB)</p>
    </div>

    <!-- Upload History -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-800">Upload History</h3>
      </div>
      <table class="w-full text-left text-sm text-gray-600">
        <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
          <tr>
            <th class="px-5 py-3 font-medium">File Name</th>
            <th class="px-5 py-3 font-medium">Rows</th>
            <th class="px-5 py-3 font-medium">Columns</th>
            <th class="px-5 py-3 font-medium">Uploaded At</th>
            <th class="px-5 py-3 font-medium">Status</th>
            <th class="px-5 py-3 font-medium">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="ds in history" :key="ds.name" class="hover:bg-gray-50">
            <td class="px-5 py-3 font-medium text-gray-900">{{ ds.name }}</td>
            <td class="px-5 py-3">{{ ds.rows }}</td>
            <td class="px-5 py-3">{{ ds.cols }}</td>
            <td class="px-5 py-3">{{ ds.date }}</td>
            <td class="px-5 py-3">
              <span class="text-green-600 text-xs font-medium">{{ ds.status }}</span>
            </td>
            <td class="px-5 py-3 flex gap-2">
              <button class="p-1 text-gray-400 hover:text-blue-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg></button>
              <button class="p-1 text-gray-400 hover:text-red-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const history = ref([]);
onMounted(async () => {
  const res = await new Promise(r => setTimeout(() => r({
    data: [
      { name: 'sales_data.csv', rows: '24,532', cols: 18, date: 'May 19, 2024 10:30 AM', status: 'Processed' },
      { name: 'customer_churn.xlsx', rows: '10,345', cols: 15, date: 'May 18, 2024 02:15 PM', status: 'Processed' },
      { name: 'marketing_data.csv', rows: '8,765', cols: 21, date: 'May 16, 2024 11:45 AM', status: 'Processed' },
      { name: 'transactions.csv', rows: '152,324', cols: 12, date: 'May 14, 2024 09:20 AM', status: 'Processed' },
    ]
  }), 500));
  history.value = res.data;
});
</script>