import RPi.GPIO as GPIO
import time

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Установка сигнала на выходе
pwm = GPIO.PWM(servo_pin, 50)  # Частота 50 Гц для сервопривода
pwm.start(0)  # Начальное значение

# Функция для поворота сервопривода
def set_angle(angle):
    duty = 2 + (angle / 18)  # Перевод угла в значение скважности (duty cycle)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Остановим сигнал для предотвращения шума

# Пример использования
try:
    set_angle(0)   # Позиция 0 градусов
    time.sleep(1)
    set_angle(90)  # Позиция 90 градусов
    time.sleep(1)
    set_angle(180) # Позиция 180 градусов
    time.sleep(1)
finally:
    pwm.stop()
    GPIO.cleanup()
