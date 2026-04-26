import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const fallbackBaseUrl = 'http://127.0.0.1:8000'

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || fallbackBaseUrl).replace(/\/$/, '')

export const buildApiUrl = (path) => `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`

axios.defaults.baseURL = API_BASE_URL
axios.defaults.timeout = 30000

axios.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('access_token') || ''
  if (accessToken) {
    config.headers = config.headers || {}
    if (!config.headers.Authorization) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
  }
  return config
})

const statusTextMap = {
  401: '登录已过期，请重新登录',
  403: '无权限执行该操作',
  500: '服务器异常，请稍后重试',
}

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status
    const detail = error?.response?.data?.detail

    if (status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      const currentPath = router.currentRoute.value?.path || ''
      if (currentPath !== '/login') {
        ElMessage.error('登录已过期，请重新登录')
        router.replace('/login')
      }
      return Promise.reject(error)
    }

    const message = detail || statusTextMap[status] || '请求失败，请稍后重试'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)
