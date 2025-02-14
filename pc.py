from paho.mqtt import client as mqtt # type: ignore

port= 8883
broker = "ca99add77b634afe8e68917f0339aec6.s1.eu.hivemq.cloud"

client=mqtt.Client()
client.connect(broker, port)