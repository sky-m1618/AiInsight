<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-bold text-gray-800">Overview</h2>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <template v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Datasets</p>
          <p class="text-3xl font-bold text-gray-900 mt-2">{{ datasets.length }}</p>
          <p class="text-xs text-gray-400 mt-1">Total uploaded datasets</p>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Processed</p>
          <p class="text-3xl font-bold text-gray-900 mt-2">{{ processedCount }}</p>
          <p class="text-xs text-gray-400 mt-1">Datasets with EDA complete</p>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Pending</p>
          <p class="text-3xl font-bold text-gray-900 mt-2">{{ pendingCount }}</p>
          <p class="text-xs text-gray-400 mt-1">Awaiting analysis</p>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Total Rows</p>
          <p class="text-3xl font-bold text-gray-900 mt-2">{{ totalRows.toLocaleString() }}</p>
          <p class="text-xs text-gray-400 mt-1">Across all datasets</p>
        </div>
      </div>

      <!-- Recent Datasets Table -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="font-semibold text-gray-800">Recent Datasets</h3>
          <router-link to="/datasets" class="text-sm text-blue-600 hover:text-blue-700 font-medium">View all →</router-link>
        </div>
        <table v-if="datasets.length" class="w-full text-left text-sm text-gray-600">
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
            <tr v-for="ds in datasets" :key="ds.id" class="hover:bg-gray-50">
              <td class="px-5 py-3 font-medium text-gray-900">{{ ds.name }}</td>
              <td class="px-5 py-3">{{ ds.rows?.toLocaleString() ?? '—' }}</td>
              <td class="px-5 py-3">{{ ds.columns ?? '—' }}</td>
              <td class="px-5 py-3 text-xs text-gray-500">{{ formatDate(ds.created_at) }}</td>
              <td class="px-5 py-3">
                <span class="flex items-center gap-1.5 text-xs font-medium"
                  :class="ds.status === 'processed' ? 'text-green-600' : 'text-yellow-600'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="ds.status === 'processed' ? 'bg-green-500' : 'bg-yellow-500'"></span>
                  {{ ds.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="px-5 py-12 text-center text-gray-400">
          <p class="mb-2">No datasets yet</p>
          <router-link to="/datasets" class="text-blue-600 text-sm font-medium hover:text-blue-700">Upload your first dataset →</router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api/api.js'

const datasets = ref([])
const loading = ref(true)

const processedCount = computed(() => datasets.value.filter(d => d.status === 'processed').length)
const pendingCount = computed(() => datasets.value.filter(d => d.status !== 'processed').length)
const totalRows = computed(() => datasets.value.reduce((sum, d) => sum + (d.rows || 0), 0))

const formatDate = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

onMounted(async () => {
  try {
    const response = await api.user.overviewdata()
    datasets.value = response.data.datasets || []
  } catch (err) {
    console.error('Failed to load overview:', err)
  } finally {
    loading.value = false
  }
})
</script>