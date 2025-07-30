from machine import Pin, time_pulse_us
import time

trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

def get_distance():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duration = time_pulse_us(echo, 1, 30000)  
    distance = (duration / 2) / 29.1
    return distance

while True:
    try:
        dist = get_distance()
        print("Distance: {:.2f} cm".format(dist))
    except OSError:
        print("Out of range")
    time.sleep(1)
