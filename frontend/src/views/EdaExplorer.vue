<!-- src/views/EdaExplorer.vue -->
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2 text-sm text-gray-500">
        <router-link to="/" class="hover:text-gray-700">Back to Datasets</router-link>
        <span>/</span>
        <span class="font-medium text-gray-800">EDA Explorer</span>
      </div>
      <div class="flex items-center gap-2 text-sm">
        <span class="text-gray-500">Dataset:</span>
        <select class="border border-gray-300 rounded-md py-1 px-2 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option>sales_data.csv</option>
        </select>
      </div>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex gap-6 text-sm font-medium">
        <a href="#" class="pb-3 border-b-2 border-blue-600 text-blue-600">Overview</a>
        <a href="#" class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Summary Statistics</a>
        <a href="#" class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Missing Values</a>
        <a href="#" class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Distributions</a>
        <a href="#" class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Correlation</a>
        <a href="#" class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Outliers</a>
        <a href="#" class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Time Series</a>
      </nav>
    </div>

    <!-- Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Dataset Overview Stats -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-4">
        <h3 class="font-semibold text-gray-800">Dataset Overview</h3>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div><p class="text-gray-500">Rows</p><p class="font-bold text-gray-900">24,532</p></div>
          <div><p class="text-gray-500">Columns</p><p class="font-bold text-gray-900">18</p></div>
          <div><p class="text-gray-500">Missing Values</p><p class="font-bold text-gray-900">2,345</p></div>
          <div><p class="text-gray-500">Duplicate Rows</p><p class="font-bold text-gray-900">0.12%</p></div>
        </div>
        <div>
          <p class="text-sm text-gray-500 mb-2">Data Types</p>
          <div class="flex gap-2 text-xs">
            <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-md">Numerical</span>
            <span class="px-2 py-1 bg-green-100 text-green-700 rounded-md">Categorical</span>
            <span class="px-2 py-1 bg-purple-100 text-purple-700 rounded-md">Date</span>
          </div>
        </div>
        <!-- Mini Bar Chart Placeholder -->
        <div class="h-24 flex items-end gap-1 pt-2">
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 60%"></div>
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 40%"></div>
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 80%"></div>
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 30%"></div>
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 50%"></div>
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 70%"></div>
           <div class="flex-1 bg-blue-500 rounded-t" style="height: 20%"></div>
        </div>
      </div>

      <!-- Missing Values Heatmap Placeholder -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h3 class="font-semibold text-gray-800 mb-4">Missing Values Heatmap</h3>
        <div class="grid grid-cols-8 gap-1">
           <!-- Create a grid of squares to simulate heatmap -->
           <div v-for="n in 64" :key="n" class="aspect-square rounded-sm" :class="n % 7 === 0 ? 'bg-red-400' : 'bg-gray-100'"></div>
        </div>
        <div class="flex justify-between text-xs text-gray-400 mt-2">
           <span>A</span><span>B</span><span>C</span><span>D</span><span>E</span><span>F</span><span>G</span><span>H</span>
        </div>
      </div>

      <!-- Correlation Matrix Placeholder -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h3 class="font-semibold text-gray-800 mb-4">Correlation Matrix</h3>
        <div class="grid grid-cols-8 gap-1">
           <div v-for="n in 64" :key="n" class="aspect-square rounded-sm" :class="n % 5 === 0 ? 'bg-blue-600' : 'bg-gray-100'"></div>
        </div>
        <div class="flex justify-between text-xs text-gray-400 mt-2">
           <span>A</span><span>B</span><span>C</span><span>D</span><span>E</span><span>F</span><span>G</span><span>H</span>
        </div>
      </div>
    </div>

    <!-- Feature Distributions Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h4 class="text-sm font-medium text-gray-600 mb-2">Histogram (Sales)</h4>
        <div class="h-24 flex items-end gap-1">
           <div v-for="n in 10" :key="n" class="flex-1 bg-gray-300 rounded-t" :style="{ height: (20 + Math.random() * 80) + '%' }"></div>
        </div>
      </div>
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h4 class="text-sm font-medium text-gray-600 mb-2">Boxplot (Profit)</h4>
        <div class="h-24 flex items-center justify-center">
           <div class="w-8 h-16 border border-gray-400 relative">
              <div class="absolute w-full h-0.5 bg-gray-400 top-1/4"></div>
              <div class="absolute w-full h-0.5 bg-gray-400 bottom-1/4"></div>
              <div class="absolute w-1/2 h-0.5 bg-gray-400 top-1/2 left-1/4"></div>
           </div>
        </div>
      </div>
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h4 class="text-sm font-medium text-gray-600 mb-2">Distribution (Quantity)</h4>
        <div class="h-24 flex items-end">
           <svg class="w-full h-full text-blue-400" viewBox="0 0 100 50" preserveAspectRatio="none">
              <path d="M0,50 Q25,50 40,10 Q50,0 60,10 Q75,50 100,50 Z" fill="currentColor" opacity="0.5"></path>
           </svg>
        </div>
      </div>
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h4 class="text-sm font-medium text-gray-600 mb-2">Time Series (Sales)</h4>
        <div class="h-24 flex items-center">
           <svg class="w-full h-full text-gray-400" viewBox="0 0 100 50" preserveAspectRatio="none">
              <path d="M0,40 L10,30 L20,35 L30,20 L40,25 L50,10 L60,15 L70,5 L80,20 L90,10 L100,25" fill="none" stroke="currentColor" stroke-width="2"></path>
           </svg>
        </div>
      </div>
    </div>
  </div>
</template>