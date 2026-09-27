<template>
  <div>
    <!-- Upload Area Component Wrapper -->
    <div 
      class="bg-white p-8 rounded-xl border-2 border-dashed border-gray-300 flex flex-col items-center justify-center text-center hover:bg-gray-50 transition-colors cursor-pointer relative"
      @click="triggerFileInput"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      :class="{ 'border-blue-500 bg-blue-50': isDragging }"
    >
      <!-- Hidden Native Input Element -->
      <input 
        type="file" 
        ref="fileInputRef" 
        class="hidden" 
        accept=".csv" 
        @change="handleFileChange" 
      />

      <svg class="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
      </svg>
      
      <p class="text-gray-700 font-medium">
        {{ selectedFile ? `Selected: ${selectedFile.name}` : 'Drag & Drop your file here' }}
      </p>
      <p class="text-sm text-gray-500 mb-4" v-if="!selectedFile">or</p>
      
      <button 
        type="button"
        class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
      >
        Browse files
      </button>
      
      <p class="text-xs text-gray-400 mt-4">Supports: CSV (Max size: 32MB)</p>
    </div>

    <!-- Action Button to Trigger Flask API Upload -->
    <button 
      @click="uploadToServer" 
      :disabled="!selectedFile || isUploading"
      class="mt-4 w-full px-4 py-2 text-white font-medium rounded-lg transition-colors bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
    >
      {{ isUploading ? 'Processing EDA...' : 'Analyze Dataset' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // ◄— Import Vue Router for programmatic navigation

const fileInputRef = ref(null);
const selectedFile = ref(null);
const isDragging = ref(false);
const isUploading = ref(false);

const router = useRouter(); // ◄— Initialize the router instance

const triggerFileInput = () => { fileInputRef.value.click(); };
const handleFileChange = (event) => { validateAndAssignFile(event.target.files[0]); };

const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.target.files?.[0] || event.dataTransfer?.files?.[0];
  validateAndAssignFile(file);
};

const validateAndAssignFile = (file) => {
  if (!file) return;
  if (!file.name.endsWith('.csv')) { alert('Please upload a valid CSV file.'); return; }
  selectedFile.value = file;
};

// Communicate payload over HTTP boundary and redirect upon success
const uploadToServer = async () => {
  if (!selectedFile.value) return;
  
  isUploading.value = true;
  const formData = new FormData();
  formData.append('file', selectedFile.value);

  try {
    // Call the Flask endpoint (which handles AutoML EDA calculations and DB ingestion)
    const response = await fetch('http://127.0.0.1:5000/api/dataset/csv', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Server returned status code: ${response.status}`);
    }

    const data = await response.json();
    console.log('Backend confirmation payload received:', data);
    
    // ◄— SUCCESS: Programmatically route user to the Reports view dashboard
    // Replace 'Reports' with the exact 'name' or '/path' defined in your router configuration file
    router.push({ name: 'Reports' }); 
    
  } catch (error) {
    console.error('Network dispatch failure encountered:', error);
    alert('Failed to connect to backend server. Verify your Flask app is actively running.');
  } finally {
    isUploading.value = false;
  }
};
</script>
