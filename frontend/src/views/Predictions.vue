<!-- src/views/Predictions.vue -->
<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <div class="flex items-center gap-6 border-b border-gray-200">
      <button class="pb-3 border-b-2 border-blue-600 text-blue-600 font-medium text-sm">Single Prediction</button>
      <button class="pb-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm">Batch Prediction</button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Input Form -->
      <div class="md:col-span-1 bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <h3 class="font-semibold text-gray-800 mb-4">Input Features</h3>
        <div class="space-y-4">
          <div v-for="field in inputFields" :key="field.label">
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ field.label }}</label>
            <input type="text" :value="field.value" class="w-full border border-gray-300 rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
          </div>
          <button class="w-full py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors mt-2">Predict</button>
        </div>
      </div>

      <!-- Prediction Result -->
      <div class="md:col-span-2 space-y-6">
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col items-center justify-center py-10">
          <h3 class="text-sm font-medium text-gray-500 mb-2">Prediction Result</h3>
          <p class="text-4xl font-bold text-gray-900 mb-2">high_risk</p>
          <p class="text-sm text-gray-500">Confidence: 0.92</p>
        </div>

        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <h3 class="font-semibold text-gray-800 mb-4">Probability Distribution</h3>
          <div class="flex items-end justify-around h-24 gap-2">
             <div class="flex flex-col items-center">
                <div class="w-12 bg-gray-200 rounded-t" style="height: 20%"></div>
                <span class="text-xs text-gray-500 mt-1">low_risk</span>
             </div>
             <div class="flex flex-col items-center">
                <div class="w-12 bg-gray-200 rounded-t" style="height: 40%"></div>
                <span class="text-xs text-gray-500 mt-1">medium_risk</span>
             </div>
             <div class="flex flex-col items-center">
                <div class="w-12 bg-blue-500 rounded-t" style="height: 80%"></div>
                <span class="text-xs text-gray-500 mt-1">high_risk</span>
             </div>
          </div>
        </div>

        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
           <h3 class="font-semibold text-gray-800 mb-3">Explanation (Top Features)</h3>
           <table class="w-full text-sm text-left">
              <thead class="text-gray-500 border-b border-gray-100">
                 <tr><th class="pb-2 font-medium">Feature</th><th class="pb-2 font-medium text-right">Impact</th></tr>
              </thead>
              <tbody>
                 <tr v-for="feat in topFeatures" :key="feat.name" class="border-b border-gray-50 last:border-0">
                    <td class="py-2 text-gray-700">{{ feat.name }}</td>
                    <td class="py-2 text-right">
                       <span class="px-2 py-0.5 rounded text-xs font-medium" 
                        :class="feat.impact === 'High' ? 'bg-red-100 text-red-700' : feat.impact === 'Medium' ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-600'">
                         {{ feat.impact }}
                       </span>
                    </td>
                 </tr>
              </tbody>
           </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const inputFields = ref([
  { label: 'Age', value: '34' },
  { label: 'Income', value: '60000' },
  { label: 'Transactions', value: '14' },
  { label: 'Account Age (Months)', value: '24' },
  { label: 'Credit Score', value: '680' },
]);

const topFeatures = ref([
  { name: 'Credit Score', impact: 'High' },
  { name: 'Income', impact: 'Medium' },
  { name: 'Transactions', impact: 'Medium' },
  { name: 'Account Age', impact: 'Low' },
]);
</script>