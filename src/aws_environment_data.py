from umqtt.robust import MQTTClient
from machine import Pin
from dht import DHT22

import json
import time

CERT_FILE = "/cert/cert.der"
KEY_FILE = "/cert/private.der"

MQTT_CLIENT_ID = "my_d1_mini"
MQTT_HOST = "a1lo9dnpk3t0qk-ats.iot.eu-central-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "environment-data"


def publish_msg(mqtt_client, msg):
    try:
        mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise


def create_msg(temperature, humidity, timestamp):
    message = {'temperature': temperature,
               'humidity': humidity,
               'timestamp' : timestamp }
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


def go():
    while True:
        try:
            sensor = DHT22(Pin(5))

            print("Connecting MQTT")
            mqtt_client = connect_mqtt()

            print("Publishing environment data")
            while True:
                sensor.measure()
                ts = time.localtime()
                formated_ts = '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])
                publish_msg(mqtt_client, create_msg(sensor.temperature(), sensor.humidity(), formated_ts))
                time.sleep(5)

        except Exception as e:
            print(str(e))
