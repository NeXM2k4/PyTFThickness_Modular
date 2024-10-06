from machine import Pin,PWM
from time import sleep

lrs_pin=15

lsr_con=Pin(lsr_pv,mode=Pin.OUT)
lsr_con.on()
sleep(3)
lsr_con.off()
