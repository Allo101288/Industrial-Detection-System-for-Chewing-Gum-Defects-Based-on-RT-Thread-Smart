'use strict';
const db = uniCloud.database();
const users = db.collection('users');

exports.main = async (event, context) => {
	// 获取客户端传递的参数
	const {
		username,
		password
	} = event;

	// 参数校验
	if (!username || !password) {
		return {
			code: 400,
			message: '用户名和密码不能为空'
		};
	}

	// 直接比较明文密码（仅用于演示，实际项目不推荐）
	const userRes = await users.where({
		username: username,
		password: password // 明文比较
	}).get();

	if (userRes.data.length === 0) {
		return {
			code: 401,
			message: '用户名或密码错误'
		};
	}

	const user = userRes.data[0];

	return {
		code: 200,
		message: '登录成功',
		data: {
			userInfo: {
				userId: user._id,
				username: user.username
			}
		}
	};
};