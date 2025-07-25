from machine import Pin, PWM #importing Pin and PWM
from time import sleep #importing sleep or delay

AIN1=Pin(27,Pin.OUT) #Input for terminal 1 of motor A
AIN2=Pin(26,Pin.OUT) #Input for terminal 2 of motor A
pwmA=PWM(Pin(25))
pwmA.freq(1000)  # Set frequency

BIN1=Pin(19,Pin.OUT) #Input for terminal 1 of motor B
BIN2=Pin(18,Pin.OUT) #Input for terminal 2 of motor B
pwmB=PWM(Pin(5))
pwmB.freq(1000)  # Set frequency

STBY=Pin(33,Pin.OUT) #Input for Standby of driver
STBY.value(1)        #Value is 1 to power the driver

def motorA_forward(speed): #defining a function for motor A to rotate in forward direction
    AIN1.value(1)          #Terminal 1 is powered
    AIN2.value(0)          #Terminal 2 is grounded
    pwmA.duty(speed)       #To control speed of the motor between 0-1023
    
def motorA_reverse(speed): #defining a function for motor A to rotate in reverse direction
    AIN1.value(0)          #Terminal 1 is grounded
    AIN2.value(1)          #Terminal 2 is powered
    pwmA.duty(speed)       #To control speed of the motor between 0-1023
    
def motorA_stop():         #defining a function for motor A to stop rotating
    AIN1.value(0)          #Terminal 1 is grounded
    AIN2.value(0)          #Terminal 2 is grounded
    pwmA.duty(0)           #Speed of the motor is given zero
    
def motorB_forward(speed): #defining a function for motor B to rotate in forward direction
    BIN1.value(1)          #Terminal 1 is powered
    BIN2.value(0)          #Terminal 2 is grounded
    pwmB.duty(speed)       #To control speed of the motor between 0-1023
    
def motorB_reverse(speed): #defining a function for motor B to rotate in reverse direction
    BIN1.value(0)          #Terminal 1 is grounded
    BIN2.value(1)          #Terminal 2 is powered
    pwmB.duty(speed)       #To control speed of the motor between 0-1023
    
def motorB_stop():         #defining a function for motor B to stop rotating
    BIN1.value(0)          #Terminal 1 is grounded
    BIN2.value(0)          #Terminal 1 is grounded
    pwmB.duty(0)           #Speed of the motor is given zero

while True:                      #Using while loop to run the code inside it to run continuously
    print("Both motors forward") 
    motorA_forward(1000)         #Calling the function with speed
    motorB_forward(1000)         #Calling the function with speed
    sleep(1)                     #Delay for 1sec,so that the motor rotates for 1sec

    print("Both motors reverse") 
    motorA_reverse(1000)         #Calling the function with speed
    motorB_reverse(1000)         #Calling the function with speed
    sleep(1)                     #Delay for 1sec,so that the motor rotates for 1sec

    print("Both motors stop")    
    motorA_stop()                #Calling the function to stop
    motorB_stop()                #Calling the function to stop
    sleep(2)                     #Delay for 2sec,so that it stops for 2sec