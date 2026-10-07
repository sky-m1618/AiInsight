<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Datasets</h2>
        <p class="text-sm text-gray-500">Upload and manage your CSV datasets</p>
      </div>
    </div>

    <!-- Upload Area -->
    <div
      class="bg-white p-8 rounded-xl border-2 border-dashed border-gray-300 flex flex-col items-center justify-center text-center hover:bg-gray-50 transition-colors cursor-pointer relative"
      @click="triggerFileInput"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      :class="{ 'border-blue-500 bg-blue-50': isDragging }">

      <input type="file" ref="fileInputRef" class="hidden" accept=".csv" @change="handleFileChange" />

      <svg class="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
      </svg>

      <p class="text-gray-700 font-medium">
        {{ selectedFile ? `Selected: ${selectedFile.name}` : 'Drag & Drop your file here' }}
      </p>
      <p class="text-sm text-gray-500 mb-4" v-if="!selectedFile">or</p>

      <button type="button" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors">
        Browse files
      </button>

      <p class="text-xs text-gray-400 mt-4">Supports: CSV (Max size: 32MB)</p>
    </div>

    <!-- Target Column (optional) -->
    <div v-if="selectedFile" class="bg-white p-4 rounded-xl border border-gray-200">
      <label class="block text-sm font-medium text-gray-700 mb-1">Target Column (optional)</label>
      <input v-model="targetCol" type="text" placeholder="e.g. price, label, class"
        class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
      <p class="text-xs text-gray-400 mt-1">If provided, you'll get an AI model suggestion for this column</p>
    </div>

    <!-- Upload Button -->
    <button
      @click="uploadToServer"
      :disabled="!selectedFile || isUploading"
      class="w-full px-4 py-2 text-white font-medium rounded-lg transition-colors bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
      {{ isUploading ? 'Processing EDA...' : 'Analyze Dataset' }}
    </button>

    <!-- Error -->
    <div v-if="uploadError" class="bg-red-50 text-red-700 p-4 rounded-lg text-sm">{{ uploadError }}</div>

    <!-- Success -->
    <div v-if="uploadSuccess" class="bg-green-50 text-green-700 p-4 rounded-lg text-sm">
      {{ uploadSuccess }}
    </div>

    <!-- Previous Datasets -->
    <div v-if="datasets.length" class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-800">Your Datasets</h3>
      </div>
      <table class="w-full text-left text-sm text-gray-600">
        <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
          <tr>
            <th class="px-5 py-3 font-medium">Name</th>
            <th class="px-5 py-3 font-medium">Rows</th>
            <th class="px-5 py-3 font-medium">Columns</th>
            <th class="px-5 py-3 font-medium">Status</th>
            <th class="px-5 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="ds in datasets" :key="ds.id" class="hover:bg-gray-50">
            <td class="px-5 py-3 font-medium text-gray-900">{{ ds.name }}</td>
            <td class="px-5 py-3">{{ ds.rows ?? '—' }}</td>
            <td class="px-5 py-3">{{ ds.columns ?? '—' }}</td>
            <td class="px-5 py-3">
              <span class="flex items-center gap-1.5 text-xs font-medium"
                :class="ds.status === 'processed' ? 'text-green-600' : 'text-yellow-600'">
                <span class="w-1.5 h-1.5 rounded-full" :class="ds.status === 'processed' ? 'bg-green-500' : 'bg-yellow-500'"></span>
                {{ ds.status }}
              </span>
            </td>
            <td class="px-5 py-3">
              <button @click="viewEda(ds.id)" class="text-blue-600 hover:text-blue-700 text-xs font-medium mr-3">View EDA</button>
              <button @click="deleteDataset(ds.id)" class="text-red-500 hover:text-red-700 text-xs font-medium">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api/api.js'

const router = useRouter()
const fileInputRef = ref(null)
const selectedFile = ref(null)
const isDragging = ref(false)
const isUploading = ref(false)
const targetCol = ref('')
const uploadError = ref('')
const uploadSuccess = ref('')
const datasets = ref([])

const triggerFileInput = () => { fileInputRef.value.click() }
const handleFileChange = (event) => { validateAndAssignFile(event.target.files[0]) }

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer?.files?.[0]
  validateAndAssignFile(file)
}

const validateAndAssignFile = (file) => {
  if (!file) return
  if (!file.name.endsWith('.csv')) { alert('Please upload a valid CSV file.'); return }
  selectedFile.value = file
  uploadError.value = ''
  uploadSuccess.value = ''
}

const uploadToServer = async () => {
  if (!selectedFile.value) return

  isUploading.value = true
  uploadError.value = ''
  uploadSuccess.value = ''

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  if (targetCol.value.trim()) {
    formData.append('target_col', targetCol.value.trim())
  }

  try {
    const response = await api.datasets.upload(formData)
    const data = response.data
    uploadSuccess.value = `Upload complete! Dataset ID: ${data.dataset_id}, ${data.file_size_mb} MB processed.`
    selectedFile.value = null
    targetCol.value = ''

    // Refresh the dataset list
    await fetchDatasets()

    // Navigate to EDA view
    router.push({ name: 'EDA Explorer' })
  } catch (error) {
    uploadError.value = error.response?.data?.error || 'Failed to upload. Make sure the backend is running.'
  } finally {
    isUploading.value = false
  }
}

const fetchDatasets = async () => {
  try {
    const res = await api.datasets.list()
    datasets.value = res.data.datasets || []
  } catch (err) {
    console.error('Failed to load datasets:', err)
  }
}

const viewEda = (datasetId) => {
  router.push({ name: 'EDA Explorer', query: { dataset_id: datasetId } })
}

const deleteDataset = async (datasetId) => {
  if (!confirm('Delete this dataset and all its reports?')) return
  try {
    await api.user.deleteDataset(datasetId)
    datasets.value = datasets.value.filter(d => d.id !== datasetId)
  } catch (err) {
    alert(err.response?.data?.error || 'Failed to delete dataset')
  }
}

onMounted(fetchDatasets)
</script>