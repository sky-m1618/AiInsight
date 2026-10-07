<template>
  <div class="min-h-screen bg-gray-50 flex font-sans">

    <!-- AUTHENTICATED SIDEBAR: Shows only if route meta requires auth -->
    <aside v-if="isDashboardLayout" class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col fixed h-full z-10">
      <div class="h-16 flex items-center px-6 border-b border-gray-200">
        <h1 class="text-xl font-bold text-gray-800 flex items-center gap-2">
          <span class="w-6 h-6 bg-blue-600 rounded-md flex items-center justify-center text-white text-xs">A</span>
          AutoML
        </h1>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        <!-- Admin link (only for admins) -->
        <router-link v-if="isAdmin" to="/admin"
          class="flex items-center gap-3 px-3 py-2 rounded-lg font-medium transition-colors mb-2"
          :class="[$route.path === '/admin' ? 'bg-red-50 text-red-700' : 'text-red-600 hover:bg-red-50']">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
          Admin Panel
        </router-link>

        <router-link v-for="item in navItems" :key="item.name" :to="item.path"
          class="flex items-center gap-3 px-3 py-2 rounded-lg font-medium transition-colors"
          :class="[$route.name === item.name ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50']">
          <component :is="item.icon" class="w-5 h-5" />
          {{ item.name }}
        </router-link>
      </nav>

      <div class="p-4 border-t border-gray-200">
        <button @click="handleLogout" class="flex items-center gap-3 px-3 py-2 w-full text-gray-600 hover:bg-gray-50 rounded-lg font-medium transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT AREA -->
    <main class="flex-1 flex flex-col" :class="isDashboardLayout ? 'ml-0 md:ml-64' : 'w-full'">

      <!-- AUTHENTICATED TOP HEADER -->
      <header v-if="isDashboardLayout" class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 sticky top-0 z-20">
        <div class="flex items-center gap-4 w-1/3">
          <div class="relative w-full max-w-md hidden sm:block">
            <svg class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            <input type="text" placeholder="Search anything..." class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button class="p-2 text-gray-400 hover:text-gray-600 relative">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
          </button>
          <div class="flex items-center gap-2 cursor-pointer">
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm"
              :class="isAdmin ? 'bg-blue-100 text-blue-700' : 'bg-gray-200 text-gray-600'">
              {{ userInitial }}
            </div>
            <span class="text-sm font-medium text-gray-700">{{ displayName }}</span>
            <span v-if="isAdmin" class="text-xs bg-red-100 text-red-600 px-1.5 py-0.5 rounded-full font-medium">Admin</span>
          </div>
        </div>
      </header>

      <!-- PUBLIC LANDING NAVBAR: Shows when not on dashboard -->
      <LandingNavbar v-else-if="isPublicLayout" />

      <!-- DYNAMIC PAGE CONTENT -->
      <div class="flex-1 p-6 overflow-y-auto">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LandingNavbar from '../components/LandingNavBar.vue'

const route = useRoute()
const router = useRouter()

const isDashboardLayout = computed(() => route.meta.layout === 'dashboard' || route.meta.layout === 'admin')
const isPublicLayout = computed(() => route.meta.layout === 'public')
const isAdmin = computed(() => localStorage.getItem('user_role') === 'ADMIN')

const displayName = computed(() => {
  try {
    const u = JSON.parse(localStorage.getItem('user') || '{}')
    return u.username || 'User'
  } catch { return 'User' }
})

const userInitial = computed(() => {
  const name = displayName.value
  return name ? name.charAt(0).toUpperCase() : 'U'
})

const handleLogout = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_role')
  localStorage.removeItem('user')
  router.push('/')
}

const IconOverview = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })])
const IconDatasets = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4' })])
const IconEDA = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z' }), h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z' })])
const IconModels = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })])
const IconPredictions = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })])
const IconReports = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })])
const IconDeployments = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2' })])
const IconSettings = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }), h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })])

const navItems = [
  { name: 'Overview', path: '/overview', icon: IconOverview },
  { name: 'Datasets', path: '/datasets', icon: IconDatasets },
  { name: 'EDA Explorer', path: '/eda', icon: IconEDA },
  { name: 'ML Models', path: '/models', icon: IconModels },
  { name: 'Predictions', path: '/predictions', icon: IconPredictions },
  { name: 'Reports', path: '/reports', icon: IconReports },
  { name: 'Deployments', path: '/deployments', icon: IconDeployments },
  { name: 'Settings', path: '/settings', icon: IconSettings },
]
</script>