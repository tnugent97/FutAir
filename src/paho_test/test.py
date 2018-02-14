import paho.mqtt.client as mqtt
import datetime
import json

saved_data = json.loads(open('../../website/web/db/mqtt.json'))

# connect and subscribe to esys/Thom&Doug/test
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("esys/Thom&Doug/test")

# When message received dump as JSON into our 'database'
def on_message(client, userdata, msg):
    t = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")

    payload = json.loads(msg.payload)
    payload["time"] = t

    dev_id = payload["id"]
    del payload["id"]

    if str(dev_id) in saved_data:
        data_list = saved_data[str(dev_id)]
        data_list.append(payload)
        saved_data[str(dev_id)] = data_list

    else:
        saved_data[str(dev_id)] = [payload]

    print(saved_data)
    # with open('../../website/web/db/mqtt.json', 'a') as outfile:
    #     json.dump(payload, outfile)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect on the right IP and port
client.connect("192.168.0.10", 1883, 60)

client.loop_forever()