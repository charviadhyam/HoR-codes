from machine import Pin
from time import sleep
led= Pin(2, Pin.OUT)
push= Pin(18, Pin.IN)
while True:
    if push.value():
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
        print("working")
