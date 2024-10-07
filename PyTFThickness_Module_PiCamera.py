from picamera2 import Picamera2
#from libcamera.controls.AfModeEnum import Manual
import matplotlib.pyplot as plt
from numpy import uint16,sum

def CamStart():
	picam2=Picamera2()
	config=picam2.create_still_configuration(raw={'format':'SBGGR10','size':(3280, 2464)})
	picam2.configure(config)
	picam2.set_controls({"ExposureTime": 100000, "AnalogueGain": 1.0, "AwbEnable": False})
	return picam2


def Pix_Inten(pico_obj,pico_ord,picam2_obj,cap_lab,cap_fil):
	R_pico_cmd=pico_ord+"\n"
	pico_obj.Pico_Write(R_pico_cmd)
	picam2_obj.start()
	data8=picam2_obj.capture_array('raw') #capture_array('raw')
	data16=data8.view(uint16)
	data16=data16[1000:1800,1400:2100]
	data16=data16/1024
    
	cam_shw=plt.figure("Capture")
	cam_shw.clear()
	cam_shw.suptitle(cap_lab,fontsize=10)
    
	plt.imshow(data16,cmap="gray",vmin=0,vmax=1)  
	plt.colorbar()
	plt_name=cap_fil+".png"    
	plt.savefig(plt_name)
    
	#plt.close()
	pix_int_rscl=sum(data16)/(800*700)
	if pico_ord=="D": print("Offset:",pix_int_rscl)
	else: print("Measure:",pix_int_rscl)
	picam2_obj.stop()
	#picam2_obj.close()
	return picam2_obj,pix_int_rscl

def CameraStart():    
    picam2 = Picamera2()
    config = picam2.create_still_configuration(raw={'format':'SBGGR10','size':(3280,2464)}) #820*4,616*4
    picam2.configure(config)
    picam2.set_controls({"ExposureTime":100000,"AnalogueGain":1.0,"AwbEnable":False,"ScalerCrop":(1210,924,3280,2464)}) #"AfState":Manual,"LensPosition":0
    return picam2
