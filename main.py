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
SERVO_PIN_LEFT = 17
SERVO_PIN_RIGTH = 18
SERVO_PIN_CRAB = 14
SERVO_PIN_BASE = 3
# Начальная настройка угла сервопривода
ANGLE_SERVO_LEFT = 90
ANGLE_SERVO_RIGTH = 90
ANGLE_SERVO_CRAB = 80
ANGLE_SERVO_BASE = 90



def set_angle_servo_left(angle):
    """Принимает угол левого стика контролера xbox и передает на сервопривод подключеный к RaspberryPi"""
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN_LEFT, pulsewidth)


def set_angle_servo_rigth(angle):
    """Принимает угол правого стика контролера xbox и передает на сервопривод подключеный к RaspberryPi"""
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN_RIGTH, pulsewidth)

def set_angle_servo_crab(angle):
    """Принимает угол левого стика контролера xbox и передает на сервопривод подключеный к RaspberryPi"""
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN_CRAB, pulsewidth)

def set_angle_servo_base(angle):
    """Принимает угол левого стика контролера xbox и передает на сервопривод подключеный к RaspberryPi"""
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN_BASE, pulsewidth)


set_angle_servo_left(ANGLE_SERVO_LEFT)
set_angle_servo_rigth(ANGLE_SERVO_RIGTH)
set_angle_servo_crab(ANGLE_SERVO_CRAB)
set_angle_servo_base(ANGLE_SERVO_BASE)


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
                if event.code == ecodes.ABS_HAT0X:  # Событие оси X левого стика
                    print(f"Левый стик (ось X): {event.value}")

                    if event.value == -1:
                        if ANGLE_SERVO_LEFT < 130:
                            ANGLE_SERVO_LEFT += 2
                        else:
                            ANGLE_SERVO_LEFT = 130
                    if event.value == 1:
                        if ANGLE_SERVO_LEFT > 20:
                                ANGLE_SERVO_LEFT -= 2
                        else:
                            ANGLE_SERVO_LEFT = 20
                    print(ANGLE_SERVO_LEFT)
                    set_angle_servo_left(ANGLE_SERVO_LEFT)
            
            
            if event.code == ecodes.ABS_HAT0Y:  # Событие оси X правого стика
                print(f"Правый стик (ось X): {event.value}")
                if event.value == -1:
                    if ANGLE_SERVO_RIGTH < 120:
                        ANGLE_SERVO_RIGTH += 2
                    else:
                        ANGLE_SERVO_RIGTH = 120
                if event.value == 1:
                    if ANGLE_SERVO_RIGTH > 20:
                        ANGLE_SERVO_RIGTH -= 2
                    else:
                        ANGLE_SERVO_RIGTH = 20
                print(ANGLE_SERVO_RIGTH)
                set_angle_servo_rigth(ANGLE_SERVO_RIGTH)
                
                
            if event.type == ecodes.EV_KEY:  # Кнопки
                button = button_map.get(event.code, f"Кнопка {event.code}")
                if event.value == 1:
                    print(f"Нажата кнопка: {button}")
                    if button == "X" and ANGLE_SERVO_BASE < 120:
                        ANGLE_SERVO_BASE += 2
                        print(f"ANGLE_SERVO_BASE: {ANGLE_SERVO_BASE}")
                        set_angle_servo_base(ANGLE_SERVO_BASE)
                        
                    if button == "B" and ANGLE_SERVO_BASE > 20:
                        ANGLE_SERVO_BASE -= 2
                        print(f"ANGLE_SERVO_BASE: {ANGLE_SERVO_BASE}")
                        set_angle_servo_base(ANGLE_SERVO_BASE)
                    if button == "RB" and ANGLE_SERVO_CRAB < 180:
                        ANGLE_SERVO_CRAB += 4
                        print(f"ANGLE_SERVO_CRAB: {ANGLE_SERVO_CRAB}")
                        set_angle_servo_crab(ANGLE_SERVO_CRAB)
                        
                    if button == "LB" and ANGLE_SERVO_CRAB > 80:
                        ANGLE_SERVO_CRAB -= 4
                        print(f"ANGLE_SERVO_CRAB: {ANGLE_SERVO_CRAB}")
                        set_angle_servo_crab(ANGLE_SERVO_CRAB)
                        
                elif event.value == 0:
                    print(f"Отпущена кнопка: {button}")
                # angle = event.value//(65535/180)
                # time.sleep()
       
finally:
    # Остановка и отключение
    #pi.set_servo_pulsewidth(SERVO_PIN1, 0)
    pi.stop()