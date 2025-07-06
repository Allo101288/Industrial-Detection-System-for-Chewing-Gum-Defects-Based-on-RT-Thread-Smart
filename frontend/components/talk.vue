<template>
	<view class="box">
		<view class="chat" v-for="(item,index) in talkList" :key="index">
			<!-- 用户-图片 -->
			<view v-if="item.list&&item.list.length>0" class="chat-right">
				<view class="user">
					<image class="user-img"
						src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/user.png"
						mode=""></image>
				</view>
				<view class="chat-right-dialog-img">
					<u-album :urls="item.list" keyName="url"></u-album>
				</view>
			</view>
			<!-- 用户-文字 -->
			<view v-if="item.question" class="chat-right">
				<view class="user">
					<image class="user-img"
						src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/user.png"
						mode=""></image>
				</view>
				<view class="chat-right-dialog">
					{{item.question}}
				</view>
			</view>
			<!-- 机器人 -->
			<view v-if="item.answer" class="chat-left">
				<view class="jqr">
					<image class="jqr-img"
						src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/jqr.png"
						mode=""></image>
				</view>
				<view class="chat-left-dialog">
					<u-parse :content="item.answer"></u-parse>
					<!-- {{item.answer?item.answer:"暂时无法为您解答"}} -->
					<view class="yuyin-tip">
						<view class="yuyin-tip-left">AI生成仅供参考</view>
						<view class="yuyin-tip-right">
							<image v-show="!item.isDianzan"
								src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/dianzan.png"
								mode="" @click="handleOperate(index,'1')"></image>
							<image v-show="item.isDianzan"
								src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/dianzan_active.png"
								mode="" @click="handleOperate(index,'2')"></image>
							<image v-show="!item.isKuangcai"
								src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/kuangcai.png"
								mode="" @click="handleOperate(index,'3')"></image>
							<image v-show="item.isKuangcai"
								src="cloud://ai-eye-2024-0422-1f8bpcyc7ba2db2.6169-ai-eye-2024-0422-1f8bpcyc7ba2db2-1322792584/static/images/pagesIntellect/kuangcai_active.png"
								mode="" @click="handleOperate(index,'4')"></image>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		props: {
			talkList: {
				type: Array
			}
		},
		data() {
			return {}
		},
		methods: {
			// 点赞，狂踩
			handleOperate(index, val) {
				this.$emit("handleOperate", index, val)
			},
		}
	}
</script>

<style lang="scss" scoped>
	.chat {
		.chat-left {
			.jqr {
				font-weight: 500;
				font-size: 24rpx;
				color: #828FB7;
				line-height: 33rpx;
				display: flex;
				align-items: top;

				.jqr-img {
					width: 48rpx;
					height: 48rpx;
					margin-right: 15rpx;
				}
			}

			.chat-left-dialog {
				max-width: 610rpx;
				width: fit-content;
				position: relative;
				left: 60rpx;
				top: -5rpx;
				background-color: #fff;
				padding: 20px 30rpx;
				box-shadow: 3rpx 3rpx 7rpx 0rpx rgba(227, 238, 242, 0.7);
				border-radius: 0rpx 10rpx 10rpx 10rpx;
				font-size: 32rpx;
				color: #111A34;
				line-height: 54rpx;

				.yuyin-tip {
					display: flex;
					align-items: center;
					justify-content: space-between;
					margin-top: 15rpx;
					padding-top: 10rpx;
					border-top: 1rpx solid #DFE5EA;

					.yuyin-tip-left {
						font-size: 24rpx;
						color: #828FB7;
					}

					.yuyin-tip-right {
						image {
							width: 25rpx;
							height: 25rpx;
							margin: 0 10rpx;
						}
					}
				}
			}

			.chat-left-dialog:before {
				content: '';
				border: 10px solid transparent;
				border-right-color: #fff;
				/*和#notice框一致*/
				position: absolute;
				top: 0px;
				left: -5px;
				transform: rotate(-90deg);
			}
		}

		.chat-right {
			margin: 20rpx 0;
			display: flex;
			align-items: top;
			justify-content: flex-end;
			flex-wrap: wrap;

			.user {
				width: 100%;
				font-weight: 500;
				font-size: 24rpx;
				color: #828FB7;
				line-height: 33rpx;
				text-align: right;

				.user-img {
					width: 48rpx;
					height: 48rpx;
					margin-left: 15rpx;
				}
			}

			.chat-right-dialog-img {
				margin-top: -40rpx;
				margin-right: 60rpx;
				background-color: none;
				max-width: 500rpx;
				max-height: 300rpx;

				image {
					width: 100%;
					height: 100%;
					// object-fit: contain;
				}
			}

			.chat-right-dialog {
				max-width: 610rpx;
				width: fit-content;
				position: relative;
				right: 60rpx;
				top: -20rpx;
				background-color: #2593FA;
				padding: 20px 30rpx;
				box-shadow: 3rpx 3rpx 7rpx 0rpx rgba(227, 238, 242, 0.7);
				border-radius: 10rpx 0rpx 10rpx 10rpx;
				font-size: 32rpx;
				color: #fff;
				line-height: 54rpx;
			}

			.chat-right-dialog:before {
				content: '';
				border: 10px solid transparent;
				border-right-color: #2593FA;
				/*和#notice框一致*/
				position: absolute;
				top: 0px;
				right: -5px;
				transform: rotate(-90deg);
			}
		}
	}
</style>