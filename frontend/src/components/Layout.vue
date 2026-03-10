<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
        </div>
        <span class="logo-text">Aero Smart</span>
      </div>

      <nav class="sidebar-nav">
        <div 
          class="nav-item" 
          :class="{ active: route.path === '/dashboard' }"
          @click="router.push('/dashboard')"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
          </svg>
          <span>仪表板</span>
        </div>

        <div class="nav-group">
          <div class="nav-item has-children" @click="toggleGroup('detect')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span>检测管理</span>
            <svg class="chevron" :class="{ open: groups.detect }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
          <div class="nav-children" v-show="groups.detect">
            <div 
              class="nav-child" 
              :class="{ 'child-active': route.path === '/detection/upload' }"
              @click="router.push('/detection/upload')"
            >上传检测</div>
            <div 
              class="nav-child"
              :class="{ 'child-active': route.path === '/detection/tasks' }"
              @click="router.push('/detection/tasks')"
            >检测任务</div>
          </div>
        </div>

        <div class="nav-group">
          <div class="nav-item has-children" @click="toggleGroup('camera')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 7 16 12 23 17V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
            </svg>
            <span>摄像头管理</span>
            <svg class="chevron" :class="{ open: groups.camera }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
          <div class="nav-children" v-show="groups.camera">
            <div 
              class="nav-child"
              :class="{ 'child-active': route.path === '/camera/config' }"
              @click="router.push('/camera/config')"
            >摄像头配置</div>
            <div 
              class="nav-child"
              :class="{ 'child-active': route.path === '/camera/realtime' }"
              @click="router.push('/camera/realtime')"
            >实时监控</div>
          </div>
        </div>

        <!-- 系统管理：仅管理员可见 -->
        <div 
          v-if="currentUser.role === 'admin'"
          class="nav-item"
          :class="{ active: route.path.startsWith('/system') }"
          @click="router.push('/system/users')"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          <span>系统管理</span>
        </div>
      </nav>

      <div class="sidebar-logout" @click="handleLogout">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        <span>退出系统</span>
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
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <input type="text" placeholder="全局搜索..." class="search-input"/>
          </div>
        </div>
        <div class="top-right">
          <button class="icon-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-5.05"/>
            </svg>
          </button>
          <button class="icon-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
          </button>
          <button class="icon-btn notify">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <span class="notify-dot"></span>
          </button>
          <div class="user-info">
            <div class="user-text">
              <!-- 显示真实用户名和角色标签 -->
              <span class="user-name">
                {{ currentUser.name }}
                <span class="role-badge" :class="currentUser.role === 'admin' ? 'badge-admin' : 'badge-user'">
                  {{ currentUser.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </span>
              <span class="user-email">{{ currentUser.email }}</span>
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

      <footer class="main-footer">
        <span>© 2026 Aero Smart Monitoring. All rights reserved.</span>
        <div class="footer-links">
          <a href="#">服务协议</a>
          <a href="#">隐私政策</a>
          <a href="#">版本 v1.0.4</a>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route  = useRoute()

const groups = reactive({ detect: true, camera: true })
const toggleGroup = (key) => { groups[key] = !groups[key] }

// ─────────────────────────────────────────────
// 当前登录用户
// 实际项目中从 登录接口 / Pinia / localStorage 读取
// role: 'admin' | 'user'
// ─────────────────────────────────────────────
const currentUser = reactive({
  id: 1,
  name: '张伟',
  email: 'zhangwei@aero-tech.cn',
  role: 'admin',   // 切换为 'user' 即可测试普通用户视角
})

// 向所有子孙组件注入
provide('currentUser', currentUser)

// ─────────────────────────────────────────────
const handleLogout = () => { router.push('/login') }

const currentRouteName = computed(() => {
  if (route.path === '/dashboard') return '运行概览'
  if (route.path.includes('/detection/upload')) return '上传检测'
  if (route.path.includes('/detection/tasks')) return '检测任务'
  if (route.path.includes('/camera/config')) return '摄像头配置'
  if (route.path.includes('/camera/realtime')) return '实时监控'
  if (route.path.includes('/system')) return '用户管理'
  return '系统页面'
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard-layout {
  display: flex; min-height: 100vh; width: 100vw;
  background: #f4f7fa;
  font-family: 'Sora', 'Noto Sans SC', sans-serif;
  color: #1a2332;
}

/* SIDEBAR */
.sidebar {
  width: 220px; flex-shrink: 0; background: #fff;
  display: flex; flex-direction: column;
  border-right: 1px solid #edf0f5;
  position: sticky; top: 0; height: 100vh; align-self: flex-start; z-index: 100;
}
.sidebar-logo {
  display: flex; align-items: center; gap: 9px;
  padding: 18px 20px; border-bottom: 1px solid #f0f3f8; height: 60px;
}
.logo-icon {
  width: 30px; height: 30px; background: #3b9eff; border-radius: 7px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.logo-text { font-size: 16px; font-weight: 700; color: #3b9eff; letter-spacing: -.2px; }

.sidebar-nav { flex: 1; padding: 14px 0; overflow-y: auto; }
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 20px; font-size: 14px; color: #5a6475;
  cursor: pointer; transition: all .18s; position: relative;
}
.nav-item:hover { background: #f5f8ff; color: #3b9eff; }
.nav-item.active { background: #eff6ff; color: #3b9eff; font-weight: 600; }
.nav-item.active::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0;
  width: 3px; background: #3b9eff; border-radius: 0 2px 2px 0;
}
.chevron { margin-left: auto; transition: transform .2s; }
.chevron.open { transform: rotate(180deg); }
.nav-children { background: #fafbfc; }
.nav-child {
  padding: 10px 20px 10px 46px; font-size: 13.5px; color: #6b7a90; cursor: pointer; transition: all .15s;
}
.nav-child:hover { color: #3b9eff; background: #f0f7ff; }
.child-active { color: #3b9eff; font-weight: 500; }

.sidebar-logout {
  display: flex; align-items: center; gap: 10px; padding: 18px 20px;
  border-top: 1px solid #f0f3f8; font-size: 14px; color: #e85c5c;
  cursor: pointer; font-weight: 500; transition: opacity .18s;
}
.sidebar-logout:hover { opacity: .75; background: #fff1f0; }

/* MAIN WRAP */
.main-wrap { flex: 1; min-width: 0; display: flex; flex-direction: column; min-height: 100vh; }

/* TOPBAR */
.topbar {
  height: 60px; background: #fff; border-bottom: 1px solid #edf0f5;
  display: flex; align-items: center; padding: 0 24px; gap: 16px;
  position: sticky; top: 0; z-index: 50;
}
.breadcrumb { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.bc-item { color: #9aa5b4; }
.bc-item.active { color: #1a2332; font-weight: 500; }
.bc-sep { color: #c8d0dc; }
.top-center { flex: 1; display: flex; justify-content: center; }
.search-box {
  display: flex; align-items: center; gap: 8px;
  background: #f4f7fa; border: 1px solid #e8ecf2;
  border-radius: 8px; padding: 8px 14px; width: 260px; transition: all 0.2s;
}
.search-box:focus-within { border-color: #3b9eff; background: #fff; box-shadow: 0 0 0 3px rgba(59,158,255,.1); }
.search-input {
  border: none; background: transparent; font-size: 13.5px;
  color: #1a2332; outline: none; width: 100%; font-family: inherit;
}
.search-input::placeholder { color: #b0bcc8; }
.top-right { display: flex; align-items: center; gap: 12px; }
.icon-btn {
  width: 36px; height: 36px; border: 1px solid #edf0f5; border-radius: 8px;
  background: #fff; display: flex; align-items: center; justify-content: center;
  color: #6b7a90; cursor: pointer; transition: all .18s;
}
.icon-btn:hover { background: #f5f8ff; color: #3b9eff; border-color: #d0e4ff; }
.notify { position: relative; }
.notify-dot {
  position: absolute; top: 6px; right: 6px; width: 8px; height: 8px;
  background: #f5615a; border-radius: 50%; border: 1.5px solid white;
}
.user-info {
  display: flex; align-items: center; gap: 12px; margin-left: 8px;
  cursor: pointer; padding-left: 12px; border-left: 1px solid #edf0f5;
}
.user-text { text-align: right; }
.user-name  {
  display: flex; align-items: center; justify-content: flex-end; gap: 6px;
  font-size: 13.5px; font-weight: 600; color: #1a2332;
}
.user-email { display: block; font-size: 11.5px; color: #9aa5b4; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; border: 2px solid #e8ecf2; }

/* 角色徽标 */
.role-badge {
  display: inline-block;
  padding: 1px 7px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
}
.badge-admin { background: #1677ff; color: #fff; }
.badge-user  { background: #f0f0f0; color: #6b7280; }

/* CONTENT */
.content-container { flex: 1; padding: 28px; overflow-y: auto; }

/* FOOTER */
.main-footer {
  height: 50px; background: #fff; border-top: 1px solid #edf0f5;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 28px; font-size: 12.5px; color: #9aa5b4;
}
.footer-links { display: flex; gap: 20px; }
.footer-links a { color: #9aa5b4; text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: #3b9eff; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>