import sys
from machine import Pin,PWM,ADC
from utime import sleep_ms,sleep_us,ticks_us,ticks_diff

led_pin=Pin(25,Pin.OUT)
led_blk=10
srv_wat_tim=1
V_cnv=(3.3/65535)*1e4 #convertion of analog signal to digital signal
pls_cnv=1e5

def led_on_off(state):
    if state==True: led_pin(1)
    else: led_pin(0)

def led_blink(blk_num):
    state_on_off=False
    led_on_off(False)
    for blk in range(blk_num): 
        if state_on_off: state_on_off=False
        else: state_on_off=True
        led_on_off(state_on_off)
        sleep_ms(srv_wat_tim)
    led_on_off(True)

def Pi3_Read(complete,num):
    pi3_cmd_read=sys.stdin.readline().strip() 
    pi3_cmd_slc=pi3_cmd_read.split()
    return pi3_cmd_slc
    
def Pi3_Write(pico_cmd_wrt):
    pico_cmd_wrt_bytes=str.encode(pico_cmd_wrt)
    sys.stdout.write(pico_cmd_wrt_bytes)
    return

def Pi3_VW(vol_mea_int):
    vol_mea_str=""
    if vol_mea_int<10: vol_mea_str=str(0)+str(0)+str(0)+str(0)+str(vol_mea_int)
    elif vol_mea_int<100: vol_mea_str=str(0)+str(0)+str(0)+str(vol_mea_int)
    elif vol_mea_int<1000: vol_mea_str=str(0)+str(0)+str(vol_mea_int)
    elif vol_mea_int<10000: vol_mea_str=str(0)+str(vol_mea_int)
    else: vol_mea_str=str(vol_mea_int)
    Pi3_Write(vol_mea_str)
    return

if __name__=='__main__':
    pico_on=True
    led_on_off(pico_on)
    srv_x_pwm,srv_y_pwm,srv_pht_pwm,srv_lsr_pwm=None,None,None,None
    srv_x_pin,srv_y_pin,srv_pht_pin,srv_lsr_pin=None,None,None,None
    srv_x_frq,srv_y_frq,srv_pht_frq,srv_lsr_frq=None,None,None,None
    srv_x_pul,srv_y_pul,srv_pht_pul,srv_lsr_pul=None,None,None,None
    srv_x_wb,srv_x_ws,srv_x_wf,srv_y_wb,srv_y_ws,srv_y_wf=None,None,None,None,None,None
    pht_pin,lsr_pin,v_pin,lsr_stb,v_scns=None,None,None,None,None
    pht_sen,lsr_sen,v_sen=None,None,None
    ir_xc_pin,ir_yc_pin,ir_x1_pin,ir_x2_pin,ir_y1_pin,ir_y2_pin=None,None,None,None,None,None
    xc_sen,yc_sen,x1_sen,x2_sen,y1_sen,y2_sen=None,None,None,None,None,None
    while pico_on:
        pi3_cmd=Pi3_Read(True,0)
        if pi3_cmd[0]=="C": #C=Config Servo Motors and sensors.
            if srv_x_pin is int: srv_x_pwm.close()
            if srv_y_pin is int: srv_y_pwm.close()
            if srv_pht_pin is int: srv_pht_pwm.close()  
            if srv_lsr_pin is int: srv_lsr_pwm.close()  
            if pht_pin is int: pht_sen.close()
            if lsr_pin is int: lsr_sen.close() 
            if v_pin is int: v_sen.close() 
            if ir_xc_pin is int: xc_sen.close() 
            if ir_x1_pin is int: x1_sen.close()
            if ir_x2_pin is int: x2_sen.close()
            if ir_yc_pin is int: yc_sen.close() 
            if ir_y1_pin is int: y1_sen.close()
            if ir_y2_pin is int: y2_sen.close() 
            srv_x_pin,srv_y_pin,srv_pht_pin,srv_lsr_pin=int(pi3_cmd[1]),int(pi3_cmd[2]),int(pi3_cmd[3]),int(pi3_cmd[4])
            pi3_cmd=Pi3_Read(True,0)
            srv_x_frq,srv_y_frq,srv_pht_frq,srv_lsr_frq=int(pi3_cmd[1]),int(pi3_cmd[2]),int(pi3_cmd[3]),int(pi3_cmd[4])
            srv_x_pwm=PWM(Pin(srv_x_pin,mode=Pin.OUT))
            srv_y_pwm=PWM(Pin(srv_y_pin,mode=Pin.OUT))
            srv_pht_pwm=PWM(Pin(srv_pht_pin,mode=Pin.OUT))
            srv_lsr_pwm=PWM(Pin(srv_lsr_pin,mode=Pin.OUT))
            srv_x_pwm.freq(srv_x_frq)
            srv_y_pwm.freq(srv_y_frq)
            srv_pht_pwm.freq(srv_pht_frq)
            srv_lsr_pwm.freq(srv_lsr_frq)
            pi3_cmd=Pi3_Read(True,0)
            srv_x_wb,srv_x_ws,srv_x_wf,srv_y_wb,srv_y_ws,srv_y_wf=int(pi3_cmd[1]),int(pi3_cmd[2]),int(pi3_cmd[3]),int(pi3_cmd[4]),int(pi3_cmd[5]),int(pi3_cmd[6])
            srv_x_wb,srv_x_ws,srv_x_wf,srv_y_wb,srv_y_ws,srv_y_wf=int(srv_x_wb*pls_cnv),int(srv_x_ws*pls_cnv),int(srv_x_wf*pls_cnv),int(srv_y_wb*pls_cnv),int(srv_y_ws*pls_cnv),int(srv_y_wf*pls_cnv)
            Pi3_Write("SrvMotSet")
            pi3_cmd=Pi3_Read(True,0)
            pht_pin,lsr_pin,v_pin,lsr_stb,v_scns=int(pi3_cmd[1]),int(pi3_cmd[2]),int(pi3_cmd[3]),int(pi3_cmd[4]),int(pi3_cmd[5])
            pht_sen=Pin(pht_pin,mode=Pin.OUT)
            pht_sen.on()
            lsr_sen=Pin(lsr_pin,mode=Pin.OUT)
            lsr_sen.off()
            v_adc_in=Pin(v_pin,mode=Pin.IN)
            v_sen=ADC(v_adc_in)  
            Pi3_Write("PLVSenSet")      
            pi3_cmd=Pi3_Read(True,0)
            ir_xc_pin,ir_x1_pin,ir_x2_pin=int(pi3_cmd[1]),int(pi3_cmd[2]),int(pi3_cmd[3])
            pi3_cmd=Pi3_Read(True,0)
            ir_yc_pin,ir_y1_pin,ir_y2_pin=int(pi3_cmd[1]),int(pi3_cmd[2]),int(pi3_cmd[3])
            xc_sen=Pin(ir_xc_pin,Pin.IN)
            x1_sen=Pin(ir_x1_pin,Pin.IN)
            x2_sen=Pin(ir_x2_pin,Pin.IN)
            yc_sen=Pin(ir_yc_pin,Pin.IN)
            y1_sen=Pin(ir_y1_pin,Pin.IN)
            y2_sen=Pin(ir_y2_pin,Pin.IN)
            Pi3_Write("IRsSenSet")   
            Pi3_Write("AllSSPSet")
        elif pi3_cmd[0]=="X" or pi3_cmd[0]=="Y":
            srv_axs,srv_dir,srv_cen,srv_xy_tim=pi3_cmd[0],pi3_cmd[1],pi3_cmd[2],int(pi3_cmd[3])
            if srv_axs=="X":
                if srv_dir=="B": srv_x_pwm.duty_ns(srv_x_wb)
                elif srv_dir=="F": srv_x_pwm.duty_ns(srv_x_wf)
            elif srv_axs=="Y":
                if srv_dir=="B": srv_y_pwm.duty_ns(srv_y_wb)
                elif srv_dir=="F": srv_y_pwm.duty_ns(srv_y_wf)
            led_blink(led_blk)
            pico_cmd="Mov"+srv_axs+srv_dir+srv_cen+"******"
            tim_mvm=0
            t_ls,t_le=0,0
            while tim_mvm<srv_xy_tim:
                t_ls=ticks_us()
                xb,xf,yf,yb=x1_sen.value(),x2_sen.value(),y1_sen.value(),y2_sen.value()
                xc,yc=xc_sen.value(),yc_sen.value()
                mvm_stp=False
                if srv_axs=="X" and srv_dir=="F" and xf==0: mvm_stp=True
                elif srv_axs=="X" and srv_dir=="B" and xb==0: mvm_stp=True
                elif srv_axs=="Y" and srv_dir=="F" and yf==0: mvm_stp=True
                elif srv_axs=="Y" and srv_dir=="B" and yb==0: mvm_stp=True
                if srv_axs=="X" and srv_cen=="C" and xc==1: mvm_stp=True
                elif srv_axs=="Y" and srv_cen=="C" and yc==1: mvm_stp=True
                if mvm_stp:
                    srv_x_pwm.duty_ns(srv_x_ws)
                    srv_y_pwm.duty_ns(srv_y_ws)
                    pico_cmd="Mov"+srv_axs+srv_dir+srv_cen+str(xc)+str(xb)+str(xf)+str(yc)+str(yb)+str(yf)
                    break
                else: 
                    t_le=ticks_us()
                    tim_mvm+=ticks_diff(t_le,t_ls)
                    sleep_us(1)
            if pi3_cmd[0]=="X": srv_x_pwm.duty_ns(srv_x_ws)
            elif pi3_cmd[0]=="Y": srv_y_pwm.duty_ns(srv_y_ws)             
            Pi3_Write(pico_cmd)
        elif pi3_cmd[0]=="T": #Set theta for laser and phototransistor
            srv_pht_pwm.duty_ns(int(pi3_cmd[1]))
            srv_lsr_pwm.duty_ns(int(pi3_cmd[2]))
            sleep_ms(1500)
            Pi3_Write("SetThtPL")
        elif pi3_cmd[0]=="U": #Make v measurement
            lsr_sen.on()
            #sleep_ms(lsr_stb)
            #vol_val=int(V_cnv*v_sen.read_u16())
            #Pi3_VW(vol_val)
            #lsr_sen.off()
            #sleep_ms(lsr_stb)
        elif pi3_cmd[0]=="D": #Make v offset
            lsr_sen.off()
            #sleep_ms(lsr_stb)
            #vol_val=int(V_cnv*v_sen.read_u16())
            #Pi3_VW(vol_val)
        elif pi3_cmd[0]=="F":  pico_on=False #F=Finish
        else: Pi3_Write("DatRecBad")
    led_on_off(pico_on)
