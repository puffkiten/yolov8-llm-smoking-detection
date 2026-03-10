import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 👇 引入 Element Plus 的核心和样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/global.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
// 👇 告诉 Vue 使用 Element Plus
app.use(ElementPlus)

app.mount('#app')