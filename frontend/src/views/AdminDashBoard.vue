<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar (Simplified for Admin context) -->
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col">
      <div class="h-16 flex items-center px-6 border-b border-gray-200">
        <h1 class="text-xl font-bold text-gray-800 flex items-center gap-2">
          <span class="w-6 h-6 bg-blue-600 rounded-md flex items-center justify-center text-white text-xs">A</span>
          AutoML
        </h1>
      </div>
      <nav class="flex-1 px-4 py-6 space-y-1">
        <a href="#" class="flex items-center gap-3 px-3 py-2 bg-blue-50 text-blue-700 rounded-lg font-medium">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
          Admin Overview
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg font-medium transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          User Management
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg font-medium transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          System Logs
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg font-medium transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          Settings
        </a>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Header -->
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-semibold text-gray-800">Admin Overview</h2>
        <div class="flex items-center gap-4">
          <button class="p-2 text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
          </button>
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm">A</div>
            <span class="text-sm font-medium text-gray-700">Admin User</span>
          </div>
        </div>
      </header>

      <!-- Dashboard Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg">
          {{ error }}
        </div>

        <!-- Dashboard Grid -->
        <div v-else class="space-y-6">
          
          <!-- Top Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <p class="text-sm font-medium text-gray-500">Total Users</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalUsers }}</p>
              <p class="text-xs text-green-600 mt-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                +12% from last month
              </p>
            </div>
            <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <p class="text-sm font-medium text-gray-500">Active Sessions</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.activeSessions }}</p>
              <p class="text-xs text-gray-500 mt-1">Current live users</p>
            </div>
            <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <p class="text-sm font-medium text-gray-500">Total Datasets</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalDatasets }}</p>
              <p class="text-xs text-green-600 mt-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                +8% from last month
              </p>
            </div>
            <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <p class="text-sm font-medium text-gray-500">Models Trained</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.modelsTrained }}</p>
              <p class="text-xs text-gray-500 mt-1">Across all users</p>
            </div>
          </div>

          <!-- Middle Section: Chart and System Health -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- User Activity Chart Placeholder -->
            <div class="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
              <h3 class="text-base font-semibold text-gray-800 mb-4">User Activity (Last 7 Days)</h3>
              <!-- Note: In a real app, you would use a library like Chart.js or ApexCharts here -->
              <div class="h-64 flex items-end justify-between gap-2 pt-4">
                <div v-for="(val, index) in activityChart.datasets[0].data" :key="index" class="flex flex-col items-center flex-1">
                  <div class="w-full bg-blue-100 rounded-t-sm relative group">
                    <div class="absolute bottom-0 w-full bg-blue-500 rounded-t-sm transition-all duration-300" :style="{ height: (val / 400) * 100 + '%' }"></div>
                  </div>
                  <span class="text-xs text-gray-500 mt-2">{{ activityChart.labels[index] }}</span>
                </div>
              </div>
            </div>

            <!-- System Health -->
            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
              <h3 class="text-base font-semibold text-gray-800 mb-4">System Health</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-gray-600">CPU Usage</span>
                    <span class="font-medium text-gray-900">{{ systemHealth.cpu }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-500 h-2 rounded-full" style="width: 45%"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-gray-600">Memory Usage</span>
                    <span class="font-medium text-gray-900">{{ systemHealth.memory }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-500 h-2 rounded-full" style="width: 62%"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-gray-600">API Latency</span>
                    <span class="font-medium text-gray-900">{{ systemHealth.apiLatency }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full" style="width: 20%"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Section: Recent Activities Table -->
          <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h3 class="text-base font-semibold text-gray-800">Recent User Activities</h3>
              <button class="text-sm text-blue-600 hover:text-blue-700 font-medium">View All Logs</button>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm text-gray-600">
                <thead class="bg-gray-50 text-gray-500 text-xs uppercase font-medium">
                  <tr>
                    <th class="px-6 py-3">User</th>
                    <th class="px-6 py-3">Action</th>
                    <th class="px-6 py-3">Target</th>
                    <th class="px-6 py-3">Time</th>
                    <th class="px-6 py-3">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="activity in recentActivities" :key="activity.id" class="hover:bg-gray-50 transition-colors">
                    <td class="px-6 py-4 font-medium text-gray-900">{{ activity.user }}</td>
                    <td class="px-6 py-4">{{ activity.action }}</td>
                    <td class="px-6 py-4 font-mono text-xs bg-gray-100 rounded px-2 py-1 inline-block mt-2">{{ activity.target }}</td>
                    <td class="px-6 py-4">{{ activity.time }}</td>
                    <td class="px-6 py-4">
                      <span 
                        class="px-2 py-1 rounded-full text-xs font-medium"
                        :class="{
                          'bg-green-100 text-green-700': activity.status === 'Success',
                          'bg-yellow-100 text-yellow-700': activity.status === 'Warning',
                          'bg-red-100 text-red-700': activity.status === 'Error'
                        }"
                      >
                        {{ activity.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// import { fetchAdminOverview } from '../api/admin';

// Reactive state
const loading = ref(true);
const error = ref(null);
const stats = ref({});
const activityChart = ref({ labels: [], datasets: [] });
const recentActivities = ref([]);
const systemHealth = ref({});

// Fetch data on component mount
onMounted(async () => {
  try {
    loading.value = true;
    const response = await fetchAdminOverview();
    
    // Assign data from the mocked API response
    stats.value = response.data.stats;
    activityChart.value = response.data.activityChart;
    recentActivities.value = response.data.recentActivities;
    systemHealth.value = response.data.systemHealth;
    
  } catch (err) {
    console.error("Failed to fetch admin data:", err);
    error.value = "Failed to load dashboard data. Please try again later.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Optional: Add custom scrollbar styling for a polished look */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>