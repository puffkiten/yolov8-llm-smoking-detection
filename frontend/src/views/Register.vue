<template>
  <div class="page">
    <div class="card">
      <div class="logo">
        <div class="logo-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
        </div>
        <span class="logo-text">Aero Smart</span>
      </div>

      <div class="header">
        <h1 class="title">Create your account</h1>
        <p class="subtitle">注册功能前端已就绪，后续接入后端即可完成真实注册。</p>
      </div>

      <div class="field-group">
        <label class="field-label">电子邮箱</label>
        <div class="input-wrap">
          <span class="ico-left">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="2" y="4" width="20" height="16" rx="2"/>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
            </svg>
          </span>
          <input v-model.trim="form.email" class="f-input" type="email" placeholder="name@company.com" />
        </div>
      </div>

      <div class="field-group">
        <label class="field-label">用户名</label>
        <div class="input-wrap">
          <span class="ico-left">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </span>
          <input v-model.trim="form.name" class="f-input" type="text" placeholder="请输入用户名" />
        </div>
      </div>

      <div class="field-group">
        <label class="field-label">密码</label>
        <div class="input-wrap">
          <span class="ico-left">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
          </span>
          <input v-model="form.password" class="f-input" :type="showPwd ? 'text' : 'password'" placeholder="至少 6 位密码" />
          <button class="ico-btn" type="button" @click="showPwd = !showPwd" :aria-label="showPwd ? '隐藏密码' : '显示密码'">
            <svg v-if="!showPwd" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="field-group">
        <label class="field-label">确认密码</label>
        <div class="input-wrap">
          <span class="ico-left">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </span>
          <input v-model="form.password2" class="f-input" :type="showPwd2 ? 'text' : 'password'" placeholder="再次输入密码" />
          <button class="ico-btn" type="button" @click="showPwd2 = !showPwd2" :aria-label="showPwd2 ? '隐藏密码' : '显示密码'">
            <svg v-if="!showPwd2" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="actions">
        <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
        <BaseButton type="primary" @click="handleRegister">立即注册</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const showPwd = ref(false)
const showPwd2 = ref(false)

const form = reactive({
  email: '',
  name: '',
  password: '',
  password2: '',
})

const handleRegister = () => {
  if (!form.email) return ElMessage.warning('请输入邮箱')
  if (!form.name) return ElMessage.warning('请输入用户名')
  if (!form.password || form.password.length < 6) return ElMessage.warning('密码至少 6 位')
  if (form.password !== form.password2) return ElMessage.warning('两次输入的密码不一致')

  ElMessage.success('注册信息已校验通过（等待后端接入）')
  router.push('/login')
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
  background: radial-gradient(900px 420px at 20% 20%, rgba(59, 158, 255, .22), transparent 60%),
              radial-gradient(700px 380px at 85% 30%, rgba(124, 92, 232, .18), transparent 60%),
              #edf5ee;
}

.card {
  width: 520px;
  max-width: 92vw;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(255, 255, 255, 0.55);
  border-radius: 18px;
  padding: 26px;
  box-shadow: 0 20px 60px rgba(17, 27, 39, 0.12);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 14px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: #3b9eff;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 10px 28px rgba(59, 158, 255, .25);
}

.logo-text {
  font-size: 17px;
  font-weight: 800;
  color: #111b27;
  letter-spacing: -0.3px;
}

.header {
  text-align: center;
  margin-bottom: 18px;
}

.title {
  margin: 0 0 6px 0;
  font-size: 22px;
  font-weight: 800;
  color: #0d1724;
  letter-spacing: -0.6px;
}

.subtitle {
  margin: 0;
  color: #6b7a90;
  font-size: 13.5px;
}

.field-group {
  margin-bottom: 14px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #2d3a4a;
  margin-bottom: 7px;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.ico-left {
  position: absolute;
  left: 14px;
  color: #aab4c0;
  display: flex;
  align-items: center;
  pointer-events: none;
}

.ico-btn {
  position: absolute;
  right: 10px;
  height: 32px;
  width: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #aab4c0;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.2s, color 0.2s;
}

.ico-btn:hover {
  background: rgba(17, 27, 39, 0.06);
  color: #4a90d9;
}

.f-input {
  width: 100%;
  height: 46px;
  padding: 0 46px 0 40px;
  background: rgba(255, 255, 255, 0.75);
  border: 1.5px solid rgba(221, 229, 238, 0.95);
  border-radius: 12px;
  font-size: 14px;
  color: #1a2332;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

.f-input::placeholder {
  color: #b8c4d0;
}

.f-input:focus {
  border-color: #3b9eff;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 0 0 4px rgba(59, 158, 255, 0.12);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}
</style>

