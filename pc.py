import paho.mqtt.client as mqtt
import time
import url


######### khai bao domain ##########
domainMqtt = url.domainMqtt
portMqtt = url.portMqtt
domainXacnhanketnoi = url.domainXacnhanketnoi
domainLogbantin = url.domainLogbantin
domainPing = url.domainPing
domainXacnhanketnoilai = url.domainXacnhanketnoilai
domainStartStream = url.domainStartStream
# Thông tin về broker MQTT
# domainMqtt = "mqtt.example.com"  # Địa chỉ broker MQTT (thay bằng địa chỉ thực tế)
# portMqtt = 1883  # Cổng kết nối MQTT (thường là 1883 cho MQTT không mã hóa)
id = "646ada9d1f271419db8b124e"  # ID thiết bị (thay bằng ID thực tế của bạn)

# Biến trạng thái kết nối
client = mqtt.Client()  # Khởi tạo MQTT Client
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

# Đăng ký các callback cho client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Lệnh "will" để gửi thông báo nếu thiết bị mất kết nối
client.will_set("device/offline", payload=id, qos=1, retain=False)

# Thử kết nối tới broker MQTT tối đa 3 lần
while not client.connected_flag and client.retry_count < 3:
    try:
        print("Đang kết nối tới broker:", domainMqtt)
        client.connect(domainMqtt, portMqtt, 60)  # Kết nối tới broker
        break  # Nếu kết nối thành công, thoát khỏi vòng lặp
    except Exception as e:
        print("Kết nối không thành công, thử lại:", e)
        client.retry_count += 1
        if client.retry_count == 3:
            print("Không thể kết nối tới broker sau 3 lần thử")
            break  # Nếu thử 3 lần mà không thành công, thoát vòng lặp
        time.sleep(5)  # Chờ 5 giây trước khi thử lại

# Nếu kết nối thành công, bắt đầu vòng lặp để nhận tin nhắn
if client.connected_flag:
    client.loop_start()  # Bắt đầu lắng nghe các sự kiện MQTT

    # Đăng ký chủ đề cần theo dõi
    client.subscribe("device/status")  # Thay "device/status" bằng chủ đề bạn muốn theo dõi

    # Chạy vòng lặp chính, tiếp tục lắng nghe và xử lý tin nhắn
    try:
        while True:
            time.sleep(1)  # Duy trì vòng lặp
    except KeyboardInterrupt:
        print("Ngừng chương trình")
        client.loop_stop()  # Dừng vòng lặp khi có sự ngắt quãng từ người dùng

# Đóng kết nối MQTT khi chương trình kết thúc
client.disconnect()
