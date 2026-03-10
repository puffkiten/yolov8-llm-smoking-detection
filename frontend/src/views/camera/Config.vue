<template>
  <div class="camera-config-page">
    
    <div class="page-content" :class="{ 'blur-bg': showModal || showRegionModal }">
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon-wrap blue"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg></div>
          <div class="stat-info"><p class="stat-label">总摄像头</p><p class="stat-val">{{ totalCameras }}</p></div>
        </div>
        <div class="stat-card">
          <div class="stat-icon-wrap green"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div>
          <div class="stat-info"><p class="stat-label">在线监控</p><p class="stat-val">{{ onlineCameras }}</p></div>
        </div>
        <div class="stat-card">
          <div class="stat-icon-wrap red"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M17.31 17.31A10.43 10.43 0 0 1 12 19c-7 0-10-7-10-7a13.16 13.16 0 0 1 1.67-2.68"/><path d="M22 2L2 22"/></svg></div>
          <div class="stat-info"><p class="stat-label">离线告警</p><p class="stat-val">{{ offlineCameras }}</p></div>
        </div>
      </div>

      <div class="table-container">
        <div class="table-toolbar">
          <div class="tb-left">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
            <h2 class="tb-title">摄像头列表</h2>
          </div>
          <div class="tb-right">
            <div class="search-wrap">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input
                v-model="cameraSearch"
                type="text"
                placeholder="搜索设备名或区域..."
                class="search-input"
              >
            </div>
            <button class="btn-primary" @click="openModal">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              添加摄像头
            </button>
          </div>
        </div>

        <table class="aero-table">
          <thead>
            <tr>
              <th>摄像头 ID</th><th>摄像头名称</th><th>所属区域</th><th>置信度阈值</th><th>状态</th><th align="right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cam in pagedCameras" :key="cam.id">
              <td class="td-id">{{ cam.id }}</td><td>{{ cam.name }}</td><td>{{ cam.region }}</td><td>{{ cam.threshold }}%</td>
              <td>
                <div class="status-cell">
                  <span class="status-dot" :class="cam.status === '在线' ? 'online' : 'offline'"></span>
                  <div class="status-text-wrap"><span class="st-main">{{ cam.status }}</span><span class="st-sub">最后同步: {{ cam.lastSync }}</span></div>
                </div>
              </td>
              <td align="right">
                <div class="action-icons">
                  <svg class="ico view" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" @click="handleView(cam)"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg class="ico edit" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" @click="handleEdit(cam)"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  <svg class="ico delete" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" @click="handleDelete(cam)"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <span class="page-info">
            显示 {{ pageStartIndex }} 到 {{ pageEndIndex }} 项，共 {{ filteredCameras.length }} 项
          </span>
          <div class="page-controls">
            <button class="page-btn" :disabled="currentPage === 1" @click="currentPage > 1 && (currentPage -= 1)">上一页</button>
            <button class="page-num active">{{ currentPage }} / {{ totalPages }}</button>
            <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage < totalPages && (currentPage += 1)">下一页</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal-card">
        
        <div class="modal-header">
          <div class="mh-title-area">
            <div class="mh-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></div>
            <div class="mh-text">
              <h3>新增监控摄像头</h3>
              <p>配置摄像头的物理位置、视频流来源以及 AI 识别触发的置信度阈值。</p>
            </div>
          </div>
          <button class="close-btn" @click="closeModal"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        </div>

        <div class="modal-body">
          
          <div class="form-row-flex">
            <div class="form-group half-width">
              <label>摄像头名称</label>
              <input type="text" class="aero-input" placeholder="请输入设备识别名称" v-model="form.name">
            </div>
            
            <div class="form-group half-width">
              <div class="label-row-header">
                <label>所属区域</label>
                <a href="#" class="link-btn" @click.prevent="openRegionModal">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  管理区域
                </a>
              </div>
              <div class="select-wrapper">
                <select class="aero-input aero-select" v-model="form.region" :class="{'placeholder-color': !form.region}">
                  <option value="" disabled>请选择所属区域</option>
                  <option v-for="r in customRegions" :key="r" :value="r">{{ r }}</option>
                </select>
                <svg class="select-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
              <p class="input-hint">请在点击右上角的“管理区域”进行添加区域后，再进行勾选</p>
            </div>
          </div>

          <div class="form-group">
            <label>安装位置描述</label>
            <input type="text" class="aero-input" placeholder="例如：一楼正门左侧支架" v-model="form.location">
          </div>

          <div class="segment-control">
            <div class="segment" :class="{ active: activeTab === 'stream' }" @click="activeTab = 'stream'">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
              视频流地址
            </div>
            <div class="segment" :class="{ active: activeTab === 'file' }" @click="activeTab = 'file'">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>
              录像文件
            </div>
          </div>

          <div class="tab-content-area">
            <div v-show="activeTab === 'stream'" class="form-group mt-16">
              <div class="input-with-btn">
                <input type="text" class="aero-input" placeholder="输入 RTSP, RTMP 或 HLS 流地址" v-model="form.streamUrl" @input="resetTestStatus">
                <button class="btn-test" :class="testStatus" @click="testConnection" :disabled="testStatus === 'testing'">
                  <svg v-if="testStatus === 'idle'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                  <svg v-if="testStatus === 'testing'" class="spin-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>
                  <svg v-if="testStatus === 'success'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                  <svg v-if="testStatus === 'error'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  {{ testBtnText }}
                </button>
              </div>
              <div class="video-preview-box" v-if="testStatus === 'success'">
                <div class="preview-placeholder">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
                  <span>画面拉取成功，正在解码渲染...</span>
                </div>
              </div>
              <p class="input-hint" :class="{'error-text': testStatus === 'error', 'success-text': testStatus === 'success'}">
                {{ testMessage || '支持主流协议：rtsp://, rtmp://, http(s)://...m3u8' }}
              </p>
            </div>

            <div v-show="activeTab === 'file'" class="form-group mt-16">
              <input type="file" ref="fileInputRef" accept="video/mp4,video/avi" style="display: none;" @change="handleFileChange">
              <div class="upload-dropzone" @click="triggerFileInput">
                <div v-if="!selectedFile" class="upload-placeholder">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <p class="dz-text">点击选择本地监控录像</p>
                  <p class="dz-hint">支持 MP4 / AVI 格式</p>
                </div>
                <div v-else class="upload-selected">
                   <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                   <span class="file-name">{{ selectedFile.name }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group border-top-group">
            <div class="label-row">
              <div class="label-with-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                <label>置信度阈值 (Confidence Threshold)</label>
              </div>
              <span class="val-display">{{ form.threshold }}%</span>
            </div>
            <div class="slider-wrap">
              <input type="range" min="0" max="100" v-model="form.threshold" class="aero-slider" :style="{ '--val': form.threshold + '%' }">
            </div>
            <p class="input-hint slider-hint">阈值越高，检测越严格（减少误报）；阈值越低，灵敏度越高。</p>
          </div>
          
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">取消</button>
          <button class="btn-confirm" @click="submitForm">确认添加</button>
        </div>

      </div>
    </div>

    <div class="modal-overlay" style="z-index: 1000;" v-if="showRegionModal" @click.self="closeRegionModal">
      <div class="modal-card region-card">
        <div class="modal-header">
          <div class="mh-title-area">
            <div class="mh-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <div class="mh-text">
              <h3>管理系统区域</h3>
              <p>在此维护整个监控系统支持选择的物理区域位置。</p>
            </div>
          </div>
          <button class="close-btn" @click="closeRegionModal"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>新增区域</label>
            <div class="add-region-flex">
              <input type="text" class="aero-input" placeholder="输入新的区域名称 (如: 车间B区)" v-model="newRegionInput" @keyup.enter="handleAddRegion">
              <button class="btn-secondary" @click="handleAddRegion">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                添加
              </button>
            </div>
          </div>

          <div class="form-group border-top-group" style="padding-top: 12px; margin-top: 16px;">
            <label>已有区域列表</label>
            <div class="region-list">
              <div v-if="customRegions.length === 0" class="empty-region">
                暂无自定义区域，请在上方添加。
              </div>
              <div class="region-item" v-for="(r, index) in customRegions" :key="index">
                <span>{{ r }}</span>
                <span class="delete-link" @click="handleDeleteRegion(index)">删除</span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-confirm" @click="closeRegionModal">完成并返回</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// --- 第一层：添加/编辑摄像头弹窗 ---
const showModal = ref(false) // 🚨 修复1：默认不再弹出
const mode = ref('add') // add | edit
const editingId = ref('')

const openModal = () => {
  mode.value = 'add'
  editingId.value = ''
  form.value = { name: '', region: '', location: '', streamUrl: '', threshold: 75 }
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
  resetTestStatus()
}

const form = ref({
  name: '',
  region: '',
  location: '',
  streamUrl: '',
  threshold: 75
})

// --- 第二层：区域管理与交互 ---
const showRegionModal = ref(false)
const newRegionInput = ref('')
const customRegions = ref([]) // 🚨 修复2：默认下拉框没有数据 (空数组)

const openRegionModal = () => showRegionModal.value = true
const closeRegionModal = () => {
  showRegionModal.value = false
  newRegionInput.value = ''
}

// 添加新区域
const handleAddRegion = () => {
  const val = newRegionInput.value.trim()
  if (!val) return ElMessage.warning('区域名称不能为空')
  if (customRegions.value.includes(val)) return ElMessage.warning('该区域已存在')
  
  customRegions.value.push(val)
  newRegionInput.value = ''
  ElMessage.success(`区域 "${val}" 添加成功`)
  
  // 贴心小交互：如果主表单还没选区域，自动帮他选中刚加的这个
  if (!form.value.region) {
    form.value.region = val
  }
}

// 删除区域
const handleDeleteRegion = (index) => {
  const removed = customRegions.value.splice(index, 1)[0]
  // 如果主表单正好选着这个被删的区域，清空它
  if (form.value.region === removed) {
    form.value.region = ''
  }
}


// --- Tab 切换与文件上传 ---
const activeTab = ref('stream')
const fileInputRef = ref(null)
const selectedFile = ref(null)

const triggerFileInput = () => fileInputRef.value?.click()
const handleFileChange = (e) => {
  if (e.target.files.length > 0) selectedFile.value = e.target.files[0]
}

// --- 测试连接逻辑 ---
const testStatus = ref('idle') 
const testMessage = ref('')

const testBtnText = computed(() => {
  if (testStatus.value === 'testing') return '正在连接...'
  if (testStatus.value === 'success') return '连接成功'
  if (testStatus.value === 'error') return '连接失败'
  return '测试连接'
})

const resetTestStatus = () => {
  testStatus.value = 'idle'
  testMessage.value = ''
}

const testConnection = async () => {
  if (!form.value.streamUrl) {
    testStatus.value = 'error'
    testMessage.value = '错误：请输入流媒体地址 (如 rtsp://...)'
    return
  }

  testStatus.value = 'testing'
  testMessage.value = '正在向目标地址发起协议握手...'

  await new Promise(resolve => setTimeout(resolve, 1500))

  if (form.value.streamUrl.startsWith('rtsp') || form.value.streamUrl.startsWith('rtmp') || form.value.streamUrl.startsWith('http')) {
    testStatus.value = 'success'
    testMessage.value = '连接成功，视频流解码正常，延迟 120ms。'
  } else {
    testStatus.value = 'error'
    testMessage.value = '连接超时或协议不支持，请检查网络或地址拼写。'
  }
}

const submitForm = () => {
  if (!form.value.name || !form.value.region) {
    ElMessage.warning('请填写摄像头名称与所属区域')
    return
  }
  if (mode.value === 'edit') {
    const idx = cameras.value.findIndex((c) => c.id === editingId.value)
    if (idx !== -1) {
      cameras.value[idx] = {
        ...cameras.value[idx],
        name: form.value.name,
        region: form.value.region,
        threshold: Number(form.value.threshold),
      }
      ElMessage.success('摄像头信息已更新')
    }
  } else {
    const newId = `CAM-${String(cameras.value.length + 1).padStart(3, '0')}`
    cameras.value.push({
      id: newId,
      name: form.value.name,
      region: form.value.region,
      threshold: Number(form.value.threshold),
      status: '在线',
      lastSync: new Date().toLocaleTimeString('zh-CN', { hour12: false }).slice(0, 8),
    })
    ElMessage.success('摄像头添加成功！')
  }
  closeModal()
}

// 底部页面的假数据
const cameras = ref([
  { id: 'CAM-001', name: '车间A1高清流', region: '生产A区', threshold: 85, status: '在线', lastSync: '14:30:22' },
  { id: 'CAM-002', name: '门禁入口球机', region: '办公大楼', threshold: 75, status: '在线', lastSync: '14:31:05' },
  { id: 'CAM-003', name: '仓库装卸货台', region: '仓储区', threshold: 80, status: '离线', lastSync: '22:15:40' }
])

const cameraSearch = ref('')

const filteredCameras = computed(() => {
  const kw = cameraSearch.value.trim()
  if (!kw) return cameras.value
  return cameras.value.filter((c) => {
    return c.name.includes(kw) || c.region.includes(kw) || c.id.includes(kw)
  })
})

// 统计卡片（定义：基于当前 cameras 列表，不受搜索过滤影响）
const totalCameras = computed(() => cameras.value.length)
const onlineCameras = computed(() => cameras.value.filter(c => c.status === '在线').length)
const offlineCameras = computed(() => cameras.value.filter(c => c.status !== '在线').length)

// 列表分页（定义：对 filteredCameras 分页，搜索会影响列表与分页）
const pageSize = ref(5)
const currentPage = ref(1)

const totalPages = computed(() => Math.max(1, Math.ceil(filteredCameras.value.length / pageSize.value)))

const pagedCameras = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredCameras.value.slice(start, start + pageSize.value)
})

const pageStartIndex = computed(() => (filteredCameras.value.length ? (currentPage.value - 1) * pageSize.value + 1 : 0))
const pageEndIndex = computed(() => (filteredCameras.value.length ? Math.min(currentPage.value * pageSize.value, filteredCameras.value.length) : 0))

// 搜索/过滤变化时回到第一页；数据变化时把页码夹到有效范围
watch(cameraSearch, () => {
  currentPage.value = 1
})

watch(filteredCameras, () => {
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
}, { deep: true })

const handleView = (cam) => {
  ElMessage.info(`预览：${cam.name}（${cam.region} / 阈值 ${cam.threshold}% / ${cam.status}）`)
}

const handleEdit = (cam) => {
  mode.value = 'edit'
  editingId.value = cam.id
  form.value = {
    name: cam.name,
    region: cam.region,
    location: '',
    streamUrl: '',
    threshold: cam.threshold,
  }
  showModal.value = true
}

const handleDelete = async (cam) => {
  try {
    await ElMessageBox.confirm(
      `确认删除摄像头「${cam.name}」（${cam.id}）吗？此操作不可恢复。`,
      '删除确认',
      { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' }
    )
    cameras.value = cameras.value.filter((c) => c.id !== cam.id)
    ElMessage.success('已删除摄像头')
  } catch {
    // cancelled
  }
}
</script>

<style scoped>
* { box-sizing: border-box; }
.camera-config-page { position: relative; min-height: calc(100vh - 60px); font-family: inherit; color: #1a2332; }
.page-content { padding: 0; transition: filter 0.3s ease; }
.blur-bg { filter: grayscale(20%) opacity(0.8); }

/* --- 底部表格样式 --- */
.stats-row { display: flex; gap: 20px; margin-bottom: 24px; }
.stat-card { flex: 1; background: #fff; border: 1px solid #edf0f5; border-radius: 12px; padding: 20px 24px; display: flex; align-items: center; gap: 16px; }
.stat-icon-wrap { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-icon-wrap.blue { background: rgba(59,158,255,0.1); color: #3b9eff; }
.stat-icon-wrap.green { background: rgba(0,188,164,0.1); color: #00bca4; }
.stat-icon-wrap.red { background: rgba(232,92,92,0.1); color: #e85c5c; }
.stat-info .stat-label { font-size: 13.5px; color: #6b7a90; margin: 0 0 4px 0; }
.stat-info .stat-val { font-size: 24px; font-weight: 700; color: #1a2332; margin: 0; line-height: 1; }
.table-container { background: #fff; border: 1px solid #edf0f5; border-radius: 12px; padding: 24px; }
.table-toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.tb-left { display: flex; align-items: center; gap: 10px; }
.tb-title { font-size: 16px; font-weight: 700; margin: 0; color: #1a2332; }
.tb-right { display: flex; align-items: center; gap: 12px; }
.search-wrap { display: flex; align-items: center; gap: 8px; background: #f4f7fa; border: 1px solid #e8ecf2; border-radius: 8px; padding: 0 12px; height: 36px; width: 220px; }
.search-wrap svg { color: #9aa5b4; }
.search-input { border: none; background: transparent; outline: none; font-size: 13px; width: 100%; }
.btn-primary { display: flex; align-items: center; gap: 6px; height: 36px; padding: 0 16px; background: #3b9eff; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; transition: background 0.2s;}
.btn-primary:hover { background: #2a8aee; }
.aero-table { width: 100%; border-collapse: collapse; }
.aero-table th { font-size: 13px; color: #9aa5b4; font-weight: 500; text-align: left; padding: 12px 0; border-bottom: 1px solid #f0f3f8; }
.aero-table td { padding: 16px 0; font-size: 13.5px; border-bottom: 1px solid #f8f9fc; }
.td-id { font-family: monospace; color: #6b7a90; }
.status-cell { display: flex; align-items: center; gap: 10px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.online { background: #10b981; }
.status-dot.offline { background: #e85c5c; }
.status-text-wrap { display: flex; flex-direction: column; }
.st-main { font-weight: 500; color: #1a2332; }
.st-sub { font-size: 11px; color: #9aa5b4; margin-top: 2px;}
.action-icons { display: flex; gap: 16px; justify-content: flex-end; color: #9aa5b4; }
.ico { cursor: pointer; transition: color 0.2s; }
.ico.view:hover { color: #3b9eff; }
.ico.edit:hover { color: #f5a623; }
.ico.delete:hover { color: #e85c5c; }
.pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; }
.page-info { font-size: 13px; color: #6b7a90; }
.page-controls { display: flex; align-items: center; gap: 8px; }
.page-btn, .page-num { height: 32px; background: #fff; border: 1px solid #e8ecf2; border-radius: 6px; font-size: 13px; color: #4a5568; cursor: pointer; padding: 0 12px; }
.page-num.active { background: #f4f7fa; font-weight: 600; color: #1a2332; border-color: #dcdfe6;}

/* ================= 通用弹窗遮罩层 ================= */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(17, 27, 39, 0.6); backdrop-filter: blur(2px); z-index: 999;
  display: flex; align-items: center; justify-content: center; animation: fadeIn 0.2s ease;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.modal-card {
  width: 580px; background: #fff; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  display: flex; flex-direction: column; animation: slideUp 0.3s ease;
}
.region-card { width: 420px; } /* 第二层弹窗小一点 */
@keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

.modal-header { padding: 24px 30px; display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid transparent; }
.mh-title-area { display: flex; gap: 12px; }
.mh-icon { color: #3b9eff; margin-top: 2px; }
.mh-text h3 { margin: 0 0 6px 0; font-size: 18px; font-weight: 700; color: #1a2332; }
.mh-text p { margin: 0; font-size: 13px; color: #6b7a90; line-height: 1.5; }
.close-btn { background: transparent; border: none; color: #9aa5b4; cursor: pointer; padding: 4px; transition: color 0.2s; }
.close-btn:hover { color: #1a2332; }

/* ================= 弹窗表单内容 ================= */
.modal-body { padding: 0 30px 24px 30px; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; color: #2d3a4a; margin-bottom: 8px; }

.form-row-flex { display: flex; gap: 16px; width: 100%; }
.half-width { flex: 1; min-width: 0; }

.aero-input {
  width: 100%; height: 36px; padding: 0 12px;
  background: #ffffff; border: 1px solid #dcdfe6; border-radius: 6px;
  font-size: 13px; color: #303133; font-family: inherit; outline: none; transition: border-color 0.2s;
}
.aero-input::placeholder { color: #a8abb2; }
.aero-input:focus { border-color: #3b9eff; box-shadow: 0 0 0 2px rgba(59,158,255,0.1); }

.label-row-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.label-row-header label { margin-bottom: 0; }
.link-btn { display: flex; align-items: center; gap: 4px; font-size: 12px; color: #3b9eff; text-decoration: none; font-weight: 500; }
.link-btn:hover { opacity: 0.8; text-decoration: underline; }

.select-wrapper { position: relative; width: 100%; }
.aero-select { appearance: none; -webkit-appearance: none; cursor: pointer; padding-right: 30px; }
.placeholder-color { color: #a8abb2; } 
.select-arrow { position: absolute; right: 10px; top: 11px; color: #9aa5b4; pointer-events: none; }

.segment-control { display: flex; background: #f4f7fa; padding: 4px; border-radius: 8px; margin-bottom: 12px; }
.segment { flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; height: 32px; font-size: 13px; font-weight: 500; color: #6b7a90; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
.segment.active { background: #fff; color: #1a2332; font-weight: 600; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }

.tab-content-area { min-height: 80px; }
.mt-16 { margin-top: 12px; }
.input-with-btn { display: flex; gap: 8px; width: 100%; }

.btn-test {
  display: flex; align-items: center; justify-content: center; gap: 6px; 
  height: 36px; padding: 0 16px; min-width: 100px; flex-shrink: 0;
  background: #f4f7fa; border: 1px solid #dcdfe6; border-radius: 6px;
  font-size: 13px; font-weight: 600; color: #4a5568; cursor: pointer; transition: all 0.2s;
}
.btn-test:hover:not(:disabled) { background: #e8ecf2; }
.btn-test:disabled { opacity: 0.7; cursor: wait; }
.btn-test.success { background: #f0fdf4; border-color: #10b981; color: #10b981; }
.btn-test.error { background: #fff1f0; border-color: #e85c5c; color: #e85c5c; }

.spin-icon { animation: spin 1s linear infinite; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.video-preview-box {
  margin-top: 12px; width: 100%; height: 160px; background: #111b27; border-radius: 8px;
  border: 1px solid #2d3a4a; display: flex; align-items: center; justify-content: center;
  animation: slideDown 0.3s ease;
}
@keyframes slideDown { from { height: 0; opacity: 0; } to { height: 160px; opacity: 1; } }
.preview-placeholder { display: flex; flex-direction: column; align-items: center; gap: 10px; color: rgba(255,255,255,0.6); font-size: 12px; }

.input-hint { margin: 8px 0 0 0; font-size: 12px; color: #9aa5b4; }
.success-text { color: #10b981; font-weight: 500; }
.error-text { color: #e85c5c; font-weight: 500; }

.upload-dropzone { border: 1px dashed #dcdfe6; border-radius: 6px; background: #fafbfc; height: 60px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; width: 100%; }
.upload-dropzone:hover { border-color: #3b9eff; background: #f0f7ff; }
.upload-placeholder { display: flex; align-items: center; gap: 10px; }
.dz-text { margin: 0; font-size: 13px; font-weight: 500; color: #4a5568; }
.dz-hint { margin: 0; font-size: 12px; color: #9aa5b4; }
.upload-selected { display: flex; align-items: center; gap: 8px; }
.file-name { font-size: 13px; font-weight: 600; color: #1a2332; }

.border-top-group { border-top: 1px dashed #edf0f5; padding-top: 16px; margin-top: 4px; }
.label-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.label-with-icon { display: flex; align-items: center; gap: 8px; }
.label-with-icon svg { color: #1a2332; }
.label-with-icon label { margin: 0; }
.val-display { font-size: 14px; font-weight: 700; color: #1a2332; }

.slider-wrap { width: 100%; }
.aero-slider { appearance: none; -webkit-appearance: none; width: 100%; height: 4px; border-radius: 2px; outline: none; background: linear-gradient(to right, #3b9eff var(--val), #edf0f5 var(--val)); cursor: pointer; }
.aero-slider::-webkit-slider-thumb { appearance: none; -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; background: #fff; border: 2px solid #3b9eff; box-shadow: 0 2px 4px rgba(59,158,255,.2); }
.slider-hint { line-height: 1.5; margin-top: 10px; }
.aero-textarea { height: 70px; padding: 10px 12px; resize: none; }

/* --- 区域管理弹窗特有样式 --- */
.add-region-flex { display: flex; gap: 8px; }
.btn-secondary { display: flex; align-items: center; justify-content: center; gap: 4px; height: 36px; padding: 0 16px; background: #f0f7ff; color: #3b9eff; border: 1px solid #d0e4ff; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-secondary:hover { background: #e0f0ff; }
.empty-region { font-size: 13px; color: #a8abb2; text-align: center; padding: 20px 0; background: #fafbfc; border-radius: 6px; border: 1px dashed #dcdfe6;}
.region-list { display: flex; flex-direction: column; gap: 8px; max-height: 150px; overflow-y: auto; }
.region-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: #f4f7fa; border-radius: 6px; font-size: 13px; color: #1a2332; font-weight: 500; }
.delete-link { color: #e85c5c; font-size: 12px; cursor: pointer; }
.delete-link:hover { text-decoration: underline; }

.modal-footer { padding: 16px 30px; border-top: 1px solid #f0f3f8; display: flex; justify-content: flex-end; gap: 12px; background: #fafbfc; border-radius: 0 0 12px 12px; }
.btn-cancel { height: 36px; padding: 0 20px; background: #fff; border: 1px solid #dcdfe6; border-radius: 6px; font-size: 13px; font-weight: 500; color: #4a5568; cursor: pointer; transition: all 0.2s; }
.btn-cancel:hover { background: #f4f7fa; color: #1a2332; }
.btn-confirm { height: 36px; padding: 0 20px; background: #3b9eff; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; color: #fff; cursor: pointer; transition: all 0.2s; }
.btn-confirm:hover { background: #2a8aee; box-shadow: 0 2px 8px rgba(59,158,255,0.3); }
</style>