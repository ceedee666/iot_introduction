from machine import Pin
from time import sleep

# Global variable to store the information if the
# button was pressed
button_pressed = False

# Callback
# This function is invoked when the button is pressed
# It only set the global variable button_pressed to True
def handle_interrupt(pin):
    global button_pressed
    button_pressed = True


def blink_led():
    for _ in range(5):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)


led = Pin(5, Pin.OUT)
button = Pin(15, Pin.IN)

# When the button is pressed (i.e. the value of D8 changes
# from low to high) the callback function handle_interrupt
# shall be invoked.
button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)


# Endless loop.
# Whenever the global variable button_pressed is True the function
# blink_led() is called. Afterwards the global variable button_pressed is
# set to false.
while True:
    if button_pressed:
        blink_led()
        button_pressed = False
