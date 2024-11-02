import pigpio #Включить в терминале демона командой  sudo pigpiod
import time
import evdev
from evdev import InputDevice, categorize, ecodes

# Connect gamepad
gamepad = InputDevice("/dev/input/event7")

print(f"Connect device name: {gamepad.name}")

# Подключение к pigpio
pi = pigpio.pi()

# Настройка GPIO для PWM
SERVO_PIN1 = 17
SERVO_PIN2 = 18
# Начальная настройка угла сервопривода
ANGLE_SERVO_LEFT = 90
ANGLE_SERVO_RIGTH = 90


def set_angle_servo_left(angle):
    """Принимает угол левого стика контролера xbox и передает на сервопривод подключеный к RaspberryPi"""
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN1, pulsewidth)


def set_angle_servo_rigth(angle):
    """Принимает угол правого стика контролера xbox и передает на сервопривод подключеный к RaspberryPi"""
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN2, pulsewidth)


set_angle_servo_left(ANGLE_SERVO_LEFT)
set_angle_servo_rigth(ANGLE_SERVO_RIGTH)


button_map = {
    ecodes.BTN_A: "A",
    ecodes.BTN_B: "B",
    ecodes.BTN_X: "X",
    ecodes.BTN_Y: "Y",
    ecodes.BTN_START: "START",
    ecodes.BTN_SELECT: "SELECT",
    ecodes.BTN_TL: "LB",
    ecodes.BTN_TR: "RB",
}

try:

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if event.code == ecodes.ABS_X:  # Событие оси X левого стика
                print(f"Левый стик (ось X): {event.value}")

                if event.value >= 40000:
                    if ANGLE_SERVO_LEFT < 130:
                        ANGLE_SERVO_LEFT += 1
                    else:
                        ANGLE_SERVO_LEFT = 130
                if event.value <= 30000:
                    if ANGLE_SERVO_LEFT > 20:
                        ANGLE_SERVO_LEFT -= 1
                    else:
                        ANGLE_SERVO_LEFT = 20
            elif event.code == ecodes.ABS_Z:  # Событие оси X правого стика
                print(f"Правый стик (ось X): {event.value}")
                if event.value >= 40000:
                    if ANGLE_SERVO_RIGTH < 120:
                        ANGLE_SERVO_RIGTH += 1
                    else:
                        ANGLE_SERVO_RIGTH = 120
                if event.value <= 30000:
                    if ANGLE_SERVO_RIGTH > 20:
                        ANGLE_SERVO_RIGTH -= 1
                    else:
                        ANGLE_SERVO_RIGTH = 20
            elif event.type == ecodes.EV_KEY:  # Кнопки
                button = button_map.get(event.code, f"Кнопка {event.code}")
                if event.value == 1:
                    print(f"Нажата кнопка: {button}")
                elif event.value == 0:
                    print(f"Отпущена кнопка: {button}")
                # angle = event.value//(65535/180)
                # time.sleep()
            print(ANGLE_SERVO_LEFT)
            print(ANGLE_SERVO_RIGTH)
            #time.sleep(0.01)
            set_angle_servo_left(ANGLE_SERVO_LEFT)
            set_angle_servo_rigth(ANGLE_SERVO_RIGTH)


finally:
    # Остановка и отключение
    pi.set_servo_pulsewidth(SERVO_PIN1, 0)
    pi.stop()