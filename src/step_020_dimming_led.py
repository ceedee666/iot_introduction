from machine import Pin, PWM
from time import sleep_ms

# ATTENTION: The pin numbers printed on the D1 mini and the NodeMCU
#           are not the GPIO numbers used to initialize the pins
#           in a python script.
#           The mapping between the number on the micorcontroller
#           and the GPIO numbers can be found here
#           https://docs.wemos.cc/en/latest/d1/d1_mini.html
#           https://cdn.shopify.com/s/files/1/2930/7174/files/esp8266_devkit_horizontal-01.png

d1_pwm = PWM(Pin(5), freq=1000, duty=512)

dc_values = list(range(0, 257, 8))

while True:
    for dc in dc_values:
        d1_pwm.duty(dc)
        sleep_ms(100)
