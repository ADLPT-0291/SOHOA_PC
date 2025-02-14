# #!/usr/bin/env python3
# import time
# from time import sleep
# import os
# from threading import Timer
# import subprocess
# import json
# import paho.mqtt.client as mqtt
# import paho.mqtt.publish as publish
# import url
# import khaibao
# import requests
# import socket
# import configparser
# # import signal
# # import psutil
# # import alsaaudio
# # import pyaudio

# from threading  import Thread
# from datetime import datetime, timezone


# # Khởi tạo giờ, phút, giây ban đầu là 0
# REMOTE_SERVER = "8.8.8.8"
# hour = 0
# minute = 0
# second = 0
# darkice_process = ''
# darkice_cmd = ['darkice', '-c', '/etc/darkice.cfg']
# # Đường dẫn đến tệp cấu hình của Darkice
# CONFIG_FILE = "/etc/darkice.cfg"
# # Tạo đối tượng ConfigParser
# config = configparser.ConfigParser()
# config.optionxform = lambda option: option

# ######### khai bao domain ##########
# domainMqtt = url.domainMqtt
# portMqtt = url.portMqtt
# domainXacnhanketnoi = url.domainXacnhanketnoi
# domainLogbantin = url.domainLogbantin
# domainPing = url.domainPing
# domainXacnhanketnoilai = url.domainXacnhanketnoilai
# domainStartStream = url.domainStartStream

# def api_xacnhanketnoi(data):
#   global trangthaiguiApi, userName, password, domainLoginTinh, domainPingTinh, domainLogTinh, imel, tenthietbi, madiaban, tendiaban, lat, lng, Status, Video, khoaguidulieu
#   try:
#     responsePingtest = requests.post(domainXacnhanketnoi, json = data)
#     jsonResponse = responsePingtest.json()
#     if jsonResponse.get('success', False):
#         print("Đã nhận dữ liệu từ API")
#         # config.read(CONFIG_FILE)
#     else:
#         print("Không thành công trong việc nhận dữ liệu")
#     # if(jsonResponse['success'] == True):
#     #   print("đã nhận")
#       # dieu khien volume #
#     #   setVolume(jsonResponse['data']['data']['volume'])
#        # Đọc nội dung của tệp cấu hình
#     #   config.read(CONFIG_FILE)

#     #   -----------------------------
#     # Kiểm tra nếu tệp đã được đọc
#     # if len(config.read(CONFIG_FILE)) == 0:
#     #     print("Không thể đọc tệp cấu hình hoặc tệp không tồn tại!")
#     # else:
#     #     print("Đã đọc tệp cấu hình!")

#     # # In toàn bộ nội dung của tệp
#     # for section in config.sections():
#     #     print(f"[{section}]")
#     #     for key, value in config.items(section):
#     #         print(f"{key} = {value}")
#     #     print()
#     # ------------------------------
#       # Thay đổi giá trị input
#     #   config.set("input", "device", jsonResponse['data']['data']['deviceinput'])
#     #   config.set("input", "channel", jsonResponse['data']['data']['channel'])
#     #   config.set("icecast2-0", "bitrate", jsonResponse['data']['data']['bitrate'])
#     #   config.set("icecast2-0", "server", jsonResponse['data']['data']['serverstream'])
#     #   config.set("icecast2-0", "port", jsonResponse['data']['data']['portstream'])
#     #   config.set("icecast2-0", "password", jsonResponse['data']['data']['password'])
#     #   config.set("icecast2-0", "name", jsonResponse['data']['data']['nameStream'])
#     #   config.set("icecast2-0", "mountPoint", jsonResponse['data']['data']['mountPoint'])
#       # Ghi lại nội dung vào tệp cấu hình
#     #   with open(CONFIG_FILE, "w") as configfile:
#     #     config.write(configfile)
#       # dieu khien play #
#     #   if(jsonResponse['data']['data']['statusPlay'] == 'play'):   
#     #     if(jsonResponse['data']['data']['deviceId'] == id):  
#     #      for proc in subprocess.Popen(['pgrep', '-f', 'darkice'], stdout=subprocess.PIPE).stdout:
#     #         pid = int(proc.decode())
#     #         os.kill(pid, signal.SIGTERM)   
#     #      start_darkice() 
#     #   else:
#     #     stop_darkice()
#   except:
#     print('loi xac nhan ket noi')

print("hello")
print("Hello, world!")
