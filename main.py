#new code
import pigpio
import time
import evdev
from evdev import InputDevice, categorize, ecodes

#Connect gamepad
gamepad = InputDevice('/dev/input/event7')

print(f"Connect device name: {gamepad.name}")

# Подключение к pigpio
pi = pigpio.pi()

# Настройка GPIO для PWM
servo_pin1 = 17

def set_angle1(angle1):
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle1 / 180) * 2000
    pi.set_servo_pulsewidth(servo_pin1, pulsewidth)
set_angle1(90)
angle1 = 90
try:
    
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if event.code == ecodes.ABS_X:  # Событие оси X левого стика
                print(f'Левый стик (ось X): {event.value}')
                
                if event.value >= 40000:
                    if angle1 < 130:
                        angle1+=1
                    else:
                        angle1 = 130
                if event.value <= 30000:
                    if angle1 > 20:
                        angle1-=1
                    else:
                        angle1 = 20
                
                #angle = event.value//(65535/180)
                #time.sleep()
                print(angle1)
                time.sleep(0.01)
                set_angle1(angle1)
            

        
finally:
    # Остановка и отключение
    pi.set_servo_pulsewidth(servo_pin1, 0)
    pi.stop()
