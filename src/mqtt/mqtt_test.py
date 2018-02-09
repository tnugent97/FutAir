from umqtt.simple import MQTTClient
import network
import machine
import json

def main(server="192.168.0.10"):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('EEERover','exhibition')

    send_msg = {
        'data_to_send': "heloo",
        'also_send_this': 56
    }

    c = MQTTClient(machine.unique_id(), server)
    c.connect()
    c.publish(b"esys/Thom&Doug/test", bytes(json.dumps(send_msg), 'utf-8'))
    c.disconnect()

if __name__ == "__main__":
    main()
