<template>
  <div class="page">
    <div class="card">
      <h1>Google 登录</h1>
      <p class="sub">
        点击下面按钮会跳转到后端发起 Google OAuth；授权成功后后端会回跳到本页面体系并写入你系统的 JWT。
      </p>

      <ol class="steps">
        <li>前端跳转：<code>/api/auth/google/login</code></li>
        <li>Google 授权后回调：<code>/api/auth/google/callback</code></li>
        <li>后端签发 JWT 后跳回：<code>/auth/google/callback</code></li>
      </ol>

      <div class="actions-row">
        <BaseButton type="primary" @click="startGoogleLogin">使用 Google 账号登录</BaseButton>
        <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import BaseButton from '@/components/ui/BaseButton.vue'
import { buildApiUrl } from '@/utils/http'

const router = useRouter()

const startGoogleLogin = () => {
  // OAuth 必须走浏览器跳转，不能纯 XHR
  // 后端端点会 302 跳转到 Google
  const url = buildApiUrl('/api/auth/google/login')
  ElMessage.info('正在跳转到 Google 授权页...')
  window.location.href = url
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
}

.card {
  width: 720px;
  max-width: 92vw;
  background: #fff;
  border: 1px solid #edf0f5;
  border-radius: 14px;
  padding: 24px;
  box-shadow: var(--shadow-card);
}

h1 {
  margin: 0 0 8px 0;
  font-size: 22px;
}

.sub {
  margin: 0;
  color: #6b7280;
  font-size: 13.5px;
  line-height: 1.6;
}

.actions {
  margin-top: 18px;
  display: flex;
  justify-content: flex-end;
}

.actions-row {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.steps {
  margin: 12px 0 0 18px;
  color: #334155;
  font-size: 13.5px;
  line-height: 1.7;
}
</style>

