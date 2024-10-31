import pigpio
import time

# Подключение к pigpio
pi = pigpio.pi()

# Настройка GPIO 18 для PWM
servo_pin = 18

def set_angle(angle):
    # Преобразование угла в значение широты импульса (500–2500 микросекунд)
    pulsewidth = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(servo_pin, pulsewidth)

try:
    # Поворот на 0, 90 и 180 градусов
    set_angle(0)
    time.sleep(2)
    set_angle(90)
    time.sleep(2)
    set_angle(180)
    time.sleep(2)
finally:
    # Остановка и отключение
    pi.set_servo_pulsewidth(servo_pin, 0)
    pi.stop()
