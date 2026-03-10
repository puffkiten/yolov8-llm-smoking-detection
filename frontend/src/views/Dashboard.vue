<template>
  <div class="dashboard-content" v-loading.fullscreen.lock="pageLoading" element-loading-text="正在加载实时监控数据...">
    
    <div class="page-header">
      <div>
        <h1 class="page-title">概览仪表板</h1>
        <p class="page-sub">欢迎回来，这是您今天的系统运行快报。</p>
      </div>
      <div class="page-actions">
        <button class="btn-refresh" @click="fetchDashboardData" :disabled="isLoading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{'spinning': isLoading}">
            <polyline points="1 4 1 10 7 10"/>
            <path d="M3.51 15a9 9 0 1 0 .49-5.05"/>
          </svg>
          {{ isLoading ? '刷新中...' : '刷新数据' }}
        </button>
        <button class="btn-new" @click="$emit('new-detection')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          发起新检测
        </button>
      </div>
    </div>

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
            <p class="chart-sub">过去 30 天的任务总量与违规事件统计</p>
          </div>
          <a href="#" class="chart-link">查看详细报告</a>
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
        <div class="type-bars">
          <div v-if="typeStats.length === 0" class="empty-text">暂无数据</div>
          <div class="type-bar-item" v-for="item in typeStats" :key="item.label">
            <span class="type-label">{{ item.label }} ({{ item.percent }}%)</span>
            <div class="type-bar-track">
              <div class="type-bar-fill" :style="{ width: item.percent + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-row">
      <div class="bottom-card tasks" v-loading="isLoading">
        <div class="card-header">
          <h3 class="card-title">最近任务状态</h3>
          <a href="#" class="card-link">查看全部 →</a>
        </div>
        <table class="task-table">
          <thead>
            <tr><th>任务ID</th><th>类型</th><th>状态</th><th>时间</th></tr>
          </thead>
          <tbody>
            <tr v-if="tasks.length === 0">
              <td colspan="4" class="empty-text" style="text-align: center; padding: 30px;">暂无任务数据</td>
            </tr>
            <tr v-for="task in tasks" :key="task.taskId">
              <td class="task-id">{{ task.taskId }}</td>
              <td>{{ task.type }}</td>
              <td><span class="status-tag" :class="task.statusClass">{{ task.statusText }}</span></td>
              <td class="task-time">{{ task.time }}</td>
            </tr>
          </tbody>
        </table>
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
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { useRouter } from 'vue-router'
// import axios from 'axios' // 预留：等后端写好后引入

const router = useRouter()

// 状态控制
const pageLoading = ref(true) // 控制全屏首次加载
const isLoading = ref(false)  // 控制刷新按钮和局部加载

// 纯净的响应式数据源 (初始状态全空，等待后端注入)
const stats = ref({ total: '', totalTrend: '', today: '', todayTrend: '', avgTime: '', avgTimeTrend: '', uptime: '', uptimeTrend: '' })
const typeStats = ref([])
const tasks = ref([])
const logs = ref([])
const systemStatus = ref({ title: '', description: '', status: '' })

// ECharts 实例引用
const trendChartRef = ref(null)
let trendChart = null

// 动态判断涨跌颜色样式
const getTrendClass = (trendStr) => {
  if (!trendStr) return 'stable'
  if (trendStr.includes('+') || trendStr.includes('↗')) return 'up'
  if (trendStr.includes('-') || trendStr.includes('↘')) return 'down'
  return 'stable'
}

// 渲染 ECharts 图表的方法
const renderChart = (xAxisData, seriesTotal, seriesSmoke) => {
  if (!trendChartRef.value) return
  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value)
    window.addEventListener('resize', () => trendChart.resize())
  }
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { top: 30, right: 20, bottom: 20, left: 40 },
    xAxis: { type: 'category', data: xAxisData, axisLine: { lineStyle: { color: '#e8ecf2' } } },
    yAxis: { type: 'value', splitLine: { lineStyle: { type: 'dashed', color: '#f0f3f8' } } },
    series: [
      { name: '任务总数', type: 'line', smooth: true, data: seriesTotal, itemStyle: { color: '#3b9eff' }, symbolSize: 6 },
      { name: '吸烟事件', type: 'bar', barWidth: '30%', data: seriesSmoke, itemStyle: { color: '#f5a623', borderRadius: [4, 4, 0, 0] } }
    ]
  })
}

// 核心：请求真实后端数据的函数
const fetchDashboardData = async () => {
  isLoading.value = true
  if (trendChart) trendChart.showLoading({ text: '数据拉取中...', color: '#3b9eff' })
  
  try {
    /* // ==========================================
    // TODO: 后期对接真实后端 API 的代码逻辑
    // ==========================================
    const res = await axios.get('http://localhost:8000/api/dashboard/summary')
    if (res.data.code === 200) {
      const data = res.data.data
      stats.value = data.stats
      typeStats.value = data.typeStats
      tasks.value = data.tasks
      logs.value = data.logs
      systemStatus.value = data.systemStatus
      
      // 渲染图表真实数据
      renderChart(data.chart.dates, data.chart.totalTasks, data.chart.smokeEvents)
    }
    */

    // --- 目前用 setTimeout 模拟一次真实的异步网络请求 ---
    await new Promise(resolve => setTimeout(resolve, 800))
    // 模拟数据结构（未来删掉即可）
    stats.value = { total: '12,482', totalTrend: '↗ 12.5%', today: '843', todayTrend: '↗ 5.2%', avgTime: '1.2s', avgTimeTrend: '↘ 0.3s', uptime: '99.98%', uptimeTrend: '稳定' }
    typeStats.value = [{ label: '视频流检测', percent: 78 }, { label: '离线图片检测', percent: 22 }]
    tasks.value = [
      { taskId: 'TASK-8291', type: '视频流', statusClass: 'progress', statusText: '进行中', time: '10:24' },
      { taskId: 'TASK-8290', type: '批量图片', statusClass: 'done', statusText: '已完成', time: '10:15' }
    ]
    logs.value = [
      { id: 1, operator: '管理员', description: '配置了摄像头 #04 阈值', time: '5分钟前' }
    ]
    systemStatus.value = { title: '系统运行良好', description: 'GPU 算力充足，负载 24%', status: 'ok' }
    renderChart(['10-01', '10-05', '10-10', '10-15', '10-20'], [200, 300, 450, 400, 500], [50, 80, 120, 100, 150])

  } catch (error) {
    console.error('获取 Dashboard 数据失败:', error)
    // 可以在这里引入 ElMessage.error('网络请求失败')
  } finally {
    isLoading.value = false
    pageLoading.value = false
    if (trendChart) trendChart.hideLoading()
  }
}

onMounted(() => {
  // 进入页面自动触发数据获取
  fetchDashboardData()
})

onUnmounted(() => {
  if (trendChart) trendChart.dispose()
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

.type-bars { padding-top: 8px; }
.type-bar-item { margin-bottom: 24px; }
.type-label { display: block; font-size: 12.5px; color: #6b7a90; margin-bottom: 8px; }
.type-bar-track { height: 72px; background: #f4f7fa; border-radius: 6px; overflow: hidden; display: flex; align-items: flex-end; }
.type-bar-fill  { height: 100%; border-radius: 6px; background: #00bca4; transition: width .6s cubic-bezier(0.4, 0, 0.2, 1); }

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