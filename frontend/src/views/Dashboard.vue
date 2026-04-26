<template>
  <div class="dashboard-page" v-loading.fullscreen.lock="pageLoading" element-loading-text="正在加载仪表盘数据...">
    <div class="dashboard-header">
      <div>
        <h1 class="page-title">概览仪表板</h1>
        <p class="page-sub">欢迎回来，这是您今天的系统运行快报。</p>
      </div>
      <div class="header-actions">
        <BaseButton type="primary" @click="openNewDetection" :disabled="isLoading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          发起新检测
        </BaseButton>
        <BaseButton type="primary" @click="fetchDashboardData" :disabled="isLoading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ spinning: isLoading }">
            <polyline points="1 4 1 10 7 10"/>
            <path d="M3.51 15a9 9 0 1 0 .49-5.05"/>
          </svg>
          {{ isLoading ? '刷新中...' : '刷新数据' }}
        </BaseButton>
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
          <div class="nd-slider-row">
            <el-slider v-model="newDetectionForm.confidence" :min="0" :max="1" :step="0.01" style="flex:1;" />
            <span class="nd-val">{{ newDetectionForm.confidence.toFixed(2) }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <BaseButton type="default" @click="newDetectionVisible = false">取消</BaseButton>
          <BaseButton type="primary" @click="submitNewDetection">去上传并开始</BaseButton>
        </div>
      </template>
    </el-dialog>

    <section class="top-stats">
      <div class="metric-card">
        <div class="metric-icon blue"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
        <button class="metric-more">···</button>
        <div class="metric-label">总检测任务数</div>
        <div class="metric-value">{{ stats.total || '--' }}</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon amber"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
        <button class="metric-more">···</button>
        <div class="metric-label">今日检测数</div>
        <div class="metric-value">{{ stats.today || '--' }}</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon mint"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
        <button class="metric-more">···</button>
        <div class="metric-label">平均处理时间</div>
        <div class="metric-value">{{ stats.avgTime || '--' }}</div>
      </div>
    </section>

    <section class="content-grid">
      <div class="panel panel-trend">
        <div class="panel-head">
          <div>
            <h3 class="panel-title">检测趋势分析</h3>
            <p class="panel-sub">任务总量与违规事件统计</p>
          </div>
          <div class="range-tabs">
            <button class="range-tab" :class="{ active: rangePreset === '1h' }" @click="setRange('1h')">1小时</button>
            <button class="range-tab" :class="{ active: rangePreset === '1d' }" @click="setRange('1d')">1天</button>
            <button class="range-tab" :class="{ active: rangePreset === '1w' }" @click="setRange('1w')">1周</button>
          </div>
        </div>
        <div class="trend-chart" ref="trendChartRef"></div>
      </div>

      <div class="panel panel-status">
        <div class="panel-head compact panel-head-status">
          <div>
            <h3 class="panel-title">设备状态</h3>
            <p class="panel-sub">在线率与异常设备分布</p>
          </div>
        </div>
        <div class="status-body">
          <div class="status-ring" ref="typeChartRef"></div>
          <div class="status-legend">
            <div class="status-item"><span class="legend-dot green"></span><div><div class="legend-label">在线设备</div><div class="legend-value">{{ onlineCount }}（{{ onlinePercent }}%）</div></div></div>
            <div class="status-item"><span class="legend-dot yellow"></span><div><div class="legend-label">离线设备</div><div class="legend-value">{{ offlineCount }}（{{ offlinePercent }}%）</div></div></div>
            <div class="status-item"><span class="legend-dot red"></span><div><div class="legend-label">告警设备</div><div class="legend-value">{{ alertDeviceCount }}（{{ alertPercent }}%）</div></div></div>
          </div>
        </div>
      </div>
    </section>

    <section class="bottom-grid">
      <div class="panel panel-tasks">
        <div class="panel-head compact">
          <h3 class="panel-title">最近任务状态</h3>
          <a href="#" class="panel-link" @click.prevent="router.push('/detection/tasks')">查看更多</a>
        </div>
        <div v-if="tasks.length === 0" class="empty-state">暂无任务数据</div>
        <el-table v-else :data="tasks" size="small" style="width: 100%" class="dashboard-table">
          <el-table-column prop="id" label="任务ID" width="80" />
          <el-table-column prop="typeText" label="类型" width="90" />
          <el-table-column label="状态" width="100"><template #default="{ row }"><el-tag :type="statusTagType(row.status)" effect="light">{{ statusTextCn(row.status) }}</el-tag></template></el-table-column>
          <el-table-column label="核实状态" width="110"><template #default="{ row }"><el-tag :type="verifyTagType(row.verify_status)" effect="light">{{ verifyTextCn(row.verify_status) }}</el-tag></template></el-table-column>
          <el-table-column label="时间" min-width="130"><template #default="{ row }">{{ formatShortTime(row.created_at) }}</template></el-table-column>
          <el-table-column label="操作" width="100" align="right"><template #default="{ row }"><el-button v-if="row.verify_status === 'pending'" type="primary" size="small" @click="goVerify(row)">去核实</el-button><span v-else class="table-placeholder">—</span></template></el-table-column>
        </el-table>
      </div>

      <div class="panel panel-actions">
        <div class="panel-head compact"><h3 class="panel-title">快捷操作</h3></div>
        <div class="quick-grid">
          <div class="quick-card" @click="$router.push('/camera/realtime')"><div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M23 7 16 12 23 17V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div><div class="quick-title">实时监控</div><div class="quick-sub">查看实时预览</div></div>
          <div class="quick-card" @click="$router.push('/detection/tasks')"><div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div><div class="quick-title">检测记录</div><div class="quick-sub">查看历史记录</div></div>
          <div class="quick-card" @click="$router.push('/camera/config')"><div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></div><div class="quick-title">配置中心</div><div class="quick-sub">系统参数配置</div></div>
          <div class="quick-card" @click="$router.push('/system/users')"><div class="quick-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div><div class="quick-title">成员管理</div><div class="quick-sub">管理系统成员</div></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, reactive, computed } from 'vue'
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

const stats = ref({ total: '', today: '', avgTime: '' })
const tasks = ref([])
const cameraStats = ref({ total_count: 0, online_count: 0, offline_count: 0, alert_count: 0 })

const onlineCount = computed(() => Number(cameraStats.value.online_count || 0))
const offlineCount = computed(() => Number(cameraStats.value.offline_count || 0))
const alertDeviceCount = computed(() => Number(cameraStats.value.alert_count || 0))
const deviceTotal = computed(() => {
  const total = Number(cameraStats.value.total_count || 0)
  return Math.max(1, total || onlineCount.value + offlineCount.value + alertDeviceCount.value)
})
const onlinePercent = computed(() => Math.round((onlineCount.value / deviceTotal.value) * 100))
const offlinePercent = computed(() => Math.round((offlineCount.value / deviceTotal.value) * 100))
const alertPercent = computed(() => Math.round((alertDeviceCount.value / deviceTotal.value) * 100))

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
    legend: { top: 6, right: 12, itemWidth: 9, itemHeight: 9, textStyle: { color: '#8a97aa', fontSize: 12, fontWeight: 600 } },
    grid: { top: 54, right: 12, bottom: 18, left: 28 },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLine: { lineStyle: { color: '#edf1f6' } },
      axisTick: { show: false },
      axisLabel: { color: '#9aa6b2', fontSize: 11, margin: 10, ...(xAxisLabel || {}) }
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      axisLabel: { color: '#9aa6b2', fontSize: 11 },
      splitLine: { lineStyle: { type: 'solid', color: '#f3f6fa' } }
    },
    series: [
      { name: 'AI 告警数', type: 'line', smooth: true, data: seriesTotal, lineStyle: { color: '#49a6ff', width: 3 }, itemStyle: { color: '#49a6ff' }, symbolSize: 6, areaStyle: { color: 'rgba(73,166,255,0.06)' } },
      { name: '待核实数', type: 'bar', data: seriesSmoke, barWidth: 14, itemStyle: { color: '#f5b43b', borderRadius: [6, 6, 0, 0] } }
    ]
  })
}

const renderStatusRing = () => {
  if (!typeChartRef.value) return
  if (!typeChart) {
    typeChart = echarts.init(typeChartRef.value)
  }
  typeChart.setOption({
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'pie',
        radius: ['62%', '82%'],
        center: ['50%', '46%'],
        label: { show: false },
        labelLine: { show: false },
        silent: true,
        data: [
          { value: onlineCount.value, name: '在线设备', itemStyle: { color: '#39c98a' } },
          { value: offlineCount.value, name: '离线设备', itemStyle: { color: '#ffbe3d' } },
          { value: alertDeviceCount.value, name: '告警设备', itemStyle: { color: '#ff6b6b' } },
        ]
      }
    ],
    graphic: [
      {
        type: 'text',
        left: 'center',
        top: '36%',
        style: {
          text: String(cameraStats.value.total_count || 0),
          fill: '#1f2937',
          fontSize: 28,
          fontWeight: 700,
          textAlign: 'center'
        }
      },
      {
        type: 'text',
        left: 'center',
        top: '52%',
        style: {
          text: '总设备',
          fill: '#94a3b8',
          fontSize: 12,
          fontWeight: 600,
          textAlign: 'center'
        }
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
    const resp = await axios.get('/api/dashboard/trend', {
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
    today: String(today),
    avgTime,
  }

  tasks.value = items.slice(0, 6).map(it => ({
    id: it.id,
    name: it.name,
    type: it.type,
    typeText: it.type === 'video' ? '视频流' : '图片',
    status: it.status,
    verify_status: it.verify_status || 'verified',
    created_at: it.created_at
  }))

  renderStatusRing()
}

const fetchCameraStats = async () => {
  try {
    const [statsRes, groupedRes] = await Promise.all([
      axios.get('/api/cameras/stats/', { headers: authHeaders() }),
      axios.get('/api/cameras/grouped/', { headers: authHeaders() })
    ])
    const base = statsRes.data || {}
    const grouped = groupedRes.data || {}
    const alertIds = new Set()
    Object.values(grouped).forEach((items) => {
      if (!Array.isArray(items)) return
      items.forEach((it) => {
        if (Number(it.latest_confidence || 0) > 0 || it.has_alert === true) {
          alertIds.add(it.id)
        }
      })
    })
    cameraStats.value = {
      total_count: Number(base.total_count || 0),
      online_count: Number(base.online_count || 0),
      offline_count: Number(base.offline_count || 0),
      alert_count: alertIds.size,
    }
    renderStatusRing()
  } catch {
    cameraStats.value = { total_count: 0, online_count: 0, offline_count: 0, alert_count: 0 }
    renderStatusRing()
  }
}

const fetchDashboardData = async () => {
  isLoading.value = true
  if (trendChart) trendChart.showLoading({ text: '数据拉取中...', color: '#3b9eff' })
  
  try {
    const res = await axios.get('/api/detection/tasks', { headers: authHeaders() })
    rawItems.value = Array.isArray(res.data?.results) ? res.data.results : []
    recomputeDashboard()
    await Promise.all([fetchTrend(), fetchCameraStats()])
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
  resizeHandler = () => {
    if (trendChart) trendChart.resize()
    if (typeChart) typeChart.resize()
  }
  window.addEventListener('resize', resizeHandler)
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
.dashboard-page { width: 100%; }
.spinning { animation: spin 1s linear infinite; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}
.page-title {
  margin: 0 0 4px;
  font-size: 30px;
  font-weight: 700;
  color: #1f2937;
  letter-spacing: -0.5px;
}
.page-sub { margin: 0; color: #97a3b5; font-size: 12.5px; }
.header-actions { display: flex; gap: 10px; align-items: center; }

.nd-form { display: grid; gap: 14px; }
.nd-row { display: grid; gap: 8px; }
.nd-label { font-size: 13px; font-weight: 600; color: #1f2937; }
.nd-slider-row { display: flex; gap: 12px; align-items: center; width: 100%; }
.nd-val { font-weight: 700; color: #1f2937; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 10px; }

.top-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 14px;
}
.metric-card {
  position: relative;
  background: #fff;
  border: 1px solid #edf1f5;
  border-radius: 18px;
  padding: 18px 20px 16px;
  min-height: 132px;
  box-shadow: 0 8px 22px rgba(30, 64, 175, 0.035);
}
.metric-icon { width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; }
.metric-icon.blue { background: rgba(73, 166, 255, 0.12); color: #49a6ff; }
.metric-icon.amber { background: rgba(255, 190, 61, 0.16); color: #ffbe3d; }
.metric-icon.mint { background: rgba(73, 214, 170, 0.14); color: #49d6aa; }
.metric-more { position: absolute; top: 14px; right: 16px; border: none; background: transparent; color: #c8d1dd; font-size: 16px; cursor: pointer; }
.metric-label { color: #8e9aac; font-size: 12px; margin-bottom: 6px; }
.metric-value { color: #111827; font-size: 37px; font-weight: 700; line-height: 1; letter-spacing: -0.6px; }

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.48fr) minmax(320px, 0.82fr);
  gap: 14px;
  margin-bottom: 14px;
}
.panel {
  background: #fff;
  border: 1px solid #edf1f5;
  border-radius: 18px;
  box-shadow: 0 8px 22px rgba(30, 64, 175, 0.035);
}
.panel-trend,
.panel-status,
.panel-tasks,
.panel-actions { padding: 18px 20px; }
.panel-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
.panel-head.compact { margin-bottom: 14px; }
.panel-title { margin: 0 0 3px; font-size: 18px; font-weight: 700; color: #1f2937; }
.panel-sub { margin: 0; font-size: 12px; color: #98a4b5; }
.panel-link { font-size: 12px; font-weight: 600; color: #49a6ff; text-decoration: none; }
.range-tabs { display: inline-flex; gap: 2px; padding: 3px; border-radius: 999px; background: #f5f7fb; }
.range-tab { height: 28px; padding: 0 11px; border: none; border-radius: 999px; background: transparent; color: #95a1b2; font-size: 11px; font-weight: 700; cursor: pointer; }
.range-tab.active { background: #ffffff; color: #49a6ff; box-shadow: 0 3px 8px rgba(15, 23, 42, 0.06); }
.trend-chart { width: 100%; height: 320px; }

.status-body { display: grid; grid-template-columns: 170px 1fr; align-items: center; gap: 8px; min-height: 320px; }
.status-ring { width: 170px; height: 170px; margin: 0 auto; }
.status-legend { display: flex; flex-direction: column; gap: 15px; }
.status-item { display: flex; gap: 10px; align-items: flex-start; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.legend-dot.green { background: #39c98a; }
.legend-dot.yellow { background: #ffbe3d; }
.legend-dot.red { background: #ff6b6b; }
.legend-label { color: #7f8a9c; font-size: 12px; margin-bottom: 4px; }
.legend-value { color: #111827; font-size: 14px; font-weight: 700; }

.bottom-grid { display: grid; grid-template-columns: minmax(0, 1.42fr) minmax(340px, 0.88fr); gap: 14px; }
.panel-tasks, .panel-actions { min-height: 332px; }
.dashboard-table :deep(.el-table__header th) {
  background: #fff;
  color: #9ba7b8;
  font-weight: 600;
  font-size: 12px;
  height: 40px;
  padding: 0;
}
.dashboard-table :deep(.el-table__cell) {
  padding: 10px 0;
  font-size: 13px;
  color: #4b5563;
}
.dashboard-table :deep(.el-table__row td) {
  height: 48px;
}
.dashboard-table :deep(.cell) {
  line-height: 1.2;
}
.table-placeholder { color: #b0b8c4; font-size: 12px; }
.empty-state { display: flex; align-items: center; justify-content: center; min-height: 220px; color: #9aa5b4; font-size: 14px; }

.quick-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-top: 4px; }
.quick-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 124px;
  border: 1px solid #edf1f5;
  border-radius: 16px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}
.quick-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(73, 166, 255, 0.08);
  border-color: #dbeafe;
}
.quick-icon {
  width: 58px;
  height: 58px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f5fbff 0%, #edf6ff 100%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
}
.quick-title { color: #1f2937; font-size: 14px; font-weight: 700; }
.quick-sub { color: #a0acbb; font-size: 11px; }

@media (max-width: 1280px) {
  .content-grid,
  .bottom-grid { grid-template-columns: 1fr; }
}

@media (max-width: 960px) {
  .dashboard-header,
  .panel-head { flex-direction: column; align-items: stretch; }
  .top-stats { grid-template-columns: 1fr; }
  .status-body { grid-template-columns: 1fr; justify-items: center; }
  .bottom-grid { grid-template-columns: 1fr; }
}
</style>
