<template>
  <div class="tasks-page">
    <div class="page-header">
      <h1 class="page-title">检测任务</h1>
      <p class="page-sub">查看 YOLOv8 + 大模型 对图片与视频的检测结果，并进行人工核实。</p>
    </div>

    <section class="stats-grid">
      <div class="stat-card"><div class="stat-label">总任务数</div><div class="stat-value">{{ stats.total }}</div><div class="stat-sub">全部检测任务</div></div>
      <div class="stat-card"><div class="stat-label">待核实</div><div class="stat-value warn">{{ stats.pending }}</div><div class="stat-sub">待人工核实</div></div>
      <div class="stat-card"><div class="stat-label">已核实</div><div class="stat-value success">{{ stats.verified }}</div><div class="stat-sub">已完成核实</div></div>
      <div class="stat-card"><div class="stat-label">平均置信度</div><div class="stat-value">{{ avgConfidence }}</div><div class="stat-sub">近30天平均</div></div>
    </section>

    <section class="main-grid">
      <div class="panel-card list-card">
        <div class="section-head">
          <h3>任务列表</h3>
          <div class="toolbar">
            <el-input v-model="keyword" placeholder="搜索任务名称、ID" clearable class="toolbar-input" @input="resetPagination" />
            <el-select v-model="typeFilter" class="toolbar-select" @change="resetPagination">
              <el-option label="全部类型" value="all" />
              <el-option label="图片" value="image" />
              <el-option label="视频" value="video" />
            </el-select>
            <el-select v-model="verifyFilter" class="toolbar-select" @change="resetPagination">
              <el-option label="全部状态" value="all" />
              <el-option label="待核实" value="pending" />
              <el-option label="已核实" value="verified" />
            </el-select>
            <el-button @click="loadTasks">刷新</el-button>
          </div>
        </div>

        <el-table :data="pagedTasks" v-loading="loading" empty-text="暂无任务数据" highlight-current-row @current-change="handleCurrentChange" :row-class-name="rowClassName">
          <el-table-column prop="id" width="92">
            <template #header>
              <div class="id-sort-head" @click="toggleIdSortOrder">
                <span>任务ID</span>
                <span class="sort-indicator">{{ idSortOrder === 'asc' ? '↑' : '↓' }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="类型" width="68">
            <template #default="{ row }">{{ row.type === 'video' ? '视频' : '图片' }}</template>
          </el-table-column>
          <el-table-column prop="name" label="任务名称" min-width="150" show-overflow-tooltip />
          <el-table-column label="状态" width="84">
            <template #default="{ row }"><el-tag size="small" :type="statusTag(row.status)" round>{{ statusText(row.status) }}</el-tag></template>
          </el-table-column>
          <el-table-column label="核实状态" width="88">
            <template #default="{ row }"><el-tag size="small" :type="row.verify_status === 'pending' ? 'warning' : 'success'" round>{{ row.verify_status === 'pending' ? '待核实' : '已核实' }}</el-tag></template>
          </el-table-column>
          <el-table-column prop="created_at" label="时间" width="104" />
          <el-table-column label="操作" width="70">
            <template #default="{ row }"><el-button link type="primary" @click="selectTask(row.id)">查看</el-button></template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrap" v-if="filteredTasks.length">
          <div class="pagination-left">共 {{ filteredTasks.length }} 条</div>
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            layout="sizes, prev, pager, next"
            :total="filteredTasks.length"
            small
            @size-change="handlePageSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>

      <div class="panel-card detail-card" v-loading="detailLoading">
        <template v-if="selectedTask">
          <div class="section-head detail-head">
            <h3>任务核实</h3>
            <div class="detail-model">分析引擎：YOLOv8 + {{ selectedTask.model || '大模型' }}</div>
          </div>

          <div class="preview-box image-preview-box" ref="previewBoxRef">
            <template v-if="selectedTask.type === 'image'">
              <img :src="selectedTask.result_url || selectedTask.original_url" class="preview-media" alt="preview" ref="previewImgRef" @load="updatePreviewRect" />
              <div class="bbox-layer" v-if="bboxList.length">
                <div v-for="(box, index) in bboxList" :key="`${box.label}-${index}`" class="bbox-item" :style="bboxStyle(box)">
                  <span class="bbox-tag">{{ box.label }} {{ box.confidenceText }}</span>
                </div>
              </div>
            </template>
            <template v-else>
              <video :src="selectedTask.result_url || selectedTask.original_url" class="preview-media" controls />
              <div class="bbox-layer" v-if="bboxList.length">
                <div v-for="(box, index) in bboxList" :key="`${box.label}-${index}`" class="bbox-item" :style="bboxStyle(box)">
                  <span class="bbox-tag">{{ box.label }} {{ box.confidenceText }}</span>
                </div>
              </div>
            </template>
          </div>

          <div class="detail-info-grid detail-meta-grid">
            <div class="meta-item"><span class="meta-label">任务ID</span><strong class="meta-value">{{ selectedTask.id }}</strong></div>
            <div class="meta-item"><span class="meta-label">置信度</span><strong class="meta-value">{{ confidenceText(selectedTask.confidence) }}</strong></div>
            <div class="meta-item"><span class="meta-label">检测时间</span><strong class="meta-value">{{ selectedTask.created_at }}</strong></div>
            <div class="meta-item"><span class="meta-label">模型</span><strong class="meta-value">{{ selectedTask.model }}</strong></div>
            <div class="meta-item"><span class="meta-label">类型</span><strong class="meta-value">{{ selectedTask.type === 'video' ? '视频' : '图片' }}</strong></div>
            <div class="meta-item"><span class="meta-label">文件</span><strong class="meta-value ellipsis">{{ fileNameFromUrl(selectedTask.original_url) }}</strong></div>
          </div>

          <div class="analysis-box summary-box">
            <div class="analysis-title">AI 分析结论</div>
            <p>{{ latestReport }}</p>
          </div>

          <div class="verify-box verify-panel">
            <div class="verify-title">人工核实</div>
            <el-radio-group v-model="verifyChoice" class="verify-radios">
              <el-radio value="violation">确认违规</el-radio>
              <el-radio value="pass">误报</el-radio>
              <el-radio value="pending">待复核</el-radio>
            </el-radio-group>
            <el-input v-model="verifyNote" type="textarea" :rows="3" placeholder="请输入核实备注（选填）" maxlength="200" show-word-limit />
            <div class="verify-actions verify-action-row">
              <el-button type="primary" :loading="verifyLoading" @click="submitVerify('pass')">确认核实</el-button>
              <el-button :loading="verifyLoading" @click="submitVerify('violation')">标记误报</el-button>
            </div>
          </div>
        </template>
        <el-empty v-else description="请选择左侧任务查看详情" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const loading = ref(false)
const detailLoading = ref(false)
const verifyLoading = ref(false)
const tasks = ref([])
const selectedTask = ref(null)
const keyword = ref('')
const typeFilter = ref('all')
const verifyFilter = ref('all')
const verifyChoice = ref('pending')
const verifyNote = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const idSortOrder = ref('desc')
const previewBoxRef = ref(null)
const previewImgRef = ref(null)
const previewRect = ref({ offsetX: 0, offsetY: 0, drawW: 0, drawH: 0 })

const authHeaders = () => {
  const access = localStorage.getItem('access_token') || ''
  return access ? { Authorization: `Bearer ${access}` } : {}
}

const stats = computed(() => ({
  total: tasks.value.length,
  pending: tasks.value.filter((t) => t.verify_status === 'pending').length,
  verified: tasks.value.filter((t) => t.verify_status === 'verified').length,
}))

const avgConfidence = computed(() => {
  if (!tasks.value.length) return '0.00'
  const sum = tasks.value.reduce((acc, item) => acc + Number(item.confidence || 0), 0)
  return (sum / tasks.value.length).toFixed(2)
})

const filteredTasks = computed(() => {
  const list = tasks.value.filter((item) => {
    const kw = keyword.value.trim().toLowerCase()
    const matchKeyword = !kw || String(item.id).includes(kw) || String(item.name || '').toLowerCase().includes(kw)
    const matchType = typeFilter.value === 'all' || item.type === typeFilter.value
    const matchVerify = verifyFilter.value === 'all' || item.verify_status === verifyFilter.value
    return matchKeyword && matchType && matchVerify
  })
  return [...list].sort((a, b) => idSortOrder.value === 'asc' ? Number(a.id) - Number(b.id) : Number(b.id) - Number(a.id))
})

const pagedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredTasks.value.slice(start, start + pageSize.value)
})

const latestReport = computed(() => selectedTask.value?.records?.[0]?.llm_report || 'AI 已完成检测，请结合画面与目标框信息进行人工核实。')

const bboxList = computed(() => {
  const dets = selectedTask.value?.detections
  if (!Array.isArray(dets)) return []
  return dets
    .filter((item) => item && typeof item === 'object')
    .map((item) => ({
      label: item.label || (Number(item.cls) === 0 ? '吸烟行为' : `目标${item.cls ?? ''}`),
      conf: Number(item.conf || 0),
      confidenceText: Number(item.conf || 0).toFixed(2),
      x: Number(item.x || 0),
      y: Number(item.y || 0),
      w: Number(item.w || 0),
      h: Number(item.h || 0),
    }))
})

const statusText = (status) => ({ processing: '检测中', completed: '已完成', failed: '任务中断', pending: '等待中' }[status] || '等待中')
const statusTag = (status) => status === 'completed' ? 'success' : status === 'failed' ? 'danger' : 'warning'
const confidenceText = (value) => typeof value === 'number' ? value.toFixed(2) : '-'
const fileNameFromUrl = (url) => (url || '').split('/').pop() || '-'
const rowClassName = ({ row }) => selectedTask.value?.id === row.id ? 'current-row' : ''

const updatePreviewRect = () => {
  const container = previewBoxRef.value
  const img = previewImgRef.value
  if (!container || !img || !img.naturalWidth || !img.naturalHeight) return
  const cw = container.clientWidth
  const ch = container.clientHeight
  const iw = img.naturalWidth
  const ih = img.naturalHeight
  const scale = Math.min(cw / iw, ch / ih)
  const drawW = iw * scale
  const drawH = ih * scale
  previewRect.value = {
    offsetX: (cw - drawW) / 2,
    offsetY: (ch - drawH) / 2,
    drawW,
    drawH,
  }
}

const bboxStyle = (box) => {
  const rect = previewRect.value
  if (!rect.drawW || !rect.drawH) {
    return {
      left: `${box.x}%`,
      top: `${box.y}%`,
      width: `${box.w}%`,
      height: `${box.h}%`,
    }
  }
  return {
    left: `${rect.offsetX + (box.x / 100) * rect.drawW}px`,
    top: `${rect.offsetY + (box.y / 100) * rect.drawH}px`,
    width: `${(box.w / 100) * rect.drawW}px`,
    height: `${(box.h / 100) * rect.drawH}px`,
  }
}

const updatePreviewRectByResolution = () => {
  const container = previewBoxRef.value
  const task = selectedTask.value
  const rw = Number(task?.resolution?.w || 0)
  const rh = Number(task?.resolution?.h || 0)
  if (!container || !rw || !rh) return
  const cw = container.clientWidth
  const ch = container.clientHeight
  const scale = Math.min(cw / rw, ch / rh)
  const drawW = rw * scale
  const drawH = rh * scale
  previewRect.value = {
    offsetX: (cw - drawW) / 2,
    offsetY: (ch - drawH) / 2,
    drawW,
    drawH,
  }
}

const loadTasks = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/detection/tasks', { headers: authHeaders() })
    tasks.value = data?.results || []
    if (!selectedTask.value && tasks.value.length) await selectTask(tasks.value[0].id)
    if (selectedTask.value && !tasks.value.some((item) => item.id === selectedTask.value.id) && tasks.value.length) {
      await selectTask(tasks.value[0].id)
    }
  } finally {
    loading.value = false
    requestAnimationFrame(() => {
      updatePreviewRect()
      updatePreviewRectByResolution()
    })
  }
}

const selectTask = async (id) => {
  if (!id) return
  detailLoading.value = true
  try {
    const { data } = await axios.get(`/api/detection/tasks/${id}`, { headers: authHeaders() })
    selectedTask.value = data || null
    verifyChoice.value = data?.verify_status === 'pending' ? 'pending' : (data?.verify_result || 'pass')
    verifyNote.value = ''
  } finally {
    detailLoading.value = false
    requestAnimationFrame(() => {
      updatePreviewRect()
      updatePreviewRectByResolution()
    })
  }
}

const handleCurrentChange = (row) => {
  if (row?.id) selectTask(row.id)
}

const resetPagination = () => {
  currentPage.value = 1
}

const handlePageChange = (page) => {
  currentPage.value = page
}

const handlePageSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const toggleIdSortOrder = () => {
  idSortOrder.value = idSortOrder.value === 'asc' ? 'desc' : 'asc'
  currentPage.value = 1
}

const submitVerify = async (mode) => {
  if (!selectedTask.value?.id) return ElMessage.warning('请先选择任务')
  verifyLoading.value = true
  try {
    const payload = mode === 'pass'
      ? { verify_status: 'verified', verify_result: 'pass' }
      : { verify_status: 'verified', verify_result: 'violation' }
    await axios.patch(`/api/detection/tasks/${selectedTask.value.id}/verify`, payload, { headers: authHeaders() })
    ElMessage.success('核实结果已提交')
    await loadTasks()
    await selectTask(selectedTask.value.id)
  } finally {
    verifyLoading.value = false
  }
}

onMounted(() => {
  loadTasks()
  window.addEventListener('resize', updatePreviewRect)
  window.addEventListener('resize', updatePreviewRectByResolution)
})

onUnmounted(() => {
  window.removeEventListener('resize', updatePreviewRect)
  window.removeEventListener('resize', updatePreviewRectByResolution)
})
</script>

<style scoped>
.tasks-page{width:100%;max-width:100%;overflow-x:hidden;color:#1a2332;padding-bottom:8px}.page-header{margin-bottom:18px}.page-title{font-size:22px;font-weight:700;color:#0d1724;margin-bottom:6px}.page-sub{font-size:13px;color:#6b7a90;margin:0}.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:18px}.stat-card{background:#fff;border:1px solid #edf0f5;border-radius:14px;padding:18px 20px}.stat-label{font-size:12px;color:#8a97ab;margin-bottom:8px}.stat-value{font-size:28px;font-weight:700;color:#132033;line-height:1}.stat-value.success{color:#16a34a}.stat-value.warn{color:#f59e0b}.stat-sub{margin-top:8px;font-size:12px;color:#9aa5b4}.main-grid{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(380px,.98fr);gap:18px;align-items:start}.panel-card{background:#fff;border:1px solid #edf0f5;border-radius:14px;padding:18px 18px 16px;min-width:0;height:auto}.list-card,.detail-card{display:flex;flex-direction:column;min-width:0}.detail-card{position:sticky;top:92px;align-self:start}.section-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:14px}.section-head h3{font-size:18px;margin:0;color:#132033}.toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.toolbar-input{width:180px}.toolbar-select{width:96px}.id-sort-head{display:inline-flex;align-items:center;gap:4px;cursor:pointer;user-select:none}.sort-indicator{font-size:12px;color:#3b82f6;font-weight:700}.detail-head{margin-bottom:14px}.detail-model{font-size:12px;color:#8a97ab;padding-top:4px}.image-preview-box{position:relative;height:260px;border-radius:12px;overflow:hidden;background:#f6f8fb;border:1px solid #edf0f5;margin-bottom:16px;flex-shrink:0}.preview-media{width:100%;height:100%;object-fit:contain;display:block;background:#f6f8fb}.bbox-layer{position:absolute;inset:0;pointer-events:none}.bbox-item{position:absolute;border:2px solid #ef4444;box-shadow:0 0 0 1px rgba(255,255,255,.25) inset}.bbox-tag{position:absolute;left:-2px;top:-28px;background:#ef4444;color:#fff;font-size:12px;line-height:1;padding:6px 8px;border-radius:8px 8px 8px 2px;font-weight:600;white-space:nowrap}.detail-meta-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px 18px;margin-bottom:18px}.meta-item{min-width:0;display:flex;flex-direction:column;gap:4px}.meta-label{font-size:12px;color:#98a2b3;line-height:1.2}.meta-value{font-size:14px;font-weight:600;color:#1f2937;line-height:1.5;min-width:0}.ellipsis{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.summary-box{border:none;background:#f7fbff;border:1px solid #dbeafe;border-radius:14px;padding:16px 16px 14px;margin-bottom:16px}.analysis-title,.verify-title{font-size:15px;font-weight:700;color:#132033;margin-bottom:10px}.summary-box p{font-size:13px;line-height:1.8;color:#4f6177;margin:0}.verify-panel{border-top:1px solid #eef2f6;padding-top:16px;margin-top:auto}.verify-radios{display:flex;flex-wrap:wrap;gap:18px;margin-bottom:14px}.verify-panel :deep(.el-radio__label){font-size:13px;color:#475569}.verify-panel :deep(.el-textarea__inner){border-radius:12px;min-height:92px}.verify-action-row{display:flex;justify-content:flex-end;gap:10px;margin-top:14px}.pagination-wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:12px;margin-top:8px;border-top:1px solid #f1f5f9}.pagination-left{font-size:12px;color:#8a97ab;white-space:nowrap}.list-card :deep(.el-table){width:100%}.list-card :deep(.el-table th.el-table__cell){background:#f8fafc;color:#64748b;font-size:12px;font-weight:600}.list-card :deep(.el-table td.el-table__cell){font-size:13px;padding-top:10px;padding-bottom:10px}.list-card :deep(.current-row td){background:#f5f9ff !important}.list-card :deep(.el-table__inner-wrapper::before){display:none}.list-card :deep(.cell){white-space:nowrap}.list-card :deep(.el-tag){max-width:100%}.pagination-wrap :deep(.el-pagination){gap:6px}.pagination-wrap :deep(.el-pagination__sizes .el-select .el-input__wrapper){border-radius:10px;box-shadow:none;border:1px solid #e5e7eb;background:#fff;min-height:32px}.pagination-wrap :deep(.btn-prev),.pagination-wrap :deep(.btn-next),.pagination-wrap :deep(.el-pager li){min-width:32px;height:32px;line-height:32px;border-radius:10px;border:1px solid #e5e7eb;background:#fff;color:#475569;font-weight:600;margin:0;transition:all .18s ease}.pagination-wrap :deep(.el-pager li.is-active){background:#3b82f6;border-color:#3b82f6;color:#fff;box-shadow:0 6px 14px rgba(59,130,246,.18)}.pagination-wrap :deep(.btn-prev:hover),.pagination-wrap :deep(.btn-next:hover),.pagination-wrap :deep(.el-pager li:hover){color:#2563eb;border-color:#bfdbfe;background:#f8fbff}.pagination-wrap :deep(.btn-prev:disabled),.pagination-wrap :deep(.btn-next:disabled){opacity:.45;background:#f8fafc;color:#94a3b8}.pagination-wrap :deep(.el-pagination__jump),.pagination-wrap :deep(.el-pagination__total){color:#94a3b8;font-size:12px}@media (max-width:1280px){.stats-grid{grid-template-columns:repeat(2,1fr)}.main-grid{grid-template-columns:minmax(0,1fr)}.detail-card{position:static;top:auto}.toolbar-input{width:220px}.toolbar-select{width:110px}.image-preview-box{height:300px}}@media (max-width:768px){.stats-grid,.detail-meta-grid{grid-template-columns:1fr}.verify-action-row,.pagination-wrap{flex-direction:column;align-items:stretch}.toolbar{align-items:stretch}.toolbar-input,.toolbar-select{width:100%}.pagination-left{text-align:center}.bbox-tag{font-size:11px;padding:5px 7px}}
</style>
