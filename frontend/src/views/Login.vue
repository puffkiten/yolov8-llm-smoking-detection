<template>
  <div class="login-page">

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

    <!-- ══════════ RIGHT PANEL ══════════ -->
    <div class="right-panel">

      <!-- 大卡片：圆角渐变 + 粒子 + AI状态条 -->
      <div class="vis-card">
        <canvas ref="particleCanvas" class="p-canvas"></canvas>
        <!-- AI Status bar — 在卡片内底部 -->
        <div class="ai-bar">
          <div class="ai-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <div class="ai-info">
            <p class="ai-title">实时 AI 解析中</p>
            <p class="ai-sub">YOLOv8 模型正在全速运行</p>
          </div>
          <span class="pulse-dot"></span>
        </div>
      </div>

      <!-- Feature cards — 卡片外面，背景透明 -->
      <div class="feat-row">
        <div class="feat-card">
          <div class="feat-ico blue">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <div>
            <p class="feat-title">极高准确率</p>
            <p class="feat-desc">依托 YOLOv8 视觉算法，针对吸烟手势及烟雾进行多维度深度识别。</p>
          </div>
        </div>
        <div class="feat-card">
          <div class="feat-ico purple">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
          </div>
          <div>
            <p class="feat-title">毫秒级响应</p>
            <p class="feat-desc">毫秒级延迟处理流数据，确保违规行为第一时间被系统发现并记录。</p>
          </div>
        </div>
      </div>

      <!-- Quote — 卡片外面 -->
      <p class="quote">"Aero 致力于构建更加安全、健康的办公空间，让智能监测无处不在。"</p>

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

  const resize = () => { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight }
  resize()
  window.addEventListener('resize', resize)

  const N = 80, DIST = 115
  const mouse = { x: -999, y: -999 }
  const onMove = e => { const r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top }
  const onOut  = () => { mouse.x = -999; mouse.y = -999 }
  canvas.addEventListener('mousemove', onMove)
  canvas.addEventListener('mouseleave', onOut)

  const colors = [[160,210,255],[180,160,255],[100,230,240],[200,170,255],[80,200,255]]

  class P {
    constructor() { this.reset() }
    reset() {
      this.x  = Math.random() * canvas.width
      this.y  = Math.random() * canvas.height
      this.vx = (Math.random() - .5) * .55
      this.vy = (Math.random() - .5) * .55
      this.r  = Math.random() * 2 + 1.1
      this.c  = colors[Math.floor(Math.random() * colors.length)]
      this.a  = Math.random() * .45 + .3
    }
    step() {
      const dx = this.x - mouse.x, dy = this.y - mouse.y
      const d  = Math.sqrt(dx*dx + dy*dy)
      if (d < 85) { this.vx += (dx/d)*.45; this.vy += (dy/d)*.45 }
      const spd = Math.sqrt(this.vx*this.vx + this.vy*this.vy)
      if (spd > 2) { this.vx = this.vx/spd*2; this.vy = this.vy/spd*2 }
      this.vx *= .99; this.vy *= .99
      this.x  += this.vx; this.y += this.vy
      if (this.x < 0) this.x = canvas.width
      if (this.x > canvas.width) this.x = 0
      if (this.y < 0) this.y = canvas.height
      if (this.y > canvas.height) this.y = 0
    }
    draw() {
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.r, 0, Math.PI*2)
      ctx.fillStyle = `rgba(${this.c},${this.a})`
      ctx.fill()
    }
  }

  const pts = Array.from({length: N}, () => new P())

  const loop = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (let i = 0; i < pts.length; i++) {
      for (let j = i+1; j < pts.length; j++) {
        const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y
        const d  = Math.sqrt(dx*dx + dy*dy)
        if (d < DIST) {
          ctx.beginPath()
          ctx.moveTo(pts[i].x, pts[i].y)
          ctx.lineTo(pts[j].x, pts[j].y)
          ctx.strokeStyle = `rgba(180,210,255,${(1 - d/DIST)*.28})`
          ctx.lineWidth = .7
          ctx.stroke()
        }
      }
    }
    pts.forEach(p => { p.step(); p.draw() })
    raf = requestAnimationFrame(loop)
  }
  loop()

  return () => {
    window.removeEventListener('resize', resize)
    canvas.removeEventListener('mousemove', onMove)
    canvas.removeEventListener('mouseleave', onOut)
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
  background: #edf5ee;
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
  background: #edf5ee;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  /* Logo 与 Welcome 之间留足距离 */
  margin-bottom: 56px;
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
  background: #fff;
  border: 1.5px solid #dde5ee;
  border-radius: 10px;
  font-size: 14px; color: #1a2332;
  font-family: inherit; outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.f-input::placeholder { color: #b8c4d0; }
.f-input:focus { border-color: #3b9eff; box-shadow: 0 0 0 3px rgba(59,158,255,.12); }

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
  flex-direction: column;          /* 纵向排列：大卡片 → feat行 → quote */
  justify-content: center;
  gap: 20px;
  padding: 40px 44px 40px 16px;
}

/* 大卡片 — 圆角渐变，内含粒子画布 + AI状态条 */
.vis-card {
  position: relative;
  width: 100%;
  /* 高度自适应，但给个最小高度 */
  height: 340px;
  border-radius: 22px;
  overflow: hidden;
  /* 蓝→紫→粉渐变，还原原图色彩 */
  background: linear-gradient(135deg,
    #7ab8e8 0%,
    #9a88d0 25%,
    #c080c0 50%,
    #d090b0 70%,
    #8ab4d8 100%
  );
  box-shadow: 0 20px 56px rgba(80,100,200,.20);
  flex-shrink: 0;
}

.p-canvas {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  cursor: crosshair;
}

/* AI Status bar */
.ai-bar {
  position: absolute;
  bottom: 16px; left: 16px; right: 16px;
  background: rgba(255,255,255,.18);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,.28);
  border-radius: 14px;
  padding: 12px 16px;
  display: flex; align-items: center; gap: 13px;
}

.ai-icon {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, #4a9eff, #7c5ce8);
  border-radius: 11px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(74,158,255,.38);
}

.ai-info { flex: 1; }
.ai-title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 3px; text-shadow: 0 1px 6px rgba(0,0,0,.2); }
.ai-sub   { font-size: 12px; color: rgba(255,255,255,.78); }

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

/* Feature row — 在大卡片外面，白色半透明卡片 */
.feat-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.feat-card {
  background: rgba(255,255,255,.62);
  border: 1px solid rgba(220,228,240,.7);
  border-radius: 14px;
  padding: 16px 15px;
  display: flex; gap: 12px; align-items: flex-start;
  backdrop-filter: blur(8px);
}

.feat-ico {
  width: 34px; height: 34px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.feat-ico.blue   { background: rgba(59,158,255,.13); color: #3b9eff; }
.feat-ico.purple { background: rgba(124,92,232,.11); color: #7c5ce8; }

.feat-title { font-size: 13px; font-weight: 700; color: #1a2332; margin-bottom: 5px; }
.feat-desc  { font-size: 11.5px; color: #6b7a90; line-height: 1.65; }

/* Quote — 在最底部，背景透明 */
.quote {
  text-align: center;
  font-size: 13px; color: #7a8896;
  font-style: italic; line-height: 1.6;
}

/* ── RESPONSIVE ── */
@media (max-width: 960px) {
  .right-panel { display: none; }
  .left-panel  { flex: 1; max-width: 100%; min-width: 0; padding: 36px 32px; }
}
</style>