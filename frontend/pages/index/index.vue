<template>
  <loading :show="isLoading"></loading>
  <view class="page-container">
    <view class="app-title"><text class="www">口香糖缺陷工业检测系统</text></view>
    <view class="card">
      <view class="chat-header">实时图像展示</view>
      <view class="chat-window">
        <view class="imgs" v-for="item in items">
          <img :src="item.src" alt="" @click="onLongPress(item.src)" />
		  <view style="width: 100%; height: 20px; display: flex; justify-content: space-between; align-items: center;">
			<view class="time-text">{{ item.created }}</view>
		  <view class="time-text">缺肉数量：{{ item.defect_count }}</view>
		  </view>
			
          
        </view>
        <view style="width: 100%; height: 30px"> </view>
      </view>
    </view>
    <view class="datas">
      <view class="data-item">
        <view class="data-label">缺肉总数：</view>
        <view class="data-value">{{ defectCount }}</view>
      </view>
      <view class="data-item">
        <view class="data-label">堵塞状态：</view>
        <view class="data-value">正常</view>
      </view>
    </view>
    <view class="btns">
      <view class="btn" @click="kaishi(1.0)"> {{ kaikai }} </view>
      <view class="btn" @click="kaishi(2.0)"> 暂停 </view>
      <view class="btn" @click="kaishi(0.0)"> 结束 </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { onShow, onLoad, onHide } from "@dcloudio/uni-app";
import Loading from "../../components/Loading.vue";
let timer = null;
const kaikai = ref("开始");
const defectCount = ref(0);
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
//   {
//     src: "https://picsum.photos/200",
//   },
//   {
//     src: "https://picsum.photos/200",
//   },
//   {
//     src: "https://picsum.photos/200",
//   },
//   {
//     src: "https://picsum.photos/200",
//   },
//   {
//     src: "https://picsum.photos/200",
//   },
]);
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
          .slice(0, 80) // 截取前50个数据
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

<style lang="scss" scoped>
.page-container {
  background: linear-gradient(to bottom, #f8f9ff, #ffffff);
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.app-title {
  width: 100%;
  height: 34px;
  padding: 16px 8px;
  background: linear-gradient(135deg, #4f78ff 0%, #3a5bd9 100%);
  color: white;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  box-shadow: 0 4px 15px rgba(79, 120, 255, 0.3);
  margin-bottom: 15px;
  position: relative;
  letter-spacing: 1px;
}

.www {
  position: absolute;
  left: 50px;
  top: 21.5px;
}

.app-title::before {
  content: "";
  position: absolute;
  left: 20px;
  top: 24px;
  width: 24px;
  height: 24px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm-1.06 13.54L7.4 12l1.41-1.41 2.12 2.12 4.24-4.24 1.41 1.41-5.64 5.66z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
}

.card {
  margin-top: 5px;
  width: 90vw;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(79, 120, 255, 0.1);
  overflow: hidden;
}

.chat-header {
  background-color: #4f78ff;
  color: #fff;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 500;
}

.chat-window {
  height: 58vh;
  overflow-y: auto;
  padding-left: 10px;
  padding-right: 10px;
}

.imgs {
  width: 94%;
  margin-left: 3%;
  margin-top: 10px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.imgs img {
  width: 100%;
  height: auto;
  display: block;
}

.time-text {
  color: #999;
  font-size: 12px;
  padding: 0px 8px 4px 8px;
}
.time-text2{

}
.datas {
  width: 90vw;
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.data-item {
  width: 42%;
  background: #fff;
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 2px 10px rgba(79, 120, 255, 0.1);
}

.data-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.data-value {
  font-size: 18px;
  font-weight: bold;
  color: #4f78ff;
}

.btns {
  width: 90vw;
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  margin-bottom: 5px;
}

.btn {
  width: 30%;
  height: 42px;
  border-radius: 8px;
  background-color: #4f78ff;
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(79, 120, 255, 0.3);
}

.btn:active {
  transform: scale(0.96);
  box-shadow: 0 1px 4px rgba(79, 120, 255, 0.3);
}
</style>
