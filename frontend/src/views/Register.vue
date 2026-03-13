<template>
  <div class="auth-page">
    <div class="bg-visual" aria-hidden="true">
      <canvas ref="particleCanvas" class="bg-canvas"></canvas>
    </div>

    <div class="bg-copy" aria-hidden="true">
      <div class="bg-badge">YOLOv8</div>
      <h2 class="bg-title">Real‑time vision inference</h2>
      <p class="bg-sub">Streaming • Multi‑camera • Low latency</p>
      <div class="bg-tags">
        <span class="bg-tag">Detection</span>
        <span class="bg-tag">Tracking</span>
        <span class="bg-tag">Deploy</span>
      </div>
    </div>

    <div class="center-wrap">
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
            <svg v-if="showPwd" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
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
            <svg v-if="showPwd2" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
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
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const showPwd = ref(false)
const showPwd2 = ref(false)
const particleCanvas = ref(null)
let raf = null, cleanup = null

const form = reactive({
  email: '',
  name: '',
  password: '',
  password2: '',
})

const handleRegister = async () => {
  if (!form.email) return ElMessage.warning('请输入邮箱')
  if (!form.name) return ElMessage.warning('请输入用户名')
  if (!form.password || form.password.length < 6) return ElMessage.warning('密码至少 6 位')
  if (form.password !== form.password2) return ElMessage.warning('两次输入的密码不一致')

  try {
    await axios.post('http://127.0.0.1:8000/api/auth/register', {
      email: form.email,
      username: form.name,
      password: form.password,
    })
    ElMessage.success('注册成功，请使用新账号登录')
    router.push('/login')
  } catch (e) {
    const msg = e?.response?.data?.detail || '注册失败，请稍后再试'
    ElMessage.error(msg)
  }
}

function initParticles() {
  const canvas = particleCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  resize()
  window.addEventListener('resize', resize)

  const N = 72
  const mouse = { x: -9999, y: -9999 }
  const onMove = (e) => { mouse.x = e.clientX; mouse.y = e.clientY }
  const onOut  = () => { mouse.x = -9999; mouse.y = -9999 }
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseleave', onOut)

  const colors = [
    [59, 158, 255], [124, 92, 232], [0, 188, 164], [245, 166, 35], [232, 92, 92],
  ]

  class P {
    constructor() { this.reset() }
    reset() {
      this.x  = Math.random() * canvas.width
      this.y  = Math.random() * canvas.height
      this.vx = (Math.random() - .5) * 0.35
      this.vy = (Math.random() - .5) * 0.35
      this.r  = Math.random() * 5.5 + 3.0
      this.c  = colors[Math.floor(Math.random() * colors.length)]
      this.a  = Math.random() * 0.18 + 0.08
    }
    step() {
      const dx = this.x - mouse.x, dy = this.y - mouse.y
      const d  = Math.sqrt(dx*dx + dy*dy)
      if (d < 120) { this.vx += (dx/d)*0.20; this.vy += (dy/d)*0.20 }
      const spd = Math.sqrt(this.vx*this.vx + this.vy*this.vy)
      if (spd > 1.2) { this.vx = this.vx/spd*1.2; this.vy = this.vy/spd*1.2 }
      this.vx *= .99; this.vy *= .99
      this.x  += this.vx; this.y += this.vy
      if (this.x < 0) this.x = canvas.width
      if (this.x > canvas.width) this.x = 0
      if (this.y < 0) this.y = canvas.height
      if (this.y > canvas.height) this.y = 0
    }
    draw() {
      const g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.r * 3.2)
      g.addColorStop(0, `rgba(${this.c[0]},${this.c[1]},${this.c[2]},${this.a})`)
      g.addColorStop(0.35, `rgba(${this.c[0]},${this.c[1]},${this.c[2]},${this.a * 0.35})`)
      g.addColorStop(1, `rgba(${this.c[0]},${this.c[1]},${this.c[2]},0)`)
      ctx.fillStyle = g
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.r * 3.2, 0, Math.PI * 2)
      ctx.fill()
    }
  }

  const pts = Array.from({length: N}, () => new P())

  const loop = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.save()
    ctx.globalCompositeOperation = 'lighter'
    pts.forEach(p => { p.step(); p.draw() })
    ctx.restore()
    raf = requestAnimationFrame(loop)
  }
  loop()

  return () => {
    window.removeEventListener('resize', resize)
    window.removeEventListener('mousemove', onMove)
    window.removeEventListener('mouseleave', onOut)
  }
}

onMounted(() => { cleanup = initParticles() })
onUnmounted(() => { if (raf) cancelAnimationFrame(raf); if (cleanup) cleanup() })
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
  background: radial-gradient(1100px 520px at 18% 18%, rgba(59, 158, 255, .16), transparent 62%),
              radial-gradient(900px 520px at 86% 26%, rgba(124, 92, 232, .12), transparent 62%),
              #edf5ee;
  position: relative;
  overflow: hidden;
}

.bg-visual { position: fixed; inset: 0; z-index: 0; pointer-events: none; }
.bg-canvas { width: 100%; height: 100%; display: block; }

.bg-copy {
  position: absolute;
  right: 56px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  pointer-events: none;
  width: min(520px, 42vw);
}
.bg-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.62);
  border: 1px solid rgba(255,255,255,0.22);
  color: rgba(255,255,255,0.92);
  font-weight: 800;
  letter-spacing: .6px;
  font-size: 12px;
}
.bg-title { margin: 12px 0 6px 0; font-size: clamp(26px, 3.2vw, 40px); font-weight: 900; color: #0d1724; letter-spacing: -1px; }
.bg-sub { margin: 0 0 14px 0; color: rgba(17, 24, 39, .62); font-weight: 700; }
.bg-tags { display: flex; flex-wrap: wrap; gap: 10px; }
.bg-tag { padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.55); border: 1px solid rgba(255,255,255,0.55); color: #0d1724; font-weight: 800; font-size: 12px; }

.center-wrap { position: relative; z-index: 2; width: 520px; max-width: 92vw; }
.card {
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

@media (max-width: 960px) {
  .bg-copy { display: none; }
}
</style>
