import paho.mqtt.client as mqtt
import time

# Cấu hình MQTT Broker
MQTT_BROKER = "mqtt.gtechdn.vn"  # Thay bằng địa chỉ broker của bạn
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_SUBSCRIBE = "device/control"  # Chủ đề nhận lệnh
MQTT_TOPIC_PUBLISH = "device/status"  # Chủ đề gửi trạng thái

# Biến kiểm soát kết nối
is_connected = False

def on_connect(client, userdata, flags, rc):
    global is_connected
    if rc == 0:
        print("Kết nối MQTT thành công!")
        is_connected = True
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
    else:
        print(f"Lỗi kết nối MQTT, mã lỗi: {rc}")

def on_disconnect(client, userdata, rc):
    global is_connected
    print("Mất kết nối MQTT, thử kết nối lại...")
    is_connected = False
    while not is_connected:
        try:
            client.reconnect()
            time.sleep(5)
        except Exception as e:
            print("Lỗi kết nối lại MQTT:", str(e))
            time.sleep(5)

def on_message(client, userdata, msg):
    print(f"Nhận lệnh từ MQTT: {msg.topic} - {msg.payload.decode()}")
    # Xử lý nội dung tin nhắn tại đây

# Tạo client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Kết nối MQTT Broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
except Exception as e:
    print("Lỗi kết nối MQTT:", str(e))

# Chạy vòng lặp để duy trì kết nối
client.loop_start()

# Gửi trạng thái định kỳ
while True:
    if is_connected:
        client.publish(MQTT_TOPIC_PUBLISH, "Thiết bị hoạt động bình thường")
    time.sleep(10)
