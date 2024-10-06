###################################################################################
##PyMA&ZDOAS Module Initial Parameters -- Version 1.5                                ##
##The parameters on this module are used to adjust the measurements of MA&ZDOAS.##
###################################################################################

#Directories path settings.
Dir_Sav_Mai_Pth='/home/cisneros/Documentos/PyTFThickness/' #Dir_Sav_Mai_Pth=Directory Save Main Path. String parameter. No units.
Dir_Sav_Scn_Pth='V_Time_Scans/' #Dir_Sav_Mai_Pth=Directory Save Main Path. String parameter. No units.
Dir_Sav_Tht_Pth='V_Theta_Points/' #Dir_Sav_Mai_Pth=Directory Save Main Path. String parameter. No units.
Dir_Sav_XYZ_Pth='XYZN_Values/' #Dir_Sav_Mai_Pth=Directory Save Main Path. String parameter. No units.
Dir_Sav_Cam_Pth='Camera_Captures/' #Dir_Sav_Mai_Pth=Directory Save Main Path. String parameter. No units.

#Time settings.
Cap_Tim_Sta=[0,1,0] #Cap_Tim_Sta=Capture Time Start. Integer array of [3] dimentions. Units on [hours,minutes,seconds]. 24 hours format used.
Cap_Tim_Fin=[23,59,0] #Cap_Tim_Fin=Capture Time Finish. Integer array of [3] dimentions. Units on [hours,minutes,seconds]. 24 hours format used.
Cap_Tim_Sta_Wai_His=1 #Cap_Tim_Sta_Wai_His=Capture Time Start Waiting History. Integer parameter. Units on Hours.
Cap_Tim_Sta_Wai_Scr=50 #Cap_Tim_Sta_Wai_Scr=Capture Time Start Waiting Screen. Integer parameter. Units on seconds.

#Measurement angles settings.
R_Ang_Num=20 #R_Ang_Num=Reflectance Angles Number. Integer parameter. No units.
R_Ext_Ang_Num=30 #R_Ext_Ang_Num=Reflectance Extended Angles Number. Integer parameter. No units.
R_Ang_Rng=[25,40]#[25,75]#[22.5,58.5] #R_Ang_Rng=Azimutal Angles Range. Float array of [R_Ang_Num] dimension. Units in Degrees.
	#Minimun angle recomened is 25 degrees. Least than that and there is risk of colisition between sensors.
R_V_Nrm_Mea=False#True
R_V_Nrm=2000	
	
#Measurement XY settings.
X_Range=[-1.5,+1.5] #X_Range=X range. Float parameter. Units in mm.
Y_Range=[-1.5,+1.5] #Y_Range=Y range. Float parameter. Units in mm.
X_Pnts=10 #X_Pnts=X Points. Integer parameter. No units.
Y_Pnts=10 #Y_Pnts=Y Points. Integer parameter. No units.

#Data storage settings.
Dat_Fld_Nam="TFT_Measurements_" #Dat_Fld_Nam=Data Folder Measurement. String parameter. No units.
Dat_Cnt_Nam="TFT_Measurements_Control_" #Dat_Cnt_Nam=Data Control Name. String parameter. No units.
Dat_His_Nam="TFT_Measurements_History_" #Dat_His_Nam=Data History Name. String parameter. No units.
Dat_Sto_HD5=False #Dat_Sto_DH5=Data Storage Hierarchical Data file 5. Boolean parameter. No units.
Dat_Sto_Txt=True #Dat_Sto_Tex=Data Storage Text file. Boolean parameter. No units.
Dat_Cnt_CHe=[['Set','Azimutal','Elevation','time','Temp Outside','Temp Inside'],['No units','degrees','degrees','hours','C','C']] #Dat_Cnt_CHe=Data Control Column Headers. String array of [2][5] dimention. No units.

#Servo-motor settings.
Srv_Cmd_Prt='/dev/ttyACM' #Srv_Cmd_Prt=Servo Command Port. String variable. No units.
Srv_Rpb_3b_ofp=3 #Srv_Rpb_3b_ofp=Servo Raspberry 3b+ on off pico. Integer variable. No units.
Srv_Rpb_Pico_Ser="2e8a:0005" #Srv_Rpb_Pico_Ser=Servo Raspberry Pico Serial. String variable. No units. 
Srv_Pico_Frq=115200 #Srv_Pico_Frq=Servo (Raspberry) Pico Frecuency. String variable. Units in hz.
Srv_Sea_Ran=9 #Srv_Sea_Ran=Servo Search Range. Integer variable. No units.
Srv_Wai_Tim=1 #Srv_Wai_Tim=Servo Waiting Time. Float parameter. Units in s.
Srv_X_W=147 #Srv_X_W=Servo X W. Float parameter. Units degres/s.
Srv_Y_W=143 #Srv_Y_W=Servo Y W. Float parameter. Units degres/s.
Srv_X_W_Mea=False #Srv_X_W_Mea=Servo X W Measure. Boolean parameter. No units.
Srv_Y_W_Mea=False #Srv_Y_W_Mea=Servo Y W Measure. Boolean parameter. No units.
Srv_X_DdT=500 #Srv_X_DdT=Servo X Dead Time. Float parameter. Unit in ms.
Srv_Y_DdT=500 #Srv_Y_DdT=Servo Y Dead Time. Float parameter. Unit in ms.
Srv_X_Pin=2 #Srv_X_Pin=Servo X Pinout. Integer variable. No units.
Srv_Y_Pin=3 #Srv_Y_Pin=Servo Y Pinout. Integer variable. No units.
Srv_Pht_Pin=4 #Srv_Pht_Pin=Servo Phototransistor Pinout. Integer variable. No units.
Srv_Lsr_Pin=5 #Srv_Lsr_Pin=Servo Laser Pinout. Integer variable. No units.
Srv_X_Frq=50 #Srv_X_Frq=Servo X Frecuency. Integer variable. Units in Mhz.
Srv_Y_Frq=50 #Srv_Y_Frq=Servo Y Frecuency. Integer variable. Units in Mhz.
Srv_Pht_Frq=50 #Srv_Pht_Frq=Servo Phototransistor Frecuency. Integer variable. Units in Mhz.
Srv_Lsr_Frq=50 #Srv_Lsr_Frq=Servo Laser Frecuency. Integer variable. Units in Mhz.
Srv_X_FSB=[1.3e6,1.5e6,1.7e6] #Srv_X_FSB=Servo X Foward Stop Backward. Float variable. Units in s.
Srv_Y_FSB=[1.3e6,1.5e6,1.7e6] #Srv_Y_FSB=Servo Y Foward Stop Backward. Float variable. Units in s.
Srv_Pht_m=-0.015e6 #-0.01e6 #(0.5-1.5)*1e6/90 #Srv_Pht_m=Servo Phototransistor m (slope). float variable. Units in radians/grades.
Srv_Pht_b=1.7775e6 #1.5e6 #Srv_Pht_b=Servo Phototransistor b (intercep). float variable. Units in radians. se cambio de 1.8 a 1.7775
Srv_Lsr_m=-0.015e6 #-0.01e6 #(0.55-1.5)*1e6/90 #Srv_Las_m=Servo Laser m (slope). float variable. Units in radians/grades.
Srv_Lsr_b=1.7775e6 #1.5e6 #Srv_Las_b=Servo Laser b (intercep). float variable. Units in radians. se cambio de 1.8 a 1.7775

#Rail settings.
Rai_X_DpR=565 #Rai_X_DpR=Rail X Distance per Revolution. Float variable. Units in um/rev.
Rai_X_DST=35 #2 40-205 #Rai_X_DT=Rail X Distance Sensors Total. Float variable. Units in mm.
Rai_Y_DpR=565 #Rai_X_DpR=Rail Y Distance per Revolution. Float variable. Units in um/rev.
Rai_Y_DST=70 #270-200 #Rai_X_DT=Rail Y Distance Sensors Total. Float variable. Units in mm.

#Sensors settings
Vol_Pin=28 #Vol_Pin=Voltage Pinout. Integer variable. No units.
Pht_Pin=26 #Pht_Pin=Phototransistor Pinout. Integer variable. No units
Lsr_Pin=27 #Lsr_Pin=Laser Pinout. Integer variable. No units.
Lsr_StS=1000 #Lsr_StS=Laser Stability Seconds. Integer variable. Units ms.
Pht_Scns=5 #Pht_Scns=Phototransistor Scans. No units.
IR_SXC_Pin=16 #IR_SXC_Pin=Infra-Red Sensor X Center Pin. Integer variable. No units.
IR_SYC_Pin=17 #IR_SYC_Pin=Infra-Red Sensor Y Center Pin. Integer variable. No units.
IR_SX1_Pin=18 #IR_SX1_Pin=Infra-Red Sensor X 1 Pin. Integer variable. No units.
IR_SX2_Pin=19 #IR_SX2_Pin=Infra-Red Sensor X 2 Pin. Integer variable. No units.
IR_SY1_Pin=20 #IR_SY1_Pin=Infra-Red Sensor Y 1 Pin. Integer variable. No units.
IR_SY2_Pin=21 #IR_SY2_Pin=Infra-Red Sensor Y 2 Pin. Integer variable. No units.

#Measureament fiting settings.
Lsr_Wav=650 #Lsr_Wav=Laser Wavelength. Float variable. Units in nm, tenia escrito 638

#Plot settings.
Plt_Sav=False #Plt_Itn_Sav=Plot Intensities Saving. Boolean parameter. No Units.
Plt_N=6 #Plt_N=Plot N. Integer parameter. No units.
Plt_M=6 #Plt_M=Plot M. Integer parameter. No units.
