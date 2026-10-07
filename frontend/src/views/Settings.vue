<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-bold text-gray-800">Settings</h2>
    </div>

    <!-- Admin Settings -->
    <div v-if="isAdmin" class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm max-w-2xl">
      <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Platform Administration</h3>

      <div v-if="loading" class="text-gray-500 py-4">Loading settings...</div>

      <div v-else class="space-y-6">
        <!-- Auth Toggle -->
        <div class="flex items-center justify-between">
          <div>
            <h4 class="font-medium text-gray-900">Enforce Authentication</h4>
            <p class="text-sm text-gray-500 mt-1">When off, the platform acts as a public demo.</p>
          </div>
          <button @click="updateSetting('auth_enabled', !settings.auth_enabled)"
            class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            :class="settings.auth_enabled ? 'bg-blue-600' : 'bg-gray-200'">
            <span aria-hidden="true" class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
              :class="settings.auth_enabled ? 'translate-x-5' : 'translate-x-0'"></span>
          </button>
        </div>

        <!-- Public Upload Toggle -->
        <div class="flex items-center justify-between">
          <div>
            <h4 class="font-medium text-gray-900">Allow Public Uploads</h4>
            <p class="text-sm text-gray-500 mt-1">Allow datasets to be uploaded without an account.</p>
          </div>
          <button @click="updateSetting('allow_public_upload', !settings.allow_public_upload)"
            class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            :class="settings.allow_public_upload ? 'bg-blue-600' : 'bg-gray-200'">
            <span aria-hidden="true" class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
              :class="settings.allow_public_upload ? 'translate-x-5' : 'translate-x-0'"></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Normal Settings -->
    <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm max-w-2xl">
      <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Account Preferences</h3>
      <div class="flex items-center text-sm text-gray-500">
        No configurable preferences available for this account yet.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../api/api.js'

const isAdmin = computed(() => localStorage.getItem('user_role') === 'ADMIN')
const loading = ref(false)
const settings = ref({ auth_enabled: true, allow_public_upload: true })

const fetchSettings = async () => {
  if (!isAdmin.value) return
  loading.value = true
  try {
    const res = await api.admin.getSettings()
    settings.value = res.data
  } catch (err) {
    console.error('Failed to load settings', err)
  } finally {
    loading.value = false
  }
}

const updateSetting = async (key, val) => {
  try {
    const res = await api.admin.updateSettings({ [key]: val })
    settings.value = res.data.settings
  } catch (err) {
    console.error('Failed to update setting', err)
    alert('Failed to save setting.')
  }
}

onMounted(fetchSettings)
</script>