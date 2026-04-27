<template>
  <div class="realtime-page">
    <div class="layout-grid">
      <main class="left-panel">
        <div class="matrix-header">
          <div class="mh-left">
            <h2 class="mh-title">监控矩阵 <span class="count-tag">({{ activeCameraCount }}路已联)</span></h2>
            <div class="live-status-pill" v-if="totalCount > 0">
              <span class="pulse-dot"></span> {{ onlineCount > 0 ? 'AI 实时推理中' : '暂无在线设备' }}
            </div>
          </div>

          <div class="mh-right">
            <div class="pill-group">
              <button class="p-btn" :class="{ active: viewMode === 'grid' }" @click="viewMode = 'grid'">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                网格视图
              </button>
              <button class="p-btn" :class="{ active: viewMode === 'list' }" @click="viewMode = 'list'">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="3" cy="6" r="1"/><circle cx="3" cy="12" r="1"/><circle cx="3" cy="18" r="1"/></svg>
                列表视图
              </button>
              <div class="p-divider"></div>
              <button class="p-btn text-muted" @click="showLabels = !showLabels">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                {{ showLabels ? '隐藏标注' : '显示标注' }}
              </button>
            </div>
          </div>
        </div>

        <div class="video-container" :class="viewMode + '-layout'">
          <template v-if="selectedCams.length > 0">
            <div class="v-card" v-for="cam in selectedCams" :key="cam.id">
              <img :src="buildStreamUrl(cam)" style="width: 100%; height: 100%; object-fit: cover;" />
              <div class="v-overlay">
                <div class="vo-header">
                  <div class="cam-info-label">
                    <span class="dot-indicator" :class="cam.status"></span>
                    <span class="name">{{ cam.name }}</span>
                  </div>
                  <span class="spec-label">MJPEG</span>
                </div>
                <div class="vo-footer">{{ new Date().toLocaleString() }}</div>
              </div>
            </div>
          </template>
          <div class="v-card empty" v-else>
            <div class="empty-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e2e8f0" stroke-width="1.5"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
              <p>{{ totalCount > 0 ? '请从右侧列表中选择要监控的摄像头' : '请先添加摄像头' }}</p>
            </div>
          </div>
        </div>

        <div class="status-footer">
          <div class="s-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg></div>
          <div class="s-text">
            <h4>{{ totalCount > 0 ? '系统状态良好' : '暂无摄像头设备' }}</h4>
            <p>{{ totalCount > 0 ? `当前在线设备: ${onlineCount} / ${totalCount}` : '请前往摄像头配置页添加设备后再开始实时监控' }}</p>
          </div>
        </div>
      </main>

      <aside class="right-panel">
        <div class="panel-header">
          <h3 class="panel-title">设备列表</h3>
          <span class="online-status">{{ onlineCount }} / {{ totalCount }} 在线</span>
        </div>

        <div class="tree-container">
          <div class="tree-group" v-for="group in deviceTree" :key="group.name">
            <div class="group-header">
              <span class="group-name">{{ group.name }}</span>
              <span class="group-count">{{ group.devices.length }}</span>
            </div>
            
            <div class="device-node" v-for="dev in group.devices" :key="dev.id" @click="selectDevice(dev)" :class="{ active: isSelected(dev.id) }">
              <span class="status-dot" :class="dev.status"></span>
              <div class="device-details">
                <span class="d-name">{{ dev.name }}</span>
                <span class="d-loc"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> {{ dev.loc }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="alert-result-card" v-if="false">
          <div class="arc-header">
            <div class="arc-title-row">
              <span class="pulse-red-dot"></span>
              <h3 class="arc-title">实时检测结果</h3>
              <span class="arc-status-tag" :class="{ confirmed: latestAlert.is_confirmed }">Detected</span>
            </div>
            <p class="arc-time">{{ latestAlert.detected_at }}</p>
          </div>
          
          <div class="arc-body">
            <div class="report-box">
              <div class="rb-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                检测到违规行为 (置信度: {{ latestAlert.confidence }}%)
              </div>
              <p class="rb-content">{{ latestAlert.llm_report }}</p>
            </div>
          </div>

          <div class="arc-footer">
             <button class="arc-btn-outline" @click="$router.push('/detection/tasks')">查看详情</button>
          </div>
        </div>

        <div class="suggestion-card" v-if="suggestion && totalCount > 0">
          <div class="sug-title">{{ suggestion.title }}</div>
          <p class="sug-desc">{{ suggestion.desc }}</p>
          <a href="#" class="sug-btn" @click.prevent="$router.push(suggestion.action_url)">{{ suggestion.action_text }} &rarr;</a>
        </div>

        <button class="btn-add-ghost" @click="$router.push('/camera/config')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          添加新摄像头
        </button>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { buildApiUrl } from '@/utils/http'

const ACTIVATED_CAMERA_IDS_KEY = 'activated_camera_ids'
const readActivatedCameraIds = () => {
  try {
    const raw = JSON.parse(localStorage.getItem(ACTIVATED_CAMERA_IDS_KEY) || '[]')
    return Array.isArray(raw) ? raw.map((id) => Number(id)).filter((id) => Number.isFinite(id)) : []
  } catch {
    return []
  }
}
const writeActivatedCameraIds = (ids) => {
  localStorage.setItem(ACTIVATED_CAMERA_IDS_KEY, JSON.stringify(ids))
}

const authHeaders = () => {
  const access = localStorage.getItem('access_token') || ''
  return access ? { Authorization: `Bearer ${access}` } : {}
}

const viewMode = ref('grid')
const showLabels = ref(true)

const cameraList = ref([])
const selectedCams = ref([])
const deviceTree = ref([])

const activeCameraCount = computed(() => selectedCams.value.length)
const onlineCount = ref(0)
const totalCount = ref(0)
const suggestion = ref(null)

const buildStreamUrl = (cam) => buildApiUrl(`/api/cameras/${cam.id}/stream/?t=${Date.now()}`)

const isSelected = (id) => selectedCams.value.some(c => c.id === id)
const isActivated = (id) => readActivatedCameraIds().includes(Number(id))

const selectDevice = (dev) => {
  const index = selectedCams.value.findIndex(c => c.id === dev.id)
  if (index > -1) {
    selectedCams.value.splice(index, 1)
  } else {
    if (selectedCams.value.length >= 4) {
      selectedCams.value.shift()
    }
    selectedCams.value.push(dev)
  }
  writeActivatedCameraIds(selectedCams.value.map((item) => Number(item.id)))
  fetchStats()
  fetchGrouped()
}

const fetchSuggestions = async () => {
  try {
    const res = await axios.get('/api/cameras/suggestions/', { headers: authHeaders() })
    const payload = res.data || {}
    if (Array.isArray(payload.results) && payload.results.length > 0) {
      const first = payload.results[0]
      suggestion.value = {
        title: `推荐关注：${first.name}`,
        desc: first.region ? `所属区域：${first.region}` : '已为你加载摄像头建议',
        action_text: '前往摄像头配置',
        action_url: '/camera/config',
      }
    } else {
      suggestion.value = null
    }
  } catch {
    suggestion.value = null
  }
}

const fetchStats = async () => {
  try {
    const res = await axios.get('/api/cameras/stats/', { headers: authHeaders() })
    totalCount.value = Number(res.data?.total_count || 0)
    onlineCount.value = readActivatedCameraIds().length
  } catch {
    onlineCount.value = readActivatedCameraIds().length
    totalCount.value = 0
  }
}

const fetchGrouped = async () => {
  try {
    const res = await axios.get('/api/cameras/grouped/', { headers: authHeaders() })
    const payload = res.data || {}
    const rawGroups = Array.isArray(payload.results)
      ? payload.results
      : Object.keys(payload).map((k) => ({ region: k, items: Array.isArray(payload[k]) ? payload[k] : [] }))

    const groups = rawGroups.map((group) => {
      const items = Array.isArray(group.items)
        ? group.items
        : Array.isArray(group.devices)
          ? group.devices
          : []
      return {
        name: group.region || group.name || '未分组',
        devices: items.map(it => ({
          id: it.id,
          name: it.name,
          loc: it.region || group.region || '',
          stream_url: it.stream_url || '',
          stream_kind: it.stream_kind || 'stream',
          status: isActivated(it.id) ? 'online' : 'offline'
        }))
      }
    }).filter(group => group.devices.length > 0)
    deviceTree.value = groups

    const allDevices = groups.flatMap(g => g.devices)
    cameraList.value = allDevices
    const activatedIds = readActivatedCameraIds()
    selectedCams.value = allDevices.filter((device) => activatedIds.includes(Number(device.id))).slice(0, 4)
  } catch {
    deviceTree.value = []
    selectedCams.value = []
    cameraList.value = []
  }
}

const handleActivatedCameraStorageChange = (event) => {
  if (event.key && event.key !== ACTIVATED_CAMERA_IDS_KEY) return
  fetchStats()
  fetchGrouped()
}

onMounted(async () => {
  await fetchStats()
  await fetchGrouped()
  await fetchSuggestions()
  const refresh = async () => {
    await fetchStats()
    await fetchGrouped()
    await fetchSuggestions()
  }
  window.addEventListener('focus', refresh)
  window.addEventListener('storage', handleActivatedCameraStorageChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', handleActivatedCameraStorageChange)
  // 移除不再需要的定时器
})
</script>

<style scoped>
.realtime-page { width: 100%; color: var(--color-text-main); font-family: inherit; }
.layout-grid { display: grid; grid-template-columns: 1fr 320px; gap: 24px; align-items: flex-start; }

/* 左侧样式纠偏 */
.mh-left { display: flex; align-items: baseline; gap: 16px; margin-bottom: 16px; }
.mh-title { font-size: 20px; font-weight: 700; margin: 0; display: flex; align-items: baseline; gap: 8px;}
.count-tag { color: var(--color-text-sub); font-size: 16px; font-weight: 500; }
.live-status-pill { display: flex; align-items: center; gap: 6px; padding: 4px 10px; background: rgba(59,158,255,0.1); color: var(--color-primary); border-radius: 20px; font-size: 12px; font-weight: 600; transform: translateY(-2px); }
.pulse-dot { width: 6px; height: 6px; background: var(--color-primary); border-radius: 50%; animation: blink 1.5s infinite; }
@keyframes blink { 0%, 100% { opacity: 1 } 50% { opacity: 0.3 } }

/* 药丸按钮组 */
.pill-group { display: flex; align-items: center; background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 10px; padding: 4px; gap: 4px; box-shadow: var(--shadow-card); }
.p-btn { display: flex; align-items: center; gap: 6px; border: none; background: transparent; padding: 6px 12px; font-size: 12px; font-weight: 600; color: var(--color-text-sub); cursor: pointer; border-radius: 6px; transition: all 0.2s; }
.p-btn.active { background: var(--color-bg-page); color: var(--color-text-main); }
.p-divider { width: 1px; height: 16px; background: var(--color-border); margin: 0 4px; }
.text-muted { color: var(--color-text-light); }

/* 视频网格与布局切换 */
.video-container { display: grid; gap: 16px; margin-bottom: 24px; transition: all 0.3s ease; }

.grid-layout { grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); }
.grid-layout:has(.v-card:nth-child(1):last-child) { grid-template-columns: 1fr; }
.grid-layout:has(.v-card:nth-child(2):last-child) { grid-template-columns: 1fr 1fr; }
.grid-layout:has(.v-card:nth-child(n+3)) { grid-template-columns: 1fr 1fr; }

.list-layout { grid-template-columns: 1fr; }

.v-card { position: relative; aspect-ratio: 16/9; background: #000; border-radius: 12px; overflow: hidden; border: 1.5px solid transparent; transition: all 0.3s; }
.v-card.empty { background: var(--color-bg-page); border: 1.5px dashed var(--color-border); display: flex; align-items: center; justify-content: center; }
.empty-placeholder { text-align: center; color: var(--color-text-light); }
.empty-placeholder p { margin-top: 12px; font-size: 14px; }
.v-card.alert-border { border-color: #e85c5c; box-shadow: 0 0 20px rgba(232,92,92,0.25); }
.v-stream { width: 100%; height: 100%; object-fit: cover; opacity: 0.85; }

/* 视频叠加层对齐 */
.v-overlay { position: absolute; inset: 0; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; background: linear-gradient(180deg, rgba(0,0,0,0.5) 0%, transparent 40%, transparent 60%, rgba(0,0,0,0.5) 100%); pointer-events: none;}
.vo-header { display: flex; justify-content: space-between; align-items: center; }
.cam-info-label { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.15); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); }
.dot-indicator { width: 6px; height: 6px; border-radius: 50%; }
.dot-indicator.online { background: #10b981; box-shadow: 0 0 8px #10b981; }
.dot-indicator.alert { background: #e85c5c; }
.dot-indicator.offline { background: #9aa5b4; }
.cam-info-label .name { color: #fff; font-size: 12px; font-weight: 600; }
.spec-label { color: rgba(255,255,255,0.6); font-size: 11px; font-family: monospace; font-weight: 500; }
.vo-footer { color: rgba(255,255,255,0.8); font-size: 12px; font-family: monospace; }
.vo-alert-tag { align-self: flex-end; background: #e85c5c; color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(232,92,92,0.4); }

/* 底部状态条 */
.status-footer { display: flex; align-items: center; gap: 16px; background: var(--color-bg-page); padding: 18px 24px; border-radius: 12px; border: 1px solid var(--color-border); }
.s-text h4 { margin: 0 0 4px 0; font-size: 14px; font-weight: 600; color: var(--color-text-main); }
.s-text p { margin: 0; font-size: 12px; color: var(--color-text-sub); font-family: monospace; }

/* ================= 右侧面板纠偏 ================= */
.right-panel { background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 12px; padding: 24px; box-shadow: var(--shadow-card); display: flex; flex-direction: column; gap: 24px; }
.panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--color-border); padding-bottom: 16px; }
.panel-title { font-size: 16px; font-weight: 700; margin: 0; }
.online-status { font-size: 12px; color: var(--color-text-sub); font-weight: 600; background: var(--color-bg-page); padding: 4px 10px; border-radius: 20px; border: 1px solid var(--color-border); }

.tree-group { display: flex; flex-direction: column; gap: 12px; }
.group-header { display: flex; justify-content: space-between; align-items: center; }
.group-name { font-size: 12px; font-weight: 600; color: var(--color-text-light); text-transform: uppercase; letter-spacing: 0.5px; }
.group-count { font-size: 10px; color: var(--color-text-light); background: var(--color-bg-page); padding: 1px 6px; border-radius: 4px; }

/* 🌟 设备节点样式完全还原 UI */
.device-node { display: flex; align-items: flex-start; gap: 12px; padding: 4px 0; cursor: pointer; transition: opacity 0.2s; }
.device-node:hover { opacity: 0.7; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.status-dot.online { background: #10b981; }
.status-dot.alert { background: #e85c5c; animation: blink 1s infinite; }
.device-details { display: flex; flex-direction: column; gap: 2px; }
.d-name { font-size: 14px; font-weight: 500; color: var(--color-text-main); }
.red-text { color: #e85c5c; font-weight: 600; }
.d-loc { font-size: 11px; color: var(--color-text-light); display: flex; align-items: center; gap: 4px; }

.suggestion-card { background: rgba(59,158,255,0.1); border: 1px solid rgba(59,158,255,0.2); border-radius: 10px; padding: 16px; }
.sug-title { font-size: 13px; font-weight: 700; color: var(--color-primary); margin-bottom: 8px; }
.sug-desc { font-size: 12px; color: var(--color-text-sub); line-height: 1.5; margin: 0 0 12px 0; }
.sug-btn { font-size: 12px; color: var(--color-primary); font-weight: 600; text-decoration: none; }

.btn-add-ghost { height: 44px; background: var(--color-bg-card); border: 1px dashed var(--color-border); border-radius: 8px; font-size: 13px; font-weight: 600; color: var(--color-text-sub); cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-add-ghost:hover { border-color: var(--color-primary); color: var(--color-primary); background: rgba(59,158,255,0.05); }

/* 🌟 实时报警结果卡片样式 */
.alert-result-card { background: var(--color-bg-card); border: 1.5px solid #ffedec; border-radius: 12px; padding: 16px; box-shadow: var(--shadow-card); }
.arc-header { margin-bottom: 12px; }
.arc-title-row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.pulse-red-dot { width: 8px; height: 8px; background: #e85c5c; border-radius: 50%; animation: pulse-red 1.5s infinite; }
@keyframes pulse-red { 0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(232,92,92,0.7); } 70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(232,92,92,0); } 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(232,92,92,0); } }
.arc-title { font-size: 15px; font-weight: 700; color: var(--color-text-main); margin: 0; }
.arc-status-tag { margin-left: auto; font-size: 11px; font-weight: 700; color: #e85c5c; background: #fff1f0; padding: 2px 8px; border-radius: 4px; border: 1px solid #ffccc7; }
.arc-time { font-size: 11px; color: var(--color-text-light); margin: 0; font-family: monospace; }

.arc-body { margin-bottom: 16px; }
.report-box { background: rgba(232,92,92,0.05); border: 1px solid rgba(232,92,92,0.1); border-radius: 8px; padding: 12px; }
.rb-label { display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; color: #e85c5c; margin-bottom: 8px; }
.rb-content { font-size: 12px; color: var(--color-text-sub); line-height: 1.6; margin: 0; white-space: pre-line; }

.arc-footer { display: flex; justify-content: flex-end; }
.arc-btn-outline { background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 6px; padding: 6px 16px; font-size: 12px; font-weight: 600; color: var(--color-text-sub); cursor: pointer; transition: all 0.2s; }
.arc-btn-outline:hover { border-color: var(--color-primary); color: var(--color-primary); background: rgba(59,158,255,0.05); }

.device-node.active { background: rgba(59,158,255,0.1); border-radius: 8px; padding: 4px 8px; margin-left: -8px; width: calc(100% + 16px); }
</style>
