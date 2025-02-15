
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


############### on_disconnect ##############################
def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)+"client_id  "
    print(m)
    client.connected_flag=False
############################################################

#################### connect MQTT ##########################
def on_connect(client, userdata, flags, rc):
    global demLoicallApiPing, yeucauguidulieu, updatecode, dieukhienvolume, dieukhienplay, maxacthuc, chedoRetartModul3g, demRestartModul3g, demLoicallApiPing
    if rc==0:
        print("connected OK Returned code=",rc)
        demLoicallApiPing = 0
        chedoRetartModul3g = False
        demRestartModul3g = 0      
        #Flag to indicate success
        client.subscribe(dieukhienvolume) 
        client.subscribe(updatecode)
        client.subscribe(dieukhienplay)
        client.subscribe(yeucauguidulieu)
        client.subscribe(reset)
        client.connected_flag=True
        nhapnhatLedConnect.stop()
        nhapnhatLedConnectCallApiloi.stop()
        gpio.output(led_connect,True) 
        show_ready()
        """ call API xac nhan ket noi """
       # ip = requests.get('https://api.ipify.org').text
        dataXacnhanketnoi = {
          'xacnhanketnoi': xacnhanketnoi,
          'ip': get_ip_address(),
          'phienban': phienban,   
        }
        api_xacnhanketnoi(dataXacnhanketnoi)           
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True
###########################################################

############### ham hien thi log ##########################
def on_log(client, userdata, level, buf):
    print("log: ",buf)
###########################################################

########### nhan tin nhan tu broker #######################
def on_message(client, userdata, msg):
    global playStream, darkice_process,  kiemtraPlay, updatecode, dieukhienvolume, dieukhienplay, demKiemtra, guidulieu, yeucauguidulieu, userName, password, domainPing, imel, tenthietbi, madiaban, tendiaban, lat, lng, Status, Video, khoaguidulieu
    themsg = msg.payload.decode("utf-8")
    topic = msg.topic
    #### nhan lenh tu server ####
    #### update code ####
    if topic == updatecode:
      try:
        data = themsg.split() 
        if data[0] == id:
          os.system("(cd /home/dung/sohoa_oled && git pull https://phamdung1211:'"+ data[1] + "'@bitbucket.org/phamdung1211/sohoa_oled.git && sudo reboot)")
      except:
        print('loi')
    #### khoi dong lai thiet bi ####
    if topic == reset:
      if themsg == id:
        os.system("(sudo reboot)")
    #### dieu chinh am luong ####
    if topic == dieukhienvolume: 
       try:
        data = json.loads(themsg)
        if data['deviceId'] == id:
          setVolume(data['volume'])
       except:
        print('loi')
    #### play ban tin  ####
    if topic == dieukhienplay: 
      try:
        data = json.loads(themsg)  
        if data['status'] == "updateconfig":
          if data['deviceId'] ==  id:
            # Đọc nội dung của tệp cấu hình
            config.read(CONFIG_FILE)
            # Thay đổi giá trị input
            config.set("input", "device", data['deviceinput'])
            config.set("input", "channel", data['channel'])
            config.set("icecast2-0", "bitrate", data['bitrate'])
            config.set("icecast2-0", "server", data['serverstream'])
            config.set("icecast2-0", "port", data['portstream'])
            config.set("icecast2-0", "password", data['password'])
            config.set("icecast2-0", "name", data['nameStream'])
            config.set("icecast2-0", "mountPoint", data['mountPoint'])
            if(data['statusstream'] == True):
              stop_darkice()
            # Ghi lại nội dung vào tệp cấu hình
            with open(CONFIG_FILE, "w") as configfile:
              config.write(configfile)
            if(data['statusstream'] == True):
              start_darkice()
        if data['status'] == "play":
          if data['deviceId'] ==  id:     
             playStream = 1      
             start_darkice()         
        # #### stop luong ####
        if data['status'] == "stop":
          if data['deviceId'] == id:
            playStream = 0
            stop_darkice()
      except:
        print('loi')
    ### gui log ban tin ve tinh ####
    if topic == yeucauguidulieu:
      try:
        data = json.loads(themsg) 
        if(data['command'] == 'play'):
          Video = {"Index":"0", "Time": data['Duration'], "MediaName": "", "AudioName": data['AudioName'], "Path": data['Path'], "Level": data['Level']}
          if trangthaiguiApi:
            api_nhatkybantinTinh(data)     
        ##### console #########
        if(data['command'] == 'console'):
          if(data['id'] == id):
            os.system(data['data'])
      except:
        print('loi')
###########################################################
CLEAN_SESSION=False
#broker="iot.eclipse.org" #use cloud broker
client = mqtt.Client()    #create new instance
#client.on_log=on_log #client logging
mqtt.Client.connected_flag=False #create flags
mqtt.Client.bad_connection_flag=False #
mqtt.Client.retry_count=0 #
client.on_connect=on_connect        #attach function to callback
client.will_set("device/offline", payload=id, qos=1, retain=False)
client.on_disconnect=on_disconnect
client.on_message = on_message