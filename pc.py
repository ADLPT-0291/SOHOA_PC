from paho.mqtt import client as mqtt # type: ignore
import time
import ssl
led_status = 16

port= 8883
broker = "ca99add77b634afe8e68917f0339aec6.s1.eu.hivemq.cloud"
username = "gtechdn"
password = "Kontum12@"

topic = "gtechdn/sohoa_pc"
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.verify_mode = ssl.CERT_NONE
client=mqtt.Client()
client.connect(broker, port)
print("Connected to the HIVEMQ Broker")


client.publish(topic,led_status)
print("show led_status")