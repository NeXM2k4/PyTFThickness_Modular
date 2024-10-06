from machine import Pin,PWM
from time import sleep

w=1.3e6
srv_pin=3 #3
sen_pin=16 #17

srv_ax=PWM(Pin(srv_pin,mode=Pin.OUT))
srv_ax.freq(50)

sen_obj=Pin(sen_pin,mode=Pin.IN)
while True:
    srv_ax.duty_ns(int(w))
    sleep(1)
    srv_ax.duty_ns(int(1.5e6))
    print(sen_obj.value())
    