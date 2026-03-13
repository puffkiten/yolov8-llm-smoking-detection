<template>
  <div class="task-detail-page">
    
    <div class="layout-grid">
      <aside class="left-panel">
        <div class="panel-card" ref="leftPanelRef">
          
          <div class="task-head">
            <div class="head-row">
              <span class="status-badge" :class="statusText === '检测中' ? 'processing' : statusText === '任务中断' ? 'failed' : 'success'">
                <span v-if="statusText === '检测中'" class="spin"></span>
                {{ statusText }}
              </span>
              <svg class="share-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" @click="shareReport">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15 3 21 3 21 9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </div>
            <div class="id-row">
              <h1 class="task-id">{{ runIndex }}</h1>
              <div class="task-id-actions">
                <button class="tiny-btn" @click="copyRunIndex">复制</button>
                <button class="tiny-btn ghost" @click="clearRunIndex">清空</button>
              </div>
            </div>
          </div>

          <div class="info-section">
            <h3 class="section-title">核心参数</h3>
            <ul class="info-list">
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 置信度阈值</div>
                <div class="value">{{ taskInfo.confidence }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/></svg> 检测模型</div>
                <div class="value">{{ taskInfo.model }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg> 运行设备</div>
                <div class="value">{{ taskInfo.device }}</div>
              </li>
            </ul>
          </div>

          <div class="info-section">
            <h3 class="section-title">文件与耗时</h3>
            <ul class="info-list">
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg> 文件大小</div>
                <div class="value">{{ fileSizeText }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg> 画面分辨率</div>
                <div class="value">{{ resolutionText }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 处理耗时</div>
                <div class="value">{{ processTimeText }}</div>
              </li>
            </ul>
          </div>

          <div class="info-section">
            <h3 class="section-title">时间流水</h3>
            <ul class="info-list">
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> 创建时间</div>
                <div class="value">{{ createdText }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 完成时间</div>
                <div class="value">{{ finishedText }}</div>
              </li>
            </ul>
          </div>

          <div class="action-buttons">
            <button class="btn-primary" @click="handleExport">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              导出结果
            </button>
            <button class="btn-outline" @click="handleRetry">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-5.05"/></svg>
              重新检测
            </button>
          </div>

          <div class="alert-box" v-if="taskInfo.hasViolation || statusText === '任务中断'">
            <div class="alert-header">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              {{ statusText === '任务中断' ? '检测中断' : '检测到违规行为' }}
            </div>
            <p class="alert-desc" v-if="statusText === '任务中断'">
              <span>{{ friendlyErrorReason }}</span>
              <span v-if="taskErrorMessage">（{{ taskErrorMessage }}）</span>
            </p>
            <p class="alert-desc" v-else>
              <span v-if="llmReport">{{ llmReport }}</span>
              <span v-else>YOLO 发现疑似吸烟目标，建议人工复核。</span>
            </p>
          </div>

        </div>
      </aside>

      <main class="right-panel">
        
        <div class="image-card">
          <div class="img-header">
            <div class="img-title"><span class="dot gray"></span> 原始图像 (Original Source)</div>
            <div class="img-subtitle">{{ isVideo ? '视频' : '图片' }}</div>
          </div>
          <div class="img-container" :style="{ height: imgHeight + 'px' }">
            <img v-if="!isVideo" :src="originalUrl" alt="Original Source" class="source-img" :style="{ height: imgHeight + 'px' }">
            <video v-else :src="originalUrl" class="source-video" controls :style="{ height: imgHeight + 'px' }"></video>
          </div>
        </div>

        <div class="image-card">
          <div class="img-header">
            <div class="img-title"><span class="dot blue"></span> AI 检测结果 (Aero YOLOv8 Analysis)</div>
            <div class="badge-blue" v-if="taskInfo.hasViolation">Detected</div>
          </div>
          <div class="no-dets" v-if="!isVideo && statusText !== '检测中' && detections.length === 0">
            未检测到目标，可尝试降低置信度阈值（建议 0.3~0.5）
          </div>
          <div class="img-container relative-container" ref="aiContainerRef" :style="{ height: imgHeight + 'px' }">
            <img v-if="!isVideo" ref="aiImgRef" :src="resultUrl" alt="AI Result" class="source-img" :style="{ height: imgHeight + 'px' }" @load="recomputeAiDrawRect">
            <video v-else :src="resultUrl" class="source-video" controls :style="{ height: imgHeight + 'px' }"></video>
            <div v-if="!isVideo" class="overlay">
              <div v-for="(b, idx) in detections" :key="idx" class="bbox" :class="{ danger: Number(b.cls) === 0 }"
                   :style="bboxStyle(b)">
                <span class="bbox-label">{{ b.label }} {{ (b.conf * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bottom-actions">
          <button class="btn-back" @click="$router.push('/dashboard')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
            返回任务列表
          </button>
          <div class="bottom-right">
            <div class="verify-state">
              <span class="verify-label">核实状态</span>
              <span class="verify-pill" :class="verifyStatus">{{ verifyTextCn(verifyStatus) }}</span>
            </div>
            <div class="verify-actions">
              <button v-if="verifyStatus === 'pending'" class="btn-soft-success" :disabled="verifyUpdating" @click="markAsPass">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                {{ verifyUpdating ? '提交中...' : '核实通过' }}
              </button>
              <button v-if="verifyStatus === 'pending'" class="btn-soft-danger" :disabled="verifyUpdating" @click="markAsViolation">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                {{ verifyUpdating ? '提交中...' : '标记违规' }}
              </button>
              <div v-if="verifyStatus === 'verified'" class="verify-result">
                <span class="verify-result-label">核实结果</span>
                <span class="verify-result-pill" :class="verifyResult || ''">{{ verifyResultTextCn(verifyResult) }}</span>
              </div>
              <button
                v-if="verifyStatus === 'verified'"
                class="btn-cancel-verify"
                :disabled="verifyUpdating"
                @click="cancelVerify"
              >
                取消核实
              </button>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const authHeaders = () => {
  const access = localStorage.getItem('access_token') || ''
  return access ? { Authorization: `Bearer ${access}` } : {}
}

const taskInfo = ref({
  id: '',
  confidence: '',
  model: 'Aero-YOLO-v8s',
  device: 'GPU',
  fileSize: '',
  resolution: '',
  processTime: '',
  createTime: '',
  finishTime: '',
  hasViolation: false
})

const currentTaskId = ref(null)
const verifyStatus = ref('verified')
const verifyResult = ref(null)
const verifyUpdating = ref(false)
const originalUrl = ref('')
const resultUrl = ref('')
const statusText = ref('已完成')
const fileSizeText = ref('')
const resolutionText = ref('')
const processTimeText = ref('')
const createdText = ref('')
const finishedText = ref('')
const isVideo = ref(false)
const detections = ref([])
const llmReport = ref('')
const taskErrorMessage = ref('')
let pollTimer = null
const leftPanelRef = ref(null)
const imgHeight = ref(320)
const aiContainerRef = ref(null)
const aiImgRef = ref(null)
const aiDrawRect = ref({ offsetX: 0, offsetY: 0, drawW: 0, drawH: 0 })
const recomputeHeights = () => {
  const h = leftPanelRef.value ? leftPanelRef.value.offsetHeight : 640
  const padding = 40
  const target = Math.max(240, Math.floor((h - padding) / 2))
  imgHeight.value = target
}

const recomputeAiDrawRect = () => {
  const container = aiContainerRef.value
  const img = aiImgRef.value
  if (!container || !img || !img.naturalWidth || !img.naturalHeight) return
  const cw = container.clientWidth
  const ch = container.clientHeight
  const iw = img.naturalWidth
  const ih = img.naturalHeight
  const scale = Math.min(cw / iw, ch / ih)
  const drawW = iw * scale
  const drawH = ih * scale
  const offsetX = (cw - drawW) / 2
  const offsetY = (ch - drawH) / 2
  aiDrawRect.value = { offsetX, offsetY, drawW, drawH }
}

const bboxStyle = (b) => {
  const r = aiDrawRect.value || {}
  if (!r.drawW || !r.drawH) {
    return { left: (b.x || 0) + '%', top: (b.y || 0) + '%', width: (b.w || 0) + '%', height: (b.h || 0) + '%' }
  }
  const x = r.offsetX + (Number(b.x || 0) / 100) * r.drawW
  const y = r.offsetY + (Number(b.y || 0) / 100) * r.drawH
  const w = (Number(b.w || 0) / 100) * r.drawW
  const h = (Number(b.h || 0) / 100) * r.drawH
  return { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' }
}

const route = useRoute()
const router = useRouter()

const verifyTextCn = (s) => s === 'pending' ? '待核实' : '已核实'
const verifyResultTextCn = (s) => s === 'violation' ? '违规' : s === 'pass' ? '通过' : '—'

const loadTask = async () => {
  try {
    const routeId = route.params?.id ? Number(route.params.id) : null
    let id = routeId
    if (!id) {
      const list = await axios.get('http://127.0.0.1:8000/api/detection/tasks', { headers: authHeaders() })
      const items = list.data?.results || []
      if (!items.length) return
      id = items[0].id
    }
    currentTaskId.value = id
    const resp = await axios.get(`http://127.0.0.1:8000/api/detection/tasks/${id}`, { headers: authHeaders() })
    const d = resp.data
    taskInfo.value.id = d.id
    taskInfo.value.confidence = (typeof d.confidence === 'number' ? (d.confidence * 100).toFixed(0) + '%' : '')
    taskInfo.value.model = d.model || taskInfo.value.model
    taskInfo.value.device = d.device || taskInfo.value.device
    taskInfo.value.createTime = d.created_at
    taskInfo.value.finishTime = d.finished_at || d.created_at
    verifyStatus.value = d.verify_status || 'verified'
    verifyResult.value = d.verify_result || null
    taskInfo.value.hasViolation = (verifyStatus.value === 'pending') || (Array.isArray(d.detections) && d.detections.some(x => Number(x?.cls) === 0))
    originalUrl.value = d.original_url || d.source_url || ''
    resultUrl.value = d.result_url || d.source_url || d.original_url || ''
    statusText.value = d.status === 'processing' ? '检测中' : d.status === 'failed' ? '任务中断' : '已完成'
    isVideo.value = (d.type === 'video')
    detections.value = Array.isArray(d.detections) ? d.detections : []
    llmReport.value = (d.records && d.records[0] && d.records[0].llm_report) ? d.records[0].llm_report : ''
    taskErrorMessage.value = (d.error_message || '').toString()
    fileSizeText.value = d.file_size ? (d.file_size / (1024*1024)).toFixed(2) + ' MB' : ''
    if (d.resolution && d.resolution.w && d.resolution.h) {
      resolutionText.value = `${d.resolution.w} x ${d.resolution.h}`
    }
    processTimeText.value = d.process_time_ms ? (d.process_time_ms/1000).toFixed(2) + 's' : ''
    createdText.value = d.created_at
    finishedText.value = d.finished_at || ''
    const finishIso = d.finished_at_iso || d.finished_at || ''
    const completionSig = (d.status === 'completed' && finishIso) ? `${d.id}:${finishIso}:${d.process_time_ms || ''}` : ''
    if (completionSig && completionSig !== lastCountedSig.value) {
      runIndex.value = Number(runIndex.value || 0) + 1
      persistRunIndex()
      lastCountedSig.value = completionSig
      persistLastCountedSig()
    }
    if (d.status === 'processing') {
      if (!pollTimer) {
        pollTimer = window.setInterval(() => {
          loadTask()
        }, 1200)
      }
    } else if (pollTimer) {
      window.clearInterval(pollTimer)
      pollTimer = null
    }
  } catch (e) {
    // 保留静态展示
  }
}
onMounted(loadTask)
watch(() => route.params?.id, () => {
  if (pollTimer) {
    window.clearInterval(pollTimer)
    pollTimer = null
  }
  loadTask()
})
onMounted(() => {
  recomputeHeights()
  window.addEventListener('resize', recomputeHeights)
  recomputeAiDrawRect()
  window.addEventListener('resize', recomputeAiDrawRect)
})
onUnmounted(() => {
  if (pollTimer) window.clearInterval(pollTimer)
  pollTimer = null
  window.removeEventListener('resize', recomputeHeights)
  window.removeEventListener('resize', recomputeAiDrawRect)
})

const handleExport = async () => {
  if (!currentTaskId.value) return ElMessage.info('暂无可导出的任务')
  try {
    const resp = await axios.post(
      `http://127.0.0.1:8000/api/detection/tasks/${currentTaskId.value}/export`,
      {},
      { responseType: 'blob', headers: authHeaders() }
    )
    const blob = new Blob([resp.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `task_${currentTaskId.value}_export.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    ElMessage.error('导出失败')
  }
}

const handleRetry = async () => {
  if (!currentTaskId.value) return ElMessage.info('暂无任务可重试')
  try {
    await axios.post(`http://127.0.0.1:8000/api/detection/tasks/${currentTaskId.value}/retry`, {}, { headers: authHeaders() })
    ElMessage.success('已重新检测')
    loadTask()
  } catch (e) {
    ElMessage.error('重试失败')
  }
}

const patchVerifyStatus = async (next) => {
  if (!currentTaskId.value) return ElMessage.info('暂无可核实的任务')
  try {
    verifyUpdating.value = true
    await axios.patch(
      `http://127.0.0.1:8000/api/detection/tasks/${currentTaskId.value}/verify`,
      next,
      { headers: authHeaders() }
    )
    verifyStatus.value = next.verify_status
    verifyResult.value = next.verify_result || null
    ElMessage.success('核实状态已更新')
    loadTask()
    if (next.verify_status === 'verified') {
      window.setTimeout(() => {
        router.push('/dashboard')
      }, 500)
    }
  } catch (e) {
    const detail = e?.response?.data?.detail
    ElMessage.error(detail || '核实失败')
  } finally {
    verifyUpdating.value = false
  }
}

const markAsPass = () => patchVerifyStatus({ verify_status: 'verified', verify_result: 'pass' })

const markAsViolation = async () => {
  try {
    await ElMessageBox.confirm(
      '确定将该任务标记为违规？',
      '标记违规',
      { type: 'warning', confirmButtonText: '确认标记', cancelButtonText: '取消', customClass: 'aero-confirm' }
    )
    patchVerifyStatus({ verify_status: 'verified', verify_result: 'violation' })
  } catch {
  }
}

const cancelVerify = async () => {
  if (!currentTaskId.value) return
  try {
    await ElMessageBox.confirm(
      '取消当前核实结论后，可重新选择核实状态。确认取消？',
      '取消核实',
      { type: 'warning', confirmButtonText: '确认取消', cancelButtonText: '返回', customClass: 'aero-confirm' }
    )
    patchVerifyStatus({ verify_status: 'pending' })
  } catch {
  }
}

const runIndexKey = 'task_run_index'
const runIndex = ref(Number(localStorage.getItem(runIndexKey) || 0))
const lastCountedSigKey = 'task_run_last_counted_sig'
const lastCountedSig = ref(localStorage.getItem(lastCountedSigKey) || '')

const persistRunIndex = () => {
  localStorage.setItem(runIndexKey, String(runIndex.value || 0))
}

const persistLastCountedSig = () => {
  localStorage.setItem(lastCountedSigKey, String(lastCountedSig.value || ''))
}

const clearRunIndex = async () => {
  try {
    await ElMessageBox.confirm(
      '此操作仅清空本地“完成计数”，不会删除任何检测任务数据。确认清空？',
      '二次确认',
      { type: 'warning', confirmButtonText: '确认清空', cancelButtonText: '取消', customClass: 'aero-confirm' }
    )
    runIndex.value = 0
    persistRunIndex()
    lastCountedSig.value = ''
    persistLastCountedSig()
    ElMessage.success('已清空完成计数')
  } catch {
  }
}

const copyRunIndex = async () => {
  try {
    const v = String(runIndex.value ?? '')
    await navigator.clipboard.writeText(v)
    ElMessage.success('已复制')
  } catch (e) {
    ElMessage.error('复制失败')
  }
}

const shareReport = async () => {
  if (!currentTaskId.value) return ElMessage.info('暂无可分享的任务')
  try {
    const resp = await axios.post(
      `http://127.0.0.1:8000/api/detection/tasks/${currentTaskId.value}/share`,
      {},
      { headers: authHeaders() }
    )
    const url = resp.data?.url || ''
    if (!url) return ElMessage.error('生成分享链接失败')
    await navigator.clipboard.writeText(url)
    ElMessage.success('分享链接已复制，可直接在浏览器中打开')
  } catch (e) {
    const detail = e?.response?.data?.detail
    ElMessage.error(detail || '生成分享链接失败')
  }
}

const friendlyErrorReason = computed(() => {
  const msg = (taskErrorMessage.value || '').toLowerCase()
  if (!msg) return '任务运行失败，可能是网络中断或服务异常'
  if (msg.includes('timeout') || msg.includes('timed out')) return '网络中断或请求超时'
  if (msg.includes('connection') || msg.includes('gaierror') || msg.includes('dns')) return '网络连接失败（DNS/断网）'
  if (msg.includes('filenotfounderror') || msg.includes('no such file')) return '上传文件丢失或存储路径错误'
  if (msg.includes('permissionerror') || msg.includes('permission denied')) return '文件读写权限不足'
  if (msg.includes('cuda') || msg.includes('cudnn')) return 'GPU/驱动异常（CUDA/CUDNN）'
  if (msg.includes('invalid') && msg.includes('image')) return '图片格式不支持或文件损坏'
  return '任务运行失败，可能是网络中断或服务异常'
})
</script>

<style scoped>
:deep(.aero-confirm.el-message-box) {
  border-radius: 14px;
  border: 1px solid #edf0f5;
  box-shadow: 0 18px 50px rgba(17, 27, 39, 0.18);
}
:deep(.aero-confirm .el-message-box__header) {
  padding: 18px 18px 6px 18px;
}
:deep(.aero-confirm .el-message-box__title) {
  font-size: 16px;
  font-weight: 900;
  color: #0d1724;
}
:deep(.aero-confirm .el-message-box__content) {
  padding: 8px 18px 0 18px;
}
:deep(.aero-confirm .el-message-box__message) {
  font-size: 13.5px;
  line-height: 1.6;
  color: #4a5568;
}
:deep(.aero-confirm .el-message-box__btns) {
  padding: 16px 18px 18px 18px;
}
:deep(.aero-confirm .el-button) {
  border-radius: 10px;
  font-weight: 800;
  height: 38px;
  padding: 0 16px;
}

.task-detail-page {
  width: 100%;
  color: #1a2332;
  /* 取消 padding，让外部容器 Layout 决定留白 */
}

.layout-grid {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* ================= 左侧面板 ================= */
.left-panel {
  width: 320px;
  flex-shrink: 0;
}

.panel-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #edf0f5;
  padding: 24px;
}

.task-head { margin-bottom: 24px; }
.head-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.id-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.share-icon {
  color: #0d1724;
  cursor: pointer;
  transition: opacity 0.18s;
}
.share-icon:hover { opacity: 0.7; }

.status-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.status-badge.success { background: #f4f7fa; color: #4a5568; border: 1px solid #e8ecf2; }
.status-badge.processing { background: rgba(59,158,255,.10); color: #3b9eff; border: 1px solid rgba(59,158,255,.20); }
.status-badge.failed { background: rgba(232,92,92,.10); color: #e85c5c; border: 1px solid rgba(232,92,92,.20); }

.spin {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid rgba(59,158,255,.25);
  border-top-color: #3b9eff;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.task-id {
  font-size: 28px;
  font-weight: 900;
  color: #0d1724;
  margin: 0;
  word-break: break-all;
}
.task-id.muted { color: #9aa5b4; font-weight: 800; }
.task-id-actions { display: flex; gap: 8px; align-items: center; }
.tiny-btn {
  height: 28px;
  padding: 0 10px;
  border-radius: 8px;
  border: 1px solid #e8ecf2;
  background: #fff;
  color: #4a5568;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.18s;
}
.tiny-btn:hover { background: #f4f7fa; border-color: #d0e4ff; color: #3b9eff; }
.tiny-btn.ghost { background: transparent; }

.info-section {
  margin-bottom: 24px;
  border-top: 1px solid #f0f3f8;
  padding-top: 20px;
}
.info-section:first-of-type { border-top: none; padding-top: 0; }

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #1a2332;
  margin: 0 0 16px 0;
}

.info-list {
  list-style: none;
  padding: 0; margin: 0;
}
.info-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  font-size: 13px;
}
.info-list li:last-child { margin-bottom: 0; }

.label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7a90;
}
.label svg { color: #9aa5b4; }
.value {
  font-weight: 600;
  color: #1a2332;
  text-align: right;
}

/* 按钮组 */
.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}
.btn-primary, .btn-outline, .btn-danger, .btn-text {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  height: 40px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; font-family: inherit; transition: all 0.2s;
}
.btn-primary { background: #3b9eff; border: none; color: white; }
.btn-primary:hover { background: #2a8aee; box-shadow: 0 4px 12px rgba(59,158,255,0.25); }
.btn-outline { background: #fff; border: 1px solid #e8ecf2; color: #4a5568; }
.btn-outline:hover { background: #f4f7fa; border-color: #d0e4ff; color: #3b9eff; }
.btn-danger { background: #e85c5c; border: none; color: white; padding: 0 20px; }
.btn-danger:hover { background: #d74b4b; box-shadow: 0 4px 12px rgba(232,92,92,0.25); }
.btn-text { background: transparent; border: none; color: #4a5568; padding: 0 16px; }
.btn-text:hover { color: #1a2332; background: #f4f7fa; }

/* 红色告警框 */
.alert-box {
  background: #fff1f0;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(232,92,92,0.2);
}
.alert-header {
  display: flex; align-items: center; gap: 8px;
  font-size: 13.5px; font-weight: 700; color: #e85c5c; margin-bottom: 8px;
}
.alert-desc {
  font-size: 12.5px; color: #c04c4c; line-height: 1.5; margin: 0;
}
.alert-desc strong { font-weight: 700; }


/* ================= 右侧面板 ================= */
.right-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.image-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #edf0f5;
  padding: 20px;
}

.img-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.img-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 14px; font-weight: 700; color: #1a2332;
}
.dot { width: 8px; height: 8px; border-radius: 50%; }
.dot.gray { background: #c8d0dc; }
.dot.blue { background: #3b9eff; }

.img-subtitle { font-size: 12px; color: #9aa5b4; font-family: monospace; }
.badge-blue {
  font-size: 11px; font-weight: 600; color: #3b9eff;
  background: #eff6ff; padding: 3px 10px; border-radius: 20px;
}
.no-dets {
  margin: -6px 0 12px 0;
  font-size: 12.5px;
  color: #6b7a90;
}

.img-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: #f4f7fa;
  border: 1px solid #edf0f5;
}
.source-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  background: #0b1220;
}
.source-video {
  width: 100%;
  display: block;
  height: 100%;
  background: #0b1220;
}

.relative-container {
  position: relative;
}

.overlay { position: absolute; inset: 0; pointer-events: none; }
.bbox { position: absolute; border: 2px solid #3b9eff; background: rgba(59,158,255,0.08); box-shadow: 0 0 0 1px rgba(255,255,255,0.2) inset; }
.bbox.danger { border-color: #e85c5c; background: rgba(232,92,92,0.10); }
.bbox-label { position: absolute; top: -24px; left: -2px; background: rgba(13, 23, 36, 0.92); color: #fff; font-size: 11px; font-weight: 700; padding: 4px 8px; white-space: nowrap; border-radius: 6px; }

/* ================= 底部操作区 ================= */
.bottom-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  background: #fff;
  border: 1px solid #edf0f5;
  border-radius: 12px;
  padding: 14px 20px;
}

.bottom-right { display: flex; align-items: center; gap: 12px; }
.verify-state { display: inline-flex; align-items: center; gap: 10px; margin-right: 4px; }
.verify-label { font-size: 12px; font-weight: 800; color: #6b7a90; }
.verify-pill {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 900;
  border: 1px solid #edf0f5;
  color: #6b7a90;
  background: #f4f7fa;
}
.verify-pill.pending { color: #d97706; background: rgba(245,166,35,.12); border-color: rgba(245,166,35,.22); }
.verify-pill.verified { color: #2fa576; background: rgba(47,165,118,.12); border-color: rgba(47,165,118,.22); }
.verify-actions { display: inline-flex; align-items: center; gap: 12px; }
.verify-result { display: inline-flex; align-items: center; gap: 10px; margin-right: 2px; }
.verify-result-label { font-size: 12px; font-weight: 800; color: #6b7a90; }
.verify-result-pill {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 900;
  border: 1px solid #edf0f5;
  color: #6b7a90;
  background: #f4f7fa;
}
.verify-result-pill.pass { color: #2fa576; background: rgba(47,165,118,.12); border-color: rgba(47,165,118,.22); }
.verify-result-pill.violation { color: #e85c5c; background: rgba(232,92,92,.12); border-color: rgba(232,92,92,.22); }

.btn-back {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 40px;
  padding: 0 16px;
  border-radius: 10px;
  background: #fff;
  border: 1px solid #e8ecf2;
  color: #4a5568;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.18s;
}
.btn-back:hover { background: #f4f7fa; border-color: #d0e4ff; color: #3b9eff; }

.btn-soft-danger, .btn-soft-success {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 40px;
  padding: 0 18px;
  border-radius: 10px;
  border: 1px solid transparent;
  color: #fff;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.18s;
}
.btn-soft-danger {
  background: #d86161;
  border-color: rgba(216,97,97,0.92);
  box-shadow: 0 6px 16px rgba(216,97,97,0.22);
}
.btn-soft-danger:hover { background: #cf5656; box-shadow: 0 8px 18px rgba(216,97,97,0.26); }
.btn-soft-success {
  background: #2fa576;
  border-color: rgba(47,165,118,0.95);
  box-shadow: 0 6px 16px rgba(47,165,118,0.20);
}
.btn-soft-success:hover { background: #279d6f; box-shadow: 0 8px 18px rgba(47,165,118,0.25); }

.btn-soft-danger:disabled, .btn-soft-success:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  box-shadow: none;
  filter: grayscale(0.15);
}

.btn-cancel-verify {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 16px;
  border-radius: 10px;
  background: #fff;
  border: 1px solid #e8ecf2;
  color: #4a5568;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.18s;
}
.btn-cancel-verify:hover:not(:disabled) { background: #f4f7fa; border-color: #d0e4ff; color: #3b9eff; }
.btn-cancel-verify:disabled { opacity: 0.65; cursor: not-allowed; }
</style>
