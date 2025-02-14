import paho.mqtt.client as mqtt
import time

# Thông tin kết nối MQTT
domainMqtt = "mqtt.gtechdn.vn"  # Địa chỉ broker MQTT (thay bằng địa chỉ thực tế)
portMqtt = 1883  # Cổng MQTT (thường là 1883 cho MQTT không mã hóa)
id = "646ada9d1f271419db8b124e"  # ID thiết bị (thay bằng ID thực tế của bạn)
username = "mqtt"  # Tên đăng nhập MQTT
password = "adminmqtt"  # Mật khẩu MQTT

# Biến trạng thái kết nối
client = mqtt.Client()  # Khởi tạo MQTT Client với ID thiết bị
client.username_pw_set(username, password)  # Thiết lập user và password
client.retry_count = 0  # Số lần thử kết nối
client.connected_flag = False  # Cờ kết nối

# Hàm callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối thành công tới broker")
        client.connected_flag = True  # Đánh dấu kết nối thành công
    else:
        print("Kết nối thất bại. Mã lỗi:", rc)

# Hàm callback khi mất kết nối
def on_disconnect(client, userdata, rc):
    print("Mất kết nối. Mã lỗi:", rc)

# Hàm callback khi nhận tin nhắn
def on_message(client, userdata, msg):
    print("Nhận tin nhắn từ chủ đề:", msg.topic)
    print("Nội dung tin nhắn:", msg.payload.decode())

# Đăng ký các callback
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Lệnh "will" để gửi thông báo nếu thiết bị mất kết nối
client.will_set("device/offline", payload=id, qos=1, retain=False)

# Thử kết nối tới broker MQTT tối đa 3 lần
while not client.connected_flag and client.retry_count < 3:
    try:
        print(f"Đang kết nối tới broker {domainMqtt} với user: {username}")
        client.connect(domainMqtt, portMqtt, 60)  # Kết nối tới broker
        break  # Nếu kết nối thành công, thoát vòng lặp
    except Exception as e:
        print("Kết nối không thành công, thử lại:", e)
        client.retry_count += 1
        if client.retry_count == 3:
            print("Không thể kết nối tới broker sau 3 lần thử")
            break
        time.sleep(5)  # Chờ 5 giây trước khi thử lại

# Nếu kết nối thành công, bắt đầu vòng lặp để nhận tin nhắn
if client.connected_flag:
    client.loop_start()  # Bắt đầu lắng nghe MQTT

    # Đăng ký chủ đề cần theo dõi
    client.subscribe("device/status")  # Thay "device/status" bằng chủ đề thực tế

    # Vòng lặp chính để duy trì kết nối
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ngừng chương trình")
        client.loop_stop()  # Dừng vòng lặp MQTT

# Đóng kết nối MQTT khi chương trình kết thúc
client.disconnect()
