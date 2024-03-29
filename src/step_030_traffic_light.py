from machine import Pin
from time import sleep

# ATTENTION: The pin numbers printed on the D1 mini and the NodeMCU
#           are not the GPIO numbers used to initialize the pins
#           in a python script.
#           The mapping between the number on the micorcontroller
#           and the GPIO numbers can be found here
#           https://docs.wemos.cc/en/latest/d1/d1_mini.html
#           https://cdn.shopify.com/s/files/1/2930/7174/files/esp8266_devkit_horizontal-01.png

red = Pin(0, Pin.OUT)
amber = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

while True:
    red.on()
    amber.off()
    green.off()

    sleep(5)

    amber.on()

    sleep(1)

    red.off()
    amber.off()
    green.on()

    sleep(5)

    green.off()
    amber.on()

    sleep(1)
