<template>
  <button
    :class="['base-btn', `base-btn--${type}`, { 'base-btn--block': block }]"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup>
const props = defineProps({
  type: {
    type: String,
    default: 'primary', // primary | default | danger
  },
  block: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.base-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  border: 1px solid transparent;
  background: #fff;
  color: #374151;
  transition: all 0.2s;
}

.base-btn--block {
  width: 100%;
}

.base-btn--primary {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.base-btn--primary:hover {
  background: #2a8aee;
  border-color: #2a8aee;
  box-shadow: 0 4px 12px rgba(59, 158, 255, 0.3);
}

.base-btn--default {
  background: #fff;
  border-color: #d1d5db;
  color: #374151;
}

.base-btn--default:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.base-btn--danger {
  background: #e85c5c;
  border-color: #e85c5c;
  color: #fff;
}

.base-btn--danger:hover {
  background: #d74b4b;
  border-color: #d74b4b;
  box-shadow: 0 4px 12px rgba(232, 92, 92, 0.25);
}

.base-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}
</style>

