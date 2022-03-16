import json
import time

import mqtt
import wifi
from dht import DHT22
from machine import RTC, Pin, I2C
import ssd1306

# This template assumes the following file setup
# - main.py
# - wifi.py
# - mqtt.py
# - cert
#    | - cert.der
#    | - private.der
#    | - wifi_passwds.txt

MQTT_TOPIC = "environment-data"
OLED_WIDTH = 128


def convert_to_iso(datetime):
    y, m, d, _, h, mi, s, _ = datetime
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, d, h, mi, s)


def measure_environment_data():
    sensor = DHT22(Pin(16))
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def publish_environment_data(data, mqtt_client):
    iso_timestamp = convert_to_iso(RTC().datetime())

    message = {"temperature": data[0], "humidity": data[1], "timestamp": iso_timestamp}
    mqtt_client.publish(MQTT_TOPIC, json.dumps(message))


def scroll_in_screen(screen, oled):
    for i in range(0, OLED_WIDTH + 1, 4):
        oled.text(screen[0][2], 0, screen[0][1])
        oled.text(screen[1][2], 0, screen[1][1])

        for line in screen[2:]:
            oled.text(line[2], -OLED_WIDTH + i, line[1])
        oled.show()
        if i != OLED_WIDTH:
            oled.fill(0)


def init_oled():
    i2c = I2C(sda=Pin(4), scl=Pin(5))
    return ssd1306.SSD1306_I2C(128, 64, i2c)


def show_data_on_oled(data):
    oled = init_oled()

    line1 = "Temp.:    " + str(data[0]) + "C"
    line2 = "Humidity: " + str(data[1]) + "%"
    screen = [
        [0, 0, "Environment Data"],
        [0, 12, "----------------"],
        [0, 32, line1],
        [0, 48, line2],
    ]

    scroll_in_screen(screen, oled)


def show_text(text):
    oled = init_oled()
    oled.fill(0)
    oled.text(text, 0, 0, 1)
    oled.show()


def connect_and_publish():
    show_text("Connecting wifi...")
    while not wifi.connect():
        show_text("No WLAN found.")
        time.sleep(2)
        show_text("Retrying.")
        time.sleep(2)

    while not wifi.synchronize_rtc():
        show_text("NTP Error.")
        time.sleep(2)
        show_text("Retrying.")
        time.sleep(2)

    mqtt_client = None
    while not mqtt_client:
        try:
            show_text("Connecting MQTT.")
            mqtt_client = mqtt.connect_mqtt()
        except Exception as e:
            show_text("MQTT Error.")
            time.sleep(2)
            show_text("Retrying.")
            time.sleep(2)

    show_text("Start publishing data")
    while True:
        try:
            environment_data = measure_environment_data()
            publish_environment_data(environment_data, mqtt_client)
            show_data_on_oled(environment_data)
        except Exception as e:
            print(str(e))
        time.sleep(5)


if __name__ == "__main__":
    connect_and_publish()
