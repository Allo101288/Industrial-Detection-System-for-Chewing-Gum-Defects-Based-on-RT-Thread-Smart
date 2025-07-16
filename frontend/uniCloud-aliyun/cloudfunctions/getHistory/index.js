'use strict';
const db = uniCloud.database();
const historyCollection = db.collection('history-records');

exports.main = async (event, context) => {
	try {
		// 直接获取所有记录，按开始时间降序排列
		const res = await historyCollection
			.orderBy('startTime', 'desc')
			.get();

		return {
			code: 200,
			message: '获取成功',
			data: res.data
		};
	} catch (e) {
		return {
			code: 500,
			message: '服务器错误',
			error: e.message
		};
	}
};