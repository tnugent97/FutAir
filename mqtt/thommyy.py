from umqtt.simple import MQTTClient
import network
import machine

def main(server="192.168.0.10"):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('EEERover','exhibition')

    c = MQTTClient(machine.unique_id(), server)
    c.connect()
    c.publish(b"esys/Thom&Doug/test", bytes("hello", 'utf-8'))
    c.disconnect()

if __name__ == "__main__":
    main()
