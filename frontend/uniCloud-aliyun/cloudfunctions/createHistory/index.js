'use strict';
const db = uniCloud.database();
const historyCollection = db.collection('history-records');

exports.main = async (event, context) => {
	// 验证必要参数
	if (!event.userId || !event.userName || !event.startTime) {
		return {
			code: 400,
			message: '缺少必要参数: userId, userName 或 startTime'
		};
	}

	try {
		// 自动生成ID和默认值
		const newRecord = {
			userId: event.userId,
			userName: event.userName,
			startTime: event.startTime,
			endTime: event.endTime || null,
			defectCount: event.defectCount || 0,
			accuracy: event.accuracy || 0,
			status: event.status || 'running',
			createdAt: new Date().getTime()
		};

		// 插入数据库
		const res = await historyCollection.add(newRecord);

		return {
			code: 200,
			message: '记录添加成功',
			data: {
				id: res.id,
				...newRecord
			}
		};
	} catch (e) {
		return {
			code: 500,
			message: '服务器错误',
			error: e.message
		};
	}
};