import paho.mqtt.client as mqtt
import time
import threading
import khaibao
import subprocess
import socket
import requests
import url
import configparser
import alsaaudio
import os
import signal

# Cấu hình MQTT Broker
MQTT_TOPIC_SUBSCRIBE = "device/control"
MQTT_TOPIC_PUBLISH = "device/status"

# Biến kiểm soát kết nối
is_connected = False


######### khai bao domain ##########
domainMqtt = url.domainMqtt
portMqtt = url.portMqtt
domainXacnhanketnoi = url.domainXacnhanketnoi
domainLogbantin = url.domainLogbantin
domainPing = url.domainPing
domainXacnhanketnoilai = url.domainXacnhanketnoilai
domainStartStream = url.domainStartStream

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


# Khởi tạo giờ, phút, giây ban đầu là 0
REMOTE_SERVER = "8.8.8.8"
hour = 0
minute = 0
second = 0
darkice_process = ''
darkice_cmd = ['darkice', '-c', '/etc/darkice.cfg']
# Đường dẫn đến tệp cấu hình của Darkice
CONFIG_FILE = "/etc/darkice.cfg"
# Tạo đối tượng ConfigParser
config = configparser.ConfigParser()
config.optionxform = lambda option: option


################# ham dieu khien volume ####################
def setVolume(volume):
  # Khởi tạo mixer
#   mixer = alsaaudio.Mixer('Mic1 Boost', cardindex=0)
  print("oke đã qua hàm này")
  # Đặt âm lượng
#   mixer.setvolume(int(volume))
#   current_volume = mixer.getvolume()[0]

def start_darkice():   
    global trangthaiplay, led_status,playStream
    # start darkice stream
    subprocess.Popen(['sudo darkice'])
    time.sleep(1)
    # if get_darkice_status_ping():
    #   playStream = 1
    #   showStream.start()
    #   time.sleep(0.5) 
    #   countTime.start()
    #   client.publish(trangthaiplay,"play")


def stop_darkice():
    global last_start, playStream, trangthaiplay, led_status, second, minute, hour, start_time_str
    # stop darkice stream
    playStream = 0
    client.publish(trangthaiplay,"stop")
    # countTime.stop()
    # last_start = False
    # time.sleep(0.5) 
    # start_time_str = ''
    # second = 0
    # minute = 0
    # hour = 0
    # for proc in subprocess.Popen(['pgrep', '-f', 'darkice'], stdout=subprocess.PIPE).stdout:
    #     pid = int(proc.decode())
    #     os.kill(pid, signal.SIGTERM)



############# ham call api xac nhan ket noi #################
def api_xacnhanketnoi(data):
  global trangthaiguiApi, userName, password, domainLoginTinh, domainPingTinh, domainLogTinh, imel, tenthietbi, madiaban, tendiaban, lat, lng, Status, Video, khoaguidulieu
  try:
    responsePingtest = requests.post(domainXacnhanketnoi, json = data)
    jsonResponse = responsePingtest.json()
    if(jsonResponse['success'] == True):
      print("✅ Kết nối thành công!")
      # dieu khien volume #
      setVolume(jsonResponse['data']['data']['volume'])
       # Đọc nội dung của tệp cấu hình
      config.read(CONFIG_FILE)
      # Thay đổi giá trị input
      config.set("input", "device", jsonResponse['data']['data']['deviceinput'])
      config.set("input", "channel", jsonResponse['data']['data']['channel'])
      config.set("icecast2-0", "bitrate", jsonResponse['data']['data']['bitrate'])
      config.set("icecast2-0", "server", jsonResponse['data']['data']['serverstream'])
      config.set("icecast2-0", "port", jsonResponse['data']['data']['portstream'])
      config.set("icecast2-0", "password", jsonResponse['data']['data']['password'])
      config.set("icecast2-0", "name", jsonResponse['data']['data']['nameStream'])
      config.set("icecast2-0", "mountPoint", jsonResponse['data']['data']['mountPoint'])
      # Ghi lại nội dung vào tệp cấu hình
      with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    #   dieu khien play #
      if(jsonResponse['data']['data']['statusPlay'] == 'play'):   
        if(jsonResponse['data']['data']['deviceId'] == id):  
         for proc in subprocess.Popen(['pgrep', '-f', 'darkice'], stdout=subprocess.PIPE).stdout:
            pid = int(proc.decode())
            os.kill(pid, signal.SIGTERM)   
         start_darkice() 
        print("start_darkice")
      else:
        stop_darkice()
        print("stop_darkice")
    else:
        print("⚠️ Lỗi từ server:", jsonResponse)
#   except:
#     print('loi xac nhan ket noi')
  except requests.exceptions.RequestException as e:
        print("❌ Lỗi kết nối API:", e)
  except ValueError:
        print("⚠️ Phản hồi không phải JSON hợp lệ!")
  except Exception as e:
        print("❌ Lỗi không xác định:", e)



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
        api_xacnhanketnoi(dataXacnhanketnoi)
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
    client.connect(domainMqtt, portMqtt, 60)
except Exception as e:
    print("❌ Lỗi kết nối MQTT:", str(e))
    exit(1)

# Chạy luồng gửi trạng thái riêng để không chặn luồng chính
status_thread = threading.Thread(target=publish_status, daemon=True)
status_thread.start()

# Chạy vòng lặp chính để duy trì kết nối MQTT
client.loop_forever()
