from machine import Pin, ADC, PWM
import time

# Define pins
pot = ADC(Pin(34))            # Potentiometer connected to GPIO34 (ADC input)
pot.atten(ADC.ATTN_11DB)      # Full range: 0–3.3V (ESP32)
pot.width(ADC.WIDTH_12BIT)    # 12-bit resolution: 0–4095

led = PWM(Pin(5), freq=1000) # LED on GPIO5 with 1kHz PWM

while True:
    pot_value = pot.read()            # Read potentiometer (0–4095)
    duty = int((pot_value / 4095) * 1023)  # Map to PWM duty (0–1023)
    led.duty(duty)                    # Set LED brightness
    print("Pot:", pot_value, "Duty:", duty)
    time.sleep(0.05)
