import random
from registry import registry
from flags import flags

def read():
    reading = random.randint(30, 510)
    registry.sensor_reading = reading

def actuate():
    if flags.actuate:
        flags.actuate = False
        registry.valve_actuated = True
        print("Actuated pressure valve")
