<template>
  <view class="container">
    <!-- Header -->
    <view class="header">
      <view class="header-bg-circle header-bg-circle-1"></view>
      <view class="header-bg-circle header-bg-circle-2"></view>
      <view class="header-content">
        <view class="header-icon">
          <text class="icon">🤖</text>
        </view>
        <text class="header-title">口香糖检测智能助手</text>
        <text class="sparkle">✨</text>
      </view>
    </view>

    <!-- Chat Area -->
    <view class="chat-area">
      <view 
        v-for="(message, index) in messages" 
        :key="index" 
        class="message-card"
        :class="[message.sender === 'user' ? 'user-message' : 'assistant-message']"
      >
        <view class="message-content">
          <view class="avatar" :class="message.sender === 'user' ? 'user-avatar' : 'assistant-avatar'">
            <text class="icon">{{ message.sender === 'user' ? '👤' : '🤖' }}</text>
          </view>
          <view class="message-bubble" :class="message.sender === 'user' ? 'user-bubble' : 'assistant-bubble'">
            <view class="bubble-content">
              <text class="message-text">{{ message.text }}</text>
            </view>
            <text class="message-time">{{ message.time }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Input Area -->
    <view class="input-area">
      <view class="input-card">
        <input
          class="message-input"
          placeholder="输入消息..."
          v-model="inputMessage"
          @confirm="sendMessage"
        />
        <button class="send-btn" @click="sendMessage">
          <text class="icon">📤</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";

const inputMessage = ref("");
const messages = ref([
  {
    text: "你好！我是口香糖检测小助手，有什么可以帮您的吗？",
    sender: "assistant",
    time: getCurrentTime()
  }
]);

const sendMessage = () => {
  if (inputMessage.value.trim()) {
    // 添加用户消息
    messages.value.push({
      text: inputMessage.value,
      sender: "user",
      time: getCurrentTime()
    });
    
    // 清空输入框
    const userMessage = inputMessage.value;
    inputMessage.value = "";
    
    // 模拟回复
    setTimeout(() => {
      messages.value.push({
        text: getReply(userMessage),
        sender: "assistant",
        time: getCurrentTime()
      });
      
      // 滚动到底部
      scrollToBottom();
    }, 500);
  }
};

// 获取当前时间
function getCurrentTime() {
  const now = new Date();
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
}

// 获取回复的简单逻辑
const getReply = (message) => {
  const lowerMsg = message.toLowerCase();
  
  if (lowerMsg.includes("你好") || lowerMsg.includes("hi") || lowerMsg.includes("hello")) {
    return "你好！我是口香糖检测助手，很高兴为您服务！";
  } else if (lowerMsg.includes("检测") || lowerMsg.includes("识别")) {
    return "您可以使用我们的检测功能，只需将口香糖放在摄像头前，系统会自动分析其成分和状态。";
  } else if (lowerMsg.includes("历史") || lowerMsg.includes("记录")) {
    return "您可以在历史记录页面查看过往的检测结果和分析报告。";
  } else if (lowerMsg.includes("帮助") || lowerMsg.includes("怎么用")) {
    return "我可以帮助您检测口香糖的质量和成分。您可以发送消息问我任何问题，或使用下方的快捷功能按钮。";
  } else if (lowerMsg.includes("成分") || lowerMsg.includes("材料")) {
    return "口香糖通常包含胶基、甜味剂、香料和软化剂。我可以帮助您分析具体产品的成分组成。";
  } else if (lowerMsg.includes("谢谢") || lowerMsg.includes("感谢")) {
    return "不客气！如果还有其他问题，随时告诉我哦~";
  }
  
  const randomReplies = [
    "我明白了，关于口香糖检测您还有什么想了解的？",
    "这个问题很有趣，我可以帮您分析口香糖的相关信息。",
    "检测口香糖质量是我的专长，您想了解哪方面的内容呢？",
    "感谢您的咨询，我可以为您提供口香糖成分分析服务。"
  ];
  
  return randomReplies[Math.floor(Math.random() * randomReplies.length)];
};

// 滚动到底部
const scrollToBottom = () => {
  // 实际项目中可能需要使用uni.pageScrollTo
  console.log("滚动到底部");
  // 示例: uni.pageScrollTo({ scrollTop: 10000, duration: 300 })
};
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 50%, #f3e8ff 100%);
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  padding: 32rpx 48rpx 32rpx;
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
  width: 160rpx;
  height: 160rpx;
  top: -80rpx;
  right: -80rpx;
}

.header-bg-circle-2 {
  width: 128rpx;
  height: 128rpx;
  bottom: -64rpx;
  left: -64rpx;
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

.sparkle {
  font-size: 40rpx;
  color: #fbbf24;
}

.chat-area {
  flex: 1;
  padding: 30rpx;
  padding-bottom: 200rpx;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.message-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 30rpx;
  max-width: 85%;
  align-self: flex-start;
}

.user-message {
  align-self: flex-end;
  background: rgba(255, 241, 242, 0.8);
}

.message-content {
  display: flex;
  gap: 24rpx;
}

.user-message .message-content {
  flex-direction: row-reverse;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
  flex-shrink: 0;
}

.assistant-avatar {
  background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%);
}

.user-avatar {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
}

.message-bubble {
  flex: 1;
}

.assistant-bubble {
  align-items: flex-start;
}

.user-bubble {
  align-items: flex-end;
}

.bubble-content {
  border-radius: 32rpx;
  padding: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.assistant-bubble .bubble-content {
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%);
  border-radius: 32rpx 32rpx 32rpx 8rpx;
}

.user-bubble .bubble-content {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
  border-radius: 32rpx 32rpx 8rpx 32rpx;
}

.message-text {
  color: #1f2937;
  line-height: 1.6;
  font-size: 32rpx;
}

.message-time {
  font-size: 24rpx;
  color: #6b7280;
  margin-top: 16rpx;
  margin-left: 16rpx;
}

.input-area {
  position: fixed;
  bottom: 120rpx;
  left: 0;
  right: 0;
  padding: 0 30rpx;
}

.input-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 26rpx;
  padding: 30rpx;
  display: flex;
  align-items: center;
  gap: 24rpx;
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.15);
}

.message-input {
  flex: 1;
  background: #f3f4f6;
  border: none;
  border-radius: 24rpx;
  padding: 24rpx 32rpx;
  font-size: 32rpx;
  transition: background-color 0.2s;
}

.message-input:focus {
  background: white;
}

.send-btn {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(37, 99, 235, 0.3);
  transition: transform 0.2s;
}

.send-btn:active {
  transform: scale(0.9);
}

.icon {
  font-size: inherit;
}
</style>