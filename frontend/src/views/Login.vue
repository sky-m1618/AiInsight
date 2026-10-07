<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center items-center gap-2 mb-6">
        <span class="w-8 h-8 bg-blue-600 rounded-md flex items-center justify-center text-white font-bold">A</span>
        <h2 class="text-3xl font-extrabold text-gray-900">AutoML</h2>
      </div>
      <h2 class="text-center text-2xl font-bold text-gray-900">Sign in to your account</h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 border border-gray-200">
        <!-- Error Message -->
        <div v-if="errorMsg" class="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
          {{ errorMsg }}
        </div>

        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="identifier" class="block text-sm font-medium text-gray-700">
              Email or Username
            </label>
            <div class="mt-1">
              <input id="identifier" v-model="form.identifier" type="text" required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Enter email or username">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input id="password" v-model="form.password" type="password" required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="••••••••">
            </div>
          </div>

          <div>
            <button type="submit" :disabled="isLoading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:bg-gray-400">
              {{ isLoading ? 'Signing in...' : 'Sign in' }}
            </button>
          </div>
        </form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Don't have an account?
            <router-link to="/register" class="font-medium text-blue-600 hover:text-blue-500">
              Register here
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api/api.js'

const router = useRouter()
const errorMsg = ref('')
const isLoading = ref(false)

const form = reactive({
  identifier: '',
  password: ''
})

const handleLogin = async () => {
  errorMsg.value = ''
  isLoading.value = true
  try {
    const response = await api.auth.login(form)
    const data = response.data

    // Store token and role
    localStorage.setItem('auth_token', data.token)
    localStorage.setItem('user_role', data.role)

    // Store user profile
    const profile = data.user || data.admin
    if (profile) {
      localStorage.setItem('user', JSON.stringify(profile))
    }

    // Route based on role
    if (data.role === 'ADMIN') {
      router.push('/admin')
    } else {
      router.push('/overview')
    }
  } catch (error) {
    const msg = error.response?.data?.message || 'Login failed. Please try again.'
    errorMsg.value = msg
  } finally {
    isLoading.value = false
  }
}
</script>