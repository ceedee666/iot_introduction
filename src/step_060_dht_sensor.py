from machine import Pin
from dht import DHT11
from time import sleep

sensor = DHT11(Pin(5))

while True:
    sensor.measure()
    print("Temp:", sensor.temperature(), "- Humid:", sensor.humidity())
    sleep(5)
