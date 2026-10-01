import axios from 'axios'


const apiClient = axios.create({
  // Fallback to '/api' if env variable is missing
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  // 15-second timeout to prevent hung requests in production, 
  // especially important for ML tasks that might take a moment
  timeout: 15000, 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})


apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * 3. Response Interceptor (Global Error Handling)
 * Catches 401 Unauthorized errors globally and redirects to login,
 * ensuring production users don't get stuck on broken screens if a token expires.
 */
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // If the server responds with 401 Unauthorized, clear token and redirect
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('auth_token')
      // Note: If using Vue Router, you might want to import router and router.push('/login')
      window.location.href = '/login' 
    }
    
    // Log server errors in development, but keep it clean in production
    if (import.meta.env.MODE === 'development') {
      console.error('API Error:', error.response?.data || error.message)
    }
    
    return Promise.reject(error)
  }
)

/**
 * 4. Centralized API Service Object
 * Group your endpoints logically so you can call them like: api.auth.login(data)
 */
export const api = {
  // --- AUTHENTICATION ---
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    register: (userData) => apiClient.post('/auth/user/register', userData),
  },

  // --- ADMIN CONTROLS ---
  admin: {
    /**
     * Toggles global authentication on the Flask backend.
     * @param {boolean} requireAuth - true to enforce auth, false to disable it
     */
    toggleGlobalAuth: (requireAuth) => {
      return apiClient.post('/admin/settings/auth-toggle', { 
        require_auth: requireAuth 
      })
    }
  },

  // --- USER CONTROLS --- 

  user :{
    overviewdata:() => apiClient.get('/user/overview'),
    edadata :() => apiClient.get('/user/eda')
  },
  
  // --- ML PIPELINE FEATURES ---
  datasets: {
    // Override headers for file uploads
    upload: (formData) => apiClient.post('/dataset/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000 // ML file uploads need a longer timeout (60s)
    }),
    getAll: () => apiClient.get('/datasets')
  },
  
  models: {
    getSuggestions: (datasetId) => apiClient.get(`/models/suggestions/${datasetId}`),
    train: (config) => apiClient.post('/models/train', config)
  }
}

export default apiClient