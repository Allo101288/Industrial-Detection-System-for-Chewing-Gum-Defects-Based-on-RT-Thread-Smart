import os
import ujson
import aicube
from libs.PipeLine import ScopedTiming
from libs.Utils import *
from media.sensor import *
from media.display import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import time
import network
import machine
import urequests
import socket
import _thread
import sys, ujson
from umqtt.simple import MQTTClient

# ===== 全局共享变量 & 线程控制 =====
frame_lock = _thread.allocate_lock()
status_lock = _thread.allocate_lock()
mqtt_lock = _thread.allocate_lock()
shared_jpeg    = None
has_new_frame  = False
work_state  = 0.0
# ===== 基本参数 =====
root_path = "/sdcard/mp_deployment_source/"
config_path = root_path + "deploy_config.json"
debug_mode = 1

# ===== 服务器配置 =====
SERVER_IP = "112.74.32.111"
SERVER_PORT = 8000
UPLOAD_ENDPOINT = "/upload"
DEVICE_ID = "k230_camera"
MAX_RETRIES = 3
CONNECT_TIMEOUT = 15

# ===== 图像参数 =====
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540
OUT_WIDTH = 640
OUT_HEIGH = 360
JPEG_QUALITY = 75

# ===== OneNET配置 =====
product_id = "OrT98dB198"  # 替换为实际产品ID
device_id = "lotus1"       # 替换为实际设备ID
mqtt_server = "183.230.40.96"  # OneNET非SSL服务器地址[2](@ref)
mqtt_port = 1883               # 推荐使用6002端口[2](@ref)
mqtt_password = "version=2018-10-31&res=products%2FOrT98dB198%2Fdevices%2Flotus1&et=1917513743&method=md5&sign=rski44rCWDk0cXSVrbJOWg%3D%3D"  # 替换为实际Token
ONENET_PROP_FORMAT = "{\"id\":\"%u\", \"version\":\"1.0\", \"params\":%s}"  # 设备属性格式模板
# =====MQTT主题 =====
ONENET_TOPIC_PROP_SET = f"$sys/{product_id}/{device_id}/thing/property/set"
ONENET_TOPIC_PROP_POST = f"$sys/{product_id}/{device_id}/thing/property/post"  # 设备属性上报请求
ONENET_TOPIC_PROP_POST_REPLY = f"$sys/{product_id}/{device_id}/thing/property/post/reply"  # 设备属性上报响应
ONENET_TOPIC_PROP_SET_REPLY = f"$sys/{product_id}/{device_id}/thing/property/set_reply"  # 设备属性设置响应
def align_to_8(x):
    """
    将给定整数 x 向下对齐到 8 的倍数。
    """
    return (x // 8) * 8

def read_img(img_data_rgb888):
    """
    将 RGB888 格式图像转换为 (C, H, W) numpy 数组。
    """
    img_hwc=img_data_rgb888.to_numpy_ref()
    shape=img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res=img_tmp_trans.copy()
    img_return=img_res.reshape((shape[2],shape[0],shape[1]))
    return img_return

def read_deploy_config(path):
    """
    从 JSON 文件读取部署配置。
    """
    with open(path, 'r') as f:
        return ujson.load(f)

def two_side_pad_param(input_size, output_size):
    """
    计算双边填充及缩放比例，保持长宽比。
    """
    ratio = min(output_size[0] / input_size[0], output_size[1] / input_size[1])
    new_w = int(ratio * input_size[0])
    new_h = int(ratio * input_size[1])
    dw = (output_size[0] - new_w) / 2
    dh = (output_size[1] - new_h) / 2
    top = int(round(dh - 0.1))
    bottom = int(round(dh + 0.1))
    left = int(round(dw - 0.1))
    right = int(round(dw - 0.1))
    return top, bottom, left, right, ratio

def connect_ethernet():
    """
    启动并等待 LAN 接口获取 IP。
    """
    print("\n====== 有线网络连接 ======")
    try:
        lan = network.LAN(0)
        lan.active(True)
        print("激活有线网络接口...")
        timeout = 15
        while timeout > 0:
            ip_info = lan.ifconfig()
            if ip_info[0] != '0.0.0.0':
                print(f"✓ 网络连接成功! IP: {ip_info[0]}")
                print(f"网关: {ip_info[2]}, DNS: {ip_info[3]}")
                return True
            time.sleep(1)
            timeout -= 1
            print(f"等待网络连接...剩余{timeout}秒")
        print("✗ 网络连接超时")
        return False
    except Exception as e:
        print(f"✗ 网络连接异常: {e}")
        return False

def test_server_connection():
    """
    GET /test 确认服务器可达。
    """
    print("\n====== 服务器连接测试 ======")
    try:
        url = "http://" + SERVER_IP + ":" + str(SERVER_PORT) + "/test"
        resp = urequests.get(url, timeout=5)
        print("状态码:", resp.status_code,"\n")
        resp.close()
        return True
    except Exception as e:
        print("测试失败:", e)
        return False

def generate_boundary():
    """
    生成唯一的 multipart boundary。
    """
    # 使用 time.ticks_ms() 取低位确保唯一
    return "k230_%06d" % (time.ticks_ms() % 1000000)

def compress_image(img):
    """
    将图像压缩为 JPEG 并返回 bytearray。
    """
    try:
        return bytearray(img.compress(quality=JPEG_QUALITY))
    except Exception as e:
        print("✗ 压缩失败:", e)
        return None

def socket_upload(fracture_num, image_data, boundary):
    """
    通过 socket 发起 HTTP multipart 上传，携带缺陷数量。
    """
    gc.collect()
    try:
        print(f"尝试连接到 {SERVER_IP}:{SERVER_PORT}")
        addr_info = socket.getaddrinfo(SERVER_IP, SERVER_PORT)
        if not addr_info:
            print("✗ 无法解析服务器地址")
            return None, None
        _, _, _, _, addr = addr_info[0]
        ip_addr, port = addr[0], addr[1]
        s = socket.socket()
        s.settimeout(CONNECT_TIMEOUT)
        s.connect((ip_addr, port))
        print(f"成功连接到 {ip_addr}:{port}")

        # 转成 bytearray
        buf = bytearray(image_data)

        # 构造 multipart 数据体
        multipart_header = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="image"; filename="img.jpg"\r\n'
            "Content-Type: application/octet-stream\r\n\r\n"
        )
        multipart_footer = f"\r\n--{boundary}--\r\n"
        body_len = len(multipart_header) + len(buf) + len(multipart_footer)

        # 请求行
        request_line = f"POST {UPLOAD_ENDPOINT} HTTP/1.1\r\n"

        # 头信息（每行逐个拼接）
        headers = ""
        headers += "Host: {}:{}\r\n".format(SERVER_IP, SERVER_PORT)
        headers += "Device-ID: {}\r\n".format(DEVICE_ID)
        headers += "X-Defect-Count: {}\r\n".format(fracture_num)  # ← 加入缺陷数
        headers += "Content-Type: multipart/form-data; boundary={}\r\n".format(boundary)
        headers += "Content-Length: {}\r\n".format(body_len)
        headers += "Connection: close\r\n\r\n"

        # 发送请求行与头部
        print(f"发送请求头 ({len(request_line) + len(headers)} 字节)")
        s.sendall(request_line.encode() + headers.encode())

        # 发送 multipart 部分
        print(f"发送 multipart 头 ({len(multipart_header)} 字节)")
        s.sendall(multipart_header.encode())

        print(f"分块发送图片数据 ({len(buf)} 字节)")
        for i in range(0, len(buf), 4096):
            chunk = buf[i:i+4096]
            s.sendall(chunk)
            time.sleep_ms(10)

        print(f"发送结束边界 ({len(multipart_footer)} 字节)")
        s.sendall(multipart_footer.encode())

        print("等待服务器响应...")
        response = s.recv(1024)
        s.close()

        del addr_info, buf, multipart_header, multipart_footer
        gc.collect()

        if response:
            response_str = response.decode('utf-8', 'ignore')
            if "HTTP/1." in response_str:
                status_code = int(response_str.split(' ')[1])
                return status_code, response_str
            return None, f"Invalid response: {response_str[:100]}"
        return None, "无响应"

    except Exception as e:
        print(f"✗ Socket上传失败: {e}")
        return None, str(e)


def upload_image(data, fracture_num):
    """
    重试上传，直到成功或次数用尽。
    """
    gc.collect()
    print("\n====== 图像上传 ======")
    for attempt in range(MAX_RETRIES):
        print(f"上传尝试 #{attempt+1}/{MAX_RETRIES}")
        boundary = generate_boundary()
        print(f"使用边界: {boundary}")
        status, resp = socket_upload(fracture_num, data, boundary)
        del data
        if status is not None:
            print(f"HTTP状态码: {status}")
            if status == 200:
                print("✓ 图像上传成功")
                print(f"服务器响应: {resp[:100]}...")
                return True
            else:
                print(f"! 服务器返回错误: {status}")
                print(f"响应内容: {resp}")
        else:
            print("! 上传失败: 无效服务器响应")
            print(f"详情: {resp}")
        gc.collect()
#        time.sleep(attempt * 2 + 1)
    print("✗ 所有上传尝试均失败")
    return False

def on_message(topic, msg):
    """
    MQTT消息回调 - 增加错误处理
    """
    try:
        topic_str = topic.decode('utf-8')
        msg_str = msg.decode('utf-8')
        print(f"\n收到消息 - 主题: {topic_str}\n内容: {msg_str}")
        # 处理设置请求
        if topic_str == ONENET_TOPIC_PROP_SET:
            try:
                data = ujson.loads(msg_str)
                msg_id = data.get('id', 0)
                response_code = 200
                response_msg = "success"

                if "params" in data and "level" in data["params"]:
                    new_level = float(data["params"]["level"])
                    print(f"接收level值: {new_level}")

                    if new_level == 0.0:
                        print("关闭")
                        result = stop()
                        print(f"work_status:{work_status}")
                        if not result:
                            response_code = 500
                            response_msg = "Failed to stop "
                    elif new_level == 1.0:
                        print("开启")
                        result = start()
                        print(f"work_status:{work_status}")
                        if not result:
                            response_code = 500
                            response_msg = "Failed to start "
                    elif new_level == 2.0:
                        print("暂停")
                        result = pause()
                        print(f"work_status:{work_status}")
                        if not result:
                            response_code = 500
                            response_msg = "Failed to pause "
                    else:
                        print(f"无效level值: {new_level}")
                        response_code = 400
                        response_msg = "Invalid level value"
                    # 发送响应
                    response = {"id": msg_id, "code": response_code, "msg": response_msg}
                    mqtt_client.publish(
                        f"$sys/{product_id}/{device_id}/thing/property/set_reply",
                        ujson.dumps(response)
                    )
                    print(f"已回复设置响应")
            except Exception as e:
                print(f"解析设置请求失败: {e}")

        elif topic_str == ONENET_TOPIC_PROP_POST_REPLY:
            try:

                print(f"OneNET确认收到数据上传: {msg_str}")
            except Exception as e:
                print(f"处理消息时出错: {e}")
    except Exception as e:
        print(f"处理消息时出错: {e}")


# MQTT连接 - 重构连接逻辑[2,6](@ref)
def connect_mqtt():
    """
    MQTT连接函数
    """
    global mqtt_server, mqtt_port

    try:
        print(f"尝试连接MQTT: {mqtt_server}:{mqtt_port}")
        client = MQTTClient(
            client_id = device_id,
            server= mqtt_server,
            port = mqtt_port,
            user = product_id,
            password = mqtt_password,
            keepalive = 120,  # 增加心跳间隔[2](@ref)
            ssl = (mqtt_port == 8883)  # 启用SSL仅对8883端口
        )

        # 设置协议版本为3.1.1[2](@ref)
        client.set_callback(on_message)
        client.connect()
        print(f"MQTT连接成功! 服务器: {mqtt_server}:{mqtt_port}")

        # 订阅必要主题
        print(f"订阅: {ONENET_TOPIC_PROP_SET}")
        client.subscribe(ONENET_TOPIC_PROP_SET)
        print("2")
        print(f"订阅主题: {ONENET_TOPIC_PROP_POST_REPLY}")
        client.subscribe(ONENET_TOPIC_PROP_POST_REPLY)
        print("1")
        return client

    except Exception as e:
        print(f"连接失败: {e}")

    print("所有服务器连接尝试均失败")
    return None

def hardware_reboot():
    """
    延迟后复位。
    """
    time.sleep(3)
    machine.reset()

def AI_detect():
    """
    捕获、推理、绘框并返回 JPEG 数据。
    """
    global ai2d_builder, ai2d_output_tensor, kpu, frame_size, strides
    global num_classes, confidence_threshold, nms_threshold, anchors, kmodel_frame_size
    global labels, nms_option
    gc.collect()
    data = np.ones((1,3,kmodel_frame_size[1],kmodel_frame_size[0]),dtype=np.uint8)
    ai2d_output_tensor = nn.from_numpy(data)
    img = sensor.snapshot(chn=CAM_CHN_ID_2)
    if img.format() != image.RGB888:
        return None

    inp = read_img(img)
    ai2d_builder.run(nn.from_numpy(inp), ai2d_output_tensor)
    kpu.set_input_tensor(0, ai2d_output_tensor)
    kpu.run()
    outs = []
    for i in range(kpu.outputs_size()):
        out_data = kpu.get_output_tensor(i)
        out = out_data.to_numpy()
        out = out.reshape((out.shape[0]*out.shape[1]*out.shape[2]*out.shape[3]))
        del out_data
        outs.append(out)
    dets = aicube.anchorbasedet_post_process(
        outs[0], outs[1], outs[2],
        kmodel_frame_size, frame_size,
        strides, num_classes,
        confidence_threshold, nms_threshold,
        anchors, nms_option
    )
    draw = img.copy()
    fracture_num = 0
    if dets:
        for d in dets:
            cls, _, x1,y1,x2,y2 = d
            x = int(x1); y = int(y1)
            w = int(x2 - x1); h = int(y2 - y1)
            if labels[cls] == "normal":
                color = (0,255,0); txt = "正常"
            else:
                color = (255,0,0); txt = "缺肉"
                fracture_num+=1
            draw.draw_rectangle(x, y, w, h, color=color)
            draw.draw_string_advanced(x, y, 16, txt, color=color)
    del outs, img
    gc.collect()
    if fracture_num:
        return compress_image(draw), fracture_num
    else:
        return None

def start():
    """
    开始工作函数
    """
    global sensor, work_status

    try:
        sensor.reset()
        sensor.run()
        osd_img.clear()
        osd_img.draw_string_advanced(0, 0, 32, "检测已开始", color = (255,0,0))
        Display.show_image(osd_img, 0, 0, Display.LAYER_OSD3)
        with status_lock:
            work_status = True
        print("已启动！")
        return True
    except Exception as e:
        print(f"启动失败: {e}")
        return False

def stop():
    """
    停止工作函数
    """
    global sensor, work_status
    with frame_lock:
        has_new_frame = False
    with status_lock:
        work_status = False
    osd_img.clear()
    osd_img.draw_string_advanced(0, 0, 32, "检测未开始", color = (255,0,0))
    Display.show_image(osd_img, 0, 0, Display.LAYER_OSD3)
    sensor.reset()
    sensor.stop()
    gc.collect()
    print("已停止！")
#    hardware_reboot()

def pause():
    """
    暂停工作函数
    """
    global sensor, work_status
    if sensor is None:
        return False

    try:
        with frame_lock:
            has_new_frame = False
        with status_lock:
            work_status = False
        osd_img.clear()
        osd_img.draw_string_advanced(0, 0, 32, "检测已暂停", color = (255,0,0))
        Display.show_image(osd_img, 0, 0, Display.LAYER_OSD3)
        print("已暂停！")
        return True
    except Exception as e:
        print(f"暂停失败: {e}")
        return False

def detect_thread():
    """
    AI检测线程：检测图片是否有缺陷
    """
    global shared_jpeg, has_new_frame, work_status
    print("检测线程已启动")
    while True:
        with status_lock:
            running = work_status
        if running:
            buf = AI_detect()
            if buf:
                with frame_lock:
                    shared_jpeg   = buf
                    has_new_frame = True
            else:
                print(f"[Detect] Frame is normal")

def upload_thread():
    """
    上传线程：将图片和数量上传到服务器
    """
    global shared_jpeg, has_new_frame, work_status
    print("上传线程已启动")
    while True:
        with status_lock:
            running = work_status
        if running:
            with frame_lock:
                if has_new_frame:
                    buf, num = shared_jpeg
                    has_new_frame = False
                    do_upload = True
                else:
                    do_upload = False
            if do_upload:
                success = upload_image(buf, num)
                if not success:
                    print("[Upload] 图片与数量上传失败或重试")
                del buf
                gc.collect()

def publish_work_state_data(client, data, msg_id):
    """上传工作状态数据到OneNET平台 - 使用属性格式"""
    try:
        # 构造属性参数
        params = ujson.dumps({"work_state": {"value": round(data, 1)}})
        # 格式化完整JSON
        json_payload = ONENET_PROP_FORMAT % (msg_id, params)

        # 发布到OneNET
        client.publish(ONENET_TOPIC_PROP_POST, json_payload)
        print(f"已上传设备状态: {'开启' if data == 1.0 else '关闭'} (消息ID: {msg_id})")
        print(f"Payload: {json_payload}")
        return True
    except Exception as e:
        print(f"数据上传失败: {e}")
        return False

def main():
    """
    程序入口：初始化、网络检测，然后循环推理+上传。
    """
    conf = read_deploy_config(config_path)
    # 声明全局变量
    global labels, confidence_threshold, nms_threshold, num_classes
    global anchors, kmodel_frame_size, frame_size, strides, nms_option, osd_img
    global ai2d_builder, ai2d_output_tensor, kpu, sensor, mqtt_client, work_status

    # 使用json读取内容初始化部署变量
    deploy_conf=read_deploy_config(config_path)
    kmodel_name=deploy_conf["kmodel_path"]
    labels=deploy_conf["categories"]
    confidence_threshold= deploy_conf["confidence_threshold"]
    nms_threshold = deploy_conf["nms_threshold"]
    img_size=deploy_conf["img_size"]
    num_classes=deploy_conf["num_classes"]
    color_four=get_colors(num_classes)
    nms_option = deploy_conf["nms_option"]
    model_type = deploy_conf["model_type"]
    if model_type == "AnchorBaseDet":
        anchors = deploy_conf["anchors"][0] + deploy_conf["anchors"][1] + deploy_conf["anchors"][2]
    kmodel_frame_size = img_size
    frame_size = [OUT_WIDTH,OUT_HEIGH]
    strides = [8,16,32]

    # 计算padding值
    top, bottom, left, right,ratio=two_side_pad_param(frame_size,kmodel_frame_size)

    # 初始化kpu
    kpu = nn.kpu()
    kpu.load_kmodel(root_path+kmodel_name)

    # 初始化ai2d
    ai2d = nn.ai2d()
    ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)
    ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
    ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
    ai2d_builder = ai2d.build([1,3,OUT_HEIGH,OUT_WIDTH], [1,3,kmodel_frame_size[1],kmodel_frame_size[0]])

    try:
        # 初始化 sensor 和 Display
        sensor = Sensor(); sensor.reset()
        # 设置镜像
        sensor.set_hmirror(False)
        # 设置翻转
        sensor.set_vflip(False)
        sensor.set_framesize(width=DISPLAY_WIDTH, height=align_to_8(DISPLAY_HEIGHT))
        sensor.set_pixformat(Sensor.YUV420SP)
        sensor.set_framesize(width=OUT_WIDTH, height=OUT_HEIGH, chn=CAM_CHN_ID_2)
        sensor.set_pixformat(Sensor.RGB888, chn=CAM_CHN_ID_2)
        cfg = sensor.bind_info(x=0,y=0,chn=CAM_CHN_ID_0)
        Display.bind_layer(**cfg, layer=Display.LAYER_VIDEO1)
        Display.init(Display.NT35516, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
        osd_img = image.Image(DISPLAY_WIDTH, align_to_8(DISPLAY_HEIGHT), image.ARGB8888)
        MediaManager.init()
        osd_img.clear()
        osd_img.draw_string_advanced(0, 0, 32, "检测未开始", color = (255,0,0))
        Display.show_image(osd_img, 0, 0, Display.LAYER_OSD3)
        work_state = 1.0
        print("初始化成功！")
    except Exception as e:
        print(f"初始化失败: {e}")
        hardware_reboot()

    work_status = False

    # 网络检测
    if not connect_ethernet():
        hardware_reboot()

    if not test_server_connection():
        hardware_reboot()

    mqtt_client = connect_mqtt()
    if not mqtt_client:
        hardware_reboot()
        raise Exception("MQTT连接失败")
    success = publish_work_state_data(mqtt_client, work_state, 1)

    # 启动检测和上传线程
    _thread.start_new_thread(detect_thread, ())
    _thread.start_new_thread(upload_thread, ())

    mqtt_last_ping = time.time()
    mqtt_ping_interval = 30
    message_id = 1  # 消息ID计数器
    try:
        while True:
            mqtt_current_time = time.time()
            if mqtt_current_time - mqtt_last_ping >= mqtt_ping_interval:
                try:
                    with mqtt_lock:
                        if mqtt_client:
                            mqtt_client.ping()
                            print("✓ MQTT心跳已发送")

                    mqtt_last_ping = mqtt_current_time
                except Exception as e:
                    print(f"✗ 发送心跳失败: {e}")
                    # 尝试重连
                    try:
                        with mqtt_lock:
                            if mqtt_client:
                                mqtt_client.disconnect()
                        print("尝试重新连接MQTT...")
                        mqtt_client = connect_mqtt()
                        if mqtt_client:
                            last_ping_time = current_time
                            print("✓ MQTT重连成功")
                        else:
                            print("✗ MQTT重连失败")
                    except Exception as reconnect_e:
                        print(f"重连失败: {reconnect_e}")

            # 检查MQTT消息
            with mqtt_lock:
                if mqtt_client:
                    mqtt_client.check_msg()

            gc.collect()
    except Exception as e:
        print("\n=== 收到停止信号，开始清理资源 ===")
        work_state = 0.0
        with status_lock:
            work_status = False

        if mqtt_client:
            success = publish_work_state_data(mqtt_client, work_state, 1)

            print("关闭MQTT连接...")
            try:
                with mqtt_lock:
                    mqtt_client.disconnect()
                    mqtt_client = None
            except Exception as e:
                print(f"MQTT关闭异常: {e}")


        print("释放显示资源...")
        try:
            Display.deinit()
        except Exception as e:
            print(f"显示释放异常: {e}")

        print("释放媒体资源...")
        try:
            MediaManager.deinit()
        except Exception as e:
            print(f"媒体释放异常: {e}")

        print("释放AI资源...")
        try:
            kpu = None
            nn.shrink_memory_pool()
        except Exception as e:
            print(f"AI资源释放异常: {e}")

        print("执行最终垃圾回收...")
        gc.collect()
        time.sleep(1)

        print("=== 资源清理完成，安全退出 ===")
#        hardware_reboot()

if __name__ == "__main__":
    main()
