<template>
	<view class="loginMode">
		<view class="temt">欢迎来到本小程序</view>
		<view class="ser">专业的口香糖检测系统！</view>
		<view class="meng" v-if="!gous" @tap="meng"></view>
		<view class="mengs" v-if="!gous" @tap="meng"></view>
		<view class="phonelogin">
			<image src="../static/shouji.png"></image>
			手机号快捷登录
			<button class="btnLogin" open-type="getPhoneNumber" @getphonenumber="getPhoneNumber"></button>
		</view>
		<view class="msglogin" @tap="navigate" data-url="/pkgA/msg/msg">
			<image src="../static/duanxin.png"></image>
			短信验证码登录
		</view>
		<view class="ist">
			<view class="gous" @tap="toggleGous" :style="{ background: gous ? 'rgba(88, 127, 255, 1)' : '' }">
				<image v-if="gous" src="../static/gou.png" mode=""></image>
			</view>
			我已阅读并同意用户<text style="color: rgba(88, 127, 255, 1)" @tap="navigate"
				data-url="/pkgA/service/service">服务协议</text>和
			<text @tap="navigate" data-url="/pkgA/privacy/privacy" style="color: rgba(88, 127, 255, 1)">隐私政策</text>
		</view>
		<image class="chas" @tap="hideview" src="../static/guanbi.png" mode=""></image>
	</view>
</template>

<script>
	import {
		ref
	} from "vue";
	export default {
		name: "Login",
		setup(props, {
			emit
		}) {
			// 全局API地址
			const apiUrl = "";

			// 数据状态
			const gous = ref(false);

			// 切换复选框状态
			const toggleGous = () => {
				gous.value = !gous.value;
			};

			// 隐藏登录视图
			const hideview = () => {
				emit("hideLoginView", true);
			};

			// 点击遮罩层
			const meng = () => {
				//console.log("点击遮罩层");
				uni.showToast({
					title: "请先勾选阅读协议",
					icon: "none",
				});
			};

			// 获取手机号码
			const getPhoneNumber = (e) => {
				console.log("获取手机号码:", e.detail);
				const {
					errMsg,
					encryptedData,
					iv
				} = e.detail;

				if (errMsg === "getPhoneNumber:ok") {
					wx.login({
						success: (res) => {
							if (res.code) {
								console.log({
									code: res.code,
									phoneCode: e.detail.code,
								});
								wx.request({
									url: `https://api.xydsh.cn/api/wechat/phone-login`,
									method: "POST",
									data: {
										code: res.code,
										phoneCode: e.detail.code,
									},
									header: {
										"content-type": "application/json",
									},
									success: (res) => {
										console.log("登录请求结果:", res);
										// 向父组件发送登录成功的通知

										if (res.statusCode === 200) {
											wx.showToast({
												title: "登录成功！",
											});
											//hideview();
											uni.setStorageSync("loginStatus", true);
											uni.setStorageSync("jwt", res.data.data.jwt);
											uni.setStorageSync("account", res.data.data
												.account);
											uni.setStorageSync("resumeId", res.data.data
												.resumeId);
											emit("loginSuccess", true);
											// 获取用户信息
											//getUserInfo();
										} else {
											console.error("请求失败:", res);
										}
									},
									fail: (err) => {
										console.error("请求失败:", err);
									},
								});
							} else {
								wx.showToast({
									title: "获取登录凭证失败",
									icon: "none",
								});
							}
						},
						fail: (err) => {
							wx.showToast({
								title: "获取登录凭证失败",
								icon: "none",
							});
						},
					});
				} else {
					wx.showToast({
						title: "获取手机号码失败",
						icon: "none",
					});
				}
			};

			// 跳转页面
			const navigate = (e) => {
				uni.showToast({
					title: "功能暂未开发~",
					icon: "none",
				})
				return;
				const url = e.currentTarget.dataset.url;
				wx.navigateTo({
					url: url,
				});
				hideview()
			};

			// 获取用户信息
			const getUserInfo = () => {
				// 这里可以实现获取用户信息的逻辑
			};

			return {
				gous,
				toggleGous,
				hideview,
				meng,
				getPhoneNumber,
				navigate,
			};
		},
	};
</script>

<style>
	.bg {
		display: none;
		position: absolute;
		left: 0%;
		width: 100vw;
		height: 1400px;
		background-color: black;
		z-index: 1001;
		opacity: 0.7;
	}

	.loginMode {
		width: 100vw;
		height: 260px;
		opacity: 1;
		border-top-left-radius: 12px;
		border-top-right-radius: 12px;
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
		text-align: justify;
		vertical-align: top;
		margin-top: 23px;
	}

	.ser {
		/** 文本1 */
		font-size: 12px;
		font-weight: 400;
		letter-spacing: 0px;
		line-height: 17.38px;
		color: rgba(0, 0, 0, 1);
		text-align: justify;
		vertical-align: top;
		margin-top: 8px;
	}

	.phonelogin {
		width: 250px;
		height: 46px;
		opacity: 1;
		border-radius: 23px;
		background: rgba(88, 127, 255, 1);
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
		background-color: rgba(160, 70, 70, 0);
		width: 250px;
		height: 46px;
		position: absolute;
		margin-top: 20px;
		border-radius: 23px;
		left: 50%;
		transform: translateX(-50%);
		z-index: 10;
	}

	.mengs {
		background-color: rgba(160, 70, 70, 0);
		width: 250px;
		height: 46px;
		position: absolute;
		margin-top: 86px;
		border-radius: 23px;
		left: 50%;
		transform: translateX(-50%);
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
		margin: auto;
		margin-bottom: 10px;
	}

	.gous {
		width: 14px;
		height: 14px;
		border-radius: 2px;
		border: 2px solid rgba(88, 127, 255, 1);
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
		top: 19px;
		right: 13px;
	}

	.btnLogin {
		position: absolute;
		width: 100%;
		height: 100%;
		opacity: 0;
	}
</style>