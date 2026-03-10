<template>
  <div class="login-page">

    <!-- 全屏动态背景：彩色圆润粒子 -->
    <div class="bg-visual" aria-hidden="true">
      <canvas ref="particleCanvas" class="bg-canvas"></canvas>
    </div>

    <!-- 右侧文案（作为背景的一部分，不占布局，不挡交互） -->
    <div class="bg-copy" aria-hidden="true">
      <div class="bg-badge">YOLOv8</div>
      <h2 class="bg-title">Real‑time vision inference</h2>
      <p class="bg-sub">
        Streaming • Multi‑camera • Low latency
      </p>
      <div class="bg-tags">
        <span class="bg-tag">Detection</span>
        <span class="bg-tag">Tracking</span>
        <span class="bg-tag">Deploy</span>
      </div>
    </div>

    <!-- ══════════ LEFT PANEL ══════════ -->
    <div class="left-panel">
      <!-- Logo — 顶部居中 -->
      <div class="logo">
        <div class="logo-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
        </div>
        <span class="logo-text">Aero Smart</span>
      </div>

      <!-- Form — 垂直居中 -->
      <div class="form-center">
        <div class="form-header">
          <h1 class="title">Welcome to Aero</h1>
          <p class="subtitle">AI 驱动环境监测，为您打造健康无烟空间</p>
        </div>

        <!-- Email -->
        <div class="field-group">
          <label class="field-label">电子邮箱 / 账号</label>
          <div class="input-wrap">
            <span class="ico-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
            </span>
            <input v-model="form.email" type="email" class="f-input" placeholder="admin@aero.com"/>
          </div>
        </div>

        <!-- Password -->
        <div class="field-group">
          <label class="field-label">密码</label>
          <div class="input-wrap">
            <span class="ico-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </span>
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'" class="f-input" placeholder="请输入登录密码"/>
            <span class="ico-right" @click="showPwd = !showPwd">
              <svg v-if="!showPwd" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- Options -->
        <div class="opt-row">
          <label class="remember">
            <input v-model="form.remember" type="checkbox" class="cb-real"/>
            <span class="cb-box"></span>
            <span class="cb-txt">记住我</span>
          </label>
          <a href="#" class="forgot">忘记密码?</a>
        </div>

        <!-- Login btn -->
        <button class="btn-login" @click="handleLogin" :disabled="isLoading">
          <span>{{ isLoading ? '登录中...' : '立即登录' }}</span>
          <svg v-if="!isLoading" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
          </svg>
        </button>

        <!-- Divider -->
        <div class="divider"><span class="dline"></span><span class="dtxt">或者</span><span class="dline"></span></div>

        <!-- Google -->
        <button class="btn-google" @click="router.push('/auth/google')">
          <svg width="17" height="17" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          使用 Google 账号登录
        </button>

        <p class="reg-tip">还没有账号？<a href="#" class="reg-link" @click.prevent="router.push('/register')">立即注册</a></p>
      </div>

      <!-- Footer -->
      <div class="left-footer">
        <div class="badge">
          <div class="avatars">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a1" class="av" alt=""/>
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a2" class="av" alt=""/>
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a3" class="av" alt=""/>
          </div>
          <span class="badge-txt">已有 1000+ 企业接入系统</span>
        </div>
        <p class="copy">© 2026 Aero Smart Monitoring System. 全球领先的 AI 烟雾监测技术。</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const form = reactive({ email: '', password: '', remember: false })
const showPwd = ref(false)
const isLoading = ref(false)
const particleCanvas = ref(null)
let raf = null, cleanup = null

const router = useRouter()

const handleLogin = () => {
  if (isLoading.value) return
  isLoading.value = true
  setTimeout(() => { isLoading.value = false }, 1500)
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

  // 彩色圆润粒子：更“原型/舒适”，不画连线
  const N = 72
  const mouse = { x: -9999, y: -9999 }
  const onMove = (e) => { mouse.x = e.clientX; mouse.y = e.clientY }
  const onOut  = () => { mouse.x = -9999; mouse.y = -9999 }
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseleave', onOut)

  // 更柔和的彩色系（偏蓝紫青）
  const colors = [
    [59, 158, 255],
    [124, 92, 232],
    [0, 188, 164],
    [245, 166, 35],
    [232, 92, 92],
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
      // 渐变柔光圆点
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
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── PAGE ── */
.login-page {
  display: flex;
  min-height: 100vh;
  /* 让整页背景统一，避免左右割裂 */
  background: radial-gradient(1100px 520px at 18% 18%, rgba(59, 158, 255, .16), transparent 62%),
              radial-gradient(900px 520px at 86% 26%, rgba(124, 92, 232, .12), transparent 62%),
              #edf5ee;
  gap: 28px;
  position: relative;
}

/* 全屏动态背景 */
.bg-visual {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.bg-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* 右侧文案（叠在背景上） */
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
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,.55);
  border: 1px solid rgba(220,228,240,.9);
  color: #1a2332;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .2px;
  margin-bottom: 12px;
}

.bg-title {
  margin: 0 0 10px 0;
  font-size: 40px;
  line-height: 1.05;
  letter-spacing: -1.0px;
  color: #0d1724;
}

.bg-sub {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #5a6475;
  line-height: 1.7;
}

.bg-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.bg-tag {
  display: inline-flex;
  padding: 7px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,.55);
  border: 1px solid rgba(220,228,240,.9);
  color: #2d3a4a;
  font-size: 12px;
  font-weight: 700;
}

/* ══════════ LEFT PANEL ══════════ */
.left-panel {
  /* 固定宽度，约占屏幕的 42% */
  flex: 0 0 42%;
  min-width: 440px;
  max-width: 560px;
  display: flex;
  flex-direction: column;
  /* 水平内边距：左右相等，让内容真正居中 */
  padding: 44px 60px 40px 60px;
  background: transparent;
  position: relative;
  z-index: 2;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  /* Logo 与 Welcome 之间留足距离 */
  margin-bottom: 26px;
}

.logo-icon {
  width: 36px; height: 36px;
  background: #3b9eff;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.logo-text { font-size: 17px; font-weight: 700; color: #111b27; letter-spacing: -.3px; }

/* Form vertically centered */
.form-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.55);
  border-radius: 18px;
  padding: 28px 28px 24px 28px;
  box-shadow: 0 18px 52px rgba(17, 27, 39, 0.10);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  max-width: 440px;
  width: 100%;
  margin: 0 auto;
}

.form-header { margin-bottom: 30px; }

.title {
  font-size: 30px; font-weight: 700;
  color: #0d1724; letter-spacing: -.8px;
  margin-bottom: 8px; line-height: 1.2;
}

.subtitle { font-size: 14px; color: #6b7a90; }

/* Fields */
.field-group { margin-bottom: 17px; }

.field-label {
  display: block;
  font-size: 13px; font-weight: 500;
  color: #2d3a4a; margin-bottom: 7px;
}

.input-wrap { position: relative; display: flex; align-items: center; }

.ico-left {
  position: absolute; left: 14px;
  color: #aab4c0;
  display: flex; align-items: center;
  pointer-events: none;
}

.ico-right {
  position: absolute; right: 14px;
  color: #aab4c0; cursor: pointer;
  display: flex; align-items: center;
  transition: color .2s;
}
.ico-right:hover { color: #4a90d9; }

.f-input {
  width: 100%; height: 46px;
  padding: 0 40px;
  background: rgba(255, 255, 255, 0.75);
  border: 1.5px solid rgba(221, 229, 238, 0.95);
  border-radius: 10px;
  font-size: 14px; color: #1a2332;
  font-family: inherit; outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.f-input::placeholder { color: #b8c4d0; }
.f-input:focus { border-color: #3b9eff; background: rgba(255, 255, 255, 0.92); box-shadow: 0 0 0 4px rgba(59,158,255,.12); }

/* Options row */
.opt-row {
  display: flex; align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.remember { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.cb-real { display: none; }
.cb-box {
  width: 16px; height: 16px;
  border: 1.5px solid #c5cfd9;
  border-radius: 4px; background: white;
  display: inline-flex; align-items: center; justify-content: center;
  transition: all .18s; flex-shrink: 0;
}
.cb-real:checked + .cb-box { background: #111b27; border-color: #111b27; }
.cb-real:checked + .cb-box::after {
  content: '';
  width: 8px; height: 5px;
  border-left: 2px solid white; border-bottom: 2px solid white;
  transform: rotate(-45deg) translateY(-1px); display: block;
}
.cb-txt { font-size: 13px; color: #4a5568; }

.forgot { font-size: 13px; color: #3b9eff; font-weight: 500; text-decoration: none; }
.forgot:hover { opacity: .75; }

/* Login button */
.btn-login {
  width: 100%; height: 48px;
  background: #111b27; color: white; border: none;
  border-radius: 10px; font-size: 15px; font-weight: 600;
  font-family: inherit; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  transition: all .22s; letter-spacing: .4px; margin-bottom: 18px;
}
.btn-login:hover:not(:disabled) {
  background: #1e2f44;
  box-shadow: 0 8px 24px rgba(17,27,39,.28);
  transform: translateY(-1px);
}
.btn-login:disabled { opacity: .65; cursor: not-allowed; }

/* Divider */
.divider { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.dline   { flex: 1; height: 1px; background: #dde5ee; }
.dtxt    { font-size: 13px; color: #9aa5b4; }

/* Google */
.btn-google {
  width: 100%; height: 46px;
  background: white; border: 1.5px solid #dde5ee;
  border-radius: 10px; font-size: 14px; font-weight: 500;
  font-family: inherit; color: #2d3a4a; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 10px;
  transition: all .2s; margin-bottom: 18px;
}
.btn-google:hover { border-color: #bdc8d4; box-shadow: 0 2px 8px rgba(0,0,0,.07); }

.reg-tip  { text-align: center; font-size: 13px; color: #6b7a90; }
.reg-link { color: #3b9eff; font-weight: 600; text-decoration: none; }
.reg-link:hover { opacity: .75; }

/* Footer */
.left-footer { margin-top: 40px; }

.badge {
  display: inline-flex; align-items: center; gap: 10px;
  background: rgba(59,158,255,.07);
  border: 1px solid rgba(59,158,255,.16);
  border-radius: 50px; padding: 5px 14px 5px 7px;
  margin-bottom: 12px;
}

.avatars { display: flex; align-items: center; }
.av {
  width: 25px; height: 25px;
  border-radius: 50%; border: 2px solid white;
  margin-left: -5px; background: #dde8f4; overflow: hidden;
}
.av:first-child { margin-left: 0; }
.badge-txt { font-size: 12px; color: #3b7dc4; font-weight: 500; }
.copy      { font-size: 12px; color: #9eaab7; line-height: 1.5; }


/* ══════════ RIGHT PANEL ══════════ */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px 60px 40px 24px;
  align-items: center;
  position: relative;
  overflow: hidden;
  /* 右侧不做“卡片”，改为干净展示背景 */
  background:
    radial-gradient(900px 520px at 18% 20%, rgba(59, 158, 255, .14), transparent 62%),
    radial-gradient(900px 520px at 86% 26%, rgba(124, 92, 232, .10), transparent 62%);
}

.p-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  cursor: default;
  opacity: 0.8;
}

/* Hero overlay */
.hero-overlay {
  position: absolute;
  inset: 0;
  padding: 34px 36px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  pointer-events: none;
  max-width: 720px;
  width: 100%;
}

.hero-top { display: flex; justify-content: space-between; align-items: flex-start; }

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(220, 228, 240, 0.9);
  color: #1a2332;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.2px;
}

.hero-mid { max-width: 92%; }
.hero-title {
  margin: 0 0 10px 0;
  font-size: 36px;
  line-height: 1.12;
  letter-spacing: -0.8px;
  color: #0d1724;
  text-shadow: none;
}
.hero-sub {
  margin: 0;
  font-size: 14px;
  line-height: 1.7;
  color: #5a6475;
  max-width: 520px;
}

.hero-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.chips {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.chip {
  padding: 7px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(220, 228, 240, 0.9);
  color: #2d3a4a;
  font-size: 12px;
  font-weight: 600;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(220, 228, 240, 0.9);
}
.status-text { color: #1a2332; font-size: 12px; font-weight: 800; }

/* 绿色呼吸点 */
.pulse-dot {
  display: block; width: 10px; height: 10px;
  border-radius: 50%; background: #4eff91;
  animation: pulse 1.8s ease-out infinite;
  flex-shrink: 0;
}
@keyframes pulse {
  0%   { box-shadow: 0 0 0 0   rgba(78,255,145,.7); }
  70%  { box-shadow: 0 0 0 9px rgba(78,255,145,0);  }
  100% { box-shadow: 0 0 0 0   rgba(78,255,145,0);  }
}

/* 删除旧的 feature/quote 样式（改为统一 hero） */

/* ── RESPONSIVE ── */
@media (max-width: 960px) {
  .right-panel { display: none; }
  .left-panel  { flex: 1; max-width: 100%; min-width: 0; padding: 36px 32px; }
}
</style>