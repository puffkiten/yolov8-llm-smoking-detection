<template>
  <div class="login-page">

    <!-- 全屏动态背景：彩色圆润粒子 -->
    <div class="bg-visual" aria-hidden="true">
      <canvas ref="particleCanvas" class="bg-canvas"></canvas>
    </div>

    <!-- ══════════ RIGHT PANEL ══════════ -->
    <div class="right-panel">
      <div class="right-content">
        <h2 class="bg-title">AI驱动的<br/>吸烟检测与<span class="title-highlight">智能预警</span></h2>
        <p class="bg-sub">
          基于先进的计算机视觉与深度学习技术，实时识别吸烟行为，<br/>
          多场景覆盖，助力打造健康无烟环境。
        </p>
        <div class="bg-tags">
          <span class="bg-tag">⚡ 实时检测</span>
          <span class="bg-tag">📹 多路摄像头</span>
          <span class="bg-tag">⏱ 低延迟</span>
          <span class="bg-tag">🔔 智能告警</span>
        </div>
        <div class="metric-row">
          <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-info">
              <div class="metric-label">检测准确率</div>
              <div class="metric-value">96.8<span class="metric-unit">%</span></div>
              <div class="metric-desc">行业领先水平</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">⏱</div>
            <div class="metric-info">
              <div class="metric-label">平均响应</div>
              <div class="metric-value">0.8<span class="metric-unit">s</span></div>
              <div class="metric-desc">毫秒级响应速度</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">📹</div>
            <div class="metric-info">
              <div class="metric-label">支持设备</div>
              <div class="metric-value">32<span class="metric-unit">路</span></div>
              <div class="metric-desc">单系统最大接入</div>
            </div>
          </div>
        </div>
        <div class="bg-footer-row">
          <span class="bg-footnote">✅ 已为 1000+ 企业提供智能安防解决方案</span>
        </div>
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
          <h1 class="title">欢迎回来</h1>
          <p class="subtitle">登录 Aero Smart，开启智能安防新体验</p>
        </div>

        <!-- Email -->
        <div class="field-group">
          <label class="field-label">电子邮箱</label>
          <div class="input-wrap">
            <span class="ico-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
            </span>
            <input v-model="form.email" type="email" class="f-input" placeholder="请输入电子邮箱"/>
          </div>
        </div>

        <!-- Error message (placed under email field for better UX) -->
        <p v-if="errorText" class="form-error" role="alert">{{ errorText }}</p>

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
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'" class="f-input" placeholder="请输入密码"/>
            <span class="ico-right" @click="showPwd = !showPwd">
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

        <!-- Options -->
        <div class="opt-row">
          <label class="remember">
            <input v-model="form.remember" type="checkbox" class="cb-real"/>
            <span class="cb-box"></span>
            <span class="cb-txt">记住我</span>
          </label>
          <a href="#" class="forgot" @click.prevent="router.push('/forgot-password')">忘记密码?</a>
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
        <button class="btn-google" @click="handleGoogleLogin">
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
        <div class="trusted-strip" aria-label="Trusted by leading companies">
          <span class="trusted-strip-label">Trusted by</span>
          <div class="trusted-strip-line" aria-hidden="true"></div>
          <div class="trusted-logos-inline" aria-label="Trusted company logos">
            <img class="trusted-logo-inline starbucks-inline" src="/logos/starbucks.svg" alt="Starbucks" />
            <img class="trusted-logo-inline bosch-inline" src="/logos/bosch.svg" alt="Bosch" />
            <img class="trusted-logo-inline huawei-inline" src="/logos/huawei.svg" alt="Huawei" />
          </div>
        </div>
        <p class="copy">© 2026 Aero Smart Monitoring System. 企业级 AI 吸烟检测与预警平台。</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { googleTokenLogin } from 'vue3-google-login' // 👈 引入 Google 登录方法
import { ElMessage } from 'element-plus' // 👈 补上 ElMessage
import { buildApiUrl } from '@/utils/http'

const form = reactive({ email: '', password: '', remember: false })
const showPwd = ref(false)
const isLoading = ref(false)
const errorText = ref('')
const particleCanvas = ref(null)
let raf = null, cleanup = null

const router = useRouter()

// Google 登录逻辑
const handleGoogleLogin = () => {
  isLoading.value = true
  googleTokenLogin().then((response) => {
    // 获取到 Google 的 access_token 后，直接发给后端
    // 注意：后端 callback 需要兼容 access_token 参数
    const url = buildApiUrl(`/api/auth/google/callback?access_token=${response.access_token}`)
    
    // 我们手动发起 GET 请求，后端会返回 302
    // 但因为是 API 调用，我们捕获它
    window.location.href = url
  }).catch(err => {
    console.error('Google Login Error:', err)
    ElMessage.error('Google 登录取消或失败')
  }).finally(() => {
    isLoading.value = false
  })
}

// 简单邮箱格式校验
const isValidEmail = (value) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(value)
}

// 输入变化时清除错误提示
watch(() => [form.email, form.password], () => {
  if (errorText.value) errorText.value = ''
})

// 真实登录逻辑
const handleLogin = async () => {
  errorText.value = ''
  // console.log('handleLogin clicked', form.email, form.password)
  // 防止重复点击
  if (isLoading.value || !form.email || !form.password) {
    if (!form.email || !form.password) errorText.value = '请输入邮箱和密码'
    return
  }

  // 邮箱格式校验
  if (!isValidEmail(form.email)) {
    errorText.value = '请输入有效的邮箱地址，例如：admin@aero.com'
    return
  }
  
  isLoading.value = true // 开启按钮的 loading 动画

  try {
    // 1. 发送请求给 Django 后端
    const response = await axios.post('/api/login/', {
      username: form.email, // 使用邮箱字段登录
      password: form.password
    });

    // 2. 登录成功，保存 Token
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    
    // 3. 直接跳转，不再弹出成功提示
    router.push('/dashboard'); // 注意：请确保你的 Vue Router 里配了 /dashboard 这个路由

  } catch (error) {
    // 4. 处理错误
    console.error('登录异常:', error);
    const errorMsg = error.response?.data?.detail || '账号或密码不正确，请重新输入';
    errorText.value = '登录失败：' + errorMsg
  } finally {
    // 不管成功还是失败，都把 loading 状态关掉
    isLoading.value = false;
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
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── PAGE ── */
.login-page {
  display: flex;
  flex-direction: row-reverse;
  min-height: 100vh;
  background: radial-gradient(1100px 520px at 18% 18%, rgba(59, 158, 255, .16), transparent 62%),
              radial-gradient(900px 520px at 86% 26%, rgba(124, 92, 232, .12), transparent 62%),
              #edf5ee;
  position: relative;
}

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

/* ══════════ LEFT PANEL ══════════ */
.left-panel {
  flex: 0 0 50%;
  max-width: 50%;
  display: flex;
  flex-direction: column;
  padding: 44px 24px 40px 72px;
  background: transparent;
  position: relative;
  z-index: 2;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  width: 100%;
  max-width: 440px;
  margin: 0 auto 20px;
}

.logo-icon {
  width: 36px; height: 36px;
  background: #3b9eff;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.logo-text { font-size: 17px; font-weight: 700; color: #111b27; letter-spacing: -.3px; }

.form-center {
  flex: 0 0 auto;
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
  font-size: 34px; font-weight: 800;
  color: #0d1724; letter-spacing: -.8px;
  margin-bottom: 8px; line-height: 1.2;
}

.subtitle { font-size: 14px; color: #6b7a90; line-height: 1.65; }

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

.form-error {
  margin: -6px 0 14px 0;
  color: #d92d20;
  font-size: 13px;
  line-height: 1.5;
  font-weight: 600;
}

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

.divider { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.dline   { flex: 1; height: 1px; background: #dde5ee; }
.dtxt    { font-size: 13px; color: #9aa5b4; }

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

.left-footer {
  margin-top: 14px;
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  margin-right: auto;
}

.trusted-strip {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
}

.trusted-strip-label {
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: #9aa5b4;
}

.trusted-strip-line {
  width: 28px;
  height: 1px;
  background: linear-gradient(90deg, rgba(154, 165, 180, 0), rgba(154, 165, 180, .75));
  flex-shrink: 0;
}

.trusted-logos-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  min-width: 0;
}

.trusted-logo-inline {
  height: 22px;
  width: auto;
  object-fit: contain;
  display: block;
  opacity: .6;
  filter: grayscale(1) contrast(.88);
  transition: opacity .2s ease, filter .2s ease, transform .2s ease;
}

.trusted-logo-inline:hover {
  opacity: .88;
  filter: grayscale(1) contrast(1);
  transform: translateY(-1px);
}

.starbucks-inline {
  height: 22px;
}

.bosch-inline {
  height: 18px;
}

.huawei-inline {
  height: 20px;
}

.copy      { font-size: 12px; color: #9eaab7; line-height: 1.5; text-align: center; }

/* ══════════ RIGHT PANEL ══════════ */
.right-panel {
  flex: 0 0 52%;
  max-width: 52%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 60px 64px 60px 12px;
  position: relative;
  z-index: 2;
}

.right-content {
  max-width: 660px;
  width: 100%;
}

.bg-badge {
  display: inline-flex;
  align-items: center;
  padding: 7px 16px;
  border-radius: 999px;
  background: rgba(255,255,255,.55);
  border: 1px solid rgba(220,228,240,.9);
  color: #1a2332;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .2px;
  margin-bottom: 20px;
}

.bg-title {
  margin: 0 0 24px 0;
  font-size: 38px;
  line-height: 1.28;
  letter-spacing: -0.8px;
  color: #0d1724;
  font-weight: 800;
  max-width: 620px;
}

.title-highlight {
  color: #3b9eff;
}

.bg-sub {
  margin: 0 0 30px 0;
  font-size: 15px;
  color: #5a6475;
  line-height: 2;
  max-width: 600px;
}

.bg-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 34px;
}

.bg-tag {
  display: inline-flex;
  align-items: center;
  padding: 9px 16px;
  border-radius: 999px;
  background: rgba(255,255,255,.55);
  border: 1px solid rgba(220,228,240,.9);
  color: #2d3a4a;
  font-size: 13px;
  font-weight: 600;
  gap: 6px;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 14px;
}

.metric-card {
  background: rgba(255,255,255,.62);
  border: 1px solid rgba(220,228,240,.9);
  border-radius: 16px;
  padding: 20px 18px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.metric-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(59, 158, 255, .08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.metric-info {
  flex: 1;
  min-width: 0;
}

.metric-label {
  font-size: 12px;
  color: #6b7a90;
  margin-bottom: 4px;
  font-weight: 600;
}

.metric-value {
  font-size: 32px;
  line-height: 1.1;
  color: #0d1724;
  font-weight: 800;
  letter-spacing: -0.6px;
}

.metric-unit {
  font-size: 18px;
  font-weight: 700;
  color: #3b9eff;
}

.metric-desc {
  font-size: 11px;
  color: #9aa5b4;
  margin-top: 3px;
  font-weight: 500;
}

.bg-footer-row {
  margin-top: 20px;
}

.bg-footnote {
  font-size: 13px;
  color: #5f6e82;
  font-weight: 600;
}

/* ── RESPONSIVE ── */
@media (min-width: 1280px) {
  .bg-title {
    font-size: 40px;
    max-width: 680px;
  }
}

@media (max-width: 960px) {
  .right-panel { display: none; }
  .left-panel  { flex: 1; max-width: 100%; min-width: 0; padding: 36px 32px; }
  .trusted-by-card {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
