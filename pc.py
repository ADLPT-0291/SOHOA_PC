import requests
import configparser
import url

CONFIG_FILE = "/etc/darkice.cfg"
config = configparser.ConfigParser()
config.optionxform = lambda option: option

######### khai bao domain ##########
domainMqtt = url.domainMqtt
portMqtt = url.portMqtt
domainXacnhanketnoi = url.domainXacnhanketnoi
domainLogbantin = url.domainLogbantin
domainPing = url.domainPing
domainXacnhanketnoilai = url.domainXacnhanketnoilai
domainStartStream = url.domainStartStream

print("oke")

def api_xacnhanketnoi(data):
    try:
        # Gửi yêu cầu POST đến server
        responsePingtest = requests.post(domainXacnhanketnoi, json=data)
        
        # Kiểm tra nếu yêu cầu thành công
        if responsePingtest.status_code == 200:
            print("Yêu cầu thành công! Phản hồi từ server:")
            print(responsePingtest.text)  # In ra phản hồi thô từ server
        else:
            print(f"Lỗi {responsePingtest.status_code}: Không thể kết nối với server")
    except Exception as e:
        print(f'Lỗi khi kết nối: {e}')
