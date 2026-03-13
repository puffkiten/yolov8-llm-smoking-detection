<template>
  <div class="page">
    <div class="card">
      <div class="header">
        <h1 class="title">重置密码</h1>
        <p class="subtitle">请设置一个新密码（至少 6 位）。</p>
      </div>

      <div class="field-group">
        <label class="field-label">新密码</label>
        <div class="input-wrap">
          <input v-model="pwd1" class="f-input" :type="showPwd ? 'text' : 'password'" placeholder="请输入新密码" />
          <span class="ico-right" role="button" tabindex="0" @click="showPwd = !showPwd">
            <svg v-if="showPwd" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </span>
        </div>
      </div>

      <div class="field-group">
        <label class="field-label">确认新密码</label>
        <div class="input-wrap">
          <input v-model="pwd2" class="f-input" :type="showPwd2 ? 'text' : 'password'" placeholder="再次输入新密码" />
          <span class="ico-right" role="button" tabindex="0" @click="showPwd2 = !showPwd2">
            <svg v-if="showPwd2" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </span>
        </div>
      </div>

      <p v-if="errorText" class="form-error" role="alert">{{ errorText }}</p>

      <div class="actions">
        <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
        <BaseButton type="primary" :disabled="isSubmitting" @click="handleSubmit">
          {{ isSubmitting ? '提交中...' : '确认重置' }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()

const uid = computed(() => (route.query.uid || '').toString())
const token = computed(() => (route.query.token || '').toString())

const pwd1 = ref('')
const pwd2 = ref('')
const showPwd = ref(false)
const showPwd2 = ref(false)
const isSubmitting = ref(false)
const errorText = ref('')

watch([pwd1, pwd2], () => {
  if (errorText.value) errorText.value = ''
})

const handleSubmit = async () => {
  errorText.value = ''
  if (!uid.value || !token.value) {
    errorText.value = '重置链接缺少参数，请从“忘记密码”页面重新生成链接'
    return
  }
  if (!pwd1.value || pwd1.value.length < 6) {
    errorText.value = '密码至少 6 位'
    return
  }
  if (pwd1.value !== pwd2.value) {
    errorText.value = '两次输入的密码不一致'
    return
  }

  isSubmitting.value = true
  try {
    await axios.post('http://127.0.0.1:8000/api/auth/password-reset/confirm', {
      uid: uid.value,
      token: token.value,
      new_password: pwd1.value
    })
    ElMessage.success('密码已重置，请使用新密码登录')
    router.push('/login')
  } catch (e) {
    errorText.value = e?.response?.data?.detail || '重置失败，请检查链接是否过期'
  } finally {
    isSubmitting.value = false
  }
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
.header { text-align: center; margin-bottom: 18px; }
.title { margin: 0 0 6px 0; font-size: 22px; font-weight: 800; color: #0d1724; letter-spacing: -0.6px; }
.subtitle { margin: 0; color: #6b7a90; font-size: 13.5px; line-height: 1.6; }
.field-group { margin-bottom: 14px; }
.field-label { display: block; font-size: 13px; font-weight: 600; color: #2d3a4a; margin-bottom: 7px; }
.input-wrap { position: relative; display: flex; align-items: center; }
.f-input {
  flex: 1;
  height: 46px;
  padding: 0 44px 0 14px;
  background: rgba(255, 255, 255, 0.75);
  border: 1.5px solid rgba(221, 229, 238, 0.95);
  border-radius: 10px;
  font-size: 14px;
  color: #1a2332;
  font-family: inherit;
  outline: none;
}
.f-input:focus { border-color: #3b9eff; background: rgba(255, 255, 255, 0.92); box-shadow: 0 0 0 4px rgba(59,158,255,.12); }
.ico-right {
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
.ico-right:hover { background: rgba(17, 27, 39, 0.06); color: #4a90d9; }
.form-error { margin: -6px 0 14px 0; color: #d92d20; font-size: 13px; line-height: 1.5; font-weight: 600; }
.actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 8px; }
</style>
