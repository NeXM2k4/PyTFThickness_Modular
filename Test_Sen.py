from machine import Pin,PWM
from time import sleep

pin_dct=17

sen=Pin(pin_dct,mode=Pin.IN)
while True:
    print(sen.value())
    sleep(2)