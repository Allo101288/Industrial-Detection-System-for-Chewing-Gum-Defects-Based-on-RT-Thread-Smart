<template>
	<view class="loading-mask" v-if="show">
	  <view class="loading-content">
		<view class="spinner"></view>
		<text class="loading-text">{{ title }}</text>
	  </view>
	</view>
  </template>

<script>
export default {
  name: "Loading",
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '加载中...'
    }
  }
};
</script>

<style scoped>
.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0); /* 完全透明 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9998; /* 确保遮罩层在最上层 */
}

.loading-content {
  width: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8); /* 设置内容背景透明度为90% */
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: #4F78FF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin-top: 10px;
  font-size: 14px;
  color: #4F78FF;
}
</style>