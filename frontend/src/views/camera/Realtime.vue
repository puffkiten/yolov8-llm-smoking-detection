<template>
  <div class="realtime-page">
    <div class="layout-grid">
      <main class="left-panel">
        <div class="matrix-header">
          <div class="mh-left">
            <h2 class="mh-title">监控矩阵 <span class="count-tag">({{ activeCameraCount }}路已联)</span></h2>
            <div class="live-status-pill">
              <span class="pulse-dot"></span> AI 实时推理中
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
          <div class="v-card" v-for="cam in cameraList" :key="cam.id" :class="{ 'alert-border': cam.hasAlert && showLabels }">
            <img :src="cam.cover" class="v-stream">
            
            <template v-if="cam.hasAlert && showLabels">
              <div class="ai-box smoking pulse-red"><span class="tag red">SMOKING 94.5%</span></div>
              <div class="ai-box person"><span class="tag blue">PERSON 98.2%</span></div>
            </template>

            <div class="v-overlay">
              <div class="vo-header">
                <div class="cam-info-label">
                  <span class="dot-indicator" :class="cam.status"></span>
                  <span class="name">{{ cam.name }}</span>
                </div>
                <span class="spec-label">1080P / 25fps</span>
              </div>
              <div class="vo-footer">2024-05-20 14:30:16</div>
              <div class="vo-alert-tag" v-if="cam.hasAlert && showLabels">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                检测到违规吸烟
              </div>
            </div>
          </div>
        </div>

        <div class="status-footer">
          <div class="s-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b9eff" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg></div>
          <div class="s-text">
            <h4>系统状态良好</h4>
            <p>当前检测频率: 15 FPS | 检测模型: YOLOv8-Smoking-v2 | 告警延迟: &lt; 500ms</p>
          </div>
        </div>
      </main>

      <aside class="right-panel">
        <div class="panel-header">
          <h3 class="panel-title">设备列表</h3>
          <span class="online-status">5 / 6 在线</span>
        </div>

        <div class="tree-container">
          <div class="tree-group" v-for="group in deviceTree" :key="group.name">
            <div class="group-header">
              <span class="group-name">{{ group.name }}</span>
              <span class="group-count">{{ group.devices.length }}</span>
            </div>
            
            <div class="device-node" v-for="dev in group.devices" :key="dev.id">
              <span class="status-dot" :class="dev.status"></span>
              <div class="device-details">
                <span class="d-name" :class="{ 'red-text': dev.status === 'alert' }">{{ dev.name }}</span>
                <span class="d-loc"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> {{ dev.loc }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="suggestion-card">
          <div class="sug-title">智能巡检建议</div>
          <p class="sug-desc">系统检测到“仓库区-3号库入口”环境光线变化较大，建议调整阈值。</p>
          <a href="#" class="sug-btn" @click.prevent="$router.push('/camera/config')">立即调整 &rarr;</a>
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
import { ref, computed } from 'vue'

const viewMode = ref('grid')
const showLabels = ref(true)

// 模拟真实数据源
const cameraList = ref([
  { id: 1, name: '行政楼-A1大堂', status: 'online', hasAlert: false, cover: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80' },
  { id: 2, name: '仓库区-3号库入口', status: 'online', hasAlert: true, cover: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80' },
  { id: 3, name: '行政楼-西侧走廊', status: 'online', hasAlert: false, cover: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80' },
  { id: 4, name: '园区-东侧吸烟亭', status: 'online', hasAlert: false, cover: 'https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=800&q=80' }
])

// 🌟 逻辑联动：自动计算连接路数
const activeCameraCount = computed(() => cameraList.value.length)

const deviceTree = [
  { 
    name: '办公行政区', 
    devices: [
      { id: 101, name: 'A1号楼大堂', loc: '1F 大堂', status: 'online' },
      { id: 102, name: '西侧走廊', loc: '2F 走廊', status: 'online' }
    ] 
  },
  { 
    name: '生产仓库区', 
    devices: [
      { id: 201, name: '3号仓库入口', loc: '仓库区外围', status: 'alert' }
    ] 
  }
]
</script>

<style scoped>
.realtime-page { width: 100%; color: #1a2332; font-family: inherit; }
.layout-grid { display: grid; grid-template-columns: 1fr 320px; gap: 24px; align-items: flex-start; }

/* 左侧样式纠偏 */
.mh-left { display: flex; align-items: baseline; gap: 16px; margin-bottom: 16px; }
.mh-title { font-size: 20px; font-weight: 700; margin: 0; display: flex; align-items: baseline; gap: 8px;}
.count-tag { color: #6b7a90; font-size: 16px; font-weight: 500; }
.live-status-pill { display: flex; align-items: center; gap: 6px; padding: 4px 10px; background: #eff6ff; color: #3b9eff; border-radius: 20px; font-size: 12px; font-weight: 600; transform: translateY(-2px); }
.pulse-dot { width: 6px; height: 6px; background: #3b9eff; border-radius: 50%; animation: blink 1.5s infinite; }
@keyframes blink { 0%, 100% { opacity: 1 } 50% { opacity: 0.3 } }

/* 药丸按钮组 */
.pill-group { display: flex; align-items: center; background: #fff; border: 1px solid #e8ecf2; border-radius: 10px; padding: 4px; gap: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.p-btn { display: flex; align-items: center; gap: 6px; border: none; background: transparent; padding: 6px 12px; font-size: 12px; font-weight: 600; color: #4a5568; cursor: pointer; border-radius: 6px; transition: all 0.2s; }
.p-btn.active { background: #f4f7fa; color: #1a2332; }
.p-divider { width: 1px; height: 16px; background: #e8ecf2; margin: 0 4px; }
.text-muted { color: #9aa5b4; }

/* 视频网格与布局切换 */
.video-container.grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.video-container.list-layout { display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }

.v-card { position: relative; aspect-ratio: 16/9; background: #000; border-radius: 12px; overflow: hidden; border: 1.5px solid transparent; transition: all 0.3s; }
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

/* AI 识别框效果 */
.ai-box { position: absolute; border: 1.5px solid; z-index: 5; }
.ai-box.smoking { top: 32%; left: 42%; width: 14%; height: 18%; border-color: #e85c5c; background: rgba(232,92,92,0.1); }
.ai-box.person { top: 15%; left: 28%; width: 22%; height: 60%; border-color: #3b9eff; background: rgba(59,158,255,0.05); }
.pulse-red { animation: pulseAnim 1s infinite alternate; }
@keyframes pulseAnim { from { box-shadow: 0 0 2px #e85c5c; } to { box-shadow: 0 0 12px #e85c5c; } }
.tag { position: absolute; top: -20px; left: -1px; color: #fff; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 2px 2px 0 0; }
.tag.red { background: #e85c5c; }
.tag.blue { background: #3b9eff; }

/* 底部状态条 */
.status-footer { display: flex; align-items: center; gap: 16px; background: #f8fafc; padding: 18px 24px; border-radius: 12px; border: 1px solid #edf0f5; }
.s-text h4 { margin: 0 0 4px 0; font-size: 14px; font-weight: 600; color: #0d1724; }
.s-text p { margin: 0; font-size: 12px; color: #64748b; font-family: monospace; }

/* ================= 右侧面板纠偏 ================= */
.right-panel { background: #fff; border: 1px solid #edf2f7; border-radius: 12px; padding: 24px; box-shadow: 0 2px 10px rgba(0,0,0,0.01); display: flex; flex-direction: column; gap: 24px; }
.panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 16px; }
.panel-title { font-size: 16px; font-weight: 700; margin: 0; }
.online-status { font-size: 12px; color: #64748b; font-weight: 600; background: #f8fafc; padding: 4px 10px; border-radius: 20px; border: 1px solid #f1f5f9; }

.tree-group { display: flex; flex-direction: column; gap: 12px; }
.group-header { display: flex; justify-content: space-between; align-items: center; }
.group-name { font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.group-count { font-size: 10px; color: #94a3b8; background: #f1f5f9; padding: 1px 6px; border-radius: 4px; }

/* 🌟 设备节点样式完全还原 UI */
.device-node { display: flex; align-items: flex-start; gap: 12px; padding: 4px 0; cursor: pointer; transition: opacity 0.2s; }
.device-node:hover { opacity: 0.7; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.status-dot.online { background: #10b981; }
.status-dot.alert { background: #e85c5c; animation: blink 1s infinite; }
.device-details { display: flex; flex-direction: column; gap: 2px; }
.d-name { font-size: 14px; font-weight: 500; color: #1e293b; }
.red-text { color: #e85c5c; font-weight: 600; }
.d-loc { font-size: 11px; color: #94a3b8; display: flex; align-items: center; gap: 4px; }

.suggestion-card { background: #f0f7ff; border: 1px solid #d0e4ff; border-radius: 10px; padding: 16px; }
.sug-title { font-size: 13px; font-weight: 700; color: #3b9eff; margin-bottom: 8px; }
.sug-desc { font-size: 12px; color: #475569; line-height: 1.5; margin: 0 0 12px 0; }
.sug-btn { font-size: 12px; color: #3b9eff; font-weight: 600; text-decoration: none; }

.btn-add-ghost { height: 44px; background: #fff; border: 1px dashed #cbd5e1; border-radius: 8px; font-size: 13px; font-weight: 600; color: #64748b; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-add-ghost:hover { border-color: #3b9eff; color: #3b9eff; background: #f0f7ff; }
</style>