<template>
  <view class="page-container">
    <view class="custom-nav-bar" id="navBar">
      <view class="nav-title">个人中心</view>
      <view class="head-box" @click="openPopup">
        <view class="heads">
          <!-- <button class="btnLogin" open-type="getPhoneNumber" bindgetphonenumber="getPhoneNumber"></button> -->
          <image
            :src="
              loginStatus
                ? '../../static/headshot2.png'
                : '../../static/headshot1.png'
            "
            mode=""
          />
        </view>
        <view class="texts" v-if="!loginStatus">
          <view class="ts1"> 未登录/注册 </view>
          <!-- <view class="ts1">
						{{ username }}
					</view> -->
          <view class="ts2"> 点击头像可登录/注册 </view>
        </view>
        <view class="account" v-else>
          {{ account }}
        </view>
      </view>
    </view>
    <view class="pers">
      <view class="items">
        <view class="tts">常用服务</view>
        <view class="sss">
          <view class="s1" @click="navigate" data-url="/pkgA/mysubmit/mysubmit">
            <image src="../../static/submit.png" mode="" />
            <view style="margin-top: 5px">联系我们</view>
          </view>
          <view class="s1" @click="navigate" data-url="/pkgA/resume/resume">
            <image src="../../static/分组 1@2x.png" mode="" />
            <view style="margin-top: 5px">历史记录</view>
          </view>
          <view
            class="s1"
            @click="navigate"
            data-url="/pkgA/collection/collection"
          >
            <image src="../../static/collect.png" mode="" />
            <view style="margin-top: 5px">我的收藏</view>
          </view>
        </view>
      </view>
      <view class="items">
        <view class="tts">其他服务</view>
        <view class="sss">
          <view class="s2" @click="navigate" data-url="/pkgA/about/about">
            <image
              style="width: 30px; height: 26px"
              src="../../static/about.png"
              mode=""
            />
            <view style="margin-top: 5px">关于我们</view>
          </view>
          <view class="s2" @click="navigate" data-url="/pkgA/privacy/privacy">
            <image
              style="width: 24.16px; height: 26px"
              src="../../static/yinsi.png"
              mode=""
            />
            <view style="margin-top: 5px">隐私政策</view>
          </view>
          <view class="s2" @click="navigate" data-url="/pkgA/service/service">
            <image
              style="width: 24.53px; height: 26px"
              src="../../static/service.png"
              mode=""
            />
            <view style="margin-top: 5px">服务协议</view>
          </view>
          <view class="s2" @click="navigate" data-url="/pkgA/law/law">
            <image
              style="width: 23px; height: 26px"
              src="../../static/law.png"
              mode=""
            />
            <view style="margin-top: 5px">法律声明</view>
          </view>
        </view>
      </view>
    </view>
  </view>
  <uni-popup ref="popups" type="bottom" mask="true" @change="change">
    <view class="popup-content">
      <Login
        :show="showLogin"
        @loginSuccess="handleLoginSuccess"
        @hideLoginView="handleClose"
      />
    </view>
  </uni-popup>
</template>

<script setup>
import { ref } from "vue";
import Login from "../../components/Login.vue";
import { onShow, onLoad, onReachBottom } from "@dcloudio/uni-app";
onShow(async () => {
  // 页面显示时执行的逻辑
  console.log("页面显示");
  loginStatus.value = uni.getStorageSync("loginStatus") || false; // 获取登录状态
  if (loginStatus.value) {
    account.value = formatPhoneNumber(uni.getStorageSync("account"));
  }
});

function navigate(e) {
  uni.showToast({
    title: "功能暂未开发~",
    icon: "none",
  });
  return;
  console.log(e.currentTarget.dataset);
  uni.navigateTo({
    url: e.currentTarget.dataset.url,
  });
}
const loginStatus = ref(false); // 登录状态
const account = ref();
loginStatus.value = uni.getStorageSync("loginStatus") || false; // 获取登录状态
if (loginStatus.value) {
  account.value = formatPhoneNumber(uni.getStorageSync("account"));
}
const showLogin = ref(false);
const popups = ref();
// 打开弹窗
const openPopup = (e) => {
  if (loginStatus.value) {
    return; // 如果已登录，则不打开弹窗
  }
  if (popups.value) {
    uni.hideTabBar();
    showLogin.value = true;
    popups.value.open();
  }
};

// 关闭弹窗
const closePopup = () => {
  if (popups.value) {
    popups.value.close();
  }
};

const change = (event) => {
  console.log("Popup state changed");
  if (!event.show) {
    console.log("点击了蒙层，弹窗已关闭");
    showLogin.value = false;
    // 在这里写点击蒙层后的逻辑
    uni.showTabBar();
  }
};

function handleLoginSuccess(payload) {
  // 可以在这里执行登录成功后的其他逻辑
  if (payload) {
    loginStatus.value = true; // 更新登录状态
    // 更新 account 的值
    account.value = formatPhoneNumber(uni.getStorageSync("account"));
    // 关闭弹窗
    showLogin.value = false;
    closePopup();
  }
}

function handleClose(e) {
  // 处理关闭事件
  showLogin.value = false;
  closePopup();
}

function formatPhoneNumber(phone) {
  if (!phone) return "";
  return phone.replace(/(\d{3})\d{4}(\d{4})/, "$1****$2");
}
</script>

<style lang="scss" scoped>
.page-container {
  background: linear-gradient(to bottom, #dbe8ff, #f5f5f5 50%);
  backdrop-filter: blur(87px);
  height: 100vh;
  /* 使用视口高度确保填充整个页面 */
  width: 100vw;
  /* 使用视口宽度确保填充整个页面 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.custom-nav-bar {
  top: 0;
  left: 0;
  right: 0;
  padding: 0 16px;
  z-index: 10;
  /* 确保导航栏在最顶层 */
  transition: top 0.3s ease-in-out;
  /* 平滑过渡效果 */
  display: flex;
  justify-content: center;
  width: 100;
  height: 250px;
}

.nav-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 23.79px;
  width: 90px;
  height: 27px;
  opacity: 0.9;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0px;
  line-height: 26.06px;
  color: black;
  text-align: center;
  vertical-align: top;
}

.pers {
  position: fixed;
  top: 190px;
  width: 100%;

  opacity: 1;
  z-index: 1000;
  border-radius: 25px 25px 0px 0px;
  //   background: linear-gradient(
  //     180deg,
  //     rgba(227, 238, 255, 1) 0%,
  //     rgba(232, 241, 255, 1) 0%,
  //     rgba(241, 242, 243, 1) 26.39%,
  //     rgba(247, 247, 247, 1) 58.08%
  //   );
}

.items {
  width: 90vw;
  margin-left: 5vw;
  margin-top: 2vh;
  height: 104px;
  opacity: 1;
  border-radius: 15px;
  background: rgba(255, 255, 255, 1);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
}

.tts {
  position: relative;
  top: 7px;
  left: 17px;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0px;
  line-height: 20.27px;
  color: rgba(56, 56, 56, 1);
  text-align: left;
  vertical-align: top;
}

.sss {
  margin-top: 18px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.s1 {
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 17.38px;
  color: rgba(56, 56, 56, 1);
  text-align: center;
  vertical-align: top;
}

.s2 {
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 17.38px;
  color: rgba(56, 56, 56, 1);
  text-align: center;
  vertical-align: top;
}

.s1 image {
  width: 28.8px;
  height: 27.88px;
}

.heads image {
  border-radius: 50%;
  width: 65px;
  height: 65px;
}

.head-box {
  left: 31px;
  top: 84px;
  position: fixed;
  width: 300px;
}

.ts1 {
  position: fixed;
  left: 112px;
  top: 97px;
  width: 98px;
  height: 28px;
  opacity: 1;
  /** 文本1 */
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0px;
  line-height: 20.27px;
  color: rgba(0, 0, 0, 1);
  text-align: left;
  vertical-align: top;
}

.ts2 {
  position: fixed;
  left: 112px;
  top: 125px;
  width: 136px;
  height: 22px;
  opacity: 1;
  /** 文本1 */
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 15.93px;
  color: rgba(56, 56, 56, 1);
  text-align: left;
  vertical-align: top;
}

.account {
  position: fixed;
  left: 112px;
  top: 125px;
  width: 98px;
  height: 28px;
  opacity: 1;
  /** 文本1 */
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 18.82px;
  color: rgba(128, 128, 128, 1);
  text-align: left;
  vertical-align: top;
}

.btnLogin {
  width: 250px;
  height: 46px;
  position: absolute;
  opacity: 0;
}

.bg {
  display: none;
  position: absolute;

  left: 0%;
  width: 100vw;
  height: 1400px;
  background-color: black;
  z-index: 1001;
  -moz-opacity: 0.7;
  opacity: 0.7;
  filter: alpha(opacity=70);
}

.loginMode {
  width: 100vw;
  height: auto;
  opacity: 1;
  border-top-left-radius: 12px;
  /* 设置左上角圆角 */
  border-top-right-radius: 12px;
  /* 设置右上角圆角 */
  background: rgba(255, 255, 255, 1);
  position: fixed;
  z-index: 2000;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.temt {
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0px;
  line-height: 26.06px;
  color: rgba(0, 0, 0, 1);
  text-align: center;
  vertical-align: top;
  margin-top: 15px;
}

.ser {
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 17.38px;
  color: rgba(0, 0, 0, 1);
  text-align: center;
  vertical-align: top;
  margin-top: 8px;
}

.phonelogin {
  width: 250px;
  height: 46px;
  opacity: 1;
  border-radius: 23px;
  background: rgba(80, 177, 178, 1);
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 23.17px;
  color: rgba(255, 255, 255, 1);
  text-align: justify;
  vertical-align: top;
  margin-top: 20px;
  margin-bottom: 20px;
  position: relative;
}

.phonelogin image {
  width: 12.07px;
  height: 17.93px;
  margin-right: 15px;
}

.meng {
  background-color: rgb(160, 70, 70, 0);
  width: 250px;
  height: 46px;
  position: absolute;
  margin-top: 20px;
  border-radius: 23px;
  left: 50%;
  transform: translateX(-50%);
  /* 旋转并保持居中 */
  z-index: 10;
}

.mengs {
  background-color: rgb(160, 70, 70, 0);
  width: 250px;
  height: 46px;
  position: absolute;
  margin-top: 86px;
  border-radius: 23px;
  left: 50%;
  transform: translateX(-50%);
  /* 旋转并保持居中 */
  z-index: 10;
}

.msglogin image {
  width: 17.5px;
  height: 17.5px;
  margin-right: 15px;
}

.msglogin {
  width: 250px;
  height: 46px;
  opacity: 1;
  border-radius: 23px;
  background: rgba(229, 229, 229, 1);
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 23.17px;
  color: rgba(56, 56, 56, 1);
  text-align: justify;
  vertical-align: top;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.ist {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 14.48px;
  color: rgba(0, 0, 0, 1);
  text-align: justify;
  vertical-align: top;
  
  margin-bottom: 60px;
}

.gous {
  width: 14px;
  height: 14px;
  border-radius: 2px;
  border: 2px solid rgba(80, 177, 178, 1);
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gous image {
  width: 11px;
  height: 8px;
}

.chas {
  position: absolute;
  width: 20px;
  height: 20px;
  top: 11px;
  right: 13px;
}

.popup-content {
  background-color: #fff;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  min-height: 254px;
  width: 100%;
}
</style>
