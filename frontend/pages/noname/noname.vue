<template>
  <view class="chat-container">
    <!-- 标题栏 -->
    <view class="chat-header">
      <text class="chat-title">AI助手</text>
    </view>

    <!-- 消息列表 -->
    <scroll-view
      scroll-y="true"
      class="chat-messages"
      :scroll-with-animation="true"
      :scroll-into-view="'msg-' + (messages.length - 1)"
    >
      <view
        v-for="(msg, index) in messages"
        :key="index"
        :id="'msg-' + index"
        class="message-wrapper"
        :class="msg.role === 'user' ? 'user-message' : 'ai-message'"
      >
        <view class="message-bubble">
          <text>{{ msg.content }}</text>
        </view>
      </view>

      <view v-if="loading" class="message-wrapper ai-message">
        <view class="loading-bubble">
          <view class="loading-dot" style="background-color: #4f78ff"></view>
          <view
            class="loading-dot delay-1"
            style="background-color: #4f78ff"
          ></view>
          <view
            class="loading-dot delay-2"
            style="background-color: #4f78ff"
          ></view>
        </view>
      </view>
    </scroll-view>

    <!-- 输入区域 -->
    <view class="chat-input-area">
      <view class="input-wrapper">
        <input
          v-model="inputText"
          type="text"
          placeholder="输入消息..."
          class="message-input"
          @confirm="sendMessage"
        />
        <button
          @click="sendMessage"
          class="send-button"
          :disabled="!inputText.trim()"
        >
          <text class="send-icon">→</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";

const messages = ref([
  {
    role: "assistant",
    content: "你好！我是口香糖检测小助手，有什么可以帮您的吗？",
  },
]);
const inputText = ref("");
const loading = ref(false);

const sendMessage = () => {
  if (!inputText.value.trim()) return;

  const userMsg = inputText.value;
  messages.value.push({ role: "user", content: userMsg });
  inputText.value = "";
  loading.value = true;

  // 模拟AI回复
  setTimeout(() => {
    messages.value.push({
      role: "assistant",
      content: getAIResponse(userMsg),
    });
    loading.value = false;
  }, 1000);
};

const getAIResponse = (userMsg) => {
  const responses = [
    "这是一个有趣的提问！",
    "我理解您的问题是关于：" + userMsg,
    "让我思考一下如何回答这个问题...",
    "感谢您的提问，我的回答是：这取决于具体情况。",
    "您能提供更多细节吗？这样我可以更好地帮助您。",
  ];
  return responses[Math.floor(Math.random() * responses.length)];
};
</script>

<style>
page {
  height: 100vh;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f9ff;
}

.chat-header {
  height: 30px;
  padding: 16px 8px;
  background-color: #4f78ff;
  box-shadow: 0 2px 10px rgba(79, 120, 255, 0.2);
}

.chat-title {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;

  color: white;
  letter-spacing: 1px;
}

.chat-messages {
  flex: 1;
  padding: 2vw;
  width: 96vw;
  overflow-y: auto;
}

.message-wrapper {
  display: flex;
  margin-bottom: 16px;
}

.user-message {
  justify-content: flex-end;
}

.ai-message {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 18px;
}

.user-message .message-bubble {
  background-color: #4f78ff;
  color: white;
  box-shadow: 0 2px 8px rgba(79, 120, 255, 0.3);
}

.ai-message .message-bubble {
  background-color: white;
  color: #333;
  box-shadow: 0 2px 8px rgba(79, 120, 255, 0.1);
  border: 1px solid #e6ebff;
}

.loading-bubble {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: white;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(79, 120, 255, 0.1);
}

.loading-dot {
  width: 8px;
  height: 8px;
  margin: 0 4px;
  border-radius: 50%;
  animation: pulse 1.4s infinite ease-in-out;
}

.loading-dot.delay-1 {
  animation-delay: 0.2s;
}

.loading-dot.delay-2 {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.chat-input-area {
  position: fixed;
  bottom: 50px;
  width: calc(100% - 32px);
  padding: 16px;
  background-color: white;
  border-top: 1px solid #e6ebff;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.message-input {
  flex: 1;
  padding: 8px 16px;
  border: 1px solid #e6ebff;
  border-radius: 20px;
  outline: none;
  transition: all 0.2s ease;
}

.message-input:focus {
  border-color: #4f78ff;
  box-shadow: 0 0 0 2px rgba(79, 120, 255, 0.2);
}

.send-button {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4f78ff;
  color: white;
  border: none;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.send-button:not(:disabled):hover {
  background-color: #3a5bd9;
}

.send-button:active {
  transform: scale(0.95);
}

.send-button:disabled {
  opacity: 0.5;
}

.send-icon {
  font-size: 20px;
}
</style>
