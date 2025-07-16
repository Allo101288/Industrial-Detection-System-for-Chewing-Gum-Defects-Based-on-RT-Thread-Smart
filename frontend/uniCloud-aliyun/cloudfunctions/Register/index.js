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

	// 检查用户名是否已存在
	const userExist = await users.where({
		username: username
	}).count();

	if (userExist.total > 0) {
		return {
			code: 400,
			message: '用户名已存在'
		};
	}

	// 直接存储明文密码（仅用于演示，实际项目不推荐）
	const res = await users.add({
		username: username,
		password: password, // 明文存储
		createdAt: Date.now(),
		updatedAt: Date.now()
	});

	if (res.id) {
		return {
			code: 200,
			message: '注册成功',
			data: {
				userId: res.id
			}
		};
	} else {
		return {
			code: 500,
			message: '注册失败，请稍后重试'
		};
	}
};