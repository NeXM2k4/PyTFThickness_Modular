from machine import Pin,PWM
from time import sleep

led_pin=Pin(25,Pin.OUT)
led_pin(1)

lrs_pin=5
pht_pin=4
lrs_frq=50
pht_frq=50

tht_sta=25
tht_end=90
tht_stp=2
#Servo Lsr
lsr_m=-(2.5-0.1)*1e6/180 #2.0e6==> 90   0.05 ==> 35
lsr_b=1.5e6 #b=3.0e6#  ==> 0    1.75 ==> 180
#Servo Pht
pht_m=-(2.2-1.0)*1e6/180 #0.80e6 ==> 90   0.05 ==> 35
pht_b=1.5e6 #1.75e6 ==> 0    1.75 ==> 180

lsr_srv=PWM(Pin(lrs_pin,mode=Pin.OUT))
pht_srv=PWM(Pin(pht_pin,mode=Pin.OUT))
lsr_srv.freq(lrs_frq)
pht_srv.freq(pht_frq)
while True:
    for theta in range(tht_sta,tht_end,tht_stp):
        lsr_pulse=int(lsr_m*theta+lsr_b)
        pht_pulse=int(pht_m*theta+pht_b)
        lsr_srv.duty_ns(pht_pulse)
        pht_srv.duty_ns(pht_pulse)
        print(theta,lsr_pulse,pht_pulse)
        sleep(0.5)