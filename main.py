import sys

sys.path.append("/src")

import wifi
import aws_iot
import time
import json

from machine import Pin
from dht import DHT22


def current_datetime():
    ts = time.localtime()
    return '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])


def send_sensor_data(sensor, mqtt_client):
    sensor.measure()
    datetime = current_datetime()

    message = {'temperature': sensor.temperature(),
               'humidity': sensor.humidity(),
               'timestamp': datetime}
    json_msg = json.dumps(message)
    try:
        mqtt_client.publish("environment-data", json_msg)
        print("Sent: " + json_msg)
    except Exception as e:
        print("Exception publish: " + str(e))


if __name__ == "__main__":
    wifi.connect_wifi()
    wifi.synchronize_rtc()

    mqtt_client = aws_iot.connect()

    sensor = DHT22(Pin(5))

    while True:
        send_sensor_data(sensor, mqtt_client)
        time.sleep(5)
