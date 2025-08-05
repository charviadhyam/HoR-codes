from machine import Pin
from time import sleep
import dht
 
sensor = dht.DHT11(Pin(5))
 
while True:
  try:
    sleep(2)
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
    print('Temperature: %3.1f C' %t)
    print('Humidity: %3.1f %%' %h)
  except OSError as e:
    print('Sensor Reading Failed')
