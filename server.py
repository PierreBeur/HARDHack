from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn


# Arduino Data

import asyncio
import serial
import json
import math

ser = serial.Serial("COM5", 115200) # open serial port
ser.flushInput()

def length(v):
    return math.sqrt(v['x']**2 + v['y']**2 + v['z']**2)

class MySerialMonitor:
    def __init__(self):
        self.acceleration = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.gyro = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.speed = 0.0
        self.distance = 0.0
        self.temperature = 0.0


    async def run_main(self):
        while True:
            try:
                data = json.loads(ser.readline().decode().rstrip()) # read the data from the serial port
                if 'acceleration' in data:
                    self.acceleration = data['acceleration']
                    magnitude = length(self.acceleration)
                    self.speed += (magnitude - 9.8) * 0.5
                    self.distance += self.speed * 0.5
                if 'gyro' in data:
                    self.gyro = data['gyro']
                if 'temperature' in data:
                    self.temperature = data['temperature']
            except:
                pass
            await asyncio.sleep(0.5)

serial_monitor = MySerialMonitor()


# Routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def get_html():
    with open("index.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/data")
def get_data():
    data = {
        'acceleration': serial_monitor.acceleration,
        'gyro': serial_monitor.gyro,
        'speed': serial_monitor.speed,
        'distance': serial_monitor.distance,
        'temperature': serial_monitor.temperature
    }
    return data

@app.get("/reset")
def get_reset():
    serial_monitor.speed = 0.0
    serial_monitor.distance = 0.0


# Startup

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(serial_monitor.run_main())

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.137.1", port=6543)