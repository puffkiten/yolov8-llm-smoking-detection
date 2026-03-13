<template>
  <div class="dashboard-content" v-loading.fullscreen.lock="pageLoading" element-loading-text="正在加载实时监控数据...">
    
    <div class="page-header">
      <div>
        <h1 class="page-title">概览仪表板</h1>
        <p class="page-sub">欢迎回来，这是您今天的系统运行快报。</p>
      </div>
      <div class="page-actions">
        <BaseButton type="primary" @click="openNewDetection" :disabled="isLoading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          发起新检测
        </BaseButton>
        <div class="refresh-wrap">
          <BaseButton type="primary" @click="fetchDashboardData" :disabled="isLoading">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{'spinning': isLoading}">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-5.05"/>
            </svg>
            {{ isLoading ? '刷新中...' : '刷新数据' }}
          </BaseButton>
          <div class="refresh-tip" v-if="lastRefreshedAt">上次刷新 {{ lastRefreshedAt }}</div>
        </div>
      </div>
    </div>

    <el-dialog v-model="newDetectionVisible" title="发起新检测" width="520px">
      <div class="nd-form">
        <div class="nd-row">
          <div class="nd-label">任务名称</div>
          <el-input v-model="newDetectionForm.name" placeholder="例：车间二号位下午时段监控" />
        </div>
        <div class="nd-row">
          <div class="nd-label">检测类型</div>
          <el-radio-group v-model="newDetectionForm.type">
            <el-radio-button label="video">视频检测</el-radio-button>
            <el-radio-button label="image">图片检测</el-radio-button>
          </el-radio-group>
        </div>
        <div class="nd-row">
          <div class="nd-label">置信度阈值</div>
          <div style="display:flex; gap:12px; align-items:center; width:100%;">
            <el-slider v-model="newDetectionForm.confidence" :min="0" :max="1" :step="0.01" style="flex:1;" />
            <span class="nd-val">{{ newDetectionForm.confidence.toFixed(2) }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <div style="display:flex; justify-content:flex-end; gap:10px;">
          <BaseButton type="default" @click="newDetectionVisible = false">取消</BaseButton>
          <BaseButton type="primary" @click="submitNewDetection">去上传并开始</BaseButton>
        </div>
      </template>
    </el-dialog>

    <div class="stats-grid">
      <div class="stat-card" v-loading="isLoading">
        <div class="stat-top">
          <div class="stat-icon blue">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
          </div>
          <span class="stat-trend" :class="getTrendClass(stats.totalTrend)">{{ stats.totalTrend || '--' }}</span>
        </div>
        <p class="stat-label">总检测任务数</p>
        <p class="stat-value">{{ stats.total || '--' }}</p>
      </div>
      <div class="stat-card" v-loading="isLoading">
        <div class="stat-top">
          <div class="stat-icon orange">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
          </div>
          <span class="stat-trend" :class="getTrendClass(stats.todayTrend)">{{ stats.todayTrend || '--' }}</span>
        </div>
        <p class="stat-label">今日检测数</p>
        <p class="stat-value">{{ stats.today || '--' }}</p>
      </div>
      <div class="stat-card" v-loading="isLoading">
        <div class="stat-top">
          <div class="stat-icon teal">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <span class="stat-trend" :class="getTrendClass(stats.avgTimeTrend)">{{ stats.avgTimeTrend || '--' }}</span>
        </div>
        <p class="stat-label">平均处理时间</p>
        <p class="stat-value">{{ stats.avgTime || '--' }}</p>
      </div>
      <div class="stat-card" v-loading="isLoading">
        <div class="stat-top">
          <div class="stat-icon purple">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <span class="stat-trend stable">{{ stats.uptimeTrend || '--' }}</span>
        </div>
        <p class="stat-label">系统可用性</p>
        <p class="stat-value">{{ stats.uptime || '--' }}</p>
      </div>
    </div>

    <div class="charts-row">
      <div class="chart-card large">
        <div class="chart-header">
          <div>
            <h3 class="chart-title">检测趋势分析</h3>
            <p class="chart-sub">任务总量与违规事件统计</p>
          </div>
          <div class="chart-actions">
            <div class="range-tabs">
              <button class="range-tab" :class="{ active: rangePreset === '1h' }" @click="setRange('1h')">1小时</button>
              <button class="range-tab" :class="{ active: rangePreset === '1d' }" @click="setRange('1d')">1天</button>
              <button class="range-tab" :class="{ active: rangePreset === '1w' }" @click="setRange('1w')">1周</button>
            </div>
          </div>
        </div>
        <div class="chart-area" ref="trendChartRef"></div>
      </div>

      <div class="chart-card small" v-loading="isLoading">
        <div class="chart-header">
          <div>
            <h3 class="chart-title">检测类型对比</h3>
            <p class="chart-sub">不同媒介的任务处理分布比例</p>
          </div>
        </div>
        <div v-if="typeTotalCount === 0" class="empty-text">暂无数据</div>
        <div v-else class="pie-area" ref="typeChartRef"></div>
      </div>
    </div>

    <div class="bottom-row">
      <div class="bottom-card tasks" v-loading="isLoading">
        <div class="card-header">
          <h3 class="card-title">最近任务状态</h3>
          <a href="#" class="card-link">查看全部 →</a>
        </div>
        <div v-if="tasks.length === 0" class="empty-text" style="text-align: center; padding: 30px;">暂无任务数据</div>
        <el-table v-else :data="tasks" size="small" style="width: 100%">
          <el-table-column prop="id" label="任务ID" width="90" />
          <el-table-column prop="typeText" label="类型" width="90" />
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="statusTagType(row.status)" effect="light">{{ statusTextCn(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="核实状态" width="110">
            <template #default="{ row }">
              <el-tag :type="verifyTagType(row.verify_status)" effect="light">{{ verifyTextCn(row.verify_status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="时间" min-width="140">
            <template #default="{ row }">{{ formatShortTime(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="right">
            <template #default="{ row }">
              <el-button v-if="row.verify_status === 'pending'" type="primary" size="small" @click="goVerify(row)">去核实</el-button>
              <span v-else style="color:#9aa5b4; font-size:12px;">—</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="bottom-card log" v-loading="isLoading">
        <div class="card-header">
          <h3 class="card-title">系统动态日志</h3>
        </div>
        <div class="log-list">
          <div v-if="logs.length === 0" class="empty-text" style="text-align: center; padding: 30px;">暂无日志记录</div>
          <div class="log-item" v-for="log in logs" :key="log.id">
            <span class="log-dot blue"></span>
            <div class="log-content">
              <div class="log-top">
                <span class="log-user">{{ log.operator }}</span>
                <span class="log-time">{{ log.time }}</span>
              </div>
              <p class="log-desc">{{ log.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-col-right">
        <div class="bottom-card status-card" v-loading="isLoading">
          <div class="status-header">
            <div class="status-icon-wrap" :class="systemStatus.status === 'ok' ? 'ok-bg' : 'error-bg'">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
            </div>
            <div>
              <p class="status-title">{{ systemStatus.title || '系统状态检测中...' }}</p>
              <p class="status-sub">{{ systemStatus.description || '正在拉取核心服务节点状态' }}</p>
            </div>
          </div>
        </div>

        <div class="bottom-card quick-card">
          <h3 class="card-title" style="margin-bottom:14px">快捷操作入口</h3>
          <div class="quick-grid">
            <div class="quick-item" @click="$router.push('/camera/realtime')">
              <div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M23 7 16 12 23 17V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div>
              <span class="quick-label">实时监控</span>
            </div>
            <div class="quick-item" @click="$router.push('/camera/config')">
              <div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></div>
              <span class="quick-label">配置中心</span>
            </div>
            <div class="quick-item" @click="$router.push('/detection/tasks')">
              <div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
              <span class="quick-label">检测记录</span>
            </div>
            <div class="quick-item" @click="$router.push('/system/users')">
              <div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
              <span class="quick-label">成员管理</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, reactive } from 'vue'
import * as echarts from 'echarts'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

const newDetectionVisible = ref(false)
const newDetectionForm = reactive({
  name: '',
  type: 'video',
  confidence: 0.75,
})

const openNewDetection = () => {
  if (!newDetectionForm.name) {
    newDetectionForm.name = `新检测_${new Date().toLocaleString('zh-CN', { hour12: false }).replace(/[/:]/g, '-').slice(0, 16)}`
  }
  newDetectionVisible.value = true
}

const submitNewDetection = () => {
  if (!newDetectionForm.name.trim()) {
    ElMessage.warning('请输入任务名称')
    return
  }
  newDetectionVisible.value = false
  ElMessage.success('已进入上传页面（后端接入后即可真正创建任务）')
  router.push('/detection/upload')
}

const pageLoading = ref(true)
const isLoading = ref(false)
const lastRefreshedAt = ref('')
const rangePreset = ref('1d')
const rawItems = ref([])

const stats = ref({ total: '', totalTrend: '', today: '', todayTrend: '', avgTime: '', avgTimeTrend: '', uptime: '', uptimeTrend: '' })
const typeStats = ref([])
const typeTotalCount = ref(0)
const tasks = ref([])
const logs = ref([])
const systemStatus = ref({ title: '', description: '', status: '' })

const trendChartRef = ref(null)
const typeChartRef = ref(null)
let trendChart = null
let typeChart = null
let resizeHandler = null

const getTrendClass = (trendStr) => {
  if (!trendStr) return 'stable'
  if (trendStr.includes('+') || trendStr.includes('↗')) return 'up'
  if (trendStr.includes('-') || trendStr.includes('↘')) return 'down'
  return 'stable'
}

const renderChart = (xAxisData, seriesTotal, seriesSmoke, xAxisLabel) => {
  if (!trendChartRef.value) return
  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value)
    resizeHandler = () => {
      if (trendChart) {
        trendChart.resize()
      }
      if (typeChart) {
        typeChart.resize()
      }
    }
    window.addEventListener('resize', resizeHandler)
  }
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { top: 0, right: 0, itemWidth: 10, itemHeight: 10, textStyle: { color: '#6b7a90', fontSize: 12, fontWeight: 700 } },
    grid: { top: 30, right: 20, bottom: 20, left: 40 },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLine: { lineStyle: { color: '#e8ecf2' } },
      axisLabel: xAxisLabel || {}
    },
    yAxis: { type: 'value', minInterval: 1, splitLine: { lineStyle: { type: 'dashed', color: '#f0f3f8' } } },
    series: [
      { name: 'AI 告警数', type: 'line', smooth: true, data: seriesTotal, itemStyle: { color: '#3b9eff' }, symbolSize: 6 },
      { name: '待核实数', type: 'bar', data: seriesSmoke, barWidth: 18, itemStyle: { color: '#f5a623', borderRadius: [6, 6, 0, 0] } }
    ]
  })
}

const renderTypePie = (videoCount, imageCount) => {
  if (!typeChartRef.value) return
  if (!typeChart) {
    typeChart = echarts.init(typeChartRef.value)
  }
  typeChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, left: 'center' },
    series: [
      {
        type: 'pie',
        radius: ['40%', '68%'],
        avoidLabelOverlap: true,
        label: { formatter: '{b}\n{d}%', fontWeight: 700 },
        labelLine: { length: 10, length2: 8 },
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        data: [
          { value: videoCount, name: '视频流检测', itemStyle: { color: '#3b9eff' } },
          { value: imageCount, name: '离线图片检测', itemStyle: { color: '#00bca4' } },
        ]
      }
    ]
  })
}

const authHeaders = () => {
  const access = localStorage.getItem('access_token') || ''
  return access ? { Authorization: `Bearer ${access}` } : {}
}

const pad2 = (n) => (n < 10 ? '0' + n : '' + n)
const todayKey = () => {
  const d = new Date()
  return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`
}
const tsOf = (iso) => {
  const t = iso ? new Date(iso).getTime() : 0
  return Number.isFinite(t) ? t : 0
}
const formatClock = (d) => `${pad2(d.getHours())}:${pad2(d.getMinutes())}:${pad2(d.getSeconds())}`

const _rangeMs = () => {
  if (rangePreset.value === '1h') return 60 * 60 * 1000
  if (rangePreset.value === '1d') return 24 * 60 * 60 * 1000
  return 7 * 24 * 60 * 60 * 1000
}

const setRange = (preset) => {
  rangePreset.value = preset
  recomputeDashboard()
  fetchTrend()
}

const statusTextCn = (s) => s === 'completed' ? '已完成' : s === 'failed' ? '检测中断' : '检测中'
const statusTagType = (s) => s === 'completed' ? 'success' : s === 'failed' ? 'danger' : 'warning'
const verifyTextCn = (s) => s === 'pending' ? '待核实' : '已核实'
const verifyTagType = (s) => s === 'pending' ? 'warning' : 'success'
const formatShortTime = (v) => {
  const s = (v || '').toString()
  if (!s) return ''
  const m = s.match(/(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/)
  if (m) return `${m[2]}-${m[3]} ${m[4]}:${m[5]}`
  if (s.length >= 16 && s.includes('-') && s.includes(':')) return s.slice(5, 16)
  return s
}
const goVerify = (row) => {
  router.push('/task/detail/' + row.id)
}

const fetchTrend = async () => {
  try {
    const resp = await axios.get('http://127.0.0.1:8000/api/dashboard/trend', {
      headers: authHeaders(),
      params: { preset: rangePreset.value }
    })
    const d = resp.data || {}
    const labels = Array.isArray(d.labels) ? d.labels : []
    const ai = Array.isArray(d.ai_alerts) ? d.ai_alerts : []
    const pending = Array.isArray(d.pending_verifications) ? d.pending_verifications : []
    const xAxisLabel = rangePreset.value === '1d' ? { interval: 2 } : { interval: 0 }
    renderChart(labels, ai, pending, xAxisLabel)
  } catch (e) {
    renderChart([], [], [], {})
  }
}

const recomputeDashboard = () => {
  const items = Array.isArray(rawItems.value) ? rawItems.value : []
  const now = Date.now()
  const cutoff = now - _rangeMs()
  const inRange = (it) => {
    const iso = it.finished_at_iso || it.created_at_iso || ''
    const t = tsOf(iso)
    return t ? t >= cutoff : false
  }

  const total = items.length
  const tKey = todayKey()
  const today = items.filter(it => (it.created_at_iso || '').slice(0, 10) === tKey).length

  const completedInRange = items.filter(it => it.status === 'completed' && inRange(it))
  const avgMsArr = completedInRange.map(it => Number(it.process_time_ms || 0)).filter(ms => Number.isFinite(ms) && ms > 0)
  const avgTimeMs = avgMsArr.length ? Math.round(avgMsArr.reduce((a, b) => a + b, 0) / avgMsArr.length) : 0
  const avgTime = avgTimeMs ? (avgTimeMs / 1000).toFixed(2) + 's' : '--'

  stats.value = {
    total: String(total),
    totalTrend: '',
    today: String(today),
    todayTrend: '',
    avgTime,
    avgTimeTrend: '',
    uptime: '99.9%',
    uptimeTrend: '稳定'
  }

  const videoCount = items.filter(i => i.type === 'video').length
  const imageCount = items.filter(i => i.type === 'image').length
  typeTotalCount.value = videoCount + imageCount
  const denom = Math.max(1, videoCount + imageCount)
  typeStats.value = [
    { label: '视频流检测', percent: Math.round((videoCount / denom) * 100) },
    { label: '离线图片检测', percent: Math.round((imageCount / denom) * 100) },
  ]
  if (typeTotalCount.value > 0) {
    renderTypePie(videoCount, imageCount)
  }

  tasks.value = items.slice(0, 8).map(it => ({
    id: it.id,
    name: it.name,
    type: it.type,
    typeText: it.type === 'video' ? '视频流' : '图片',
    status: it.status,
    verify_status: it.verify_status || 'verified',
    created_at: it.created_at
  }))

  logs.value = items.slice(0, 6).map(it => ({
    id: it.id,
    operator: '系统',
    description: `任务 ${it.name} ${statusTextCn(it.status)}`,
    time: it.created_at
  }))
}

const fetchDashboardData = async () => {
  isLoading.value = true
  if (trendChart) trendChart.showLoading({ text: '数据拉取中...', color: '#3b9eff' })
  
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/detection/tasks', { headers: authHeaders() })
    rawItems.value = Array.isArray(res.data?.results) ? res.data.results : []
    recomputeDashboard()
    await fetchTrend()
    const now = new Date()
    lastRefreshedAt.value = formatClock(now)
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('刷新失败，请检查网络或登录状态')
  } finally {
    isLoading.value = false
    pageLoading.value = false
    if (trendChart) trendChart.hideLoading()
  }
}

onMounted(() => {
  fetchDashboardData()
})

onUnmounted(() => {
  if (trendChart) {
    trendChart.dispose()
    trendChart = null
  }
  if (typeChart) {
    typeChart.dispose()
    typeChart = null
  }
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
    resizeHandler = null
  }
})
</script>

<style scoped>
/* 继承你之前的样式，新增了骨架屏和空状态需要的样式 */
.dashboard-content { width: 100%; }

.empty-text { font-size: 13px; color: #9aa5b4; margin-top: 10px;}
.spinning { animation: spin 1s linear infinite; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 24px; }
.page-title { font-size: 22px; font-weight: 700; color: #0d1724; letter-spacing: -.4px; margin-bottom: 4px; }
.page-sub   { font-size: 13.5px; color: #7a8896; }
.page-actions { display: flex; gap: 10px; align-items: center; }
.refresh-wrap { position: relative; display: inline-flex; }
.refresh-tip {
  position: absolute;
  top: 44px;
  right: 0;
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid #edf0f5;
  background: #fff;
  color: #6b7a90;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 12px 32px rgba(17, 27, 39, 0.12);
  opacity: 0;
  transform: translateY(-6px);
  pointer-events: none;
  transition: all .18s;
  white-space: nowrap;
  z-index: 10;
}
.refresh-wrap:hover .refresh-tip { opacity: 1; transform: translateY(0); }

.nd-form { display: grid; gap: 14px; }
.nd-row { display: grid; gap: 8px; }
.nd-label { font-size: 13px; font-weight: 600; color: #374151; }
.nd-val { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; color: #1f2937; font-weight: 700; }
.btn-refresh {
  display: flex; align-items: center; gap: 6px; padding: 8px 16px;
  background: #fff; border: 1px solid #dde5ee; border-radius: 8px;
  font-size: 13.5px; font-weight: 500; color: #4a5568; cursor: pointer;
  font-family: inherit; transition: all .2s;
}
.btn-refresh:hover:not(:disabled) { border-color: #3b9eff; color: #3b9eff; }
.btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-new {
  display: flex; align-items: center; gap: 6px; padding: 8px 18px;
  background: #3b9eff; border: none; border-radius: 8px;
  font-size: 13.5px; font-weight: 600; color: white; cursor: pointer;
  font-family: inherit; transition: all .2s;
}
.btn-new:hover { background: #2a8aee; box-shadow: 0 4px 14px rgba(59,158,255,.3); }

/* STATS */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
.stat-card { background: #fff; border-radius: 12px; padding: 18px 20px; border: 1px solid #edf0f5; min-height: 115px;}
.stat-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.stat-icon { width: 36px; height: 36px; border-radius: 9px; display: flex; align-items: center; justify-content: center; }
.stat-icon.blue   { background: rgba(59,158,255,.1);  color: #3b9eff; }
.stat-icon.orange { background: rgba(245,166,35,.1);  color: #f5a623; }
.stat-icon.teal   { background: rgba(0,188,164,.1);   color: #00bca4; }
.stat-icon.purple { background: rgba(124,92,232,.1);  color: #7c5ce8; }
.stat-trend { font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
.stat-trend.up     { color: #16a34a; background: #f0fdf4; }
.stat-trend.down   { color: #3b9eff; background: #eff6ff; }
.stat-trend.stable { color: #7a8896; background: #f4f7fa; }
.stat-label { font-size: 12.5px; color: #7a8896; margin-bottom: 6px; }
.stat-value { font-size: 26px; font-weight: 700; color: #0d1724; letter-spacing: -.5px; line-height: 1; }

/* CHARTS */
.charts-row { display: grid; grid-template-columns: 1fr 300px; gap: 16px; margin-bottom: 20px; }
.chart-card { background: #fff; border-radius: 12px; padding: 20px; border: 1px solid #edf0f5; }
.chart-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 16px; }
.chart-title { font-size: 15px; font-weight: 700; color: #0d1724; margin-bottom: 3px; }
.chart-sub   { font-size: 12px; color: #9aa5b4; }
.chart-link  { font-size: 12.5px; color: #3b9eff; text-decoration: none; font-weight: 500; }
.chart-link:hover { opacity: .75; }
.chart-area  { height: 260px; width: 100%;}
.chart-actions { display: flex; align-items: center; gap: 10px; }
.range-tabs { display: inline-flex; gap: 6px; padding: 3px; border: 1px solid #edf0f5; border-radius: 999px; background: #fff; }
.range-tab {
  height: 28px;
  padding: 0 10px;
  border: none;
  border-radius: 999px;
  background: transparent;
  color: #6b7a90;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all .18s;
}
.range-tab:hover { background: #f4f7fa; color: #1a2332; }
.range-tab.active { background: #eff6ff; color: #3b9eff; }

.pie-area { height: 240px; width: 100%; }

/* BOTTOM */
.bottom-row { display: grid; grid-template-columns: 1fr 1fr 260px; gap: 16px; }
.bottom-card { background: #fff; border-radius: 12px; padding: 20px; border: 1px solid #edf0f5; min-height: 250px;}
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.card-title  { font-size: 15px; font-weight: 700; color: #0d1724; }
.card-link   { font-size: 12.5px; color: #3b9eff; text-decoration: none; font-weight: 500; }

.task-table  { width: 100%; border-collapse: collapse; }
.task-table th { font-size: 12px; color: #9aa5b4; font-weight: 500; text-align: left; padding: 0 0 10px; border-bottom: 1px solid #f0f3f8; }
.task-table td { padding: 12px 0; font-size: 13px; color: #2d3a4a; border-bottom: 1px solid #f8f9fc; }
.task-table tr:last-child td { border-bottom: none; }
.task-id   { font-weight: 600; color: #1a2332; }
.task-time { color: #9aa5b4; }
.status-tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.status-tag.progress { background: #eff6ff; color: #3b9eff; }
.status-tag.done     { background: #f0fdf4; color: #16a34a; }
.status-tag.alert    { background: #fff1f0; color: #e85c5c; }

.log-list { display: flex; flex-direction: column; gap: 16px; }
.log-item { display: flex; gap: 12px; align-items: flex-start; }
.log-dot  { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
.log-dot.blue { background: #3b9eff; }
.log-content { flex: 1; }
.log-top  { display: flex; justify-content: space-between; margin-bottom: 3px; }
.log-user { font-size: 13px; font-weight: 600; color: #1a2332; }
.log-time { font-size: 11.5px; color: #b0bcc8; }
.log-desc { font-size: 12.5px; color: #6b7a90; line-height: 1.5; }

.bottom-col-right { display: flex; flex-direction: column; gap: 14px; }
.status-header { display: flex; align-items: flex-start; gap: 12px; }
.status-icon-wrap { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #fff; }
.ok-bg { background: #3b9eff; }
.error-bg { background: #e85c5c; }
.status-title { font-size: 14px; font-weight: 700; color: #0d1724; margin-bottom: 4px; }
.status-sub   { font-size: 12px; color: #7a8896; line-height: 1.5; }
.quick-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.quick-item { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 14px 8px; background: #f8fafd; border: 1px solid #edf0f5; border-radius: 10px; cursor: pointer; transition: all .18s; }
.quick-item:hover { background: #eff6ff; border-color: #c8dfff; }
.quick-icon { width: 36px; height: 36px; background: rgba(59,158,255,.1); border-radius: 9px; display: flex; align-items: center; justify-content: center; }
.quick-label { font-size: 12px; font-weight: 500; color: #4a5568; }
</style>
