from paho.mqtt import client as mqtt # type: ignore
import time
import ssl


port= 8883
broker = "ca99add77b634afe8e68917f0339aec6.s1.eu.hivemq.cloud"
username = "gtechdn"
password = "Kontum12@"


context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE


topic = "gtechdn/sohoa_pc"
client=mqtt.Client()
client.connect(broker, port)
print("Connected to the HIVEMQ Broker")
