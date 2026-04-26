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
        <h1 class="title">忘记密码</h1>
        <p class="subtitle">请输入注册邮箱，我们将生成一条重置链接（开发环境直接展示链接）。</p>
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
          <input v-model.trim="email" class="f-input" type="email" placeholder="admin@aero.com" />
        </div>
      </div>

      <p v-if="errorText" class="form-error" role="alert">{{ errorText }}</p>

      <div v-if="resetUrl" class="result">
        <div class="result-title">重置链接（开发环境展示）</div>
        <a class="result-link" :href="resetUrl">{{ resetUrl }}</a>
        <div class="result-actions">
          <BaseButton type="primary" @click="goReset">去重置密码</BaseButton>
        </div>
      </div>

      <div class="actions">
        <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
        <BaseButton type="primary" :disabled="isSending" @click="handleSend">
          {{ isSending ? '生成中...' : '生成重置链接' }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const email = ref('')
const errorText = ref('')
const isSending = ref(false)
const resetUrl = ref('')

const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)

watch(email, () => {
  if (errorText.value) errorText.value = ''
})

const handleSend = async () => {
  errorText.value = ''
  resetUrl.value = ''

  if (!email.value) {
    errorText.value = '请输入邮箱'
    return
  }
  if (!isValidEmail(email.value)) {
    errorText.value = '请输入有效的邮箱地址，例如：admin@aero.com'
    return
  }

  isSending.value = true
  try {
    const resp = await axios.post('/api/auth/password-reset/request', {
      email: email.value
    })
    resetUrl.value = resp.data?.reset_url || ''
    if (!resetUrl.value) {
      errorText.value = resp.data?.detail || '生成失败，请稍后重试'
    }
  } catch (e) {
    errorText.value = e?.response?.data?.detail || '请求失败，请检查后端是否启动'
  } finally {
    isSending.value = false
  }
}

const goReset = () => {
  if (!resetUrl.value) return
  // 直接跳转到重置页（同域前端路由）
  const u = new URL(resetUrl.value)
  router.push(`/reset-password?uid=${encodeURIComponent(u.searchParams.get('uid') || '')}&token=${encodeURIComponent(u.searchParams.get('token') || '')}`)
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
  width: 560px;
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

.header { text-align: center; margin-bottom: 18px; }
.title { margin: 0 0 6px 0; font-size: 22px; font-weight: 800; color: #0d1724; letter-spacing: -0.6px; }
.subtitle { margin: 0; color: #6b7a90; font-size: 13.5px; line-height: 1.6; }

.field-group { margin-bottom: 14px; }
.field-label { display: block; font-size: 13px; font-weight: 600; color: #2d3a4a; margin-bottom: 7px; }
.input-wrap { position: relative; display: flex; align-items: center; }
.ico-left { position: absolute; left: 14px; color: #aab4c0; display: flex; align-items: center; pointer-events: none; }
.f-input {
  width: 100%; height: 46px;
  padding: 0 14px 0 40px;
  background: rgba(255, 255, 255, 0.75);
  border: 1.5px solid rgba(221, 229, 238, 0.95);
  border-radius: 10px;
  font-size: 14px; color: #1a2332;
  font-family: inherit; outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.f-input:focus { border-color: #3b9eff; background: rgba(255, 255, 255, 0.92); box-shadow: 0 0 0 4px rgba(59,158,255,.12); }

.form-error { margin: -6px 0 14px 0; color: #d92d20; font-size: 13px; line-height: 1.5; font-weight: 600; }

.result {
  margin: 10px 0 14px 0;
  padding: 12px 12px;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(255,255,255,0.6);
}
.result-title { font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.result-link { word-break: break-all; color: #2563eb; font-size: 13px; text-decoration: none; }
.result-link:hover { text-decoration: underline; }
.result-actions { margin-top: 10px; display: flex; justify-content: flex-end; }.actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 8px; }
</style>