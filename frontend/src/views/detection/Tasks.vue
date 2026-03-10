<template>
  <div class="task-detail-page">
    
    <div class="layout-grid">
      <aside class="left-panel">
        <div class="panel-card">
          
          <div class="task-header">
            <span class="status-badge success">已完成</span>
            <svg class="external-link" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </div>
          <h1 class="task-id">{{ taskInfo.id }}</h1>

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
                <div class="value">{{ taskInfo.fileSize }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg> 画面分辨率</div>
                <div class="value">{{ taskInfo.resolution }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 处理耗时</div>
                <div class="value">{{ taskInfo.processTime }}</div>
              </li>
            </ul>
          </div>

          <div class="info-section">
            <h3 class="section-title">时间流水</h3>
            <ul class="info-list">
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> 创建时间</div>
                <div class="value">{{ taskInfo.createTime }}</div>
              </li>
              <li>
                <div class="label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 完成时间</div>
                <div class="value">{{ taskInfo.finishTime }}</div>
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

          <div class="alert-box" v-if="taskInfo.hasViolation">
            <div class="alert-header">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              检测到违规行为
            </div>
            <p class="alert-desc">系统在图像右侧区域识别到疑似吸烟动作，置信度 <strong>96.2%</strong>。建议人工介入核实并记录。</p>
          </div>

        </div>
      </aside>

      <main class="right-panel">
        
        <div class="image-card">
          <div class="img-header">
            <div class="img-title"><span class="dot gray"></span> 原始图像 (Original Source)</div>
            <div class="img-subtitle">IMG_SOURCE_001.JPG</div>
          </div>
          <div class="img-container">
            <img src="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80" alt="Original Source" class="source-img">
          </div>
        </div>

        <div class="image-card">
          <div class="img-header">
            <div class="img-title"><span class="dot blue"></span> AI 检测结果 (Aero YOLOv8 Analysis)</div>
            <div class="badge-blue">Confidence: 0.96</div>
          </div>
          <div class="img-container relative-container">
            <img src="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80" alt="AI Result" class="source-img">
            
            <div class="bounding-box smoking-box">
              <span class="box-label">Smoking 96.2%</span>
            </div>
            <div class="bounding-box lighter-box">
              <span class="box-label outline">Lighter: 89.4%</span>
            </div>

            <div class="watermark-alert">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              检测到违规吸烟行为 - 已自动存证
            </div>
          </div>
        </div>

        <div class="bottom-actions">
          <button class="btn-outline" @click="$router.push('/dashboard')">返回任务列表</button>
          <button class="btn-danger" @click="markAsViolation">标记为违规</button>
          <button class="btn-outline" @click="verifyPass">核实通过</button>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// 模拟的任务详情数据
const taskInfo = ref({
  id: 'Aero_Task_20240520_001',
  confidence: '85%',
  model: 'Aero-YOLO-v8s-Industrial',
  device: 'NVIDIA RTX 4090 (vGPU)',
  fileSize: '4.2 MB',
  resolution: '1920 x 1080',
  processTime: '2.84s',
  createTime: '2024-05-20 14:30:22',
  finishTime: '2024-05-20 14:30:25',
  hasViolation: true
})

const handleExport = () => {
  ElMessage.success('报告导出中，请稍候...')
}

const handleRetry = () => {
  ElMessage.info('已重新加入检测队列')
}

const markAsViolation = () => {
  ElMessage.error('已人工确认违规，记录已封存。')
}

const verifyPass = () => {
  ElMessage.success('已标记为误报，核实通过。')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

.task-detail-page {
  width: 100%;
  font-family: 'Sora', 'Noto Sans SC', sans-serif;
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

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.status-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}
.status-badge.success { background: #f4f7fa; color: #4a5568; border: 1px solid #e8ecf2; }

.external-link { color: #9aa5b4; cursor: pointer; transition: color 0.2s; }
.external-link:hover { color: #3b9eff; }

.task-id {
  font-size: 18px;
  font-weight: 700;
  color: #0d1724;
  margin: 0 0 24px 0;
  word-break: break-all;
}

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

.img-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: #f4f7fa;
  border: 1px solid #edf0f5;
}
.source-img {
  width: 100%;
  height: auto;
  display: block;
}

/* --- YOLO 纯 CSS 识别框 --- */
.relative-container {
  position: relative;
}

/* 大红色吸烟框 */
.bounding-box {
  position: absolute;
  border: 2px solid #e85c5c;
  background: rgba(232,92,92,0.1);
  box-shadow: 0 0 0 1px rgba(255,255,255,0.2) inset;
}
.smoking-box {
  /* 模拟图中大框的位置 */
  top: 35%; right: 15%;
  width: 18%; height: 45%;
}
.box-label {
  position: absolute;
  top: -24px; left: -2px;
  background: #e85c5c;
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  white-space: nowrap;
}

/* 白色打火机细框 */
.lighter-box {
  top: 60%; right: 18%;
  width: 5%; height: 12%;
  border-color: #fff;
  background: transparent;
}
.box-label.outline {
  top: -22px; left: 50%; transform: translateX(-50%);
  background: transparent;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.8);
}

/* 右下角告警水印 */
.watermark-alert {
  position: absolute;
  bottom: 16px; right: 16px;
  background: #e85c5c;
  color: white;
  font-size: 13px; font-weight: 600;
  padding: 8px 16px;
  border-radius: 6px;
  display: flex; align-items: center; gap: 8px;
  box-shadow: 0 4px 12px rgba(232,92,92,0.3);
}

/* ================= 底部操作区 ================= */
.bottom-actions {
  display: flex;
  justify-content: flex-end; /* 核心修复：让内部所有按钮整体靠右对齐 */
  align-items: center;
  gap: 16px; /* 统一按钮之间的间距 */
  padding-top: 16px;
}

/* 为了保证三个按钮大小绝对一致，统一加上左右内边距 */
.btn-outline { padding: 0 20px; }
.btn-danger { padding: 0 20px; }
</style>