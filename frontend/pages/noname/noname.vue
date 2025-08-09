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
        :class="[
          message.sender === 'user' ? 'user-message' : 'assistant-message',
        ]"
      >
        <view class="message-content">
          <view
            class="avatar"
            :class="
              message.sender === 'user' ? 'user-avatar' : 'assistant-avatar'
            "
          >
            <text class="icon">{{
              message.sender === "user" ? "👤" : "🤖"
            }}</text>
          </view>
          <view
            class="message-bubble"
            :class="
              message.sender === 'user' ? 'user-bubble' : 'assistant-bubble'
            "
          >
            <view class="bubble-content">
              <!-- 文本消息 -->
              <!-- <text class="message-text" v-if="message.type === 'text'">{{ message.text }}</text> -->
              <rich-text
                v-if="message.type === 'text'"
                :nodes="message.html"
                class="markdown-body"
              />
              <!-- 报告消息 -->
              <view v-if="message.type === 'report'">
                <!-- <text class="report-title">口香糖缺陷分析报告</text> -->
                <!-- <text class="report-text">{{ message.text }}</text> -->
                <rich-text :nodes="message.html" class="markdown-body" />
                
                <view class="chart-canvas">
    <qiun-data-charts 
      type="column"
      :opts="opts"
      :chartData="chartData"
      :ontouch="true"
    />
  </view>
              </view>

              <!-- 快捷按钮 -->
              <view
                class="quick-actions"
                v-if="message.type === 'quick-actions'"
              >
                <button class="action-btn" @click="requestReport(7)">
                  生成周报
                </button>
                <button class="action-btn" @click="requestCustomReport">
                  自定义
                </button>
              </view>
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
      <!-- <view class="quick-buttons">
				<button class="quick-btn" @click="showQuickActions">生成报告</button>
			</view> -->
    </view>

    <!-- 自定义报告弹窗 -->
    <uni-popup ref="datePopup" type="dialog">
      <uni-popup-dialog title="选择日期范围" @confirm="onDateConfirm">
        <view class="date-picker-container">
          <uni-datetime-picker
            type="daterange"
            :clear-icon="false"
            @change="handleDateChange"
          />
        </view>
      </uni-popup-dialog>
    </uni-popup>

    <!-- 加载动画 -->
    <view class="loading-animation" v-if="isLoading">
      <view class="dot dot1"></view>
      <view class="dot dot2"></view>
      <view class="dot dot3"></view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
const isLoading = ref(false);
import uCharts from "@/uni_modules/qiun-data-charts/js_sdk/u-charts/u-charts.min.js";
import { marked } from "@/static/js/marked.esm.js";
//import { useDefectStore } from '@/stores/defect.js';

// 初始化消息
const inputMessage = ref("");
const messages = ref([
  {
    text: "你好！我是口香糖检测助手，可以回答口香糖相关问题，也可以为您生成缺陷分析报告",
    html: marked.parse(
      "你好！我是口香糖检测助手，可以回答口香糖相关问题，也可以为您生成缺陷分析报告"
    ), // 新增：HTML 节点
    sender: "assistant",
    time: getCurrentTime(),
    type: "text",
  },
  {
    sender: "assistant",
    time: getCurrentTime(),
    type: "quick-actions",
  },
]);

// 发送消息
const sendMessage = async () => {
  if (inputMessage.value.trim()) {
    // 添加用户消息
    const userMsg = {
      text: inputMessage.value,
      sender: "user",
      html: marked.parse(inputMessage.value), // 新增
      time: getCurrentTime(),
      type: "text",
    };
    messages.value.push(userMsg);

    const userMessage = inputMessage.value;
    inputMessage.value = "";

    nextTick(scrollToBottom); // 确保 DOM 更新后再滑动
    isLoading.value = true;
    try {
      // 处理报告请求
      if (userMessage.includes("报告") || userMessage.includes("分析")) {
        const days = extractDaysFromMessage(userMessage) || 7;
        generateReport(days);
      }
      // 普通对话
      else {
        const response = await callDeepSeekAPI({
          role: "user",
          content: userMessage,
        });
        addAssistantMessage(response);
      }
    } catch (error) {
      addAssistantMessage("处理请求时出错：" + error.message);
    } finally {
      isLoading.value = false;
    }
  }
};
const DEEPSEEK_API_KEY = "sk-95574542933b443e881bbf19a4ec2730";
// 调用DeepSeek API
const callDeepSeekAPI = async (message, onStream) => {
  const res = await uni.request({
    url: "https://api.deepseek.com/v1/chat/completions",
    method: "POST",
    header: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${DEEPSEEK_API_KEY}`, // 替换为你的API密钥
    },
    data: {
      model: "deepseek-chat",
      messages: [
        {
          role: "system",
          content: `你是一位口香糖质量检测专家，具备数据分析能力。当用户请求报告时，你会自动收到缺陷数据，请分析并生成包含以下内容的报告：
          1. 总体缺陷统计（总数、日均值）
          2. 时间趋势分析（高峰时段、日期）
          3. 关键发现和建议
          4. 使用Markdown格式输出
          其他时候回答口香糖相关问题。`,
        },
        message,
      ],
    },
  });

  return res.data.choices[0].message.content;
};

// 生成报告（完全由AI处理）
const generateReport = async (days) => {
  // 显示加载状态
  isLoading.value = true;
  addAssistantMessage(`正在生成最近${days}天的缺陷分析报告...`, "text");

  try {
    // 获取数据
    const defectData = await fetchDefectData(days);
    //console.log(defectData,'666')
    if (!defectData || defectData.length === 0) {
      addAssistantMessage("所选时间段内没有检测到缺陷数据。", "text");
      return;
    }

    // 准备数据给AI分析
    const analysisPrompt = {
      role: "user",
      content: `请分析以下口香糖缺陷数据并生成详细报告（使用Markdown格式）：
      ### 数据说明
      - 时间范围: ${days}天
      - 总记录数: ${defectData.length}
      - 总缺陷数：每个记录数中defect_count值总和
      - 时间：每个记录数中的timestamp值
      - 数据示例: 
        ${JSON.stringify(defectData)}
      
      ### 要求
      1. 统计每日缺陷数量并分析趋势
      2. 识别异常值和高发时段
      3. 提出改进建议
      4. 包含总结
      
      请使用专业但易懂的语言，报告开头用"## 口香糖缺陷分析报告"标题`,
    };

    // 调用AI生成报告文本
    const reportText = await callDeepSeekAPI(analysisPrompt);

    // 添加报告消息
    const reportMsg = {
      text: reportText,
      html: marked.parse(reportText), // 新增：HTML 节点
      sender: "assistant",
      time: getCurrentTime(),
      type: "report",
      chartData: prepareChartData(defectData),
    };

    messages.value.push(reportMsg);

    // 渲染图表
    nextTick(() => {
      setTimeout(() => renderChart(reportMsg), 500); // 延迟 50ms
    });
  } catch (error) {
    addAssistantMessage("生成报告失败：" + error.message, "text");
  }
  isLoading.value = false;
  nextTick(scrollToBottom); // 确保 DOM 更新后再滑动
};

// 准备图表数据
const prepareChartData = (defectData) => {
  // 按日期分组
  const dailyData = {};
  defectData.forEach((item) => {
    const date = item.timestamp.split("T")[0];
    dailyData[date] = (dailyData[date] || 0) + item.defect_count;
  });

  return {
    categories: Object.keys(dailyData),
    series: [
      {
        name: "缺陷数量",
        data: Object.values(dailyData),
      },
    ],
  };
};
const opts = ref( {
        color: ["#1890FF","#91CB74","#FAC858","#EE6666","#73C0DE","#3CA272","#FC8452","#9A60B4","#ea7ccc"],
        padding: [15,15,0,5],
        touchMoveLimit: 24,
        enableScroll: true,
        legend: {},
        xAxis: {
          disableGrid: true,
          scrollShow: true,
          itemCount: 4
        },
        yAxis: {
          data: [
            {
              min: 0
            }
          ]
        },
        extra: {
          column: {
            type: "group",
            width: 30,
            activeBgColor: "#000000",
            activeBgOpacity: 0.08
          }
        }
      })
      const chartData  = ref()
const chartIndex = ref(0);
const renderChart = (message) => {
  console.log(message,'sssdmm')
  chartData.value = message.chartData
};

// 快捷操作
const showQuickActions = () => {
  messages.value.push({
    sender: "assistant",
    time: getCurrentTime(),
    type: "quick-actions",
  });
  scrollToBottom();
};

const requestReport = (days) => {
  generateReport(days);
};
const datePopup = ref();
// 打开弹窗
const openPopup = (e) => {
  if (datePopup.value) {
    //uni.hideTabBar();
    //showLogin.value = true;
    datePopup.value.open();
  }
};

// 关闭弹窗
const closePopup = () => {
  if (datePopup.value) {
    datePopup.value.close();
    datePicker.value = null;
  }
};

const requestCustomReport = () => {
  if (datePopup.value) {
    datePopup.value.open();
  } else {
    uni.showToast({
      title: "日期选择组件未初始化",
      icon: "none",
    });
  }
};
const datePicker = ref(null);
const handleDateChange = (e) => {
  if (e && e.length === 2) {
    datePicker.value = e;
  } else {
    datePicker.value = null;
  }
};
const onDateConfirm = () => {
  const [start, end] = datePicker.value;
  generateCustomReport(start, end);
};
const confirmCustomDate = (value) => {
  if (!value) {
    uni.showToast({
      title: "请输入日期范围",
      icon: "none",
    });
    return;
  }

  const [start, end] = value.split("至").map((d) => d.trim());
  if (!start || !end) {
    uni.showToast({
      title: "请输入完整的日期范围",
      icon: "none",
    });
    return;
  }

  if (!isValidDate(start) || !isValidDate(end)) {
    uni.showToast({
      title: "日期格式不正确，请使用YYYY-MM-DD格式",
      icon: "none",
    });
    return;
  }

  if (new Date(start) > new Date(end)) {
    uni.showToast({
      title: "开始日期不能晚于结束日期",
      icon: "none",
    });
    return;
  }

  generateCustomReport(start, end);
};

const isValidDate = (dateString) => {
  const regEx = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateString.match(regEx)) return false;
  const d = new Date(dateString);
  return !isNaN(d.getTime());
};

const generateCustomReport = async (startDate, endDate) => {
  isLoading.value = true;
  addAssistantMessage(
    `正在生成 ${startDate} 至 ${endDate} 的缺陷分析报告...`,
    "text"
  );

  try {
    const defectData = await fetchDefectData(0); // 获取所有数据
    const filteredData = defectData.filter((item) => {
      const itemDate = item.timestamp.split("T")[0];
      return itemDate >= startDate && itemDate <= endDate;
    });

    if (filteredData.length === 0) {
      addAssistantMessage(
        `在 ${startDate} 至 ${endDate} 期间没有检测到缺陷数据`,
        "text"
      );
      return;
    }

    // 准备数据给AI分析
    const analysisPrompt = {
      role: "user",
      content: `请分析以下口香糖缺陷数据并生成详细报告（使用Markdown格式）：
### 数据说明
- 时间范围: ${startDate} 至 ${endDate}
- 总记录数: ${filteredData.length}
- 数据示例: 
${JSON.stringify(filteredData.slice(0, 3))}

### 要求
1. 统计每日缺陷数量并分析趋势
2. 识别异常值和高发时段
3. 提出改进建议
4. 包含总结

请使用专业但易懂的语言，报告开头用"## 口香糖缺陷分析报告"标题`,
    };

    const reportText = await callDeepSeekAPI(analysisPrompt);
    const reportMsg = {
      text: reportText,
      html: marked.parse(reportText),
      sender: "assistant",
      time: getCurrentTime(),
      type: "report",
      chartData: prepareChartData(filteredData),
    };

    messages.value.push(reportMsg);
    nextTick(() => {
      setTimeout(() => renderChart(reportMsg), 500);
    });
  } catch (error) {
    addAssistantMessage("生成自定义报告失败：" + error.message, "text");
  } finally {
    isLoading.value = false;
    nextTick(scrollToBottom); // 确保 DOM 更新后再滑动
  }
};

// 添加助手消息
const addAssistantMessage = (text, type = "text") => {
  messages.value.push({
    text,
    sender: "assistant",
    html: marked.parse(text),
    time: getCurrentTime(),
    type,
  });
  nextTick(scrollToBottom); // 确保 DOM 更新后再滑动
};

// 模拟数据获取
const fetchDefectData = async (days) => {
  return new Promise((resolve, reject) => {
    uni.request({
      url: "http://112.74.32.111:8000/images",
      method: "GET",
      success: (res) => {
        if (res.statusCode === 200) {
          console.log("获取检测数据成功", res.data.images);
          const filtered = res.data.images.map((item) => ({
            defect_count: item.defect_count,
            timestamp: item.timestamp,
          }));
          resolve(filtered);
        } else {
          console.error("获取图片失败", res);
          reject(res);
        }
      },
      fail: (err) => {
        console.error("请求失败", err);
        reject(err);
      },
    });
  });
  // // 实际项目中替换为API调用
  // return new Promise(resolve => {
  // 	setTimeout(() => {
  // 		// 这里使用您提供的示例数据
  // 		resolve([{
  // 				defect_count: 2,
  // 				timestamp: "2025-07-10T16:13:24.520251"
  // 			},
  // 			{
  // 				defect_count: 1,
  // 				timestamp: "2025-07-10T16:13:05.320011"
  // 			},
  // 			// ...其他数据
  // 		]);
  // 	}, 800);
  // });
};

// 其他辅助函数
function getCurrentTime() {
  const now = new Date();
  return `${now.getHours().toString().padStart(2, "0")}:${now
    .getMinutes()
    .toString()
    .padStart(2, "0")}`;
}

function scrollToBottom() {
  uni.pageScrollTo({
    scrollTop: 100000,
    duration: 300,
  });
}

function extractDaysFromMessage(message) {
  const dayMatch = message.match(/(\d+)/);
  return dayMatch ? parseInt(dayMatch[1]) : null;
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 50%, #f3e8ff 100%);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  margin: 0 auto;
  max-width: 980px; 
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
  width: 50%;
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
  box-sizing: border-box;
  margin: 0 auto;
  max-width: 980px; /* 限制输入区域宽度 */
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

.report-title {
  font-weight: bold;
  font-size: 36rpx;
  display: block;
  margin-bottom: 20rpx;
  color: #1a56db;
}

.report-text {
  white-space: pre-wrap;
  line-height: 1.8;
  font-size: 32rpx;
}

.chart-canvas {
  width: 100%;
  height: 400rpx;
  margin-top: 30rpx;
  background-color: #f9fafb;
  border-radius: 16rpx;
  border: 1rpx solid #e5e7eb;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  margin-top: 20rpx;
  justify-content: space-between;
}

.action-btn {
  height: 80rpx;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 25rpx;
  padding: 0 32rpx;
  font-size: 28rpx;
  flex: 1;
  min-width: 200rpx;
  box-shadow: 0 4rpx 12rpx rgba(37, 99, 235, 0.2);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 80rpx;
}

.action-btn:active {
  transform: scale(0.95);
  opacity: 0.9;
}

.date-picker-container {
  padding: 20rpx;
  width: 600rpx;
}

.loading-animation {
  position: fixed;
  bottom: 300rpx;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  z-index: 1000;
}

.dot {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
  background-color: #3b82f6;
  animation: bounce 1.4s infinite ease-in-out;
}

.dot1 {
  animation-delay: -0.32s;
}

.dot2 {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.quick-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20rpx;
  padding: 0 30rpx;
}

.quick-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 50rpx;
  padding: 20rpx 40rpx;
  font-size: 32rpx;
  width: 100%;
  box-shadow: 0 6rpx 16rpx rgba(16, 185, 129, 0.3);
}

/* Markdown样式增强 */
.report-text h2 {
  font-size: 36rpx;
  margin: 30rpx 0 20rpx;
  color: #1e3a8a;
  border-bottom: 2rpx solid #dbeafe;
  padding-bottom: 10rpx;
}

.report-text ul {
  padding-left: 40rpx;
  margin: 20rpx 0;
}

.report-text li {
  margin-bottom: 16rpx;
  line-height: 1.6;
}

.report-text strong {
  color: #1d4ed8;
}
.markdown-body {
  line-height: 1.8;
  font-size: 32rpx;
  color: #1f2937;
}
.markdown-body h2 {
  font-size: 36rpx;
  margin: 30rpx 0 20rpx;
  color: #1e3a8a;
  border-bottom: 2rpx solid #dbeafe;
  padding-bottom: 10rpx;
}
.markdown-body ul {
  padding-left: 40rpx;
  margin: 20rpx 0;
}
.markdown-body li {
  margin-bottom: 16rpx;
}
.markdown-body strong {
  color: #1d4ed8;
}
.markdown-body pre {
  /* background: #f3f4f6; */
  padding: 16rpx;
  border-radius: 8rpx;
  overflow-x: auto;
  font-family: monospace;
  margin: 20rpx 0;
}
</style>
