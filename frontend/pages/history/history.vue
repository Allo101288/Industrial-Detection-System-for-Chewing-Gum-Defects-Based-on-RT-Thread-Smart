<template>
  <view class="back-btn" @click="goBack">
    <text class="icon">←</text>
  </view>
  <view class="header-info">
    <!-- <view class="header-icon">
              <text class="icon">📊</text>
            </view> -->
    <text class="header-title">历史记录</text>
  </view>
  <view class="container">
    <!-- Header -->
    <view class="header">
      <view class="header-bg-circle header-bg-circle-1"></view>
      <view class="header-bg-circle header-bg-circle-2"></view>
      <view class="header-content">
        <!-- <view class="back-btn" @click="goBack">
          <text class="icon">←</text>
        </view> -->

        <!-- <view class="filter-btn" @click="showFilter">
            <text class="icon">🔍</text>
          </view> -->
      </view>
    </view>

    <!-- Statistics Summary -->
    <view class="stats-container">
      <view class="stats-card">
        <view class="stats-grid">
          <view class="stat-item">
            <view class="stat-icon stat-icon-blue">
              <text class="icon">📈</text>
            </view>
            <text class="stat-number">{{ totalRecords }}</text>
            <text class="stat-label">总记录数</text>
          </view>
          <view class="stat-item">
            <view class="stat-icon stat-icon-green">
              <text class="icon">⏱️</text>
            </view>
            <text class="stat-number">{{ totalHours }}h</text>
            <text class="stat-label">总检测时长</text>
          </view>
          <view class="stat-item">
            <view class="stat-icon stat-icon-orange">
              <text class="icon">⚠️</text>
            </view>
            <text class="stat-number">{{ totalDefects }}</text>
            <text class="stat-label">总缺陷数</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Filter Tabs -->
    <view class="filter-tabs">
      <scroll-view class="tabs-scroll" scroll-x>
        <view class="tabs-container">
          <view
            v-for="(tab, index) in filterTabs"
            :key="index"
            class="tab-item"
            :class="{ active: currentFilter === tab.value }"
            @click="switchFilter(tab.value)"
          >
            <text class="tab-icon">{{ tab.icon }}</text>
            <text class="tab-text">{{ tab.label }}</text>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- History List -->
    <scroll-view
      class="history-list"
      scroll-y
      @scrolltolower="loadMore"
      :refresher-enabled="true"
      :refresher-triggered="isRefreshing"
      @refresherrefresh="onRefresh"
    >
      <view class="list-container">
        <view
          v-for="(record, index) in filteredRecords"
          :key="record.id"
          class="history-item"
          @click="viewDetail(record)"
        >
          <view class="item-header">
            <view class="user-info">
              <view
                class="user-avatar"
                :class="getUserAvatarClass(record.userId)"
              >
                <text class="icon">{{ getUserAvatar(record.userId) }}</text>
              </view>
              <view class="user-details">
                <text class="user-name">{{ record.userName }}</text>
                <text class="user-id">ID: {{ record.userId }}</text>
              </view>
            </view>
            <view class="status-badge" :class="getStatusClass(record.status)">
              <text>{{ getStatusText(record.status) }}</text>
            </view>
          </view>

          <view class="item-content">
            <view class="time-section">
              <view class="time-item">
                <view class="time-icon start-icon">
                  <text class="icon">🟢</text>
                </view>
                <view class="time-info">
                  <text class="time-label">开始时间</text>
                  <text class="time-value">{{
                    formatTime(record.startTime)
                  }}</text>
                </view>
              </view>
              <view class="duration-line">
                <view class="duration-dot"></view>
                <view class="duration-bar"></view>
                <view class="duration-dot"></view>
              </view>
              <view class="time-item">
                <view class="time-icon end-icon">
                  <text class="icon">🔴</text>
                </view>
                <view class="time-info">
                  <text class="time-label">结束时间</text>
                  <text class="time-value">{{
                    formatTime(record.endTime)
                  }}</text>
                </view>
              </view>
            </view>

            <view class="metrics-section">
              <view class="metric-card duration-card">
                <view class="metric-icon">
                  <text class="icon">⏰</text>
                </view>
                <view class="metric-info">
                  <text class="metric-value">{{
                    getDuration(record.startTime, record.endTime)
                  }}</text>
                  <text class="metric-label">检测时长</text>
                </view>
              </view>
              <view class="metric-card defects-card">
                <view class="metric-icon">
                  <text class="icon">🎯</text>
                </view>
                <view class="metric-info">
                  <text class="metric-value">{{ record.defectCount }}</text>
                  <text class="metric-label">缺陷总数</text>
                </view>
              </view>
              <!-- <view class="metric-card accuracy-card">
                <view class="metric-icon">
                  <text class="icon">📊</text>
                </view>
                <view class="metric-info">
                  <text class="metric-value">{{ record.accuracy }}%</text>
                  <text class="metric-label">检测精度</text>
                </view>
              </view> -->
            </view>
          </view>

          <view class="item-footer">
            <text class="record-date">{{ formatDate(record.startTime) }}</text>
            <!-- <view class="action-buttons">
              <view
                class="action-btn export-btn"
                @click.stop="exportRecord(record)"
              >
                <text class="icon">📤</text>
                <text>导出</text>
              </view>
              <view
                class="action-btn detail-btn"
                @click.stop="viewDetail(record)"
              >
                <text class="icon">👁️</text>
                <text>详情</text>
              </view>
            </view> -->
          </view>
        </view>

        <!-- Loading More -->
        <view v-if="isLoading" class="loading-more">
          <view class="loading-icon">⏳</view>
          <text class="loading-text">加载中...</text>
        </view>

        <!-- No More Data -->
        <view v-if="!hasMore && filteredRecords.length > 0" class="no-more">
          <text class="no-more-text">没有更多记录了</text>
        </view>

        <!-- Empty State -->
        <view
          v-if="filteredRecords.length === 0 && !isLoading"
          class="empty-state"
        >
          <view class="empty-icon">📝</view>
          <text class="empty-title">暂无历史记录</text>
          <text class="empty-desc">开始使用检测系统后，记录将显示在这里</text>
        </view>
      </view>
    </scroll-view>
  </view>

  <!-- Filter Popup -->
  <uni-popup ref="filterPopup" type="bottom" background-color="rgba(0,0,0,0.5)">
    <view class="filter-modal">
      <view class="filter-header">
        <text class="filter-title">筛选条件</text>
        <view class="filter-close" @click="closeFilter">
          <text class="icon">✕</text>
        </view>
      </view>
      <view class="filter-content">
        <!-- Date Range -->
        <view class="filter-section">
          <text class="section-title">时间范围</text>
          <view class="date-range">
            <picker mode="date" @change="onStartDateChange">
              <view class="date-picker">
                <text>{{ startDate || "开始日期" }}</text>
                <text class="picker-icon">📅</text>
              </view>
            </picker>
            <text class="date-separator">至</text>
            <picker mode="date" @change="onEndDateChange">
              <view class="date-picker">
                <text>{{ endDate || "结束日期" }}</text>
                <text class="picker-icon">📅</text>
              </view>
            </picker>
          </view>
        </view>

        <!-- User Filter -->
        <view class="filter-section">
          <text class="section-title">用户筛选</text>
          <view class="user-filter">
            <input
              class="user-input"
              placeholder="输入用户名或ID"
              v-model="userFilter"
            />
          </view>
        </view>

        <!-- Status Filter -->
        <view class="filter-section">
          <text class="section-title">状态筛选</text>
          <view class="status-filter">
            <view
              v-for="status in statusOptions"
              :key="status.value"
              class="status-option"
              :class="{ selected: selectedStatus === status.value }"
              @click="selectStatus(status.value)"
            >
              <text class="status-icon">{{ status.icon }}</text>
              <text class="status-text">{{ status.label }}</text>
            </view>
          </view>
        </view>

        <view class="filter-actions">
          <button class="filter-btn reset-btn" @click="resetFilter">
            重置
          </button>
          <button class="filter-btn apply-btn" @click="applyFilter">
            应用
          </button>
        </view>
      </view>
    </view>
  </uni-popup>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { onShow, onLoad, onHide } from "@dcloudio/uni-app";
const filterPopup = ref(null);
const isLoading = ref(false);
const isRefreshing = ref(false);
const hasMore = ref(true);
const currentFilter = ref("all");
const startDate = ref("");
const endDate = ref("");
const userFilter = ref("");
const selectedStatus = ref("all");

// Filter tabs
const filterTabs = ref([
  { label: "全部", value: "all", icon: "📋" },
  { label: "今天", value: "today", icon: "📅" },
  { label: "本周", value: "week", icon: "📆" },
  { label: "本月", value: "month", icon: "🗓️" },
  // { label: "异常", value: "error", icon: "⚠️" },
]);

// Status options
const statusOptions = ref([
  { label: "全部", value: "all", icon: "📋" },
  { label: "正常完成", value: "completed", icon: "✅" },
  { label: "异常中断", value: "error", icon: "❌" },
  { label: "手动停止", value: "stopped", icon: "⏹️" },
]);

// Mock data
const historyRecords = ref([
  // {
  //   id: 1,
  //   userId: "U001",
  //   userName: "张三",
  //   startTime: "2025-01-16 09:30:00",
  //   endTime: "2025-01-16 11:45:00",
  //   defectCount: 15,
  //   accuracy: 98.5,
  //   status: "completed",
  // },
]);
const getAllHistoryRecords = async () => {
  const res = await uniCloud.callFunction({
          name: 'getHistory',
        });
        console.log("获取历史记录", res);
        historyRecords.value = [];
        res.result.data.forEach(e => {
          e.startTime = e.startTime.replace(/-/g, '/');
          e.endTime = e.endTime.replace(/-/g, '/');
          historyRecords.value.push({
            id: e.id,
            userId: e.userId,
            userName: e.userName,
            startTime: e.startTime,
            endTime: e.endTime,
            defectCount: e.defectCount,
            accuracy: e.accuracy,
            status: e.status
          });
        });
};
onShow(() => {
  getAllHistoryRecords();
});



// Computed properties
const filteredRecords = computed(() => {
  let records = [...historyRecords.value];

  // Filter by time range
  if (currentFilter.value === "today") {
    const today = new Date().toDateString();
    records = records.filter(
      (record) => new Date(record.startTime).toDateString() === today
    );
  } else if (currentFilter.value === "week") {
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    records = records.filter((record) => new Date(record.startTime) >= weekAgo);
  } else if (currentFilter.value === "month") {
    const monthAgo = new Date();
    monthAgo.setMonth(monthAgo.getMonth() - 1);
    records = records.filter(
      (record) => new Date(record.startTime) >= monthAgo
    );
  } else if (currentFilter.value === "error") {
    records = records.filter((record) => record.status === "error");
  }

  // Filter by user
  if (userFilter.value) {
    records = records.filter(
      (record) =>
        record.userName.includes(userFilter.value) ||
        record.userId.includes(userFilter.value)
    );
  }

  // Filter by status
  if (selectedStatus.value !== "all") {
    records = records.filter(
      (record) => record.status === selectedStatus.value
    );
  }

  // Filter by date range
  if (startDate.value) {
    records = records.filter(
      (record) => new Date(record.startTime) >= new Date(startDate.value)
    );
  }
  if (endDate.value) {
    records = records.filter(
      (record) => new Date(record.startTime) <= new Date(endDate.value)
    );
  }

  return records.sort((a, b) => new Date(b.startTime) - new Date(a.startTime));
});

const totalRecords = computed(() => historyRecords.value.length);

const totalHours = computed(() => {
  return historyRecords.value
    .reduce((total, record) => {
      const duration = getDurationInHours(record.startTime, record.endTime);
      return total + duration;
    }, 0)
    .toFixed(1);
});

const totalDefects = computed(() => {
  return historyRecords.value.reduce(
    (total, record) => total + record.defectCount,
    0
  );
});

// Methods
const goBack = () => {
  uni.switchTab({
    url: '/pages/personage/personage',
    success: (result) => {
      
    },
    fail: () => {},
    complete: () => {}
  });
    
};

const showFilter = () => {
  filterPopup.value.open();
};

const closeFilter = () => {
  filterPopup.value.close();
};

const switchFilter = (filter) => {
  currentFilter.value = filter;
};

const onRefresh = () => {
  isRefreshing.value = true;
  setTimeout(() => {
    isRefreshing.value = false;
    uni.showToast({ title: "刷新成功", icon: "success" });
  }, 1000);
};

const loadMore = () => {
  if (hasMore.value && !isLoading.value) {
    isLoading.value = true;
    setTimeout(() => {
      isLoading.value = false;
      // hasMore.value = false // 模拟没有更多数据
    }, 1000);
  }
};

const formatTime = (timeStr) => {
  const date = new Date(timeStr);
  return `${date.getHours().toString().padStart(2, "0")}:${date
    .getMinutes()
    .toString()
    .padStart(2, "0")}`;
};

const formatDate = (timeStr) => {
  const date = new Date(timeStr);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  if (date.toDateString() === today.toDateString()) {
    return "今天";
  } else if (date.toDateString() === yesterday.toDateString()) {
    return "昨天";
  } else {
    return `${date.getMonth() + 1}月${date.getDate()}日`;
  }
};

const getDuration = (startTime, endTime) => {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const diff = end - start;
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else {
    return `${minutes}m`;
  }
};

const getDurationInHours = (startTime, endTime) => {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const diff = end - start;
  return diff / (1000 * 60 * 60);
};

const getUserAvatar = (userId) => {
  const avatars = ["👨", "👩", "🧑", "👱", "👴"];
  return avatars[userId.charCodeAt(userId.length - 1) % avatars.length];
};

const getUserAvatarClass = (userId) => {
  const classes = [
    "avatar-blue",
    "avatar-green",
    "avatar-purple",
    "avatar-orange",
    "avatar-pink",
  ];
  return classes[userId.charCodeAt(userId.length - 1) % classes.length];
};

const getStatusClass = (status) => {
  const classes = {
    completed: "status-success",
    error: "status-error",
    stopped: "status-warning",
  };
  return classes[status] || "status-default";
};

const getStatusText = (status) => {
  const texts = {
    completed: "正常完成",
    error: "异常中断",
    stopped: "手动停止",
  };
  return texts[status] || "未知状态";
};

const viewDetail = (record) => {
  uni.showToast({
    title: `查看记录 ${record.id} 详情`,
    icon: "none",
  });
};

const exportRecord = (record) => {
  uni.showToast({
    title: `导出记录 ${record.id}`,
    icon: "none",
  });
};

const onStartDateChange = (e) => {
  startDate.value = e.detail.value;
};

const onEndDateChange = (e) => {
  endDate.value = e.detail.value;
};

const selectStatus = (status) => {
  selectedStatus.value = status;
};

const resetFilter = () => {
  startDate.value = "";
  endDate.value = "";
  userFilter.value = "";
  selectedStatus.value = "all";
};

const applyFilter = () => {
  filterPopup.value.close();
  uni.showToast({
    title: "筛选已应用",
    icon: "success",
  });
};

// const switchTab = (tab) => {
//   if (tab === "home") {
//     uni.navigateTo({ url: "/pages/index/index" });
//   } else if (tab === "chat") {
//     uni.navigateTo({ url: "/pages/chat/chat" });
//   } else if (tab === "profile") {
//     uni.navigateTo({ url: "/pages/profile/profile" });
//   }
// };

onMounted(() => {
  // 初始化数据
});
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 50%, #f3e8ff 100%);
}

.header {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  padding: 80rpx 48rpx 48rpx;
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
  position: relative;
  z-index: 10;
  height: 30px;
}

.back-btn,
.filter-btn {
  width: 80rpx;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  transition: all 0.3s ease;
}

.back-btn:active,
.filter-btn:active {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0.9);
}
.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 99999;
  color: white;
}
.header-info {
  display: flex;
  align-items: center;
  gap: 24rpx;
  position: absolute;
  top: 25px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 99999;
  color: #ffffff;
}
.header-infos {
  display: flex;
  align-items: center;
  gap: 24rpx;
}
.header-icon {
  width: 80rpx;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
}

.header-title {
  font-size: 40rpx;
  font-weight: bold;
}

.stats-container {
  padding: 0 48rpx;
  margin-top: -32rpx;
  position: relative;
  z-index: 10;
}

.stats-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  padding: 48rpx;
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 32rpx;
}

.stats-grid {
  display: flex;
  gap: 32rpx;
}

.stat-item {
  flex: 1;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16rpx;
}

.stat-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
}

.stat-icon-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon-green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon-orange {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-number {
  font-size: 40rpx;
  font-weight: bold;
  color: #1f2937;
}

.stat-label {
  font-size: 24rpx;
  color: #6b7280;
}

.filter-tabs {
  padding: 0 48rpx 32rpx;
}

.tabs-scroll {
  white-space: nowrap;
}

.tabs-container {
  display: flex;
  gap: 16rpx;
  padding-bottom: 16rpx;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 16rpx 32rpx;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 20rpx;
  font-size: 28rpx;
  color: #6b7280;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-item.active {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  color: white;
  box-shadow: 0 8rpx 32rpx rgba(37, 99, 235, 0.3);
}

.tab-item:active {
  transform: scale(0.95);
}

.tab-icon {
  font-size: 32rpx;
}

.history-list {
  flex: 1;
  padding: 0 1rem;
  max-width: calc(100% - 2rem);
  margin-bottom: 120rpx;
  display: flex;
  align-items: center;
}

.history-item {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  margin-bottom: 32rpx;
  overflow: hidden;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.history-item:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx 32rpx 24rpx;
  border-bottom: 2rpx solid #f3f4f6;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.user-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
}

.avatar-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.avatar-green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.avatar-purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.avatar-orange {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.avatar-pink {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.user-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #1f2937;
}

.user-id {
  font-size: 24rpx;
  color: #6b7280;
}

.status-badge {
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  font-weight: 500;
}

.status-success {
  background: #dcfce7;
  color: #166534;
}

.status-error {
  background: #fee2e2;
  color: #991b1b;
}

.status-warning {
  background: #fef3c7;
  color: #92400e;
}

.item-content {
  padding: 32rpx;
}

.time-section {
  display: flex;
  align-items: center;
  margin-bottom: 32rpx;
  justify-content: space-between;
}

.time-item {
  display: flex;
  align-items: center;
  /* gap: 16rpx;
  flex: 1; */
}

.time-icon {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
}

.start-icon {
  background: #dcfce7;
}

.end-icon {
  background: #fee2e2;
}

.time-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.time-label {
  font-size: 24rpx;
  color: #6b7280;
}

.time-value {
  font-size: 28rpx;
  font-weight: 600;
  color: #1f2937;
}

.duration-line {
  display: flex;
  align-items: center;
  margin: 0 24rpx;
}

.duration-dot {
  width: 12rpx;
  height: 12rpx;
  background: #d1d5db;
  border-radius: 50%;
}

.duration-bar {
  flex: 1;
  height: 4rpx;
  background: linear-gradient(90deg, #10b981 0%, #ef4444 100%);
  margin: 0 16rpx;
}

.metrics-section {
  display: flex;
  gap: 16rpx;
}

.metric-card {
  flex: 1;
  background: #f9fafb;
  border-radius: 16rpx;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.duration-card {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.defects-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.accuracy-card {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
}

.metric-icon {
  width: 48rpx;
  height: 48rpx;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  background: rgba(255, 255, 255, 0.8);
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.metric-value {
  font-size: 28rpx;
  font-weight: bold;
  color: #1f2937;
}

.metric-label {
  font-size: 20rpx;
  color: #6b7280;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 32rpx 32rpx;
  background: #f9fafb;
}

.record-date {
  font-size: 24rpx;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 16rpx;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 12rpx 20rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
  transition: all 0.3s ease;
}

.export-btn {
  background: #e0e7ff;
  color: #4f46e5;
}

.detail-btn {
  background: #dcfce7;
  color: #166534;
}

.action-btn:active {
  transform: scale(0.95);
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  padding: 48rpx;
  color: #6b7280;
}

.loading-icon {
  font-size: 32rpx;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 28rpx;
}

.no-more {
  text-align: center;
  padding: 48rpx;
  color: #9ca3af;
  font-size: 28rpx;
}

.empty-state {
  text-align: center;
  padding: 120rpx 48rpx;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 32rpx;
}

.empty-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16rpx;
  display: block;
}

.empty-desc {
  font-size: 28rpx;
  color: #6b7280;
  line-height: 1.5;
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

/* Filter Modal Styles */
.filter-modal {
  background: white;
  border-radius: 32rpx 32rpx 0 0;
  max-height: 80vh;
  overflow: hidden;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 48rpx;
  border-bottom: 2rpx solid #f3f4f6;
}

.filter-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #1f2937;
}

.filter-close {
  width: 64rpx;
  height: 64rpx;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  color: #6b7280;
}

.filter-content {
  padding: 48rpx;
  max-height: 60vh;
  overflow-y: auto;
}

.filter-section {
  margin-bottom: 48rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #374151;
  margin-bottom: 24rpx;
  display: block;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.date-picker {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 32rpx;
  background: #f9fafb;
  border: 2rpx solid #e5e7eb;
  border-radius: 16rpx;
  font-size: 28rpx;
  color: #374151;
}

.picker-icon {
  font-size: 32rpx;
  color: #6b7280;
}

.date-separator {
  font-size: 28rpx;
  color: #6b7280;
}

.user-input {
  width: 100%;
  padding: 24rpx 32rpx;
  background: #f9fafb;
  border: 2rpx solid #e5e7eb;
  border-radius: 16rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.user-input:focus {
  border-color: #2563eb;
  background: white;
}

.status-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.status-option {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 16rpx 24rpx;
  background: #f9fafb;
  border: 2rpx solid #e5e7eb;
  border-radius: 20rpx;
  font-size: 28rpx;
  color: #374151;
  transition: all 0.3s ease;
}

.status-option.selected {
  background: #2563eb;
  border-color: #2563eb;
  color: white;
}

.status-option:active {
  transform: scale(0.95);
}

.status-icon {
  font-size: 32rpx;
}

.filter-actions {
  display: flex;
  gap: 24rpx;
  margin-top: 48rpx;
}

.filter-btn {
  flex: 1;
  height: 88rpx;
  border: none;
  border-radius: 16rpx;
  font-size: 32rpx;
  font-weight: 600;
  transition: all 0.3s ease;
}

.reset-btn {
  background: #f3f4f6;
  color: #6b7280;
}

.apply-btn {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  color: white;
  box-shadow: 0 8rpx 32rpx rgba(37, 99, 235, 0.3);
}

.filter-btn:active {
  transform: scale(0.95);
}

.icon {
  font-size: inherit;
}
</style>
