from machine import Pin

button_pressed = False


def handle_interrupt(pin):
    global button_pressed
    button_pressed = True


def toggle_led():
    led.value(not led.value())


led = Pin(5, Pin.OUT)
button = Pin(15, Pin.IN)

button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)


while True:
    if button_pressed:
        toggle_led()
        button_pressed = False
