<template>
  <view class="container">
    <!-- Header -->
    <view class="header">
      <view class="header-bg-circle header-bg-circle-1"></view>
      <view class="header-bg-circle header-bg-circle-2"></view>
      <view class="header-title">个人中心</view>

      <!-- Profile Section -->
      <view class="profile-section">
        <view class="avatar-container">
          <view class="avatar" @click="showLogin">
            <text class="icon">👤</text>
          </view>
          <view class="online-indicator" :class="{'online': isLoggedIn}"></view>
        </view>
        <view class="profile-info">
          <text class="profile-name">{{ userName }}</text>
          <text class="profile-desc">{{ isLoggedIn ? '已登录' : '点击头像可登录/注册' }}</text>
        </view>
      </view>
    </view>

    <!-- Services -->
    <view class="services-container">
      <!-- Common Services -->
      <view class="service-card">
        <view class="service-header">
          <view class="service-indicator"></view>
          <text class="service-title">常用服务</text>
        </view>
        <view class="service-grid">
          <view class="service-item" @click="handleService('contact')">
            <view class="service-icon service-icon-blue">
              <text class="icon">📧</text>
            </view>
            <text class="service-label">联系我们</text>
          </view>
          <view class="service-item" @click="handleService('history')">
            <view class="service-icon service-icon-green">
              <text class="icon">📄</text>
            </view>
            <text class="service-label">历史记录</text>
          </view>
          <view class="service-item" @click="handleService('favorites')">
            <view class="service-icon service-icon-yellow">
              <text class="icon">⭐</text>
            </view>
            <text class="service-label">我的收藏</text>
          </view>
        </view>
      </view>

      <!-- Other Services -->
      <view class="service-card">
        <view class="service-header">
          <view class="service-indicator service-indicator-purple"></view>
          <text class="service-title">其他服务</text>
        </view>
        <view class="service-list">
          <view class="service-row" @click="handleService('about')">
            <view class="service-row-left">
              <view class="service-icon-small service-icon-indigo">
                <text class="icon">👥</text>
              </view>
              <text class="service-row-label">关于我们</text>
            </view>
            <text class="service-arrow">›</text>
          </view>
          <view class="service-row" @click="handleService('privacy')">
            <view class="service-row-left">
              <view class="service-icon-small service-icon-teal">
                <text class="icon">🛡️</text>
              </view>
              <text class="service-row-label">隐私政策</text>
            </view>
            <text class="service-arrow">›</text>
          </view>
          <view class="service-row" @click="handleService('terms')">
            <view class="service-row-left">
              <view class="service-icon-small service-icon-cyan">
                <text class="icon">📋</text>
              </view>
              <text class="service-row-label">服务协议</text>
            </view>
            <text class="service-arrow">›</text>
          </view>
          <view class="service-row" @click="handleService('legal')">
            <view class="service-row-left">
              <view class="service-icon-small service-icon-red">
                <text class="icon">⚖️</text>
              </view>
              <text class="service-row-label">法律声明</text>
            </view>
            <text class="service-arrow">›</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 登录弹框 -->
    <uni-popup ref="popup" type="center" :mask-click="false">
      <view class="login-container">
        <view class="login-header">
          <text class="login-title">{{ isLoginMode ? '登录' : '注册' }}</text>
          <text class="login-close" @click="popup.close">×</text>
        </view>
        
        <view class="login-form">
          <view class="form-item">
            <text class="form-label">账号</text>
            <input 
              class="form-input" 
              v-model="form.username" 
              placeholder="请输入账号" 
              placeholder-class="input-placeholder"
            />
          </view>
          
          <view class="form-item">
            <text class="form-label">密码</text>
            <input 
              class="form-input" 
              v-model="form.password" 
              placeholder="请输入密码" 
              placeholder-class="input-placeholder"
              password
            />
          </view>
          
          <view v-if="!isLoginMode" class="form-item">
            <text class="form-label">确认密码</text>
            <input 
              class="form-input" 
              v-model="form.confirmPassword" 
              placeholder="请再次输入密码" 
              placeholder-class="input-placeholder"
              password
            />
          </view>
          
          <button 
            class="login-btn" 
            :style="{background: isLoginMode ? 'linear-gradient(135deg, #2563eb 0%, #4f46e5 100%)' : 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'}"
            @click="handleSubmit"
            :loading="isLoading"
          >
            {{ isLoginMode ? '登 录' : '注 册' }}
          </button>
          
          <view class="login-footer">
            <text class="footer-text" @click="switchMode">
              {{ isLoginMode ? '没有账号？立即注册' : '已有账号？立即登录' }}
            </text>
          </view>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const { isLoggedIn, userName } = storeToRefs(userStore);

const popup = ref(null);
const isLoginMode = ref(true);
const isLoading = ref(false);

const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

// 检查登录状态
const checkLoginStatus = async () => {
  await userStore.checkLogin();
};

onMounted(() => {
  checkLoginStatus();
});

const showLogin = () => {
  if (isLoggedIn.value) return;
  popup.value.open();
};

const switchMode = () => {
  isLoginMode.value = !isLoginMode.value;
  form.username = '';
  form.password = '';
  form.confirmPassword = '';
};

const handleSubmit = async () => {
  if (!form.username || !form.password) {
    uni.showToast({
      title: '请输入账号和密码',
      icon: 'none'
    });
    return;
  }
  
  if (!isLoginMode.value && form.password !== form.confirmPassword) {
    uni.showToast({
      title: '两次密码输入不一致',
      icon: 'none'
    });
    return;
  }
  
  isLoading.value = true;
  
  try {
    if (isLoginMode.value) {
      // 登录逻辑
      const loginRes = await uniCloud.callFunction({
        name: 'Login',
        data: {
          username: form.username,
          password: form.password
        }
      });
      console.log('Login Response:', loginRes,loginRes.result.message);
      if (loginRes.result.code === 200) {
        // 登录成功处理
        await userStore.login({
          token: loginRes.result.data.token,
          userInfo: loginRes.result.data.userInfo
        });
        
        uni.showToast({
          title: '登录成功',
          icon: 'success'
        });
        
        popup.value.close();
      } else {
        throw new Error(loginRes.result.message || '登录失败');
      }
    } else {
      // 注册逻辑
      const registerRes = await uniCloud.callFunction({
        name: 'Register',
        data: {
          username: form.username,
          password: form.password
        }
      });
      console.log('Register Response:', registerRes);
      if (registerRes.result.code === 200) {
        uni.showToast({
          title: '注册成功，请登录',
          icon: 'success'
        });
        // 注册后自动切换到登录模式
        isLoginMode.value = true;
      } else {
        throw new Error(registerRes.result.message || '注册失败');
      }
    }
  } catch (error) {
    uni.showToast({
      title: error.message,
      icon: 'none'
    });
  } finally {
    isLoading.value = false;
    form.password = '';
    form.confirmPassword = '';
  }
};

const handleService = (service) => {
  if (!isLoggedIn.value) {
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    });
    showLogin();
    return;
  }
  
  // uni.showToast({
  //   title: `点击了${service}`,
  //   icon: "none",
  // });
  if(service!='history' ){
    uni.showToast({
      title: '该功能正在开发中~',
      icon: "none",
    });
  }
  uni.navigateTo({
    url: `/pages/${service}/${service}`
  });
};

const switchTab = (tab) => {
  if (tab === "home") {
    uni.navigateTo({ url: "/pages/index/index" });
  } else if (tab === "chat") {
    uni.navigateTo({ url: "/pages/chat/chat" });
  }
};
</script>
<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 50%, #f3e8ff 100%);
}

.header {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  padding: 48rpx 48rpx 64rpx;
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
  width: 256rpx;
  height: 256rpx;
  top: -128rpx;
  right: -128rpx;
}

.header-bg-circle-2 {
  width: 192rpx;
  height: 192rpx;
  bottom: -96rpx;
  left: -96rpx;
}

.header-title {
  font-size: 1.25rem;
  font-weight: bold;
  text-align: center;
  z-index: 10;
  width: 100%;
  margin-bottom: 22px;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 32rpx;
  position: relative;
  z-index: 10;
}

.avatar-container {
  position: relative;
}

.avatar {
  width: 128rpx;
  height: 128rpx;
  background: rgba(255, 255, 255, 0.2);
  border: 8rpx solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 64rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.online-indicator {
  position: absolute;
  bottom: -4rpx;
  right: -4rpx;
  width: 48rpx;
  height: 48rpx;
  background: #10b981;
  border: 4rpx solid white;
  border-radius: 50%;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 36rpx;
  font-weight: 600;
  margin-bottom: 8rpx;
  display: block;
}

.profile-desc {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.services-container {
  padding: 0 48rpx;
  margin-top: -32rpx;
  position: relative;
  z-index: 10;
  padding-bottom: 160rpx;
}

.service-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  margin-bottom: 48rpx;
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.service-header {
  padding: 48rpx 48rpx 32rpx;
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.service-indicator {
  width: 8rpx;
  height: 48rpx;
  background: linear-gradient(to bottom, #2563eb 0%, #4f46e5 100%);
  border-radius: 4rpx;
}

.service-indicator-purple {
  background: linear-gradient(to bottom, #8b5cf6 0%, #7c3aed 100%);
}

.service-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #1f2937;
}

.service-grid {
  display: flex;
  gap: 32rpx;
}

.service-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16rpx;
  padding: 32rpx;
  transition: all 0.2s;
}

.service-item:active {
  transform: scale(0.95);
}

.service-icon {
  width: 96rpx;
  height: 96rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.service-item:active .service-icon {
  transform: scale(1.1);
}

.service-icon-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.service-icon-green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.service-icon-yellow {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.service-label {
  font-size: 28rpx;
  font-weight: 500;
  color: #1f2937;
}

.service-list {
  padding: 0 48rpx 48rpx;
}

.service-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx 0;
  border-bottom: 1rpx solid #f3f4f6;
  transition: all 0.2s;
}

.service-row:last-child {
  border-bottom: none;
}

.service-row:active {
  background: rgba(0, 0, 0, 0.02);
  margin: 0 -32rpx;
  padding-left: 32rpx;
  padding-right: 32rpx;
}

.service-row-left {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.service-icon-small {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  transition: transform 0.2s;
}

.service-row:active .service-icon-small {
  transform: scale(1.1);
}

.service-icon-indigo {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
}

.service-icon-teal {
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
}

.service-icon-cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
}

.service-icon-red {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
}

.service-row-label {
  font-size: 32rpx;
  font-weight: 500;
  color: #1f2937;
}

.service-arrow {
  font-size: 40rpx;
  color: #9ca3af;
  transition: color 0.2s;
}

.service-row:active .service-arrow {
  color: #6b7280;
}

/* 登录弹框样式 */
.login-container {
  width: 600rpx;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 32rpx;
  overflow: hidden;
  box-shadow: 0 32rpx 96rpx rgba(0, 0, 0, 0.2);
}

.login-header {
  padding: 40rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
}

.login-title {
  font-size: 40rpx;
  font-weight: bold;
  color: white;
}

.login-close {
  font-size: 48rpx;
  color: rgba(255, 255, 255, 0.8);
  padding: 0 20rpx;
}

.login-form {
  padding: 40rpx;
}

.form-item {
  margin-bottom: 40rpx;
}

.form-label {
  display: block;
  font-size: 32rpx;
  color: #4b5563;
  margin-bottom: 16rpx;
  font-weight: 500;
}

.form-input {
  width: 88%;
  height: 96rpx;
  padding: 0 32rpx;
  background: #f9fafb;
  border-radius: 16rpx;
  font-size: 32rpx;
  border: 2rpx solid #e5e7eb;
  transition: all 0.2s;
}

.form-input:focus {
  border-color: #2563eb;
  background: #fff;
}

.input-placeholder {
  color: #9ca3af;
  font-size: 32rpx;
}

.login-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  border-radius: 16rpx;
  color: white;
  font-size: 36rpx;
  font-weight: bold;
  margin-top: 48rpx;
  border: none;
  box-shadow: 0 8rpx 24rpx rgba(37, 99, 235, 0.3);
  transition: all 0.2s;
}

.login-btn:active {
  transform: scale(0.98);
  opacity: 0.9;
}

.login-footer {
  margin-top: 48rpx;
  text-align: center;
}

.footer-text {
  color: #4f46e5;
  font-size: 28rpx;
  text-decoration: underline;
}

.footer-text:active {
  opacity: 0.8;
}

.icon {
  font-size: inherit;
}
</style>