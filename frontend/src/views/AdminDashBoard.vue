<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Admin Dashboard</h2>
        <p class="text-sm text-gray-500">Manage users, settings, and monitor platform performance</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg">{{ error }}</div>

    <div v-else class="space-y-6">

      <!-- Auth Toggle Card -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-base font-semibold text-gray-800">Global Authentication</h3>
            <p class="text-sm text-gray-500 mt-1">
              {{ settings.auth_enabled ? 'Auth is ON — users must log in to access the platform.' : 'Auth is OFF — the platform is open to everyone (demo mode).' }}
            </p>
          </div>
          <button @click="toggleAuth" :disabled="togglingAuth"
            class="relative inline-flex h-8 w-16 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            :class="settings.auth_enabled ? 'bg-blue-600' : 'bg-gray-300'">
            <span class="inline-block h-6 w-6 transform rounded-full bg-white shadow transition-transform"
              :class="settings.auth_enabled ? 'translate-x-9' : 'translate-x-1'"></span>
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Total Users</p>
          <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalUsers }}</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Total Datasets</p>
          <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalDatasets }}</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">EDA Reports</p>
          <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalReports }}</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
          <p class="text-sm font-medium text-gray-500">Charts Generated</p>
          <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalCharts }}</p>
        </div>
      </div>

      <!-- Middle Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- User Management Table -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-base font-semibold text-gray-800">User Management</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-600">
              <thead class="bg-gray-50 text-gray-500 text-xs uppercase font-medium">
                <tr>
                  <th class="px-6 py-3">Username</th>
                  <th class="px-6 py-3">Email</th>
                  <th class="px-6 py-3">Role</th>
                  <th class="px-6 py-3">Joined</th>
                  <th class="px-6 py-3">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 font-medium text-gray-900">{{ u.username }}</td>
                  <td class="px-6 py-4">{{ u.email }}</td>
                  <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded-full text-xs font-medium"
                      :class="u.role === 'ADMIN' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'">
                      {{ u.role }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-xs text-gray-500">{{ formatDate(u.created_at) }}</td>
                  <td class="px-6 py-4">
                    <button v-if="u.role !== 'ADMIN'" @click="deleteUser(u.id, u.username)"
                      class="text-red-500 hover:text-red-700 text-xs font-medium">
                      Delete
                    </button>
                    <span v-else class="text-xs text-gray-400">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Performance Overview -->
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-6">
          <h3 class="text-base font-semibold text-gray-800">Platform Performance</h3>

          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600">Datasets Processed</span>
                <span class="font-medium text-gray-900">{{ stats.datasetsProcessed }} / {{ stats.totalDatasets }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-green-500 h-2 rounded-full transition-all" :style="{ width: processedPct + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600">AI Suggestions Generated</span>
                <span class="font-medium text-gray-900">{{ stats.totalSuggestions }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-blue-500 h-2 rounded-full transition-all" :style="{ width: suggestionPct + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600">Charts Rendered</span>
                <span class="font-medium text-gray-900">{{ stats.totalCharts }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-purple-500 h-2 rounded-full transition-all" :style="{ width: chartPct + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- Settings Summary -->
          <div class="pt-4 border-t border-gray-200 space-y-2">
            <h4 class="text-sm font-semibold text-gray-700">Current Settings</h4>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="flex justify-between p-2 bg-gray-50 rounded">
                <span class="text-gray-600">Auth</span>
                <span :class="settings.auth_enabled ? 'text-green-600' : 'text-red-600'" class="font-medium">
                  {{ settings.auth_enabled ? 'ON' : 'OFF' }}
                </span>
              </div>
              <div class="flex justify-between p-2 bg-gray-50 rounded">
                <span class="text-gray-600">Public Upload</span>
                <span :class="settings.allow_public_upload ? 'text-green-600' : 'text-red-600'" class="font-medium">
                  {{ settings.allow_public_upload ? 'ON' : 'OFF' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Datasets Table -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-base font-semibold text-gray-800">Recent Datasets (All Users)</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm text-gray-600">
            <thead class="bg-gray-50 text-gray-500 text-xs uppercase font-medium">
              <tr>
                <th class="px-6 py-3">Name</th>
                <th class="px-6 py-3">Rows</th>
                <th class="px-6 py-3">Columns</th>
                <th class="px-6 py-3">Status</th>
                <th class="px-6 py-3">Created</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="d in recentDatasets" :key="d.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 font-medium text-gray-900">{{ d.name }}</td>
                <td class="px-6 py-4">{{ d.rows ?? '—' }}</td>
                <td class="px-6 py-4">{{ d.columns ?? '—' }}</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="d.status === 'processed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'">
                    {{ d.status }}
                  </span>
                </td>
                <td class="px-6 py-4 text-xs text-gray-500">{{ formatDate(d.created_at) }}</td>
              </tr>
              <tr v-if="!recentDatasets.length">
                <td colspan="5" class="px-6 py-8 text-center text-gray-400">No datasets uploaded yet</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api/api.js'

const loading = ref(true)
const error = ref(null)
const stats = ref({})
const settings = ref({})
const users = ref([])
const recentDatasets = ref([])
const togglingAuth = ref(false)

const processedPct = computed(() => {
  if (!stats.value.totalDatasets) return 0
  return Math.round((stats.value.datasetsProcessed / stats.value.totalDatasets) * 100)
})
const suggestionPct = computed(() => {
  if (!stats.value.totalDatasets) return 0
  return Math.min(100, Math.round((stats.value.totalSuggestions / stats.value.totalDatasets) * 100))
})
const chartPct = computed(() => {
  if (!stats.value.totalDatasets) return 0
  return Math.min(100, Math.round((stats.value.totalCharts / Math.max(1, stats.value.totalDatasets * 8)) * 100))
})

const formatDate = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const fetchData = async () => {
  try {
    loading.value = true
    const [overviewRes, usersRes] = await Promise.all([
      api.admin.overview(),
      api.admin.listUsers(),
    ])
    stats.value = overviewRes.data.stats
    settings.value = overviewRes.data.settings
    recentDatasets.value = overviewRes.data.recentDatasets || []
    users.value = usersRes.data.users || []
  } catch (err) {
    console.error('Failed to fetch admin data:', err)
    error.value = 'Failed to load dashboard data. Please try again later.'
  } finally {
    loading.value = false
  }
}

const toggleAuth = async () => {
  togglingAuth.value = true
  try {
    const res = await api.admin.toggleGlobalAuth(!settings.value.auth_enabled)
    settings.value = res.data.settings
  } catch (err) {
    console.error('Failed to toggle auth:', err)
    alert('Failed to toggle authentication. Check console.')
  } finally {
    togglingAuth.value = false
  }
}

const deleteUser = async (userId, username) => {
  if (!confirm(`Delete user "${username}" and all their data? This cannot be undone.`)) return
  try {
    await api.admin.deleteUser(userId)
    users.value = users.value.filter(u => u.id !== userId)
    // Refresh stats
    const res = await api.admin.overview()
    stats.value = res.data.stats
  } catch (err) {
    console.error('Failed to delete user:', err)
    alert(err.response?.data?.error || 'Failed to delete user')
  }
}

onMounted(fetchData)
</script>