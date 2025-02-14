from paho.mqtt import client as mqtt  # type: ignore

led_status = 123

port = 8883  # Cổng TLS
# port = 1883  # Cổng TLS
broker = "ca99add77b634afe8e68917f0339aec6.s1.eu.hivemq.cloud"
broker = "mqtt.gtechdn.vn"
username = "mqtt"
password = "adminmqtt"

topic = "gtechdn/sohoa_pc"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Kết nối thành công tới MQTT Broker!")
        client.subscribe(topic, qos=1)
    else:
        print(f"⚠ Kết nối thất bại, mã lỗi: {rc}")

def on_message(client, userdata, msg):
    print(f"📩 Nhận tin nhắn: {msg.topic} → {msg.payload.decode()}")

# Tạo MQTT client
client = mqtt.Client()  # Dùng phiên bản callback API 1

# Thiết lập username & password
client.username_pw_set(username, password)


# Kích hoạt TLS (SSL) để kết nối an toàn
client.tls_set(cert_reqs=mqtt.ssl.CERT_NONE)  # Không kiểm tra chứng chỉ


# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

# Kết nối tới broker
try:
    client.connect(broker, port,60)
    print("🔗 Đang kết nối tới broker...")
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
    exit(1)

# Gửi trạng thái LED
client.publish(topic, str(led_status), qos=1)
print(f"📤 Đã gửi tin nhắn: {led_status}")

# Duy trì kết nối để nhận tin nhắn
client.loop_forever()
