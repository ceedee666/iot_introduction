from dht import DHT11
from machine import RTC, Pin
import json
import time

import wifi
import mqtt

# This template assumes the following file setup
# - main.py
# - wifi.py
# - mqtt.py
# - cert
#    | - cert.der
#    | - private.der
#    | - wifi_passwds.txt

MQTT_TOPIC = "environment-data"


def convert_to_iso(datetime):
    y, m, d, _, h, mi, s, _ = datetime
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, d, h, mi, s)


def measure_environment_data():
    sensor = DHT11(Pin(5))
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def publish_environment_data(mqtt_client):
    data = measure_environment_data()
    iso_timestamp = convert_to_iso(RTC().datetime())

    message = {"temperature": data[0], "humidity": data[1], "timestamp": iso_timestamp}
    mqtt_client.publish(MQTT_TOPIC, json.dumps(message))


def connect_and_publish():
    print("connect wifi and synchronize RTC")
    wifi.connect()
    wifi.synchronize_rtc()

    print("connect mqtt")
    mqtt_client = mqtt.connect_mqtt()

    print("start publishing data")
    while True:
        try:
            publish_environment_data(mqtt_client)
        except Exception as e:
            print(str(e))
        time.sleep(5)


connect_and_publish()
