<template>
  <div class="page">
    <div class="card">
      <div class="header">
        <h1>创建账号</h1>
        <p>注册功能前端已就绪，后续接入后端即可完成真实注册。</p>
      </div>

      <div class="form">
        <label class="lbl">邮箱</label>
        <input v-model.trim="form.email" class="inp" type="email" placeholder="请输入邮箱" />

        <label class="lbl">用户名</label>
        <input v-model.trim="form.name" class="inp" type="text" placeholder="请输入用户名" />

        <label class="lbl">密码</label>
        <input v-model="form.password" class="inp" type="password" placeholder="请输入密码（至少 6 位）" />

        <label class="lbl">确认密码</label>
        <input v-model="form.password2" class="inp" type="password" placeholder="请再次输入密码" />

        <div class="actions">
          <BaseButton type="default" @click="router.push('/login')">返回登录</BaseButton>
          <BaseButton type="primary" @click="handleRegister">立即注册</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()

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
}

.card {
  width: 520px;
  max-width: 92vw;
  background: #fff;
  border: 1px solid #edf0f5;
  border-radius: 14px;
  padding: 24px;
  box-shadow: var(--shadow-card);
}

.header h1 {
  margin: 0 0 6px 0;
  font-size: 22px;
}

.header p {
  margin: 0 0 18px 0;
  color: #6b7280;
  font-size: 13px;
}

.form {
  display: grid;
  gap: 10px;
}

.lbl {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.inp {
  height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
  font-family: inherit;
}

.inp:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 158, 255, .12);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}
</style>

