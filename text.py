import paho.mqtt.client as mqtt
import time
import uuid

# Thông tin MQTT
domainMqtt = "mqtt.gtechdn.vn"
portMqtt = 1883
username = "mqtt"
password = "your_password"
client_id = f"device-{uuid.uuid4().hex[:6]}"  # Client ID ngẫu nhiên tránh trùng lặp

# Tạo client
client = mqtt.Client(client_id=client_id)
client.username_pw_set(username, password)

# Callback khi kết nối
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Kết nối thành công tới {domainMqtt} với Client ID: {client_id}")
        client.subscribe("device/status")
    else:
        print(f"Lỗi kết nối, mã lỗi: {rc}")

# Callback khi mất kết nối
def on_disconnect(client, userdata, rc):
    print(f"Mất kết nối. Mã lỗi: {rc}")
    if rc != 0:
        print("Thử kết nối lại sau 5 giây...")
        time.sleep(5)
        try_reconnect(client)

# Hàm thử kết nối lại
def try_reconnect(client):
    for i in range(3):
        try:
            print(f"Thử kết nối lại ({i+1}/3)...")
            client.reconnect()
            return
        except Exception as e:
            print(f"Lỗi kết nối lại: {e}")
        time.sleep(5)
    print("Không thể kết nối lại, dừng chương trình.")

# Callback khi nhận tin nhắn
def on_message(client, userdata, msg):
    print(f"Nhận tin nhắn từ {msg.topic}: {msg.payload.decode()}")

# Gán callback
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Kết nối
try:
    print(f"Đang kết nối tới broker {domainMqtt} với user: {username}")
    client.connect(domainMqtt, portMqtt, 60)
except Exception as e:
    print(f"Lỗi kết nối ban đầu: {e}")
    exit()

# Bắt đầu vòng lặp
client.loop_forever()
