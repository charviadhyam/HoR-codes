from machine import Pin
from time import sleep

AIN1=Pin(25,Pin.OUT)
AIN2=Pin(33,Pin.OUT)
BIN1=Pin(27,Pin.OUT)
BIN2=Pin(14,Pin.OUT)
pwma=Pin(32,Pin.OUT)
pwmb=Pin(12,Pin.OUT)
STBY= Pin(26,Pin.OUT)

pwma.on()
pwmb.on()
STBY.on()

def Move_for():
    AIN1.on();AIN2.off()
    BIN1.on();BIN2.off()
def move_back():
    AIN1.off();AIN2.on()
    BIN1.off();BIN2.on()
def right():
    AIN1.on();AIN2.off()
    BIN1.off();BIN2.on()
def left():
    AIN1.off();AIN2.on()
    BIN1.on();BIN2.off()
def stop():
    AIN1.off();AIN2.off()
    BIN1.off();BIN2.off()

print("bot is moving....")
move_for()
sleep(2)
right()
sleep(2)
move_back()
sleep(2)
left()
sleep(2)
stop()
print("bot is in stop position ..... ")