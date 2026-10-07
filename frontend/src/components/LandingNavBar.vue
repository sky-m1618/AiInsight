<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
      <div
        @click="router.push('/')"
        class="flex items-center gap-2 cursor-pointer group"
      >
        <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-blue-500/30 group-hover:scale-105 transition-transform">
          A
        </div>
        <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
          AutoML
        </span>
      </div>

      <div class="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
        <a href="#features" class="hover:text-blue-600 transition-colors">Features</a>
        <a href="#how-it-works" class="hover:text-blue-600 transition-colors">How it Works</a>
        <a href="#technology" class="hover:text-blue-600 transition-colors">Technology</a>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="goToLogin"
          class="hidden sm:block px-5 py-2.5 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all"
        >
          Sign In
        </button>
        <button
          @click="goToRegister"
          class="px-6 py-2.5 text-sm font-medium text-white bg-gray-900 hover:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all"
        >
          Get Started
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToLogin = () => router.push('/login');
const goToRegister = () => router.push('/register');
</script>