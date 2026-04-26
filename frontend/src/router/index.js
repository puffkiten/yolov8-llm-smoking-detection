// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { h } from 'vue'
import Login from '../views/Login.vue'
import Layout from '../components/Layout.vue'
import Register from '../views/Register.vue'
import AuthGoogle from '../views/AuthGoogle.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import ResetPassword from '../views/ResetPassword.vue'
import AuthGoogleCallback from '../views/AuthGoogleCallback.vue'
import ShareReport from '../views/share/ShareReport.vue'

// 💡 极客写法：用原生 render 函数创建一个占位组件，绕过 Vite 的文件检查
const Placeholder = (title) => ({ 
  render: () => h('div', { style: 'padding: 40px; font-size: 18px; color: #64748b;' }, `${title} (开发中...)`) 
})

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: ForgotPassword
    },
    {
      path: '/reset-password',
      name: 'resetPassword',
      component: ResetPassword
    },
    {
      path: '/auth/google',
      name: 'authGoogle',
      component: AuthGoogle
    },
    {
      path: '/auth/google/callback',
      name: 'authGoogleCallback',
      component: AuthGoogleCallback
    },
    {
      path: '/share/report',
      name: 'shareReport',
      component: ShareReport
    },
    {
      path: '/',
      component: Layout, // 全局骨架
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          
          component: () => import('../views/Dashboard.vue')
        },
        {
          path: 'detection/upload',
          name: 'UploadDetection',
          
          component: () => import('../views/detection/Upload.vue')
        },
        // ==========================================
        // 下面这些文件你还没建，使用安全的 Placeholder 占位！
        // ==========================================
        {
          path: 'detection/tasks',
          name: 'DetectionTasks',
          component: () => import('../views/detection/Tasks.vue')
        },
        {
          path: 'task/detail/:id',
          name: 'TaskDetail',
          component: () => import('../views/detection/Tasks.vue')
        },
        {
          path: 'camera/realtime',
          name: 'RealtimeMonitoring',
          component: () => import('../views/camera/Realtime.vue')
        },
        {
          path: 'camera/config',
          name: 'CameraConfig',
          component: () => import('../views/camera/Config.vue')
        },
        {
          path: 'system/ai-models',
          name: 'AIModelManage',
          component: () => import('../views/system/AIModelManage.vue')
        },
        {
          path: 'system/users',
          name: 'UserManage',
          component: () => import('../views/system/UserManage.vue')
        }
      ]
    }
  ]
})

export default router
