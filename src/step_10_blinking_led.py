from machine import Pin
from time import sleep_ms
#ATTENTION: The pin numbers printed on the D1 mini are not the
#           GPIO numbers used to initialize the pins in a python
#           script. The mapping can be found here
#           https://docs.wemos.cc/en/latest/d1/d1_mini.html
pin_d1 = Pin(5, Pin.OUT)

for _ in range(50):
    pin_d1.on()
    sleep_ms(200)
    pin_d1.off()
    sleep_ms(200)

print("Finished....")
