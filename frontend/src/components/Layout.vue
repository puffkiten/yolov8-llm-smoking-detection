<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
        </div>
        <div class="logo-meta">
          <span class="logo-text">Aero Smart</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-section-title">概览</div>
          <div
            class="nav-item"
            :class="{ active: route.path === '/dashboard' }"
            @click="router.push('/dashboard')"
          >
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="3" width="7" height="7" rx="1.5"/>
                <rect x="3" y="14" width="7" height="7" rx="1.5"/>
                <rect x="14" y="14" width="7" height="7" rx="1.5"/>
              </svg>
            </span>
            <span>仪表板</span>
          </div>
        </div>

        <div class="nav-divider"></div>

        <div class="nav-section">
          <div class="nav-section-title">检测中心</div>
          <div
            class="nav-item"
            :class="{ active: route.path === '/camera/realtime' }"
            @click="router.push('/camera/realtime')"
          >
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 7 16 12 23 17V7z"/>
                <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
              </svg>
            </span>
            <span>实时监控</span>
          </div>
          <div
            class="nav-item"
            :class="{ active: route.path === '/detection/upload' || route.path === '/detection/tasks' }"
            @click="router.push('/detection/upload')"
          >
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="4" y="3" width="16" height="18" rx="2"/>
                <path d="M9 3v18"/>
                <path d="M8 8h1"/>
                <path d="M8 12h1"/>
                <path d="M8 16h1"/>
              </svg>
            </span>
            <span>检测任务</span>
          </div>
        </div>

        <div class="nav-divider"></div>

        <div class="nav-section">
          <div class="nav-section-title">设备中心</div>
          <div
            class="nav-item"
            :class="{ active: route.path === '/camera/config' }"
            @click="router.push('/camera/config')"
          >
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 7 16 12 23 17V7z"/>
                <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
              </svg>
            </span>
            <span>摄像头配置</span>
          </div>
        </div>

        <div class="nav-divider"></div>

        <div class="nav-section">
          <div class="nav-section-title">系统管理</div>
          <template v-if="currentUser.role === 'admin'">
            <div
              class="nav-item"
              :class="{ active: route.path === '/system/ai-models' }"
              @click="router.push('/system/ai-models')"
            >
              <span class="nav-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2 4 7v10l8 5 8-5V7l-8-5z"/>
                  <path d="M12 22V12"/>
                  <path d="m20 7-8 5-8-5"/>
                </svg>
              </span>
              <span>AI 模型管理</span>
            </div>
            <div
              class="nav-item"
              :class="{ active: route.path === '/system/users' }"
              @click="router.push('/system/users')"
            >
              <span class="nav-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </span>
              <span>系统设置</span>
            </div>
          </template>
        </div>
      </nav>

      <div class="sidebar-user-card">
        <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${currentUser.name}`" class="sidebar-user-avatar" alt=""/>
        <div class="sidebar-user-meta">
          <div class="sidebar-user-name">{{ currentUser.name }}</div>
          <div class="sidebar-user-role">{{ currentUser.role === 'admin' ? '管理员' : '普通用户' }}</div>
        </div>
      </div>

      <div class="sidebar-logout" @click="handleLogout">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        <span>退出登录</span>
      </div>
    </aside>

    <div class="main-wrap">
      <header class="topbar">
        <div class="breadcrumb">
          <span class="bc-item">系统首页</span>
          <span class="bc-sep">/</span>
          <span class="bc-item active">{{ currentRouteName }}</span>
        </div>
        <div class="top-center">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="全局搜索..."
              class="search-input"
              @keyup.enter="handleSearch"
            />
          </div>
        </div>
        <div class="top-right">
          <button class="icon-btn" @click="handleRefreshClick">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-5.05"/>
            </svg>
          </button>
          <button class="icon-btn" @click="toggleTheme">
            <svg v-if="theme === 'light'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
          </button>
          <button class="icon-btn notify" @click="toggleNotifyPanel">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <span class="notify-badge" v-if="unreadCount > 0">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
          </button>
          <div class="notify-panel" v-show="notifyOpen">
            <div class="np-header">
              <span>通知中心</span>
              <button class="np-mark" @click="markAllRead">全部标为已读</button>
            </div>
            <div class="np-list">
              <div v-if="notifications.length === 0" class="np-empty">暂无通知</div>
              <div v-for="n in notifications" :key="n.id" class="np-item" :class="{ unread: !n.read }" @click="openNotification(n)">
                <span class="np-tag" :class="n.level">{{ n.level.toUpperCase() }}</span>
                <div class="np-content">
                  <div class="np-title">{{ n.title }}</div>
                  <div class="np-desc">{{ n.message }}</div>
                  <div class="np-time">{{ n.time }}</div>
                </div>
              </div>
            </div>
          </div>
          <div class="user-info">
            <div class="user-text">
              <span class="user-name">
                {{ currentUser.name }}
                <span class="role-badge" :class="currentUser.role === 'admin' ? 'badge-admin' : 'badge-user'">
                  {{ currentUser.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </span>
            </div>
            <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${currentUser.name}`" class="user-avatar" alt=""/>
          </div>
        </div>
      </header>

      <main class="content-container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, provide, ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const route  = useRoute()

const searchKeyword = ref('')

const theme = ref(localStorage.getItem('theme') || 'light')

const applyTheme = (t) => {
  document.documentElement.setAttribute('data-theme', t)
  theme.value = t
  localStorage.setItem('theme', t)
}

const handleSearch = () => {
  const kw = searchKeyword.value.trim()
  if (!kw) {
    ElMessage.warning('请输入搜索关键字')
    return
  }

  const lower = kw.toLowerCase()

  if (kw.includes('夜间') || lower.includes('dark')) {
    applyTheme('dark')
    ElMessage.success('已切换到夜间模式')
    return
  }

  if (kw.includes('白天') || lower.includes('light')) {
    applyTheme('light')
    ElMessage.success('已切回日间模式')
    return
  }

  if (kw.includes('仪表') || lower.includes('dashboard')) {
    router.push('/dashboard')
    return
  }
  if (kw.includes('实时') || kw.includes('监控')) {
    router.push('/camera/realtime')
    return
  }
  if (kw.includes('任务') || kw.includes('检测') || lower.includes('detection')) {
    router.push('/detection/upload')
    return
  }
  if (kw.includes('摄像头') || kw.includes('配置') || lower.includes('camera')) {
    router.push('/camera/config')
    return
  }
  if (kw.includes('模型') || kw.includes('ai')) {
    router.push('/system/ai-models')
    return
  }
  if (kw.includes('系统') || kw.includes('用户') || lower.includes('user')) {
    router.push('/system/users')
    return
  }

  ElMessage.info(`暂未找到与「${kw}」匹配的页面`)
}

const toggleTheme = () => {
  const next = theme.value === 'dark' ? 'light' : 'dark'
  applyTheme(next)
  ElMessage.success(next === 'dark' ? '已切换到夜间模式' : '已切回日间模式')
}

const handleRefreshClick = () => {
  // 简单粗暴刷新当前页面
  router.go(0)
}

const notifyOpen = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const toggleNotifyPanel = () => { notifyOpen.value = !notifyOpen.value }
const authHeaders = () => {
  const access = localStorage.getItem('access_token') || ''
  return access ? { Authorization: `Bearer ${access}` } : {}
}
const lastReadAtKey = 'notify_last_read_at'
const lastReadAt = ref(Number(localStorage.getItem(lastReadAtKey) || 0))

const runIndexKey = 'task_run_index'
const lastCountedSigKey = 'task_run_last_counted_sig'
const runIndex = ref(Number(localStorage.getItem(runIndexKey) || 0))
const lastCountedSig = ref(localStorage.getItem(lastCountedSigKey) || '')
const persistRunIndex = () => localStorage.setItem(runIndexKey, String(runIndex.value || 0))
const persistLastCountedSig = () => localStorage.setItem(lastCountedSigKey, String(lastCountedSig.value || ''))

const updateRunIndexFromLatest = async (latestId) => {
  if (!latestId) return
  try {
    const resp = await axios.get(`/api/detection/tasks/${latestId}`, { headers: authHeaders() })
    const d = resp.data || {}
    const finishIso = d.finished_at_iso || d.finished_at || ''
    const completed = d.status === 'completed'
    const sig = (completed && finishIso) ? `${d.id}:${finishIso}:${d.process_time_ms || ''}` : ''
    if (sig && sig !== lastCountedSig.value) {
      runIndex.value = Number(runIndex.value || 0) + 1
      persistRunIndex()
      lastCountedSig.value = sig
      persistLastCountedSig()
    }
  } catch (e) {
    // 忽略网络/权限错误，保持上次计数
  }
}

const fetchNotifications = async () => {
  try {
    const resp = await axios.get('/api/detection/tasks', { headers: authHeaders() })
    const items = resp.data?.results || []
    // 使用与左侧卡片相同的计数（runIndex），并在此处补充一次同步
    await updateRunIndexFromLatest(items[0]?.id)
    const completed = runIndex.value
    const processing = items.filter(i => i.status === 'processing').length
    const failed = items.filter(i => i.status === 'failed').length
    notifications.value = items.slice(0, 5).map(it => {
      const iso = it.created_at_iso || ''
      const ts = iso ? new Date(iso).getTime() : 0
      const read = ts > 0 ? ts <= lastReadAt.value : (it.status === 'completed')
      const statusText = it.status === 'completed' ? '已完成' : it.status === 'failed' ? '检测中断' : '检测中'
      const level = it.status === 'completed' ? 'info' : it.status === 'failed' ? 'error' : 'warn'
      const reason = (it.error_message || '').toString()
      return {
      id: it.id,
      title: `任务 ${it.name} ${statusText}`,
      message: it.status === 'failed' && reason ? `原因: ${reason}` : `类型: ${it.type}，状态: ${it.status}`,
      time: it.created_at,
      level,
      read,
      _ts: ts
      }
    })
    unreadCount.value = notifications.value.filter(n => !n.read && n.id !== 'summary').length
    notifications.value.unshift({
      id: 'summary',
      title: `完成 ${completed} · 检测中 ${processing} · 中断 ${failed}`,
      message: '状态总览',
      time: '',
      level: 'info',
      read: true
    })
  } catch (e) {}
}
const markAllRead = () => {
  const now = Date.now()
  lastReadAt.value = now
  localStorage.setItem(lastReadAtKey, String(now))
  notifications.value = notifications.value.map(n => ({ ...n, read: true }))
  unreadCount.value = 0
  ElMessage.success('已全部标为已读')
}
const openNotification = (n) => {
  notifyOpen.value = false
  if (n.id) router.push('/detection/tasks')
}
let notifyTimer = null

// ─────────────────────────────────────────────
// 当前登录用户
// 实际项目中从 登录接口 / Pinia / localStorage 读取
// role: 'admin' | 'user'
// ─────────────────────────────────────────────
const currentUser = reactive({
  id: 0,
  name: '未登录',
  email: '',
  role: 'user',
})

// 向所有子孙组件注入
provide('currentUser', currentUser)

// ─────────────────────────────────────────────
const handleLogout = () => { router.push('/login') }

const currentRouteName = computed(() => {
  if (route.path === '/dashboard') return '仪表板'
  if (route.path.includes('/camera/realtime')) return '实时监控'
  if (route.path.includes('/detection/upload') || route.path.includes('/detection/tasks')) return '检测任务'
  if (route.path.includes('/camera/config')) return '摄像头配置'
  if (route.path.includes('/system/ai-models')) return 'AI 模型管理'
  if (route.path.includes('/system/users')) return '系统设置'
  return '系统页面'
})

onMounted(async () => {
  // 初始化主题
  applyTheme(theme.value)

  const access = localStorage.getItem('access_token') || ''
  if (!access) return
  try {
    const resp = await axios.get('/api/me', {
      headers: { Authorization: `Bearer ${access}` }
    })
    const data = resp.data || {}
    currentUser.id = data.id || 0
    currentUser.name = data.username || '用户'
    currentUser.email = data.email || ''
    currentUser.role = data.is_staff ? 'admin' : 'user'
  } catch (e) {
    // token 失效则忽略，保持未登录态
  }
  fetchNotifications()
  notifyTimer = window.setInterval(fetchNotifications, 2000)
})
onUnmounted(() => {
  if (notifyTimer) window.clearInterval(notifyTimer)
  notifyTimer = null
})
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background:
    radial-gradient(circle at top, rgba(59, 158, 255, 0.08), transparent 32%),
    linear-gradient(180deg, #f8fbff 0%, var(--color-bg-page) 100%);
  color: var(--color-text-main);
}

.sidebar {
  width: 248px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(226, 232, 240, 0.88);
  position: sticky;
  top: 0;
  height: 100vh;
  align-self: flex-start;
  z-index: 100;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 22px;
  min-height: 74px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.78);
}

.logo-icon {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.22);
  flex-shrink: 0;
}

.logo-meta {
  min-width: 0;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: -0.03em;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 20px 14px 14px;
}

.nav-divider {
  height: 1px;
  margin: 18px 24px;
  background: linear-gradient(90deg, rgba(226, 232, 240, 0), rgba(226, 232, 240, 1), rgba(226, 232, 240, 0));
}

.nav-section + .nav-section {
  margin-top: 0;
}

.nav-section-title {
  padding: 0 24px 10px;
  font-size: 14px;
  line-height: 22px;
  font-weight: 700;
  color: #64748b;
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 56px;
  padding: 0 22px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 24px;
  font-weight: 600;
  color: var(--color-text-sub);
  cursor: pointer;
  transition: all .2s ease;
  position: relative;
}

.nav-icon {
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  flex-shrink: 0;
}

.nav-item:hover {
  background: rgba(59, 130, 246, 0.08);
  color: #2563eb;
}

.nav-item:hover .nav-icon {
  color: #2563eb;
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.16), rgba(59, 130, 246, 0.07));
  color: #2563eb;
  font-weight: 700;
  box-shadow: inset 0 0 0 1px rgba(59, 130, 246, 0.08);
}

.nav-item.active .nav-icon {
  color: #2563eb;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10px;
  bottom: 10px;
  width: 4px;
  border-radius: 0 999px 999px 0;
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
}

.chevron {
  margin-left: auto;
  color: #94a3b8;
  transition: transform .2s ease;
}

.chevron.open {
  transform: rotate(180deg);
}

.nav-children {
  margin-top: 2px;
  padding-left: 16px;
}

.nav-child {
  position: relative;
  margin: 4px 0;
  padding: 10px 14px 10px 34px;
  border-radius: 12px;
  font-size: 14px;
  color: #64748b;
  cursor: pointer;
  transition: all .18s ease;
}

.nav-child::before {
  content: '';
  position: absolute;
  left: 18px;
  top: 50%;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #cbd5e1;
  transform: translateY(-50%);
  transition: all .18s ease;
}

.nav-child:hover {
  background: rgba(59, 130, 246, 0.06);
  color: #2563eb;
}

.nav-child:hover::before,
.child-active::before {
  background: #2563eb;
}

.child-active {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
  font-weight: 600;
}

.sidebar-user-card {
  margin: 8px 16px 12px;
  padding: 14px;
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(248, 250, 252, 0.98), rgba(241, 245, 249, 0.96));
  border: 1px solid rgba(226, 232, 240, 0.96);
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-user-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid rgba(226, 232, 240, 0.96);
}

.sidebar-user-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-main);
}

.sidebar-user-role {
  margin-top: 3px;
  font-size: 12px;
  color: #64748b;
}

.sidebar-logout {
  margin: 0 16px 18px;
  min-height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px solid rgba(248, 113, 113, 0.28);
  border-radius: 14px;
  background: #fff;
  font-size: 14px;
  color: #ef4444;
  cursor: pointer;
  font-weight: 600;
  transition: all .18s ease;
}

.sidebar-logout:hover {
  background: #fff5f5;
  border-color: rgba(239, 68, 68, 0.38);
}

.main-wrap {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  height: 74px;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.84);
  display: flex;
  align-items: center;
  padding: 0 28px;
  gap: 16px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  white-space: nowrap;
}

.bc-item {
  color: #64748b;
  font-weight: 500;
}

.bc-item.active {
  color: #0f172a;
  font-weight: 700;
}

.bc-sep {
  color: #cbd5e1;
}

.top-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.search-box {
  width: min(100%, 420px);
  min-height: 42px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  background: rgba(248, 250, 252, 0.95);
  border: 1px solid rgba(226, 232, 240, 0.95);
  border-radius: 16px;
  color: #94a3b8;
  transition: all .2s ease;
}

.search-box:focus-within {
  border-color: rgba(59, 130, 246, 0.48);
  background: #fff;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08);
}

.search-input {
  border: none;
  background: transparent;
  font-size: 14px;
  color: var(--color-text-main);
  outline: none;
  width: 100%;
  font-family: inherit;
}

.search-input::placeholder {
  color: #94a3b8;
}

.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border: 1px solid rgba(226, 232, 240, 0.92);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.96);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #475569;
  cursor: pointer;
  transition: all .18s ease;
}

.icon-btn:hover {
  transform: translateY(-1px);
  color: #2563eb;
  border-color: rgba(59, 130, 246, 0.28);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.12);
}

.notify {
  position: relative;
}

.notify-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f43f5e;
  color: #fff;
  border-radius: 999px;
  border: 2px solid #fff;
  font-size: 11px;
  font-weight: 800;
  line-height: 1;
}

.notify-panel {
  position: fixed;
  right: 24px;
  top: 82px;
  width: 360px;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(226, 232, 240, 0.92);
  border-radius: 18px;
  box-shadow: 0 24px 50px rgba(15, 23, 42, 0.14);
  z-index: 9999;
  overflow: hidden;
}

.np-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.82);
}

.np-mark {
  border: none;
  background: transparent;
  color: #2563eb;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
}

.np-list {
  max-height: 320px;
  overflow: auto;
}

.np-empty {
  padding: 18px;
  color: var(--color-text-sub);
  font-size: 13px;
  text-align: center;
}

.np-item {
  display: flex;
  gap: 10px;
  padding: 12px 14px;
  cursor: pointer;
}

.np-item.unread {
  background: rgba(59, 130, 246, 0.05);
}

.np-tag {
  width: 56px;
  height: 22px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
}

.np-tag.info { background: #3b82f6; }
.np-tag.warn { background: #f59e0b; }
.np-tag.error { background: #ef4444; }

.np-content { flex: 1; }
.np-title { font-size: 13px; font-weight: 700; color: var(--color-text-main); margin-bottom: 2px; }
.np-desc { font-size: 12px; color: var(--color-text-sub); }
.np-time { font-size: 11px; color: var(--color-text-light); }

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 2px;
  padding-left: 14px;
  border-left: 1px solid rgba(226, 232, 240, 0.9);
}

.user-text {
  text-align: right;
}

.user-name {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-main);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid rgba(226, 232, 240, 0.96);
}

.role-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
}

.badge-admin {
  background: rgba(59, 130, 246, 0.12);
  color: #2563eb;
}

.badge-user {
  background: rgba(148, 163, 184, 0.14);
  color: #64748b;
}

.content-container {
  flex: 1;
  padding: 28px;
  overflow-y: auto;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 1200px) {
  .sidebar {
    width: 220px;
  }

  .topbar {
    padding: 0 18px;
  }

  .content-container {
    padding: 20px;
  }
}
</style>
