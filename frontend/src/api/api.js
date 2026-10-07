import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor — attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle 401 globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    if (import.meta.env.MODE === 'development') {
      console.error('API Error:', error.response?.data || error.message)
    }
    return Promise.reject(error)
  }
)

export const api = {
  // --- AUTHENTICATION ---
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    register: (userData) => apiClient.post('/auth/user/register', userData),
    me: () => apiClient.get('/auth/me'),
    publicSettings: () => apiClient.get('/auth/settings'),
  },

  // --- ADMIN CONTROLS ---
  admin: {
    overview: () => apiClient.get('/admin/overview'),
    getSettings: () => apiClient.get('/admin/settings'),
    toggleGlobalAuth: (requireAuth) =>
      apiClient.post('/admin/settings/auth-toggle', { require_auth: requireAuth }),
    updateSettings: (data) => apiClient.post('/admin/settings/update', data),
    listUsers: () => apiClient.get('/admin/users'),
    deleteUser: (userId) => apiClient.delete(`/admin/users/${userId}`),
    listDatasets: () => apiClient.get('/admin/datasets'),
  },

  // --- USER ---
  user: {
    overviewdata: () => apiClient.get('/user/overview'),
    edadata: (datasetId) => {
      const params = datasetId ? { dataset_id: datasetId } : {}
      return apiClient.get('/user/eda', { params })
    },
    deleteDataset: (datasetId) => apiClient.delete(`/user/dataset/${datasetId}`),
  },

  // --- DATASETS ---
  datasets: {
    upload: (formData) => apiClient.post('/dataset/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000
    }),
    list: () => apiClient.get('/dataset/list'),
  },

  // --- ML ---
  ml: {
    analyze: (datasetId) => apiClient.post('/ml/analyze', { dataset_id: datasetId }, {
      timeout: 120000
    }),
  },

  // --- REPORTS ---
  reports: {
    list: () => apiClient.get('/reports'),
    get: (reportId) => apiClient.get(`/reports/${reportId}`),
  },

  // --- PREDICTIONS ---
  predictions: {
    list: () => apiClient.get('/predictions'),
  },
}

export default apiClient