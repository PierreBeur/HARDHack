import serial
import json
import math

ser = serial.Serial('COM4', 115200) # open serial port
ser.flushInput()

acceleration = {}
gyro = {}
temperature = 0.0

while True:
    try:
        sensorValue = json.loads(ser.readline().decode().rstrip()) # read the value from the serial port
        if sensorValue['acceleration']:
            acceleration = sensorValue['acceleration']
            x = acceleration['x']
            y = acceleration['y']
            z = acceleration['z']
            print(f"acceleration: ({x}, {y}, {z})")
            print(f"acceleration magnitude: {math.sqrt(x**2 + y**2 + z**2)}")
        if sensorValue['gyro']:
            gyro = sensorValue['gyro']
            x = gyro['x']
            y = gyro['y']
            z = gyro['z']
            print(f"gyro: ({x}, {y}, {z})")
            print(f"gyro magnitude: {math.sqrt(x**2 + y**2 + z**2)}")
        if sensorValue['temperature']:
            temperature = sensorValue['temperature']
            print(f"temperature: {temperature}")
    except KeyboardInterrupt:
        break
    except:
        continue

ser.close() # close the serial port
