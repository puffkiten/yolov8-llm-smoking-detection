<template>
  <div class="ai-model-page">
    <section class="summary-grid">
      <div class="summary-card">
        <div class="summary-icon blue">
          <el-icon><Box /></el-icon>
        </div>
        <div class="summary-content">
          <div class="summary-label">当前检测模型</div>
          <div class="summary-value">YOLOv8</div>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon gold">
          <el-icon><Cpu /></el-icon>
        </div>
        <div class="summary-content">
          <div class="summary-label">当前大模型</div>
          <div class="summary-value">{{ overview.current_llm_name || '未启用' }}</div>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon green">
          <el-icon><CircleCheck /></el-icon>
        </div>
        <div class="summary-content">
          <div class="summary-label">连接状态</div>
          <div class="summary-value" :class="overview.connection_status">{{ overview.connection_status_label || '未连接' }}</div>
        </div>
      </div>
    </section>

    <section class="content-grid">
      <div class="panel-card">
        <div class="panel-header"><h3>大模型服务列表</h3></div>
        <el-table :data="services" v-loading="loading" empty-text="暂无服务商数据">
          <el-table-column prop="service_name" label="服务名称" min-width="160" />
          <el-table-column prop="model_identifier" label="模型标识" min-width="140" />
          <el-table-column label="状态" min-width="110">
            <template #default="{ row }"><el-tag :type="tagType(row.status)" round>{{ row.status_label }}</el-tag></template>
          </el-table-column>
          <el-table-column label="操作" min-width="180">
            <template #default="{ row }">
              <el-button link type="primary" @click="openDialog(row)">查看</el-button>
              <el-button link type="primary" @click="openDialog(row)">{{ row.status === 'unconfigured' ? '配置' : '切换' }}</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="panel-card current-panel" v-loading="loading">
        <div class="panel-header current-header"><h3>当前生效配置</h3></div>
        <div v-if="current.service_name" class="info-list current-info-list">
          <div class="info-row current-info-row"><span class="current-label">服务提供商:</span><span class="current-text">{{ current.service_name }}</span></div>
          <div class="info-row current-info-row"><span class="current-label">模型名称:</span><span class="current-text">{{ current.model_name || '-' }}</span></div>
          <div class="info-row current-info-row api-key-row"><span class="current-label">API Key:</span><span class="current-text mono current-key-text">{{ current.masked_api_key || '-' }}</span></div>
          <div class="info-row current-info-row"><span class="current-label">Base URL:</span><span class="current-text break current-url-text">{{ current.base_url || '-' }}</span></div>
          <div class="info-row current-info-row"><span class="current-label">请求超时:</span><span class="current-text">{{ current.request_timeout || 30 }}s</span></div>
          <div class="actions current-actions">
            <el-button class="action-btn ghost-btn" :loading="testing" @click="testCurrent">测试连接</el-button>
            <el-button class="action-btn primary-btn" type="primary" :loading="switching" @click="saveCurrent">保存配置</el-button>
          </div>
        </div>
        <el-empty v-else description="暂无生效配置" />
      </div>
    </section>

    <section class="panel-card">
      <div class="panel-header"><h3>API 配置说明</h3></div>
      <ul class="tips"><li>支持切换平台支持的大语言模型服务商</li><li>修改 API Key 后对新分析任务生效</li><li>检测模型仍固定使用 YOLOv8</li></ul>
    </section>

    <el-dialog v-model="visible" width="780px" destroy-on-close :show-close="false" class="model-config-dialog">
      <template #header>
        <div class="dialog-header">
          <div>
            <div class="dialog-title">配置大模型</div>
            <div class="dialog-subtitle">平台仅支持以下模型服务商，选择后填写 API Key 即可启用</div>
          </div>
          <button class="dialog-close" type="button" @click="visible = false">×</button>
        </div>
      </template>

      <div class="dialog-layout">
        <section class="dialog-block">
          <div class="dialog-block-head">
            <div class="dialog-block-title">服务商选择</div>
            <div class="dialog-block-desc">请选择一个平台支持的服务商</div>
          </div>

          <div class="provider-grid fancy-provider-grid">
            <button
              v-for="item in services"
              :key="item.service_key"
              type="button"
              class="provider-card"
              :class="{ active: form.service_key === item.service_key }"
              @click="pick(item.service_key)"
            >
              <div class="provider-card-top">
                <div class="provider-card-logo" :class="`logo-${item.service_key}`">{{ providerLogo(item.service_key) }}</div>
                <div v-if="form.service_key === item.service_key" class="provider-check">✓</div>
              </div>
              <div class="provider-card-name">{{ item.service_name }}</div>
              <div class="provider-card-meta">
                <el-tag size="small" round :type="tagType(item.status)">{{ item.status_label }}</el-tag>
              </div>
            </button>
          </div>
        </section>

        <section class="dialog-block config-block">
          <div class="dialog-block-head">
            <div class="dialog-block-title">模型配置</div>
            <div class="dialog-block-desc">根据服务商填写模型与认证信息</div>
          </div>

          <el-form :model="form" label-position="top" class="dialog-form">
            <el-form-item label="可用模型">
              <el-select v-model="form.model_name" placeholder="请选择模型" style="width:100%" popper-class="model-select-popper">
                <el-option v-for="m in modelOptions" :key="m.value" :label="m.label" :value="m.value">
                  <div class="model-option">
                    <span>{{ m.label }}</span>
                    <el-tag size="small" effect="plain" round>{{ m.category === 'multimodal' ? '多模态' : '文本' }}</el-tag>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item>
              <template #label>
                <div class="field-label-row">
                  <span>API Key</span>
                  <a v-if="form.service_key" class="inline-api-link" :href="linksMap[form.service_key] || '#'" target="_blank" rel="noreferrer">获取 API Key</a>
                </div>
              </template>
              <el-input v-model="form.api_key" :placeholder="form.masked_api_key ? `已配置：${form.masked_api_key}，如需更换请重新输入` : '请输入 API Key'" :type="showKey ? 'text' : 'password'" autocomplete="off">
                <template #suffix>
                  <el-button link class="eye-btn" @click="showKey = !showKey">
                    <el-icon><View v-if="!showKey" /><Hide v-else /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </el-form-item>

            <div class="enable-row">
              <div>
                <div class="enable-title">保存后立即启用</div>
                <div class="enable-desc">开启后将切换为当前生效模型</div>
              </div>
              <el-switch v-model="form.enabled" />
            </div>
          </el-form>
        </section>
      </div>

      <template #footer>
        <div class="dialog-footer product-footer">
          <el-button class="dialog-action-btn ghost-btn" :loading="dialogTesting" @click="testDialog">测试连接</el-button>
          <div class="footer-right-actions">
            <el-button class="dialog-action-btn cancel-btn" @click="visible = false">取消</el-button>
            <el-button class="dialog-action-btn primary-btn" type="primary" :loading="saving" @click="submit">保存配置</el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Box, CircleCheck, Cpu, Hide, View } from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const visible = ref(false)
const saving = ref(false)
const testing = ref(false)
const switching = ref(false)
const dialogTesting = ref(false)
const showKey = ref(false)
const services = ref([])
const overview = reactive({ current_llm_name: '', connection_status: 'disconnected', connection_status_label: '未连接' })
const current = reactive({ service_key: '', service_name: '', model_name: '', masked_api_key: '', base_url: '', request_timeout: 30, enabled: false })
const form = reactive({ service_key: '', model_name: '', api_key: '', masked_api_key: '', enabled: false, request_timeout: 30, has_api_key: false })
const modelsMap = reactive({})
const linksMap = reactive({})
const modelOptions = computed(() => modelsMap[form.service_key] || [])
const tagType = (s) => s === 'enabled' ? 'success' : s === 'standby' ? 'info' : 'warning'
const providerLogo = (key) => ({ qwen: 'Q', deepseek: 'D', openai: 'O', zhipu: '智' }[key] || 'AI')
const providerLinkLabel = (key) => ({ qwen: '通义千问控制台', deepseek: 'DeepSeek 开放平台', openai: 'OpenAI Platform', zhipu: '智谱开放平台' }[key] || '开放平台')
const modelOptionLabel = (item) => `${item.label}${item.category === 'multimodal' ? ' · 多模态' : ' · 文本'}`

const resetForm = () => {
  form.service_key = ''
  form.model_name = ''
  form.api_key = ''
  form.masked_api_key = ''
  form.enabled = false
  form.request_timeout = 30
  form.has_api_key = false
}

const apply = (data = {}) => {
  overview.current_llm_name = data.current_llm_name || '未启用'
  overview.connection_status = data.connection_status || 'disconnected'
  overview.connection_status_label = data.connection_status_label || '未连接'
  services.value = data.services || []
  Object.assign(current, data.current_config || { service_key: '', service_name: '', model_name: '', masked_api_key: '', base_url: '', request_timeout: 30, enabled: false })
  services.value.forEach(i => { linksMap[i.service_key] = i.api_key_url || '' })
}

const loadOverview = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/llm-services/overview')
    apply(data || {})
  } finally {
    loading.value = false
  }
}
const loadModels = async (key) => {
  const { data } = await axios.get(`/api/llm-services/${key}/models`)
  modelsMap[key] = data?.models || []
  linksMap[key] = data?.api_key_url || ''
  form.service_key = key
  form.model_name = data?.current_model || data?.models?.[0]?.value || ''
  form.masked_api_key = data?.masked_api_key || ''
  form.enabled = !!data?.enabled
  form.request_timeout = data?.request_timeout || 30
  form.has_api_key = !!data?.has_api_key
}
const pick = async (key) => {
  form.api_key = ''
  showKey.value = false
  await loadModels(key)
}
const openDialog = async (row) => {
  visible.value = true
  resetForm()
  await pick(row.service_key)
}
const validateForm = (forTest = false) => {
  if (!form.service_key) return ElMessage.warning('请选择服务商'), false
  if (!form.model_name) return ElMessage.warning('请选择模型名称'), false
  if (!form.api_key.trim() && !form.has_api_key) return ElMessage.warning('请输入 API Key'), false
  if (!forTest && typeof form.enabled !== 'boolean') return ElMessage.warning('请选择启用状态'), false
  return true
}
const refreshAll = async () => {
  await loadOverview()
}
const testDialog = async () => {
  if (!validateForm(true)) return
  dialogTesting.value = true
  try {
    const { data } = await axios.post('/api/llm-services/test', { service_key: form.service_key, model_name: form.model_name, api_key: form.api_key || undefined })
    ElMessage.success(data?.message || '连接测试成功')
    await refreshAll()
    await loadModels(form.service_key)
  } finally {
    dialogTesting.value = false
  }
}
const submit = async () => {
  if (!validateForm(false)) return
  saving.value = true
  try {
    const { data } = await axios.post('/api/llm-services/save', { service_key: form.service_key, model_name: form.model_name, api_key: form.api_key, enabled: form.enabled, request_timeout: form.request_timeout })
    ElMessage.success(data?.detail || '保存成功')
    apply(data?.overview || {})
    visible.value = false
    await refreshAll()
  } finally {
    saving.value = false
  }
}
const testCurrent = async () => {
  if (!current.service_key) return ElMessage.warning('暂无可测试配置')
  testing.value = true
  try {
    const { data } = await axios.post('/api/llm-services/test', { service_key: current.service_key, model_name: current.model_name })
    ElMessage.success(data?.message || '连接测试成功')
    await refreshAll()
  } finally {
    testing.value = false
  }
}
const saveCurrent = async () => {
  if (!current.service_key) return ElMessage.warning('暂无可保存配置')
  switching.value = true
  try {
    const { data } = await axios.post('/api/llm-services/switch', { service_key: current.service_key })
    ElMessage.success(data?.detail || '切换成功')
    apply(data?.overview || {})
    await refreshAll()
  } finally {
    switching.value = false
  }
}

onMounted(loadOverview)
</script>

<style scoped>
.ai-model-page{display:flex;flex-direction:column;gap:18px}.summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.content-grid{display:grid;grid-template-columns:1.6fr .9fr;gap:20px}.summary-card,.panel-card{background:#fff;border:1px solid rgba(226,232,240,.88);border-radius:18px;box-shadow:0 8px 24px rgba(15,23,42,.04)}.summary-card{padding:18px 22px;min-height:104px;display:flex;align-items:center;gap:16px}.summary-icon{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0}.summary-icon.blue{background:rgba(59,130,246,.10);color:#4b93ff}.summary-icon.gold{background:rgba(245,158,11,.12);color:#f5a623}.summary-icon.green{background:rgba(16,185,129,.12);color:#22c55e}.summary-content{display:flex;flex-direction:column;justify-content:center;min-width:0}.summary-label{font-size:13px;color:#64748b;margin-bottom:8px;font-weight:500}.summary-value{font-size:18px;font-weight:500;color:#0f172a;line-height:1.3}.summary-value.connected{color:#10b981}.summary-value.disconnected{color:#f59e0b}.panel-card{padding:20px 22px}.panel-header{margin-bottom:14px}.panel-header h3{margin:0;font-size:18px;font-weight:600;color:#0f172a}.current-panel{padding:26px 26px 24px;border-radius:22px}.current-header{margin-bottom:24px}.current-header h3{font-size:18px;font-weight:600;color:#1e293b}.current-info-list{display:flex;flex-direction:column;gap:20px}.current-info-row{display:flex;align-items:flex-start;gap:28px;font-size:14px;line-height:1.55}.current-label{width:118px;flex-shrink:0;color:#64748b}.current-text{flex:1;color:#0f172a;word-break:break-word}.current-url-text{max-width:280px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','Courier New',monospace}.break{word-break:break-all}.current-actions{display:flex;justify-content:space-between;gap:18px;padding-top:18px}.action-btn,.dialog-action-btn{height:46px;border-radius:12px;font-size:14px;font-weight:500}.action-btn{flex:1}.ghost-btn{border:1px solid #dbe4f0;color:#409eff;background:#fff}.ghost-btn:hover{border-color:#409eff;background:#f8fbff;color:#409eff}.primary-btn{border:none;background:linear-gradient(90deg,#4da2ff 0%,#2f80ed 100%)}.tips{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:10px;color:#475569;font-size:14px}.dialog-header{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.dialog-title{font-size:24px;font-weight:700;color:#1e293b;line-height:1.2}.dialog-subtitle{margin-top:8px;font-size:13px;color:#64748b}.dialog-close{border:none;background:transparent;color:#94a3b8;font-size:24px;line-height:1;cursor:pointer;padding:0 4px}.dialog-layout{display:flex;flex-direction:column;gap:18px}.dialog-block{padding:18px 18px 16px;border:1px solid #eef2f7;border-radius:18px;background:linear-gradient(180deg,#ffffff 0%,#fbfdff 100%)}.dialog-block-head{margin-bottom:14px}.dialog-block-title{font-size:16px;font-weight:600;color:#0f172a}.dialog-block-desc{margin-top:4px;font-size:12px;color:#94a3b8}.config-block{padding-bottom:18px}.fancy-provider-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.provider-card{position:relative;border:1px solid #e5e7eb;background:#fff;border-radius:16px;padding:16px 14px 14px;text-align:left;cursor:pointer;transition:all .2s ease}.provider-card:hover{border-color:#cfe2ff;box-shadow:0 10px 20px rgba(59,130,246,.08)}.provider-card.active{border-color:#66a8ff;background:#f5f9ff;box-shadow:0 0 0 2px rgba(64,158,255,.12)}.provider-card-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px}.provider-card-logo{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700}.logo-qwen{background:#eef5ff;color:#4b93ff}.logo-deepseek{background:#eef3ff;color:#5b6cff}.logo-openai{background:#f5f5f5;color:#111827}.logo-zhipu{background:#f3f4ff;color:#5b5bd6}.provider-card-name{font-size:14px;color:#1f2937}.provider-card-meta{margin-top:10px}.provider-check{width:20px;height:20px;border-radius:50%;background:#409eff;color:#fff;font-size:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0}.dialog-form{margin-top:2px}.model-option{display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%}.field-label-row{width:100%;display:flex;align-items:center;justify-content:space-between;gap:12px}.inline-api-link{font-size:12px;color:#409eff;text-decoration:none;font-weight:500}.inline-api-link:hover{text-decoration:underline}.eye-btn{padding:0;min-height:auto}.enable-row{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 16px;border:1px solid #eef2f7;border-radius:14px;background:#fbfdff}.enable-title{font-size:14px;font-weight:600;color:#0f172a}.enable-desc{margin-top:4px;font-size:12px;color:#94a3b8}.dialog-footer{display:flex;justify-content:space-between;align-items:center;gap:12px}.product-footer{padding-top:8px}.footer-right-actions{display:flex;gap:10px}.dialog-action-btn{min-width:110px}.cancel-btn{border:1px solid #dbe4f0;background:#fff;color:#475569}.el-table :deep(.el-table__inner-wrapper::before){display:none}.el-table :deep(th.el-table__cell){background:#f8fafc;color:#64748b;font-size:13px;font-weight:500}.el-table :deep(.el-table__row td){padding-top:12px;padding-bottom:12px;font-size:14px}.el-table :deep(.el-button--small),.el-table :deep(.el-button){font-size:13px;font-weight:400}@media (max-width:1200px){.content-grid{grid-template-columns:1fr}.current-url-text{max-width:none}}@media (max-width:900px){.summary-grid,.fancy-provider-grid{grid-template-columns:1fr}.current-info-row{flex-direction:column;gap:6px}.current-label{width:auto}.current-actions,.dialog-footer,.footer-right-actions,.enable-row{flex-direction:column;align-items:stretch}.field-label-row{align-items:flex-start;flex-direction:column}}</style>
