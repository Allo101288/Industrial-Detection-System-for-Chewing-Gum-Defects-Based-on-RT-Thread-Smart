<template>
  <view class="container">
    <!-- Header -->
    <view class="header">
      <view class="header-bg-circle header-bg-circle-1"></view>
      <view class="header-bg-circle header-bg-circle-2"></view>
      <view class="header-content">
        <view class="header-icon">
          <img src="../../static/111.png" alt="" />
        </view>
        <text class="header-title">口香糖缺陷工业检测系统</text>
      </view>
    </view>

    <!-- Status Card -->
    <view class="status-card">
      <view class="card-header">
        <view class="card-title">
          <text class="activity-icon">📊</text>
          <text>实时检测状态</text>
        </view>
        <view class="status-badge" :class="isRunning ? 'running' : 'stopped'">
          <text>{{ isRunning ? "运行中" : "已停止" }}</text>
        </view>
      </view>
      <view class="status-grid">
        <view class="status-item">
          <view class="status-icon status-icon-blue">
            <text class="icon">📈</text>
          </view>
          <text class="status-number">{{ defectCount }}</text>
          <text class="status-label">缺陷总数</text>
        </view>
        <view class="status-item">
          <view class="status-icon status-icon-green">
            <text class="icon">✅</text>
          </view>
          <text class="status-number">98.5%</text>
          <text class="status-label">检测精度</text>
        </view>
        <view class="status-item">
          <view class="status-icon status-icon-orange">
            <text class="icon">⚠️</text>
          </view>
          <text class="status-number">{{defectCountNow}}</text>
          <text class="status-label">当前缺陷</text>
        </view>
      </view>
    </view>
    <view class="control-buttons">
      <button class="control-btn start-btn" @click="kaishi(1.0)">
        <text class="btn-icon">▶️</text>
        <text>{{ kaikai }}</text>
      </button>
      <button class="control-btn pause-btn" @click="kaishi(2.0)">
        <text class="btn-icon">⏸️</text>
        <text>暂停</text>
      </button>
      <button class="control-btn stop-btn" @click="kaishi(0.0)">
        <text class="btn-icon">⏹️</text>
        <text>结束</text>
      </button>
    </view>
    <!-- Real-time Display -->
    <view class="detection-card">
      <view class="card-header nonono">
        <view class="card-title">
          <view class="live-indicator"></view>
          <text>实时图像展示</text>
        </view>
      </view>
      <view class="detection-list">
        <view
          v-for="(item, index) in items"
          :key="index"
          class="detection-item"
        >
          <view class="image-container">
            <view class="placeholder-image">
              <!-- <text class="placeholder-text">检测图像 {{ index + 1 }}</text> -->
              <img :src="item.src" alt="" @click="onLongPress(item.src)" />
            </view>
          </view>
          <view class="detection-info">
            <text class="detection-time">{{ item.created }}</text>
            <text class="detection-count">缺陷数量: {{ item.defect_count }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Control Buttons -->

    <!-- Bottom Navigation -->
    <!-- <view class="bottom-nav">
      <view class="nav-item active" @click="switchTab('home')">
        <text class="nav-icon">🏠</text>
        <text class="nav-label">主页</text>
      </view>
      <view class="nav-item" @click="switchTab('chat')">
        <text class="nav-icon">💬</text>
        <text class="nav-label">智能助手</text>
      </view>
      <view class="nav-item" @click="switchTab('profile')">
        <text class="nav-icon">👤</text>
        <text class="nav-label">个人</text>
      </view>
    </view> -->
  </view>
</template>

<script setup>
import { ref } from "vue";
//import { uni } from 'some-uni-library' // Declare the uni variable here
import { onShow, onLoad, onHide } from "@dcloudio/uni-app";
import Loading from "../../components/Loading.vue";
const isRunning = ref(false);
let timer = null;
  const kaikai = ref("开始");
  const defectCount = ref(0);
  const defectCountNow = ref(0);
  onShow(() => {
    getImages(); // 立即获取一次
    timer = setInterval(getImages, 500); // 每0.5秒获取一次
  });
  
  onHide(() => {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  });
  const items = ref([
  //   {
  //     src: "https://picsum.photos/200",
  //   },
  ]);
// const detectionData = ref([
//   { time: "2025-07-07 19:33:36", count: 2, status: "warning" },
//   { time: "2025-07-07 19:33:34", count: 1, status: "normal" },
//   { time: "2025-07-07 19:33:32", count: 0, status: "good" },
// ]);

//Sat Jul 05 2025
const getImages = () => {
    uni.request({
      url: "http://112.74.32.111:8000/images",
      success: (res) => {
        if (res.statusCode === 200) {
          //console.log("获取图片成功", res.data.images);
          // 获取当前日期
          const today = new Date();
          const todayDateOnly = new Date(
            today.getFullYear(),
            today.getMonth(),
            today.getDate()
          );
  
          // 获取 items.value 中的最新图片时间戳（如果有）
          const latestCreatedTime = items.value.length > 0
            ? parseDateTime(items.value[0].created)
            : null;
  
          // 筛选出当天的图片，并且只保留比最新图片时间戳更新的图片
          const filteredImages = res.data.images
            .slice(0, 1000) // 截取前1000个数据
            .map(item => {
              // 将 timestamp 转换为 create 格式 (YYYY-MM-DD HH:mm:ss)
              const createStr = item.timestamp
                .replace('T', ' ')          // 替换 T 为空格
                .split('.')[0];              // 去除毫秒部分
              
              return {
                ...item,
                created: createStr  // 使用转换后的时间字符串
              };
            })
            .filter((item) => {
              const createdDate = parseDateTime(item.created);
              return (
                createdDate.toDateString() === todayDateOnly.toDateString() &&
                (!latestCreatedTime || createdDate > latestCreatedTime)
              );
            })
            .map((item) => ({
              src: "http://112.74.32.111:8000" + item.url,
              created: item.created,
              defect_count: item.defect_count || 0, // 如果没有 defect_count，默认为 0
            }));
  
          // 如果 items 是空，则直接赋值；否则将新筛选的结果添加到数组头部
          if (filteredImages.length > 0) {
            items.value = [...filteredImages, ...items.value];
          }
          defectCount.value = 0; // 重置 defectCount
          items.value.forEach(e => {
              defectCount.value += e.defect_count || 0; // 累加 defect_count
          });
          defectCountNow.value = items.value[0]?.defect_count || 0; // 获取最新图片的 defect_count
        } else {
          console.error("获取图片失败", res);
        }
      },
      fail: (err) => {
        console.error("请求失败", err);
      },
    });
  };
  
  // 辅助函数：解析日期时间字符串（保持不变）
  function parseDateTime(dateTimeStr) {
    const dateTimeParts = dateTimeStr.split(" ");
    const dateParts = dateTimeParts[0].split("-");
    const timeParts = dateTimeParts[1].split(":");
    return new Date(
      parseInt(dateParts[0], 10), // 年
      parseInt(dateParts[1], 10) - 1, // 月（从0开始）
      parseInt(dateParts[2], 10), // 日
      parseInt(timeParts[0], 10), // 时
      parseInt(timeParts[1], 10), // 分
      parseInt(timeParts[2], 10) // 秒
    );
  }
  const kaishi = (e) => {
    uni.request({
      url: "https://iot-api.heclouds.com/thingmodel/set-device-property", // 请求的 URL
      method: "POST", // 请求方法
      header: {
        "Content-Type": "application/json", // 设置请求头
        // 如果需要，可以在这里添加其他请求头，例如认证 token
        // "api-key": "your-api-key", // 示例：添加 API 密钥
        authorization:
          "version=2018-10-31&res=products%2FOrT98dB198%2Fdevices%2Flotus1&et=1917513743&method=md5&sign=rski44rCWDk0cXSVrbJOWg%3D%3D",
      },
  
      data: {
        product_id: "OrT98dB198",
        device_name: "lotus1",
        params: {
          level: e,
        },
      },
      success: (res) => {
        console.log("请求成功", res);
        console.log(e);
        isRunning.value = e === 1 ; // 设置 isRunning 状态
        if (e == 2) kaikai.value = "继续";
        if (e == 1 || e == 0) kaikai.value = "开始";
        // 在这里处理成功的逻辑
      },
      fail: (err) => {
        console.error("请求失败", err);
        // 在这里处理失败的逻辑
      },
    });
  };
  const getNumber = (e) => {
    uni.request({
      url: "https://iot-api.heclouds.com/thingmodel/set-device-property", // 请求的 URL
      method: "POST", // 请求方法
      header: {
        "Content-Type": "application/json", // 设置请求头
        // 如果需要，可以在这里添加其他请求头，例如认证 token
        // "api-key": "your-api-key", // 示例：添加 API 密钥
        authorization:
          "version=2018-10-31&res=products%2FOrT98dB198%2Fdevices%2Flotus1&et=1917513743&method=md5&sign=rski44rCWDk0cXSVrbJOWg%3D%3D",
      },
  
      data: {
        product_id: "OrT98dB198",
        device_name: "lotus1",
        params: {
          level: e,
        },
      },
      success: (res) => {
        console.log("请求成功", res);
        console.log(e);
        if (e == 2) kaikai.value = "继续";
        if (e == 1 || e == 0) kaikai.value = "开始";
        // 在这里处理成功的逻辑
      },
      fail: (err) => {
        console.error("请求失败", err);
        // 在这里处理失败的逻辑
      },
    });
  };
  function onLongPress(imageUrl) {
    // 假设 items.value 是一个包含多个图片对象的数组
    const allImageUrls = items.value.map(item => item.src); // 提取所有图片的 URL
  
    // 找到当前点击的图片在 allImageUrls 中的索引
    const currentIndex = allImageUrls.indexOf(imageUrl);
  
    uni.previewImage({
      current: currentIndex, // 当前要显示的图片url
      urls: allImageUrls, // 需要预览的图片url列表数组
      success: function(res) {
        console.log('图片预览成功', res);
      },
      fail: function(err) {
        console.error('图片预览失败', err);
      }
    });
  }
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 50%, #f3e8ff 100%);
  padding-bottom: 120rpx;
}

.header {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  padding: 40rpx 40rpx 40rpx;
  color: white;
  position: relative;
  overflow: hidden;
}

.header-bg-circle {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.header-bg-circle-1 {
  width: 200rpx;
  height: 200rpx;
  top: -100rpx;
  right: -100rpx;
}

.header-bg-circle-2 {
  width: 160rpx;
  height: 160rpx;
  bottom: -80rpx;
  left: -80rpx;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24rpx;
  position: relative;
  z-index: 10;
}

.header-icon {
  width: 64rpx;
  height: 64rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.header-icon img {
  width: 53rpx;
  height: auto;
}
.header-title {
  font-size: 1.25rem;
  font-weight: bold;
}

.status-card {
  margin: 30rpx 30rpx 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.1);
}
.detection-card {
  margin: 30rpx 30rpx 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 30rpx 30rpx 24rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nonono {
}
.card-title {
  display: flex;
  align-items: center;
  gap: 16rpx;
  font-size: 36rpx;
  font-weight: bold;
  color: #1f2937;
}

.activity-icon {
  font-size: 40rpx;
}

.status-badge {
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  font-weight: 500;
}

.status-badge.running {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-badge.stopped {
  background: #e5e7eb;
  color: #6b7280;
}

.status-grid {
  display: flex;
  padding: 0 40rpx 30rpx;
  gap: 32rpx;
}

.status-item {
  flex: 1;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.status-icon {
  width: 96rpx;
  height: 96rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
}

.status-icon-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.status-icon-green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.status-icon-orange {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.status-number {
  font-size: 48rpx;
  font-weight: bold;
  color: #1f2937;
}

.status-label {
  font-size: 24rpx;
  color: #6b7280;
}

.live-indicator {
  width: 24rpx;
  height: 24rpx;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.detection-list {
  padding: 20rpx 38rpx 38rpx;
  overflow-y: auto;
  height: 50vh;
}

.detection-item {
  margin-bottom: 32rpx;
}

.image-container {
  position: relative;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.placeholder-image {
  width: 100%;
  height: 400rpx;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  color: #6b7280;
  font-size: 28rpx;
}

.status-overlay {
  position: absolute;
  top: 24rpx;
  left: 24rpx;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
  font-weight: 500;
  color: white;
}

.status-overlay.good {
  background: #10b981;
}

.status-overlay.warning {
  background: #ef4444;
}

.status-overlay.normal {
  background: #f59e0b;
}

.detection-info {
  display: flex;
  justify-content: space-between;
  padding: 16rpx;
  font-size: 24rpx;
  color: #6b7280;
}

.detection-count {
  font-weight: 500;
}

.control-buttons {
  display: flex;
  gap: 32rpx;
  margin: 30rpx;
}

.control-btn {
  flex: 1;
  height: 92rpx;
  border-radius: 24rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  font-size: 32rpx;
  font-weight: 500;
  color: white;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
}

.control-btn:active {
  transform: scale(0.95);
}

.start-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.pause-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stop-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.btn-icon {
  font-size: 40rpx;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-top: 1rpx solid #e5e7eb;
  display: flex;
  padding: 24rpx 0;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx;
  transition: all 0.2s;
}

.nav-item:active {
  transform: scale(0.95);
}

.nav-icon {
  font-size: 48rpx;
}

.nav-label {
  font-size: 24rpx;
  color: #6b7280;
}

.nav-item.active .nav-label {
  color: #2563eb;
  font-weight: 500;
}

.icon {
  font-size: inherit;
}
</style>
