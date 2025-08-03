from machine import ADC, Pin
from time import sleep

pot= ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)
while True:
    value= pot.read()
    print(value)
    sleep(0.5)
