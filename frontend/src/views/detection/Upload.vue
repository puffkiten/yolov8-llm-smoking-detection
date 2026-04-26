<template>
  <div class="upload-page">
    
    <div class="page-header">
      <h1 class="page-title">发起新检测</h1>
      <p class="page-sub">基于 YOLOv8 视觉识别引擎，支持针对视频监控及静态图片的吸烟违规行为精准检测。</p>
    </div>

    <div class="cards-grid">
      
      <div class="upload-card">
        <div class="card-top">
          <div class="card-title-wrap">
            <div class="icon-box video-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
            </div>
            <h2>视频检测 (Video)</h2>
          </div>
          <span class="tag">流式分析</span>
        </div>
        <p class="card-desc">上传监控录像或录屏文件，系统将逐帧扫描并标注违规时刻。</p>

        <div class="form-group">
          <label>任务名称</label>
          <input type="text" class="aero-input" v-model="videoForm.name" placeholder="例：车间二号位下午时段监控">
        </div>

        <div class="form-group">
          <div class="label-row">
            <label>置信度阈值 (Confidence)</label>
            <span class="val-display">{{ videoForm.confidence.toFixed(2) }}</span>
          </div>
          <div class="slider-wrap">
            <input type="range" min="0" max="1" step="0.01" v-model.number="videoForm.confidence" class="aero-slider" :style="{ '--val': (videoForm.confidence * 100) + '%' }">
            <div class="slider-marks">
              <span>0.0 (高召回)</span>
              <span>0.5 (平衡)</span>
              <span>1.0 (高精度)</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>上传媒体资源</label>
          <input type="file" ref="videoInputRef" accept="video/mp4,video/avi,video/quicktime" style="display: none;" @change="(e) => handleFileSelect(e, 'video')">
          
          <div class="upload-area" @click="triggerFileSelect('video')">
            <div v-if="!videoForm.file" class="upload-idle">
              <div class="upload-icon-large">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="1.5"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/><path d="M12 11v6"/><path d="M9.5 14.5L12 17l2.5-2.5"/></svg>
              </div>
              <p class="upload-text">点击选择或拖拽视频文件到此处</p>
              <p class="upload-hint">支持 MP4、AVI、MOV 格式，文件大小不超过 500MB</p>
            </div>
            
            <div v-else class="upload-progress-state">
              <div class="upload-icon-large small">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="1.5"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
              </div>
              <div class="progress-info">
                <span class="filename blue">{{ videoForm.file.name }}</span>
                <span class="percent" v-if="videoForm.isUploading">{{ videoForm.uploadProgress }}%</span>
                <span class="percent" v-else>{{ (videoForm.file.size / (1024 * 1024)).toFixed(2) }} MB</span>
              </div>
              
              <div class="progress-bar-bg" v-if="videoForm.isUploading">
                <div class="progress-bar-fill" :style="{ width: videoForm.uploadProgress + '%' }"></div>
              </div>
              <p class="time-left" v-if="videoForm.isUploading">正在同步至服务器...</p>
              <p class="time-left" v-else>文件已就绪，等待提交分析</p>
              <video v-if="videoPreviewUrl && videoForm.file && !videoForm.isUploading" :src="videoPreviewUrl" class="video-preview" controls></video>
              <p v-else-if="videoPreviewUnsupported && videoForm.file && !videoForm.isUploading" class="preview-note">当前视频格式浏览器无法预览，但仍可上传检测</p>
            </div>
          </div>
        </div>

        <button class="btn-submit" :disabled="!videoForm.name.trim() || !videoForm.file || videoForm.isUploading" @click="submitToBackend('video')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          {{ videoForm.isUploading ? '正在上传与分析中...' : '开始 AI 智能分析' }}
        </button>
        <p class="submit-hint">分析结果将自动同步至“检测任务”列表</p>
      </div>

      <div class="upload-card">
        <div class="card-top">
          <div class="card-title-wrap">
            <div class="icon-box img-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            </div>
            <h2>图片检测 (Image)</h2>
          </div>
          <span class="tag">图像处理</span>
        </div>
        <p class="card-desc">支持图片上传，快速识别静态场景中的吸烟行为。</p>

        <div class="form-group">
          <label>任务名称</label>
          <input type="text" class="aero-input" v-model="imgForm.name" placeholder="例：吸烟室周度抽检图片集">
        </div>

        <div class="form-group">
          <div class="label-row">
            <label>置信度阈值 (Confidence)</label>
            <span class="val-display">{{ imgForm.confidence.toFixed(2) }}</span>
          </div>
          <div class="slider-wrap">
            <input type="range" min="0" max="1" step="0.01" v-model.number="imgForm.confidence" class="aero-slider" :style="{ '--val': (imgForm.confidence * 100) + '%' }">
            <div class="slider-marks">
              <span>0.0 (高召回)</span>
              <span>0.5 (平衡)</span>
              <span>1.0 (高精度)</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>上传媒体资源</label>
          <input type="file" ref="imgInputRef" accept="image/jpeg,image/png,image/gif" multiple style="display: none;" @change="(e) => handleFileSelect(e, 'image')">

          <div class="upload-area" @click="triggerFileSelect('image')">
            <div v-if="imgForm.files.length === 0" class="upload-idle">
              <div class="upload-icon-large">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="1.5"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/><path d="M12 11v6"/><path d="M9.5 14.5L12 17l2.5-2.5"/></svg>
              </div>
              <p class="upload-text">点击选择或拖拽图片文件到此处</p>
              <p class="upload-hint">支持 JPG、PNG 格式，支持多选，单文件不超过 10MB</p>
            </div>
            
            <div v-else class="upload-progress-state">
              <div class="upload-icon-large small">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
              </div>
              <div class="progress-info centered">
                <span class="filename blue">已选择 {{ imgForm.files.length }} 张图片</span>
                <span class="percent" v-if="imgForm.isUploading">{{ imgForm.uploadProgress }}%</span>
              </div>
              <div class="progress-bar-bg" v-if="imgForm.isUploading">
                <div class="progress-bar-fill" :style="{ width: imgForm.uploadProgress + '%' }"></div>
              </div>
              <p class="time-left" v-if="imgForm.isUploading">正在打包上传中...</p>
              <p class="time-left" v-else>文件已就绪，等待提交分析</p>
              <div v-if="imgPreviewUrls.length === 1" class="preview-single">
                <img :src="imgPreviewUrls[0]" class="thumb-large" alt="">
              </div>
              <div class="preview-grid" v-else-if="imgPreviewUrls.length > 1">
                <img v-for="u in imgPreviewUrls.slice(0,4)" :key="u" :src="u" class="thumb" alt="">
              </div>
            </div>
          </div>
        </div>

        <button class="btn-submit" :disabled="!imgForm.name.trim() || imgForm.files.length === 0 || imgForm.isUploading" @click="submitToBackend('image')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          {{ imgForm.isUploading ? '正在上传与分析中...' : '开始 AI 智能分析' }}
        </button>
        <p class="submit-hint">分析结果将自动同步至“检测任务”列表</p>
      </div>

    </div>

    <div class="info-banner">
      <div class="info-icon-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
      </div>
      <div class="info-content">
        <h4>使用说明</h4>
        <p>置信度阈值越高，检测结果越严苛（减少误报，但可能漏检）；较低的阈值会增加检测灵敏度。视频检测任务通常需要更长的计算时间，您可以在“检测任务”页面查看实时排队及分析进度。</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

const authHeaders = () => {
  const access = localStorage.getItem('access_token') || ''
  return access ? { Authorization: `Bearer ${access}` } : {}
}

// 真实的表单数据结构
const videoForm = reactive({
  name: '',
  confidence: 0.5,
  file: null, // 存放真实的 File 对象
  isUploading: false,
  uploadProgress: 0
})

const imgForm = reactive({
  name: '',
  confidence: 0.5,
  files: [], // 存放真实的多张图片 File 对象数组
  isUploading: false,
  uploadProgress: 0
})

const imgPreviewUrls = ref([])
const videoPreviewUrl = ref('')
const videoPreviewUnsupported = ref(false)

// 对隐藏的 input 标签的引用
const videoInputRef = ref(null)
const imgInputRef = ref(null)

// 触发操作系统文件选择器
const triggerFileSelect = (type) => {
  if (type === 'video') {
    videoInputRef.value.click()
  } else {
    imgInputRef.value.click()
  }
}

// 捕获用户在文件窗口选中的真实文件
const handleFileSelect = (event, type) => {
  const selectedFiles = event.target.files
  if (!selectedFiles || selectedFiles.length === 0) return

  if (type === 'video') {
    videoForm.file = selectedFiles[0] // 视频单选
    if (!videoForm.name) videoForm.name = videoForm.file.name.split('.')[0] // 自动填充任务名
    if (videoPreviewUrl.value) URL.revokeObjectURL(videoPreviewUrl.value)
    videoPreviewUnsupported.value = false
    const f = videoForm.file
    const ok = f && (f.type === 'video/mp4' || f.type === 'video/webm' || f.type === 'video/ogg')
    if (ok) {
      videoPreviewUrl.value = URL.createObjectURL(f)
    } else {
      videoPreviewUrl.value = ''
      videoPreviewUnsupported.value = true
    }
  } else {
    imgForm.files = Array.from(selectedFiles) // 图片多选转数组
    if (!imgForm.name) imgForm.name = `批量图片检测_${new Date().getTime()}`
    imgPreviewUrls.value.forEach((u) => URL.revokeObjectURL(u))
    imgPreviewUrls.value = imgForm.files.map((f) => URL.createObjectURL(f))
  }
}

// 核心：真实向后端发送数据的函数
const submitToBackend = async (type) => {
  const form = type === 'video' ? videoForm : imgForm

  if (!form.name) {
    ElMessage.warning('请输入任务名称')
    return
  }

  // 构建真实的 FormData 格式，供后端解析
  const formData = new FormData()
  formData.append('taskName', form.name)
  formData.append('confidence', form.confidence)

  if (type === 'video') {
    formData.append('file', form.file)
  } else {
    form.files.forEach((file) => formData.append('files', file))
  }

  // 进入上传状态
  form.isUploading = true
  form.uploadProgress = 0

  try {
    const response = await axios.post('/api/detection/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data', ...authHeaders() },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        form.uploadProgress = percentCompleted
      }
    })
    
    if(response.data.code === 200) {
       const createdCount = Number(response.data.created_count || 1)
       ElMessage.success(createdCount > 1 ? `任务提交成功，已创建 ${createdCount} 个图片检测任务` : '任务提交成功，请前往「检测任务」查看结果')
    } else {
       ElMessage.info('任务已提交')
    }

    router.push('/detection/tasks')
    
    // 提交成功后重置表单（可选）
    if(type === 'video') {
      videoForm.file = null
      if (videoPreviewUrl.value) URL.revokeObjectURL(videoPreviewUrl.value)
      videoPreviewUrl.value = ''
      videoPreviewUnsupported.value = false
    } else {
      imgForm.files = []
      imgPreviewUrls.value.forEach((u) => URL.revokeObjectURL(u))
      imgPreviewUrls.value = []
    }

  } catch (error) {
    ElMessage.error('上传失败，请检查网络或后端接口')
    console.error(error)
  } finally {
    form.isUploading = false
    // 重置 input，防止选同一个文件不触发 change 事件
    if (type === 'video' && videoInputRef.value) videoInputRef.value.value = ''
    if (type === 'image' && imgInputRef.value) imgInputRef.value.value = ''
  }
}
</script>

<style scoped>
.upload-page {
  width: 100%;
  color: #1a2332;
}

.page-header { margin-bottom: 24px; }
.page-title { font-size: 22px; font-weight: 700; color: #0d1724; letter-spacing: -.4px; margin-bottom: 6px; }
.page-sub { font-size: 13.5px; color: #6b7a90; margin: 0; }

.cards-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
.upload-card { background: #fff; border-radius: 12px; border: 1px solid #edf0f5; padding: 28px 32px; display: flex; flex-direction: column; }

.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.card-title-wrap { display: flex; align-items: center; gap: 10px; }
.icon-box { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }
.icon-box.video-icon, .icon-box.img-icon { background: rgba(59,158,255,.1); color: #3b9eff; }
.card-title-wrap h2 { font-size: 16px; font-weight: 700; margin: 0; }
.tag { font-size: 12px; font-weight: 500; padding: 3px 10px; border-radius: 20px; background: #f4f7fa; color: #4a5568; border: 1px solid #e8ecf2; }
.card-desc { font-size: 13px; color: #6b7a90; margin: 0 0 28px 0; line-height: 1.5; }

.form-group { margin-bottom: 24px; }
.form-group label { display: flex; align-items: center; gap: 6px; font-size: 13.5px; font-weight: 600; color: #2d3a4a; margin-bottom: 10px; }

/* 优化后的表单输入框：严格对齐 UI 图高度、圆角与色彩 */
.aero-input { 
  width: 100%; 
  height: 38px; /* 显著降低高度，变得更紧凑 */
  padding: 0 12px; 
  background: #ffffff; 
  border: 1px solid #dcdfe6; /* 边框颜色改为更清晰硬朗的浅灰 */
  border-radius: 4px; /* 圆角改小，收起“可爱感”，增强专业感 */
  font-size: 13px; /* 字体随高度微调 */
  color: #303133; 
  font-family: inherit; 
  outline: none; 
  transition: all 0.2s ease; 
}

.aero-input::placeholder { 
  color: #a8abb2; /* 调配出和原图一模一样的浅灰占位符色 */
  font-weight: 400;
}

.aero-input:focus { 
  border-color: #3b9eff; 
  box-shadow: 0 0 0 2px rgba(59,158,255,0.15); /* 减轻 focus 时的光晕，显得更内敛 */
}

.label-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;}
.label-row label { margin-bottom: 0; }
.val-display { font-size: 14px; font-weight: 700; color: #1a2332; background: #f4f7fa; padding: 2px 10px; border-radius: 6px; border: 1px solid #e8ecf2;}

.slider-wrap { width: 100%; padding-top: 5px;}
.aero-slider {
  appearance: none;
  -webkit-appearance: none; 
  width: 100%; height: 6px; border-radius: 3px; outline: none;
  background: linear-gradient(to right, #3b9eff var(--val), #edf0f5 var(--val));
  margin-bottom: 8px; cursor: pointer;
}
.aero-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none; 
  width: 20px; height: 20px; border-radius: 50%; background: #fff;
  border: 2px solid #3b9eff; box-shadow: 0 2px 6px rgba(59,158,255,.25); cursor: grab;
}
.aero-slider::-webkit-slider-thumb:active { cursor: grabbing; transform: scale(1.1); }
.slider-marks { display: flex; justify-content: space-between; font-size: 11.5px; color: #9aa5b4; }

.upload-area { border: 1.5px dashed #c8d0dc; border-radius: 10px; background: #fafbfc; padding: 36px 20px; text-align: center; cursor: pointer; transition: all 0.2s; }
.upload-area:hover { border-color: #3b9eff; background: #f5f8ff; }
.upload-icon-large { width: 56px; height: 56px; background: #eff6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; }
.upload-icon-large.small { width: 44px; height: 44px; margin-bottom: 12px; }
.upload-text { font-size: 14px; font-weight: 500; color: #2d3a4a; margin: 0 0 6px 0; }
.upload-hint { font-size: 12px; color: #9aa5b4; margin: 0; }

.upload-progress-state { width: 100%; max-width: 520px; margin: 0 auto; text-align: center;}
.progress-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px; font-weight: 500; }
.progress-info.centered { justify-content: center; gap: 10px; }
.progress-info.centered .filename.blue { max-width: 100%; }
.filename.blue { color: #3b9eff; max-width: 80%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.percent { color: #2d3a4a; }
.progress-bar-bg { width: 100%; height: 6px; background: #edf0f5; border-radius: 3px; overflow: hidden; margin-bottom: 8px; }
.progress-bar-fill { height: 100%; background: #3b9eff; transition: width 0.3s ease; }
.time-left { font-size: 11.5px; color: #9aa5b4; margin: 0; }
.preview-single { display: flex; justify-content: center; margin-top: 12px; }
.thumb-large { width: 220px; height: 140px; object-fit: cover; border-radius: 12px; border: 1px solid #e8ecf2; background: #fff; }
.preview-grid { display: grid; grid-template-columns: repeat(4, 70px); justify-content: center; gap: 8px; margin-top: 12px; }
.thumb { width: 70px; height: 70px; object-fit: cover; border-radius: 10px; border: 1px solid #e8ecf2; background: #fff; }
.video-preview { width: 100%; margin-top: 12px; border-radius: 10px; border: 1px solid #e8ecf2; max-height: 220px; background: #000; }
.preview-note { margin-top: 10px; font-size: 12px; color: #6b7a90; }

.btn-submit {
  width: 100%; height: 48px; border-radius: 8px; background: #3b9eff; color: white; border: none; font-size: 14.5px; font-weight: 600; cursor: pointer; font-family: inherit;
  display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s; margin-top: 10px;
}
.btn-submit:hover:not(:disabled) { background: #2a8aee; box-shadow: 0 6px 16px rgba(59,158,255,.25); transform: translateY(-1px); }
.btn-submit:disabled { background: #c8d0dc; cursor: not-allowed; }

/* 按钮下方的辅助提示小字 */
.submit-hint { 
  text-align: center; 
  font-size: 12px; 
  color: #9aa5b4; /* 完美的浅灰辅助色 */
  margin: 12px 0 0 0; 
  letter-spacing: 0.5px;
}

.info-banner { background: #f0f7ff; border: 1px solid #d0e4ff; border-radius: 12px; padding: 20px 24px; display: flex; align-items: flex-start; gap: 16px; margin-top: 24px; }
.info-icon-wrap { margin-top: 2px; }
.info-content h4 { margin: 0 0 6px 0; font-size: 14px; font-weight: 600; color: #3b9eff; }
.info-content p { margin: 0; font-size: 13px; color: #5a6475; line-height: 1.6; }
</style>
