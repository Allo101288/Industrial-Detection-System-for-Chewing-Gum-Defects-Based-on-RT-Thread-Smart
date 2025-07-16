import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const token = ref('');
  const userInfo = ref(null);
  
  const isLoggedIn = computed(() => !!token.value);
  const userName = computed(() => userInfo.value?.username || '未登录/注册');
  
  // 登录
  const login = async (data) => {
    token.value = data.userInfo.userId;
    userInfo.value = data.userInfo;
    // 可以在这里添加token存储逻辑（如存到storage）
    uni.setStorageSync('token', data.userInfo.userId);
    uni.setStorageSync('userInfo', data.userInfo);
  };
  
  // 登出
  const logout = async () => {
    token.value = '';
    userInfo.value = null;
    uni.removeStorageSync('token');
    uni.removeStorageSync('userInfo');
  };
  
  // 检查登录状态
  const checkLogin = async () => {
    const storedToken = uni.getStorageSync('token');
    const storedUserInfo = uni.getStorageSync('userInfo');
    if (storedToken && storedUserInfo) {
      token.value = storedToken;
      userInfo.value = storedUserInfo;
      // 可以添加token验证逻辑
    }
  };
  
  return {
    token,
    userInfo,
    isLoggedIn,
    userName,
    login,
    logout,
    checkLogin
  };
});