from machine import Pin,PWM,ADC
from time import sleep

pht_pv=26
lsr_pv=27
vlt_pv=28
lrs_pin=5
lrs_pwm=1.5e6
lrs_frq=50
pht_pin=4
pht_pwm=1.5e6
pht_frq=50

V_cnv=(3.3/65535)*1e4

v_adc_in=Pin(vlt_pv,mode=Pin.IN)
v_sen=ADC(v_adc_in) 
lsr_pvv=Pin(lsr_pv,mode=Pin.OUT)
lsr_pvv.on()
pht_pvv=Pin(pht_pv,mode=Pin.OUT)
pht_pvv.on()
lsr_srv=PWM(Pin(lrs_pin,mode=Pin.OUT))
pht_srv=PWM(Pin(pht_pin,mode=Pin.OUT))
lsr_srv.freq(lrs_frq)
pht_srv.freq(pht_frq)
while True:
    lrs_pwm=input("Pulse for channel "+str(lrs_pin)+":"+"\t")
    lrs_pwm=int((1e6*float(lrs_pwm)))
    print("Pulse send:",lrs_pwm)
    lsr_srv.duty_ns(lrs_pwm)
    pht_pwm=input("Pulse for channel "+str(pht_pin)+":"+"\t")
    pht_pwm=int((1e6*float(pht_pwm)))
    print("Pulse send:",pht_pwm)
    pht_srv.duty_ns(pht_pwm)
    n,m=0,0
    vol_val=0
    while True:#m<1000:
        vol_val+=int(V_cnv*v_sen.read_u16())
        n+=1
        m+=1
        if n==10:
            print(int(vol_val/10))
            vol_val,n=0,0
            sleep(0.1)
    sleep(1)