<template>
  <div class="page">
    <div class="card">
      <h1>Google 登录</h1>
      <p class="sub">
        该功能需要后端接入 Google OAuth（安全地保存 client_secret、处理回调并签发你系统的登录态）。
        当前仅提供占位页面，方便你先把前端流程跑通。
      </p>

      <div class="actions">
        <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
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
</style>

