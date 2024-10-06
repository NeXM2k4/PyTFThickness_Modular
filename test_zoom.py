import time
import matplotlib.pyplot as plt
from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_still_configuration() 
picam2.configure(preview_config)

picam2.start()
time.sleep(2)

size = picam2.capture_metadata()['ScalerCrop'][2:]
full_res = picam2.camera_properties['PixelArraySize']

for _ in range(20):
    # This syncs us to the arrival of a new camera frame:
    data16=picam2.capture_metadata("raw")
    size = [int(s * 0.95) for s in size]
    print("S",size)
    offset = [(r - s) // 2 for r, s in zip(full_res, size)]
    print("O",offset)
    print("sum",offset + size)
    picam2.set_controls({"ScalerCrop": offset + size})
    cam_shw=plt.figure("Capture")
    cam_shw.clear()
    cam_shw.suptitle("plt_control",fontsize=10)
    plt.imshow(data16)
    #plt_name=cap_fil+".png"    
    #plt.savefig(plt_name)
    time.sleep(0.5)
