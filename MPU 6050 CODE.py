from machine import I2C, Pin
from time import sleep
import mpu6050
import math

# Initialize I2C for MPU6050
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
print("I2C devices found:", i2c.scan())

# Initialize MPU6050
mpu = mpu6050.accel(i2c)

while True:
    try:
        # Get sensor data
        data = mpu.get_values()

        # Raw acceleration
        ax = data["AcX"]
        ay = data["AcY"]
        az = data["AcZ"]

        # Convert to g units (±2g range → divide by 16384)
        ax_g = ax / 16384.0
        ay_g = ay / 16384.0
        az_g = az / 16384.0

        # Convert to m/s² (1g ≈ 9.81 m/s²)
        ax_ms2 = ax_g * 9.81
        ay_ms2 = ay_g * 9.81
        az_ms2 = az_g * 9.81

        # Total acceleration magnitude
        accel_magnitude = math.sqrt(ax_ms2**2 + ay_ms2**2 + az_ms2**2)

        # Temperature in °C
        temp_raw = data["Tmp"]
        temp_c = (temp_raw / 340.0) + 36.53

        # Print results
        print("Acceleration (m/s²) -> X: {:.2f}, Y: {:.2f}, Z: {:.2f}".format(ax_ms2, ay_ms2, az_ms2))
        print("Total Acceleration Magnitude: {:.2f} m/s²".format(accel_magnitude))
        print("Temperature: {:.2f} °C".format(temp_c))
        print("-------------------------------------")

    except OSError as e:
        print("Sensor error:", e)

    sleep(0.1)
