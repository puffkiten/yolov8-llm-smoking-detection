<template>
  <div class="page">
    <!-- Toast -->
    <transition name="toast">
      <div v-if="toast.show" class="toast" :class="toast.type">
        <span>{{ toast.type === 'error' ? '✕' : '✓' }}</span>
        {{ toast.msg }}
      </div>
    </transition>

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1>用户管理</h1>
        <p>管理系统访问权限、用户信息及账号状态</p>
      </div>
      <div class="header-actions">
        <button v-if="isAdmin" class="btn-primary" @click="openAddModal">
          <span>＋</span> 新增用户
        </button>
        <button v-if="isAdmin" class="btn-default" @click="handleExport">
          <span>⬇</span> 导出数据
        </button>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="card search-bar">
      <div class="search-fields">
        <div class="field-group">
          <label>用户名</label>
          <input v-model="search.name" placeholder="输入用户名关键字" />
        </div>
        <div class="field-group">
          <label>手机号</label>
          <input v-model="search.phone" placeholder="输入完整手机号" />
        </div>
        <div class="field-group">
          <label>用户类型</label>
          <select v-model="search.role" :class="{ 'placeholder-gray': search.role === '全部角色' }">
            <option>全部角色</option>
            <option>管理员</option>
            <option>普通用户</option>
          </select>
        </div>
        <div class="field-group">
          <label>账号状态</label>
          <select v-model="search.status" :class="{ 'placeholder-gray': search.status === '全部状态' }">
            <option>全部状态</option>
            <option>正常</option>
            <option>禁用</option>
          </select>
        </div>
        <div class="search-btns">
          <button class="btn-primary" @click="handleSearch">搜索</button>
          <button class="btn-primary btn-reset" @click="handleReset">重置</button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card table-card">
      <div class="table-header">
        <div class="table-title">
          <div class="title-bar"></div>
          <span>用户列表 ({{ filteredUsers.length }})</span>
        </div>
        <!-- 仅管理员显示批量操作 -->
        <button v-if="isAdmin" class="btn-default small">▽ 批量操作</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>序号</th>
            <th>用户信息</th>
            <th>昵称</th>
            <th>手机号</th>
            <th>性别</th>
            <th>用户类型</th>
            <th>状态</th>
            <th>创建时间</th>
            <!-- 仅管理员显示操作列 -->
            <th v-if="isAdmin">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td class="seq">{{ user.seq }}</td>
            <td>
              <div class="user-info">
                <div class="avatar" :style="{ background: avatarColor(user.avatar) }">
                  {{ user.avatar }}
                  <span class="dot" :class="user.status === '正常' ? 'dot-active' : 'dot-disabled'"></span>
                </div>
                <div>
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-email">{{ user.email }}</div>
                </div>
              </div>
            </td>
            <td>{{ user.nickname }}</td>
            <td>{{ user.phone }}</td>
            <td>{{ user.gender }}</td>
            <td>
              <span class="role-tag" :class="user.role === '管理员' ? 'admin' : 'normal'">
                {{ user.role }}
              </span>
            </td>
            <td>
              <span class="status-tag" :class="user.status === '正常' ? 'active' : 'disabled'">
                ⊙ {{ user.status }}
              </span>
            </td>
            <td class="date">{{ user.createdAt }}</td>
            <!-- 操作列：管理员全部可操，且不能操作自己 -->
            <td v-if="isAdmin" class="actions">
              <button class="action-btn edit" @click="openEditModal(user)">✎ 编辑</button>
              <span class="divider">|</span>

              <!-- 自己的行：禁用/删除置灰 -->
              <template v-if="user.id === currentUser.id">
                <span class="action-disabled" title="不能禁用自己">✕ 禁用</span>
                <span class="divider">|</span>
                <span class="action-disabled" title="不能删除自己">✕ 删除</span>
              </template>

              <!-- 其他管理员：禁用/删除置灰（平级无权限） -->
              <template v-else-if="user.role === '管理员'">
                <span class="action-disabled" title="不能操作其他管理员">✕ 禁用</span>
                <span class="divider">|</span>
                <span class="action-disabled" title="不能操作其他管理员">✕ 删除</span>
              </template>

              <!-- 普通用户：全部操作可用 -->
              <template v-else>
                <button
                  class="action-btn"
                  :class="user.status === '正常' ? 'ban' : 'enable'"
                  @click="openToggleModal(user)"
                >
                  {{ user.status === '正常' ? '✕ 禁用' : '✓ 启用' }}
                </button>
                <span class="divider">|</span>
                <button class="action-btn delete" @click="openDeleteModal(user)">✕ 删除</button>
              </template>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td :colspan="isAdmin ? 9 : 8" style="text-align:center; padding: 40px; color: #9ca3af;">暂无数据</td>
          </tr>
        </tbody>
      </table>

      <div class="pagination">
        <span class="page-info">显示 1 到 {{ filteredUsers.length }} 共 {{ filteredUsers.length }} 条记录</span>
        <div class="page-btns">
          <button class="page-btn">上一页</button>
          <button class="page-btn active">1</button>
          <button class="page-btn">2</button>
          <button class="page-btn">下一页</button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-card blue">
        <span class="stat-icon">📈</span>
        <div>
          <div class="stat-label">系统当前活跃用户</div>
          <div class="stat-value blue-text">{{ activeCount }}</div>
        </div>
      </div>
      <div class="stat-card green">
        <span class="stat-icon">👤</span>
        <div>
          <div class="stat-label">本月新增注册</div>
          <div class="stat-value green-text">+{{ monthlyNewCount }}</div>
        </div>
      </div>
      <div class="stat-card gray">
        <span class="stat-icon">🚫</span>
        <div>
          <div class="stat-label">当前禁用账户</div>
          <div class="stat-value gray-text">{{ disabledCount }}</div>
        </div>
      </div>
    </div>

    <!-- ===== Modal: 新增 / 编辑 ===== -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="modal.type === 'add' || modal.type === 'edit'" class="overlay" @click.self="closeModal">
          <div class="modal">
            <div class="modal-header">
              <span>{{ modal.type === 'add' ? '新增用户' : '编辑用户' }}</span>
              <button class="modal-close" @click="closeModal">×</button>
            </div>
            <div class="modal-body">
              <div class="form-grid">
                <div class="form-field">
                  <label><span class="required">*</span>用户名</label>
                  <input v-model="form.name" placeholder="请输入用户名" />
                </div>
                <div class="form-field">
                  <label>昵称</label>
                  <input v-model="form.nickname" placeholder="请输入昵称" />
                </div>
                <div class="form-field">
                  <label><span class="required">*</span>手机号</label>
                  <input v-model="form.phone" placeholder="请输入手机号" />
                </div>
                <div class="form-field">
                  <label>邮箱</label>
                  <input v-model="form.email" placeholder="请输入邮箱" />
                </div>
                <div class="form-field">
                  <label>性别</label>
                  <select v-model="form.gender">
                    <option>男</option>
                    <option>女</option>
                  </select>
                </div>
                <div class="form-field">
                  <label><span class="required">*</span>用户类型</label>
                  <select v-model="form.role">
                    <option>普通用户</option>
                    <option>管理员</option>
                  </select>
                </div>
                <div v-if="modal.type === 'add'" class="form-field">
                  <label><span class="required">*</span>初始密码</label>
                  <input v-model="form.password" type="password" placeholder="请输入初始密码" />
                </div>
                <div class="form-field">
                  <label>账号状态</label>
                  <select v-model="form.status">
                    <option>正常</option>
                    <option>禁用</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn-default" @click="closeModal">取消</button>
              <button class="btn-primary" @click="handleFormSave">确认</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- ===== Modal: 删除确认 ===== -->
      <transition name="modal">
        <div v-if="modal.type === 'delete'" class="overlay" @click.self="closeModal">
          <div class="modal confirm-modal">
            <div class="modal-header">
              <span>删除确认</span>
              <button class="modal-close" @click="closeModal">×</button>
            </div>
            <div class="modal-body center">
              <div class="confirm-icon red-bg">⚠️</div>
              <p class="confirm-title">
                确定要删除用户 <span class="red-text">「{{ modal.user?.name }}」</span> 吗？
              </p>
              <p class="confirm-desc">此操作不可恢复，该用户的所有数据将被永久删除。</p>
            </div>
            <div class="modal-footer center">
              <button class="btn-default" @click="closeModal">取消</button>
              <button class="btn-danger" @click="handleDelete">确认删除</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- ===== Modal: 禁用 / 启用确认 ===== -->
      <transition name="modal">
        <div v-if="modal.type === 'toggle'" class="overlay" @click.self="closeModal">
          <div class="modal confirm-modal">
            <div class="modal-header">
              <span>{{ modal.user?.status === '正常' ? '禁用确认' : '启用确认' }}</span>
              <button class="modal-close" @click="closeModal">×</button>
            </div>
            <div class="modal-body center">
              <div class="confirm-icon" :class="modal.user?.status === '正常' ? 'yellow-bg' : 'green-bg'">
                {{ modal.user?.status === '正常' ? '🔒' : '🔓' }}
              </div>
              <p class="confirm-title">
                确定要{{ modal.user?.status === '正常' ? '禁用' : '启用' }}用户
                <span :class="modal.user?.status === '正常' ? 'yellow-text' : 'green-text'">
                  「{{ modal.user?.name }}」
                </span> 吗？
              </p>
              <p class="confirm-desc">
                {{ modal.user?.status === '正常' ? '禁用后该用户将无法登录系统。' : '启用后该用户可正常登录系统。' }}
              </p>
            </div>
            <div class="modal-footer center">
              <button class="btn-default" @click="closeModal">取消</button>
              <button
                class="btn-confirm"
                :class="modal.user?.status === '正常' ? 'btn-warn' : 'btn-success'"
                @click="handleToggle"
              >
                {{ modal.user?.status === '正常' ? '确认禁用' : '确认启用' }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject } from 'vue'

// ───────── 注入当前登录用户 ─────────
// 由 Layout.vue 通过 provide('currentUser', ...) 注入
// role: 'admin' | 'user'
const currentUser = inject('currentUser', { id: 0, name: '', email: '', role: 'user' })
const isAdmin = computed(() => currentUser.role === 'admin')

// ───────── 初始数据 ─────────
const initialUsers = [
  { id: 1, seq: '01', name: '张伟',  email: 'zhangwei@aero-tech.cn',    nickname: '张伟',  phone: '138-0013-8001', gender: '男', role: '管理员', status: '正常', createdAt: '2023-10-12 14:30', avatar: 'ZW' },
  { id: 2, seq: '02', name: '李娜',  email: 'lina_safety@aero-tech.cn', nickname: '李娜',  phone: '139-1122-3344', gender: '女', role: '普通用户', status: '正常', createdAt: '2023-11-05 09:15', avatar: 'LN' },
  { id: 3, seq: '03', name: '王建国', email: 'jianguo.wang@aero-tech.cn', nickname: '王建国', phone: '136-5566-7788', gender: '男', role: '普通用户', status: '禁用', createdAt: '2023-12-01 16:45', avatar: 'WJ' },
  { id: 4, seq: '04', name: '赵敏',  email: 'zhaomin@aero-tech.cn',     nickname: '赵敏',  phone: '131-9988-7766', gender: '女', role: '管理员', status: '正常', createdAt: '2024-01-20 11:00', avatar: 'ZM' },
  { id: 5, seq: '05', name: '刘洋',  email: 'liuyang_dev@aero-tech.cn', nickname: '刘洋',  phone: '188-4433-2211', gender: '男', role: '普通用户', status: '正常', createdAt: '2024-02-14 10:20', avatar: 'LY' },
]

const AVATAR_COLORS = { ZW: '#4A90D9', LN: '#E8526A', WJ: '#6B7C8F', ZM: '#D4A27A', LY: '#5BAD8F' }
const avatarColor = (code) => AVATAR_COLORS[code] || '#888'

// ───────── 状态 ─────────
const users = ref(initialUsers.map(u => ({ ...u })))

const search = reactive({ name: '', phone: '', role: '全部角色', status: '全部状态' })
const filteredUsers = ref([...users.value])

const modal = reactive({ type: '', user: null })
const form = reactive({ name: '', nickname: '', phone: '', email: '', gender: '男', role: '普通用户', status: '正常', password: '' })

const toast = reactive({ show: false, msg: '', type: 'success' })

// ───────── 计算属性 ─────────
const disabledCount = computed(() => users.value.filter(u => u.status === '禁用').length)
const activeCount = computed(() => users.value.filter(u => u.status === '正常').length)
const monthlyNewCount = computed(() => {
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth() + 1
  return users.value.filter(u => {
    const d = new Date(u.createdAt)
    return d.getFullYear() === year && (d.getMonth() + 1) === month
  }).length
})

// ───────── 工具函数 ─────────
let toastTimer = null
function showToast(msg, type = 'success') {
  clearTimeout(toastTimer)
  toast.msg = msg
  toast.type = type
  toast.show = true
  toastTimer = setTimeout(() => { toast.show = false }, 2500)
}

function closeModal() { modal.type = ''; modal.user = null }

function resetForm() {
  Object.assign(form, { name: '', nickname: '', phone: '', email: '', gender: '男', role: '普通用户', status: '正常', password: '' })
}

// ───────── 搜索 ─────────
function handleSearch() {
  filteredUsers.value = users.value.filter(u => {
    if (search.name && !u.name.includes(search.name)) return false
    if (search.phone && !u.phone.replace(/-/g, '').includes(search.phone)) return false
    if (search.role !== '全部角色' && u.role !== search.role) return false
    if (search.status !== '全部状态' && u.status !== search.status) return false
    return true
  })
}

function handleReset() {
  Object.assign(search, { name: '', phone: '', role: '全部角色', status: '全部状态' })
  filteredUsers.value = [...users.value]
}

// ───────── Modal 开启 ─────────
function openAddModal() {
  resetForm()
  modal.type = 'add'
}

function openEditModal(user) {
  Object.assign(form, { ...user })
  modal.user = user
  modal.type = 'edit'
}

function openDeleteModal(user) {
  modal.user = user
  modal.type = 'delete'
}

function openToggleModal(user) {
  modal.user = user
  modal.type = 'toggle'
}

// ───────── 表单保存 ─────────
function handleFormSave() {
  if (!form.name || !form.phone) {
    showToast('请填写必填项', 'error')
    return
  }

  if (modal.type === 'add') {
    const newUser = {
      ...form,
      id: Date.now(),
      seq: String(users.value.length + 1).padStart(2, '0'),
      createdAt: new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-').slice(0, 16),
      avatar: (form.name[0] + (form.name[1] || '')).toUpperCase(),
    }
    users.value.push(newUser)
    showToast('用户新增成功')
  } else {
    const idx = users.value.findIndex(u => u.id === modal.user.id)
    if (idx !== -1) Object.assign(users.value[idx], { ...form })
    showToast('用户信息已更新')
  }

  filteredUsers.value = [...users.value]
  closeModal()
}

// ───────── 删除 ─────────
function handleDelete() {
  users.value = users.value.filter(u => u.id !== modal.user.id)
  filteredUsers.value = [...users.value]
  showToast('用户已删除', 'error')
  closeModal()
}

// ───────── 禁用 / 启用 ─────────
function handleToggle() {
  const idx = users.value.findIndex(u => u.id === modal.user.id)
  if (idx !== -1) {
    const wasNormal = users.value[idx].status === '正常'
    users.value[idx].status = wasNormal ? '禁用' : '正常'
    showToast(wasNormal ? '用户已禁用' : '用户已启用')
  }
  filteredUsers.value = [...users.value]
  closeModal()
}

// ───────── 导出（占位） ─────────
function handleExport() {
  showToast('数据导出中…')
}
</script>

<style scoped>
/* ── 基础 ── */
.page {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #1a1a1a;
  padding: 28px 32px;
  min-height: 100vh;
  background: #f5f6fa;
  box-sizing: border-box;
}

/* ── Toast ── */
.toast {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 24px;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  z-index: 3000;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,.15);
}
.toast.success { background: #22c55e; }
.toast.error   { background: #ef4444; }
.toast-enter-active, .toast-leave-active { transition: all .25s; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(-50%) translateY(-12px); }

/* ── Page Header ── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}
.page-header h1 { font-size: 22px; font-weight: 700; margin: 0 0 6px; }
.page-header p  { font-size: 13px; color: #6b7280; margin: 0; }
.header-actions { display: flex; gap: 10px; }

/* ── Buttons ── */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border: none;
  border-radius: 7px;
  background: #1677ff;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background .2s;
}
.btn-primary:hover { background: #1256cc; }

.btn-default {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  background: #fff;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: border-color .2s;
}
.btn-default:hover { border-color: #1677ff; color: #1677ff; }
.btn-default.small { padding: 5px 12px; font-size: 13px; border-radius: 5px; }

.btn-danger {
  padding: 8px 28px;
  border: none;
  border-radius: 6px;
  background: #ef4444;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.btn-confirm { padding: 8px 28px; border: none; border-radius: 6px; color: #fff; font-size: 14px; font-weight: 500; cursor: pointer; }
.btn-warn    { background: #f59e0b; }
.btn-success { background: #22c55e; }

/* ── Card ── */
.card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  margin-bottom: 20px;
}

/* ── Search Bar ── */
.search-bar { padding: 20px 24px; }
.search-fields {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
}
.field-group { display: flex; flex-direction: column; gap: 6px; flex: 1 1 180px; }
.field-group label { font-size: 13px; font-weight: 500; color: #374151; }
.field-group input,
.field-group select {
  padding: 0 12px;
  height: 36px;
  line-height: 36px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  color: #1a1a1a;
  outline: none;
  background: #fff;
  width: 100%;
  max-width: 220px;
  transition: border-color .2s;
  box-sizing: border-box;
  appearance: none;
  -webkit-appearance: none;
}
/* select 保留系统下拉箭头用背景图模拟 */
.field-group select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
  cursor: pointer;
}
.field-group input::placeholder { color: #9ca3af; }
/* select 未选中时（值为默认占位文字）置灰 */
.field-group select.placeholder-gray { color: #9ca3af; }
.field-group select option { color: #1a1a1a; }
.field-group input:focus,
.field-group select:focus { border-color: #1677ff; }
.search-btns { display: flex; gap: 10px; align-items: flex-end; flex-shrink: 0; }

.btn-reset { background: #f0f0f0; color: #374151; }
.btn-reset:hover { background: #e0e0e0; }

/* ── Table ── */
.table-card { overflow: hidden; }
.table-header {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.table-title { display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 15px; }
.title-bar { width: 4px; height: 18px; background: #1677ff; border-radius: 2px; }

table { width: 100%; border-collapse: collapse; }
thead tr { background: #fafafa; }
th {
  padding: 12px 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}
td { padding: 14px 16px; font-size: 14px; border-bottom: 1px solid #f5f5f5; }
tbody tr { transition: background .15s; }
tbody tr:hover { background: #fafcff; }
tbody tr:last-child td { border-bottom: none; }

.seq { color: #6b7280; }
.date { font-size: 13px; color: #6b7280; white-space: nowrap; }

.user-info { display: flex; align-items: center; gap: 10px; }
.avatar {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 12px; font-weight: 600;
  flex-shrink: 0; position: relative;
}
.avatar .dot {
  position: absolute; bottom: 1px; right: 1px;
  width: 8px; height: 8px; border-radius: 50%;
  border: 1.5px solid #fff;
}
.dot-active   { background: #22c55e; }
.dot-disabled { background: #9ca3af; }
.user-name  { font-weight: 600; font-size: 14px; }
.user-email { font-size: 12px; color: #9ca3af; }

.role-tag {
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}
.role-tag.admin  { background: #1677ff; color: #fff; }
.role-tag.normal { border: 1px solid #d1d5db; color: #374151; }

.status-tag { font-size: 13px; }
.status-tag.active   { color: #374151; }
.status-tag.disabled { color: #9ca3af; }

/* ── Table Actions ── */
.actions { white-space: nowrap; }
.action-btn {
  background: none;
  border: none;
  font-size: 13px;
  cursor: pointer;
  padding: 0 6px;
  transition: opacity .2s;
}
.action-btn:hover { opacity: .7; }
.action-btn.edit   { color: #1677ff; }
.action-btn.ban    { color: #f59e0b; }
.action-btn.enable { color: #22c55e; }
.action-btn.delete { color: #ef4444; }
.divider { color: #e5e7eb; padding: 0 2px; }
/* 自己行的禁用/删除：置灰不可点 */
.action-disabled {
  font-size: 13px;
  padding: 0 6px;
  color: #d1d5db;
  cursor: not-allowed;
  user-select: none;
}

/* ── Pagination ── */
.pagination {
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f0f0f0;
}
.page-info { font-size: 13px; color: #6b7280; }
.page-btns { display: flex; gap: 6px; }
.page-btn {
  padding: 5px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 5px;
  background: #fff;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  transition: all .2s;
}
.page-btn:hover { border-color: #1677ff; color: #1677ff; }
.page-btn.active { background: #1677ff; color: #fff; border-color: #1677ff; font-weight: 600; }

/* ── Stats ── */
.stats-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
.stat-card {
  border-radius: 10px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-card.blue  { background: #e8f4fd; }
.stat-card.green { background: #f0fdf4; }
.stat-card.gray  { background: #fafafa; }
.stat-icon { font-size: 22px; }
.stat-label { font-size: 12px; color: #6b7280; margin-bottom: 4px; }
.stat-value { font-size: 24px; font-weight: 700; }
.blue-text  { color: #1677ff; }
.green-text { color: #22c55e; }
.gray-text  { color: #6b7280; }

/* ── Modal ── */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  border-radius: 10px;
  width: 520px;
  max-width: 95vw;
  box-shadow: 0 8px 40px rgba(0,0,0,.18);
  overflow: hidden;
}
.confirm-modal { width: 400px; }

.modal-header {
  padding: 18px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  font-size: 16px;
  color: #1a1a1a;
}
.modal-close {
  border: none;
  background: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
  line-height: 1;
  padding: 0 4px;
  transition: color .2s;
}
.modal-close:hover { color: #1a1a1a; }

.modal-body { padding: 24px; }
.modal-body.center { text-align: center; }

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.modal-footer.center { justify-content: center; }

/* ── Form ── */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 20px; }
.form-field { margin-bottom: 18px; }
.form-field label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}
.required { color: #ef4444; margin-right: 2px; }
.form-field input,
.form-field select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  color: #1a1a1a;
  outline: none;
  background: #fff;
  box-sizing: border-box;
  transition: border-color .2s;
}
.form-field input::placeholder { color: #9ca3af; }
.form-field input:focus,
.form-field select:focus { border-color: #1677ff; }

/* ── Confirm Modal ── */
.confirm-icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: 0 auto 16px;
}
.red-bg    { background: #fff1f0; }
.yellow-bg { background: #fffbeb; }
.green-bg  { background: #f0fdf4; }

.confirm-title {
  font-size: 15px;
  color: #1a1a1a;
  margin: 0 0 8px;
  font-weight: 500;
}
.confirm-desc { font-size: 13px; color: #6b7280; margin: 0 0 24px; }

.red-text    { color: #ef4444; }
.yellow-text { color: #f59e0b; }
.green-text  { color: #22c55e; }

/* ── Modal Transition ── */
.modal-enter-active, .modal-leave-active { transition: all .2s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal, .modal-leave-to .modal { transform: scale(.95) translateY(-8px); }
</style>