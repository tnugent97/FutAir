from umqtt.simple import MQTTClient

def main(server="192.168.0.10"):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(b"esys/Thom&Doug", b"hello")
    c.disconnect()

if __name__ == "__main__":
    main()