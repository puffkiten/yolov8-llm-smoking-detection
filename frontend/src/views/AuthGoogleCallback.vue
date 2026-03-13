<template>
  <div class="page">
    <div class="card">
      <h1>Google 登录回调</h1>
      <p class="sub">{{ statusText }}</p>
      <div class="actions">
        <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()

const access = computed(() => (route.query.access || '').toString())
const refresh = computed(() => (route.query.refresh || '').toString())
const statusText = ref('处理中...')

onMounted(() => {
  if (!access.value || !refresh.value) {
    statusText.value = '未拿到登录信息，请重试'
    return
  }
  localStorage.setItem('access_token', access.value)
  localStorage.setItem('refresh_token', refresh.value)
  ElMessage.success('登录成功')
  router.replace('/dashboard')
})
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
h1 { margin: 0 0 8px 0; font-size: 22px; }
.sub { margin: 0; color: #6b7280; font-size: 13.5px; line-height: 1.6; }
.actions { margin-top: 18px; display: flex; justify-content: flex-end; }
</style>

