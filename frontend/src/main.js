import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 👇 引入 Element Plus 的核心和样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/global.css'
import vue3GoogleLogin from 'vue3-google-login' // 👈 引入 Google 登录插件

const app = createApp(App)

app.use(createPinia())
app.use(router)
// 👇 告诉 Vue 使用 Element Plus
app.use(ElementPlus)
// 👇 初始化 Google 登录
app.use(vue3GoogleLogin, {
  clientId: '1023668174872-jg6vs23283r4h884dt2v4vfs05jugptf.apps.googleusercontent.com'
})

app.mount('#app')