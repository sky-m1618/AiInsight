<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Reports</h2>
        <p class="text-sm text-gray-500">View your EDA reports and AI suggestions</p>
      </div>
      <router-link to="/datasets"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Upload Dataset
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <template v-else-if="edaData">
      <!-- Dataset Info -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h3 class="font-semibold text-gray-800 mb-3">Dataset: {{ edaData.dataset?.name }}</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div><span class="text-gray-500">Rows:</span> <span class="font-medium">{{ edaData.dataset?.rows?.toLocaleString() ?? '—' }}</span></div>
          <div><span class="text-gray-500">Columns:</span> <span class="font-medium">{{ edaData.dataset?.columns ?? '—' }}</span></div>
          <div><span class="text-gray-500">Target:</span> <span class="font-medium">{{ edaData.dataset?.target_column || 'None' }}</span></div>
          <div><span class="text-gray-500">Status:</span>
            <span class="font-medium" :class="edaData.dataset?.status === 'processed' ? 'text-green-600' : 'text-yellow-600'">{{ edaData.dataset?.status }}</span>
          </div>
        </div>
      </div>

      <!-- AI Suggestion -->
      <div v-if="edaData.suggestion" class="bg-blue-50 border border-blue-200 p-5 rounded-xl">
        <h3 class="font-semibold text-blue-800 mb-2 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          AI Model Suggestion
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-900">
          <div><span class="text-blue-600">Task:</span> {{ edaData.suggestion.task_type }}</div>
          <div><span class="text-blue-600">Model:</span> {{ edaData.suggestion.suggested_model }}</div>
          <div><span class="text-blue-600">Target:</span> {{ edaData.suggestion.target_variable }}</div>
        </div>
        <p class="text-sm text-blue-800 mt-3">{{ edaData.suggestion.ai_reasoning }}</p>
      </div>

      <!-- EDA Overview -->
      <div v-if="edaData.message" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Numerical Features -->
        <div v-if="numericalCols.length" class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <h3 class="font-semibold text-gray-800 mb-3">Numerical Features ({{ numericalCols.length }})</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-gray-600">
              <thead class="bg-gray-50 text-gray-500 uppercase">
                <tr>
                  <th class="px-3 py-2 text-left">Column</th>
                  <th class="px-3 py-2">Mean</th>
                  <th class="px-3 py-2">Min</th>
                  <th class="px-3 py-2">Max</th>
                  <th class="px-3 py-2">Std</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="col in numericalCols" :key="col">
                  <td class="px-3 py-2 font-medium text-gray-800">{{ col }}</td>
                  <td class="px-3 py-2 text-center">{{ fmt(edaData.message.numerical_features[col]?.mean) }}</td>
                  <td class="px-3 py-2 text-center">{{ fmt(edaData.message.numerical_features[col]?.min) }}</td>
                  <td class="px-3 py-2 text-center">{{ fmt(edaData.message.numerical_features[col]?.max) }}</td>
                  <td class="px-3 py-2 text-center">{{ fmt(edaData.message.numerical_features[col]?.std) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Categorical Features -->
        <div v-if="categoricalCols.length" class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <h3 class="font-semibold text-gray-800 mb-3">Categorical Features ({{ categoricalCols.length }})</h3>
          <div class="space-y-3">
            <div v-for="col in categoricalCols.slice(0, 6)" :key="col" class="text-sm">
              <p class="font-medium text-gray-800 mb-1">{{ col }} <span class="text-gray-400 text-xs">({{ edaData.message.categorical_features[col]?.unique_values_count }} unique)</span></p>
              <div class="flex flex-wrap gap-1">
                <span v-for="(count, val) in topCategories(col)" :key="val"
                  class="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs">
                  {{ val }}: {{ count }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div v-if="edaData.charts?.length" class="space-y-4">
        <h3 class="font-semibold text-gray-800">Generated Charts</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="(chart, i) in edaData.charts" :key="i" class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
            <p class="text-sm font-medium text-gray-600 mb-2">
              {{ chart.chart_type.replace(/_/g, ' ') }}
              <span v-if="chart.target_column" class="text-gray-400"> — {{ chart.target_column }}</span>
            </p>
            <img :src="chart.base64_data" :alt="chart.chart_type" class="w-full rounded" />
          </div>
        </div>
      </div>

      <!-- Missing Values -->
      <div v-if="missingValues && Object.keys(missingValues).length" class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h3 class="font-semibold text-gray-800 mb-3">Missing Values</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div v-for="(count, col) in missingValues" :key="col" class="text-sm">
            <span class="font-medium text-gray-800">{{ col }}:</span>
            <span class="text-red-600 ml-1">{{ count.toLocaleString() }}</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Empty state -->
    <div v-else class="bg-white p-12 rounded-xl border border-gray-200 text-center">
      <p class="text-gray-400 mb-2">No reports available yet</p>
      <router-link to="/datasets" class="text-blue-600 text-sm font-medium hover:text-blue-700">Upload a dataset to get started →</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api/api.js'

const edaData = ref(null)
const loading = ref(true)

const numericalCols = computed(() => Object.keys(edaData.value?.message?.numerical_features || {}))
const categoricalCols = computed(() => Object.keys(edaData.value?.message?.categorical_features || {}))
const missingValues = computed(() => edaData.value?.message?.overview?.missing_values_summary || {})

const fmt = (val) => {
  if (val === null || val === undefined) return '—'
  return typeof val === 'number' ? val.toFixed(2) : val
}

const topCategories = (col) => {
  const dist = edaData.value?.message?.categorical_features?.[col]?.top_categories_distribution || {}
  return Object.fromEntries(Object.entries(dist).slice(0, 5))
}

onMounted(async () => {
  try {
    const response = await api.user.edadata()
    edaData.value = response.data
  } catch (error) {
    console.error('Failed loading reports:', error)
  } finally {
    loading.value = false
  }
})
</script>