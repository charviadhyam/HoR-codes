from machine import Pin
import time

button = Pin(14, Pin.IN, Pin.PULL_DOWN)   # Button pin with pull-down resistor
led = Pin(5, Pin.OUT)                    # LED pin

while True:
    if button.value() == 1:   # Button pressed
        led.on()
    else:                     # Button not pressed
        led.off()
    time.sleep(0.05)          # Small delay for stability