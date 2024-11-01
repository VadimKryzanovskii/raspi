import RPi.GPIO as GPIO
import time
import evdev
from evdev import InputDevice, categorize, ecodes


gamepad = InputDevice("/dev/input/event7")

print(f"Connect device name: {gamepad.name}")
GPIO.setmode(GPIO.BCM)
SERVO_PIN = 17
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # Частота 50 Гц для сервопривода
pwm.start(0)

pwm.ChangeDutyCycle(100)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if event.code == ecodes.ABS_X:  # Событие оси X левого стика
            print(f"Левый стик (ось X): {event.value}")
        elif event.code == ecodes.ABS_Y:  # Событие оси Y левого стика
            print(f"Левый стик (ось Y): {event.value}")
        elif event.code == ecodes.ABS_Z:  # Событие оси X правого стика
            print(f"Правый стик (ось X): {event.value}")
        elif event.code == ecodes.ABS_RZ:  # Событие оси Y правого стика
            print(f"Правый стик (ось Y): {event.value}")
