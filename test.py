import RPi.GPIO as GPIO
import time
import evdev
from evdev import InputDevice, categorize, ecodes

#Connect gamepad
gamepad = InputDevice('/dev/input/event7')

print(f"Connect device name: {gamepad.name}")

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Установка сигнала на выходе
pwm = GPIO.PWM(servo_pin, 50)  # Частота 50 Гц для сервопривода
pwm.start(0)  # Начальное значение

# Функция для поворота сервопривода
def set_angle(angle):
    duty = 2 + (angle // 18)
    print(duty)# Перевод угла в значение скважности (duty cycle)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    #pwm.ChangeDutyCycle(0)  # Остановим сигнал для предотвращения шума

# Пример использования
try:
    set_angle(0)
    print("position: 0")# Позиция 0 градусов
    time.sleep(1)
    set_angle(90)
    print("position: 90")# Позиция 90 градусов
    time.sleep(1)
    set_angle(180)
    print("position: 180")# Позиция 180 градусов
    time.sleep(1)
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if event.code == ecodes.ABS_X:  # Событие оси X левого стика
                print(f'Левый стик (ось X): {event.value}')
                angle = event.value//(65535/180)
                time.sleep(0.5)
                print(angle)
                set_angle(angle)
            elif event.code == ecodes.ABS_Y:  # Событие оси Y левого стика
                print(f'Левый стик (ось Y): {event.value}')
            elif event.code == ecodes.ABS_Z:  # Событие оси X правого стика
                print(f'Правый стик (ось X): {event.value}')
            elif event.code == ecodes.ABS_RZ:  # Событие оси Y правого стика
                print(f'Правый стик (ось Y): {event.value}')
finally:
    pwm.stop()
    GPIO.cleanup()

