<template>
  <div class="share-page">
    <div class="card" v-if="state === 'ok'">
      <div class="header">
        <div class="title">违规报告</div>
        <div class="meta">
          <span class="pill danger" v-if="violationPercent > 0">{{ violationPercent.toFixed(1) }}%</span>
          <span class="pill" v-else>未检出</span>
        </div>
      </div>

      <div class="image-wrap" ref="containerRef">
        <img ref="imgRef" :src="sourceUrl" class="img" alt="report" @load="recomputeDrawRect">
        <div class="overlay">
          <div
            v-for="(b, idx) in detections"
            :key="idx"
            class="bbox"
            :class="{ danger: Number(b.cls) === 0 }"
            :style="bboxStyle(b)"
          >
            <span class="bbox-label">{{ b.label }} {{ (Number(b.conf || 0) * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>

      <div class="section">
        <div class="section-title">AI 分析</div>
        <div class="text" v-if="llmReport">{{ llmReport }}</div>
        <div class="text muted" v-else>暂无 AI 文本分析</div>
      </div>
    </div>

    <div class="card" v-else-if="state === 'loading'">
      <div class="center">正在加载报告…</div>
    </div>

    <div class="card" v-else>
      <div class="center danger-text">{{ errorText }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()

const state = ref('loading')
const errorText = ref('')

const sourceUrl = ref('')
const detections = ref([])
const llmReport = ref('')
const violationConfidence = ref(0)

const containerRef = ref(null)
const imgRef = ref(null)
const drawRect = ref({ offsetX: 0, offsetY: 0, drawW: 0, drawH: 0 })

const violationPercent = computed(() => Number(violationConfidence.value || 0) * 100)

const recomputeDrawRect = () => {
  const container = containerRef.value
  const img = imgRef.value
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
  drawRect.value = { offsetX, offsetY, drawW, drawH }
}

const bboxStyle = (b) => {
  const r = drawRect.value || {}
  if (!r.drawW || !r.drawH) {
    return { left: (b.x || 0) + '%', top: (b.y || 0) + '%', width: (b.w || 0) + '%', height: (b.h || 0) + '%' }
  }
  const x = r.offsetX + (Number(b.x || 0) / 100) * r.drawW
  const y = r.offsetY + (Number(b.y || 0) / 100) * r.drawH
  const w = (Number(b.w || 0) / 100) * r.drawW
  const h = (Number(b.h || 0) / 100) * r.drawH
  return { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' }
}

onMounted(async () => {
  const token = (route.query.id || route.query.token || '').toString().trim()
  if (!token) {
    state.value = 'error'
    errorText.value = '链接无效：缺少分享参数'
    return
  }
  try {
    const resp = await axios.get(`http://127.0.0.1:8000/api/share/report`, { params: { id: token } })
    const d = resp.data || {}
    sourceUrl.value = d.source_url || ''
    detections.value = Array.isArray(d.detections) ? d.detections : []
    llmReport.value = (d.llm_report || '').toString()
    violationConfidence.value = Number(d.violation_confidence || 0)
    state.value = 'ok'
  } catch (e) {
    const detail = e?.response?.data?.detail
    state.value = 'error'
    errorText.value = detail ? `无法打开报告：${detail}` : '无法打开报告'
  }
})
</script>

<style scoped>
.share-page {
  min-height: 100vh;
  width: 100%;
  background: #0b1220;
  display: flex;
  justify-content: center;
  padding: 18px 12px;
  color: #e6edf7;
}
.card {
  width: min(880px, 100%);
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 14px;
  backdrop-filter: blur(8px);
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 4px 2px 12px 2px;
}
.title {
  font-size: 15px;
  font-weight: 800;
}
.meta {
  display: flex;
  align-items: center;
  gap: 8px;
}
.pill {
  height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 800;
  color: #cfe2ff;
  background: rgba(59,158,255,0.15);
  border: 1px solid rgba(59,158,255,0.25);
}
.pill.danger {
  color: #ffd7d7;
  background: rgba(232,92,92,0.18);
  border-color: rgba(232,92,92,0.35);
}
.image-wrap {
  width: 100%;
  height: min(72vh, 560px);
  background: #0b1220;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
  position: relative;
}
.img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}
.overlay { position: absolute; inset: 0; pointer-events: none; }
.bbox {
  position: absolute;
  border: 2px solid rgba(59,158,255,0.95);
  background: rgba(59,158,255,0.08);
  box-shadow: 0 0 0 1px rgba(0,0,0,0.25) inset;
}
.bbox.danger {
  border-color: rgba(232,92,92,0.95);
  background: rgba(232,92,92,0.10);
}
.bbox-label {
  position: absolute;
  top: -26px;
  left: -2px;
  padding: 5px 9px;
  font-size: 12px;
  font-weight: 800;
  border-radius: 8px;
  background: rgba(13, 23, 36, 0.92);
  color: #fff;
  white-space: nowrap;
}
.section { padding: 14px 4px 6px 4px; }
.section-title { font-size: 13px; font-weight: 800; margin-bottom: 8px; color: #cfe2ff; }
.text { font-size: 13px; line-height: 1.7; color: #e6edf7; white-space: pre-wrap; }
.text.muted { color: rgba(230, 237, 247, 0.65); }
.center {
  padding: 44px 0;
  text-align: center;
  font-size: 13px;
  color: rgba(230, 237, 247, 0.75);
}
.danger-text { color: #ffd7d7; }
</style>

