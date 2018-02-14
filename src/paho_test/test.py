import paho.mqtt.client as mqtt

# connect and subscribe to esys/Thom&Doug/test
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("esys/Thom&Doug/test")

# When message received dump as JSON into our 'database'
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    with open('../../website/web/db/mqtt.json', 'a') as f:
        f.write(str(msg.payload) + "\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect on the right IP and port
client.connect("192.168.0.10", 1883, 60)

client.loop_forever()