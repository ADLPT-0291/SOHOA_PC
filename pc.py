import paho.mqtt.client as mqtt
import time
import threading
import khaibao
import socket

# Cấu hình MQTT Broker
MQTT_BROKER = "mqtt.gtechdn.vn"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_SUBSCRIBE = "device/control"
MQTT_TOPIC_PUBLISH = "device/status"

# Biến kiểm soát kết nối
is_connected = False


######## khai bao dia chi mqtt #####
id = khaibao.id
updatecode = khaibao.updatecode
trangthaiketnoi = khaibao.trangthaiketnoi
trangthaiplay = khaibao.trangthaiplay
trangthaivolume = khaibao.trangthaivolume
xacnhanketnoi = khaibao.xacnhanketnoi
dieukhienvolume = khaibao.dieukhienvolume
dieukhienplay = khaibao.dieukhienplay
yeucauguidulieu = khaibao.yeucauguidulieu
reset = khaibao.reset

####################################
phienban = "V1.0.0"


######### get dia chi ip ###################
def get_ip_address():
 ip_address = ''
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def on_connect(client, userdata, flags, rc):
    """Hàm xử lý khi kết nối thành công"""
    global is_connected, demLoicallApiPing, yeucauguidulieu, updatecode, dieukhienvolume, dieukhienplay, maxacthuc, chedoRetartModul3g, demRestartModul3g, demLoicallApiPing
    if rc == 0:
        print("✅ Kết nối MQTT thành công!")
        is_connected = True
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
        demLoicallApiPing = 0
        client.subscribe(dieukhienvolume) 
        client.subscribe(updatecode)
        client.subscribe(dieukhienplay)
        client.subscribe(yeucauguidulieu)
        client.subscribe(reset)
        client.connected_flag=True
        """ call API xac nhan ket noi """
       # ip = requests.get('https://api.ipify.org').text
        dataXacnhanketnoi = {
          'xacnhanketnoi': xacnhanketnoi,
          'ip': get_ip_address(),
          'phienban': phienban,   
        }
    else:
        print(f"⚠️ Lỗi kết nối MQTT, mã lỗi: {rc}")

def on_disconnect(client, userdata, rc):
    """Hàm xử lý khi mất kết nối"""
    global is_connected
    is_connected = False
    print("🔴 Mất kết nối MQTT. Đang thử kết nối lại...")
    while not is_connected:
        try:
            client.reconnect()
            time.sleep(5)  # Chờ trước khi thử lại
        except Exception as e:
            print("❌ Lỗi kết nối lại MQTT:", str(e))
            time.sleep(5)

def on_message(client, userdata, msg):
    """Hàm xử lý khi nhận được tin nhắn"""
    print(f"📩 Nhận lệnh từ MQTT: {msg.topic} - {msg.payload.decode()}")

def publish_status():
    """Hàm gửi trạng thái thiết bị định kỳ"""
    while True:
        if is_connected:
            client.publish(MQTT_TOPIC_PUBLISH, "Thiết bị hoạt động bình thường")
        time.sleep(10)  # Gửi mỗi 10 giây

# Tạo client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Kết nối MQTT Broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
except Exception as e:
    print("❌ Lỗi kết nối MQTT:", str(e))
    exit(1)

# Chạy luồng gửi trạng thái riêng để không chặn luồng chính
status_thread = threading.Thread(target=publish_status, daemon=True)
status_thread.start()

# Chạy vòng lặp chính để duy trì kết nối MQTT
client.loop_forever()
