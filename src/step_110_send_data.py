from umqtt.robust import MQTTClient
import random
import json
import time


# The certificate and key file need to be converted from PEM to DER format first
#
#$ openssl x509 -in aaaaaaaaa-certificate.pem.crt.txt -out cert.der -outform DER
#$ openssl rsa -in aaaaaaaaaa-private.pem.key -out private.der -outform DER

CERT_FILE = "/cert/cert.der"
KEY_FILE = "/cert/private.der"

MQTT_CLIENT_ID = "my_d1_mini"
MQTT_PORT = 8883

MQTT_TOPIC = "test-topic"

MQTT_HOST = "a1lo9dnpk3t0qk-ats.iot.eu-central-1.amazonaws.com"


def pub_msg(mqtt_client, msg):
    try:
        mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise


def create_dummy_msg():
    message = {'temperature': int(random.getrandbits(8) / 256 * 30),
               'humidity': int(random.getrandbits(8) / 256 * 100)}
    return json.dumps(message)


def connect_mqtt():
    try:
        with open(KEY_FILE, "r") as f:
            key = f.read()

        print("Got Key")

        with open(CERT_FILE, "r") as f:
            cert = f.read()

        print("Got Cert")

        mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=5000, ssl=True,
                                 ssl_params={"cert": cert, "key": key, "server_side": False})
        mqtt_client.connect()
        print('MQTT Connected')

        return mqtt_client

    except Exception as e:
        print('Cannot connect MQTT: ' + str(e))
        raise


try:
    print("Connecting MQTT")
    mqtt_client = connect_mqtt()

    print("Publishing dummy data")
    for _ in range(10):
        pub_msg(mqtt_client, create_dummy_msg())
        time.sleep(5)
    print("Done")
except Exception as e:
    print(str(e))
