import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
from PyTFThickness_Module_Register import His_Upt
from PyTFThickness_Module_Read_Write import Rep_Fil_Txt

from RPi. GPIO import setwarnings,setmode,setup,output,cleanup,BOARD,OUT,HIGH,LOW
from os.path import exists
from sys import exit
from numpy import array,zeros,linspace
from time import sleep,time
from serial import Serial

class Pico_Brd:

	#Pico_Write=(Reaspberry) Pico Send
	def Pico_Write(self,pi3_cmd_send):
		pi3_cmd_bytes=str.encode(pi3_cmd_send)
		self.pico_usb.write(pi3_cmd_bytes)	
		return
		
	#Pico_Read=(Reaspberry) Pico Read
	def Pico_Read(self,byts):
		pico_cmd_bytes=self.pico_usb.read(byts)
		pico_cmd_read=pico_cmd_bytes.decode("ascii")
		return pico_cmd_read

	def Pico_Reset(self):
		setmode(BOARD) #Use pin numbers (not GPIO numbers!)
		setwarnings(False)
		setup(mod_ipr.Srv_Rpb_3b_ofp,OUT) #Using pin 3 (= GPIO 2) for pico reset
		output(mod_ipr.Srv_Rpb_3b_ofp,HIGH)
		sleep(4)
		output(mod_ipr.Srv_Rpb_3b_ofp,LOW)
		sleep(6)
		return
		
	def Pico_Off(self):
		cleanup()
		return
		
	def Pico_Ini(self,his_fil):
		self.srv_dev_mth=True
		His_Upt(his_fil,1,'Search compleated. The servo command port was found in '+self.srv_dev_fnd)
		His_Upt(his_fil,1,'Configuration of servo and adc objects started.')
		self.r_ang_val=linspace(start=mod_ipr.R_Ang_Rng[0],stop=mod_ipr.R_Ang_Rng[1],num=mod_ipr.R_Ang_Num)
		self.srv_pht_pul=self.srv_pht_ang_to_pul(mod_ipr.R_Ang_Num,self.r_ang_val)
		self.srv_lsr_pul=self.srv_lsr_ang_to_pul(mod_ipr.R_Ang_Num,self.r_ang_val)
		self.srv_pht_ref_pul=self.srv_pht_ang_to_pul(1,[90])
		self.srv_lsr_ref_pul=self.srv_lsr_ang_to_pul(1,[90])
		self.pico_usb=Serial(port=self.srv_dev_fnd,baudrate=mod_ipr.Srv_Pico_Frq,bytesize=8)
		pi3_cmd="C"+"\t"+str(mod_ipr.Srv_X_Pin)+"\t"+str(mod_ipr.Srv_Y_Pin)+"\t"+str(mod_ipr.Srv_Pht_Pin)+"\t"+str(mod_ipr.Srv_Lsr_Pin)+"\n"
		self.Pico_Write(pi3_cmd)
		pi3_cmd="C"+"\t"+str(mod_ipr.Srv_X_Frq)+"\t"+str(mod_ipr.Srv_Y_Frq)+"\t"+str(mod_ipr.Srv_Pht_Frq)+"\t"+str(mod_ipr.Srv_Lsr_Frq)+"\n"
		self.Pico_Write(pi3_cmd)
		pi3_cmd="C"+"\t"+str(int(mod_ipr.Srv_X_FSB[0]/1e5))+"\t"+str(int(mod_ipr.Srv_X_FSB[1]/1e5))+"\t"+str(int(mod_ipr.Srv_X_FSB[2]/1e5))+"\t"+str(int(mod_ipr.Srv_Y_FSB[0]/1e5))+"\t"+str(int(mod_ipr.Srv_Y_FSB[1]/1e5))+"\t"+str(int(mod_ipr.Srv_Y_FSB[2]/1e5))+"\n"
		self.Pico_Write(pi3_cmd)		
		pico_cmd=self.Pico_Read(9)
		His_Upt(his_fil,2,pico_cmd)
		pi3_cmd="C"+"\t"+str(mod_ipr.Pht_Pin)+"\t"+str(mod_ipr.Lsr_Pin)+"\t"+str(mod_ipr.Vol_Pin)+"\t"+str(mod_ipr.Lsr_StS)+"\t"+str(mod_ipr.Pht_Scns)+"\n"
		self.Pico_Write(pi3_cmd)
		pico_cmd=self.Pico_Read(9)
		His_Upt(his_fil,2,pico_cmd)
		pi3_cmd="C"+"\t"+str(mod_ipr.IR_SXC_Pin)+"\t"+str(mod_ipr.IR_SX1_Pin)+"\t"+str(mod_ipr.IR_SX2_Pin)+"\n"
		self.Pico_Write(pi3_cmd)
		pi3_cmd="C"+"\t"+str(mod_ipr.IR_SYC_Pin)+"\t"+str(mod_ipr.IR_SY1_Pin)+"\t"+str(mod_ipr.IR_SY2_Pin)+"\n"
		self.Pico_Write(pi3_cmd)
		pico_cmd=self.Pico_Read(9)		
		His_Upt(his_fil,2,pico_cmd)
		pico_cmd=self.Pico_Read(9)		
		His_Upt(his_fil,2,pico_cmd)
		self.W_Det(his_fil)
		His_Upt(his_fil,1,'Configuration of servo object complete!')
		return

	#Initialization of the class Servo Initialization.
	#This function will found all USB servo controller devices conected to the computer.
	#Parameters.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.
	def __init__(self,his_fil):
		His_Upt(his_fil,0,'*****Checking Servo-Motors devices*****')
		His_Upt(his_fil,1,'Searching for the servo command port in the range '+mod_ipr.Srv_Cmd_Prt+str(0)+' - '+mod_ipr.Srv_Cmd_Prt+str(mod_ipr.Srv_Sea_Ran)+' ...')
		self.Pico_Reset()
		self.srv_dev_mth=False #srv_dev_mth=servo device match.
		self.srv_dev_fnd=None #srv_dev_fnd=servo device founded.
		self.srv_xw=mod_ipr.Srv_X_W #srv_xw=servo x w.
		self.srv_yw=mod_ipr.Srv_Y_W #srv_xw=servo y w.
		self.srv_xwv_cnv=int(1e3*mod_ipr.Rai_X_DpR*self.srv_xw/360) #srv_xwv_cnv=servo x vw convertion.
		self.srv_ywv_cnv=int(1e3*mod_ipr.Rai_Y_DpR*self.srv_yw/360) #srv_ywv_cnv=servo y vw convertion.
		self.srv_xct=int(0.5*mod_ipr.Rai_X_DST/self.srv_xwv_cnv)
		self.srv_yct=int(0.5*mod_ipr.Rai_Y_DST/self.srv_ywv_cnv)
		self.srv_xddt=int(1e3*mod_ipr.Srv_X_DdT) #srv_xddt=servo x dead time.
		self.srv_yddt=int(1e3*mod_ipr.Srv_Y_DdT) #srv_yddt=servo y dead time.
		self.srv_pht_m=mod_ipr.Srv_Pht_m #srv_pht_m=servo phototransistor m (slope). float variable. Units in radians/grades.
		self.srv_pht_b=mod_ipr.Srv_Pht_b #srv_pht_b=servo phototransistor b (intercep). float variable. Units in radians.
		self.srv_lsr_m=mod_ipr.Srv_Lsr_m #srv_lsr_m=servo laser m (slope). float variable. Units in radians/grades.
		self.srv_lsr_b=mod_ipr.Srv_Lsr_b #srv_lsr_b=servo laser b (intercep). float variable. Units in radians.
		self.r_ang_val=zeros(shape=(mod_ipr.R_Ang_Num),dtype=int,order='F') #srv_ang=servo reflection angles.
		self.r_ang_ref=zeros(shape=(2),dtype=int,order='F') #r_ang_ref=reflectance angle reference.
		self.srv_pht_pul=zeros(shape=(mod_ipr.R_Ang_Num),dtype=int,order='F') #srv_azi=servo azimutal pulses.
		self.srv_lsr_pul=zeros(shape=(mod_ipr.R_Ang_Num),dtype=int,order='F') #srv_ele=servo elevation pulses.
		self.srv_pht_ref_pul=zeros(shape=(1),dtype=int,order='F')
		self.srv_lsr_ref_pul=zeros(shape=(1),dtype=int,order='F')
		self.srv_pico_usb=None #srv_pico_usb=servo pico usb.
		self.Pico_Reset()
		for i_tst_rng in range(0,mod_ipr.Srv_Sea_Ran,1): #i_tst_rng=i-counter test range.
			self.srv_dev_fnd=mod_ipr.Srv_Cmd_Prt+str(i_tst_rng)
			if exists(mod_ipr.Srv_Cmd_Prt+str(i_tst_rng))==True:
				self.Pico_Ini(his_fil)
				break
		if self.srv_dev_mth==False: 
			His_Upt(his_fil,1,'Search compleated. Error, the servo command port was not found in the range provided. Increase the search range or check servo controller conection. Measurements collection will be stopped.')
			exit('Error. The servo command port was not found in the range provided. Increase the search range or check servo controller conection.')

	#srv_pht_ang_to_pul=servo phototransistor angle to pulse
	def srv_pht_ang_to_pul(self,pht_num,pht_ang):
		pht_pul=zeros(shape=(pht_num),dtype=int,order='F')
		for ang_pul in range(pht_num):
		    pht_pul[ang_pul]=int(self.srv_pht_m*pht_ang[ang_pul]+self.srv_pht_b)
		return pht_pul

	#srv_lsr_ang_to_pul=servo laser angle to pulse
	def srv_lsr_ang_to_pul(self,lsr_num,lrs_ang):
		lsr_pul=zeros(shape=(lsr_num),dtype=int,order='F')
		for ang_pul in range(lsr_num):
			lsr_pul[ang_pul]=int(self.srv_lsr_m*lrs_ang[ang_pul]+self.srv_lsr_b)
		return lsr_pul

	#XY_Set=XY Set.
	#Parameters.
		#ax_set=axis set. String parameter. This parameter indicates the axis of movement.	
		#ax_dir=axis direction. String parameter. This parameter indicates the direction of movement.
		#ax_tim=axis time. String parameter. This parameter indicates the time of movement. Units in us.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.	
	def XY_Set(self,ax_set,ax_dir,ax_cen,ax_tim,his_fil):
		ddt=0
		if ax_set=="X": ddt=self.srv_xddt
		elif ax_set=="Y": ddt=self.srv_yddt
		pi3_cmd=ax_set+"\t"+ax_dir+"\t"+ax_cen+"\t"+str(int(ax_tim+ddt))+"\n"
		self.Pico_Write(pi3_cmd)
		pico_cmd=self.Pico_Read(12)
		His_Upt(his_fil,2,pico_cmd)
		return pico_cmd
	
	#XY_UC=XY Until Completition
	#Parameters.
		#ax_set=axis set. String parameter. This parameter indicates the axis of movement.	
		#ax_dir=axis direction. String parameter. This parameter indicates the direction of movement.
	def XY_UC(self,ax_set,ax_dir):
		pico_cmd,con_xy="",True
		while con_xy:
			pi3_cmd=ax_set+"\t"+ax_dir+"\t"+"M"+"\t"+str(5000)+"\n"
			self.Pico_Write(pi3_cmd)
			pico_cmd=self.Pico_Read(12) 
			if pico_cmd!="Mov"+ax_set+ax_dir+"M******": con_xy=False
		return pico_cmd
		
	#W_TDel=W Time Delta.
	#Parameters.
		#ax_set=axis set. String parameter. This parameter indicates the axis of movement.	
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.		
	def W_TDel(self,ax_set,his_fil):
		pico_cmd=self.XY_UC(ax_set,"F")
		His_Upt(his_fil,2,pico_cmd)
		tim_sta=time()
		pico_cmd=self.XY_UC(ax_set,"B")
		His_Upt(his_fil,2,pico_cmd)
		tim_end=time()
		tim_del=(tim_end-tim_sta)
		return tim_del
		
	#W_Det=W Det.
	#Parameters.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.	
	def W_Det(self,his_fil):
		His_Upt(his_fil,1,"Starting determination of angular velocity W")
		if mod_ipr.Srv_X_W_Mea==True:
			His_Upt(his_fil,2,"Determination of angular velocity Wx in X")
			self.srv_xct=self.W_TDel("X",his_fil)/2
			self.srv_xw=360*1e3*(mod_ipr.Rai_X_DST/mod_ipr.Rai_X_DpR)/(2*self.srv_xct)
			self.srv_xwv_cnv=mod_ipr.Rai_X_DpR*self.srv_xw #srv_xwv_cnv=servo x vw convertion.
		if mod_ipr.Srv_Y_W_Mea==True:
			His_Upt(his_fil,2,"Determination of angular velocity Wy in Y")
			self.srv_yct=self.W_TDel("Y",his_fil)/2
			self.srv_yw=360*1e3*(mod_ipr.Rai_Y_DST/mod_ipr.Rai_Y_DpR)/(2*self.srv_yct)
			self.srv_ywv_cnv=mod_ipr.Rai_Y_DpR*self.srv_yw/360 #srv_ywv_cnv=servo y vw convertion.
		self.srv_xwv_cnv=1e-9*mod_ipr.Rai_X_DpR*self.srv_xw/360
		self.srv_ywv_cnv=1e-9*mod_ipr.Rai_Y_DpR*self.srv_yw/360
		His_Upt(his_fil,1,"Ending determination of angular velocity W")
		return		
		
	def XY_C_Mvm(self,ax_set,ax_tim,ax_sen,his_fil):
		pico_cmd=self.XY_Set(ax_set,"F","C",ax_tim,his_fil)
		pico_cmd_arr=array(list(pico_cmd))
		if pico_cmd_arr[ax_sen]=="1": His_Upt(his_fil,3,"Center "+ax_set+" reached")
		else: 
			pico_cmd=self.XY_Set(ax_set,"B","C",ax_tim,his_fil)
			pico_cmd_arr=array(list(pico_cmd))
			if pico_cmd_arr[ax_sen]=="1": His_Upt(his_fil,3,"Center "+ax_set+" reached")
			else: 
				His_Upt(his_fil,3,"Center "+ax_set+" cannot be reached. Check equiment")
				exit()
		return
		
	#XY_C=XY Center.
	#Parameters.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.	
	def XY_C(self,his_fil):
		His_Upt(his_fil,1,"Starting centering XY planes")
		self.srv_xc_tim=int(mod_ipr.Rai_X_DST/self.srv_xwv_cnv)
		self.srv_yc_tim=int(mod_ipr.Rai_Y_DST/self.srv_ywv_cnv)
		His_Upt(his_fil,2,"Centering X axis...")
		self.XY_C_Mvm("X",self.srv_xc_tim,6,his_fil)
		His_Upt(his_fil,2,"Centering Y axis...")
		self.XY_C_Mvm("Y",self.srv_yc_tim,9,his_fil)
		His_Upt(his_fil,1,"Ending centering XY planes")
		return

	#XY_Mvm=XY Movement.
	#Parameters.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.	
	def XY_Mvm(self,xyp,xya,xa_n,ya_m,xynm,xyt,his_fil):
		x_del,y_del=xya[0]-xyp[0],xya[1]-xyp[1]
		srv_xm_tim,srv_ym_tim=int(abs(x_del)/self.srv_xwv_cnv),int(abs(y_del)/self.srv_ywv_cnv)
		rch_msg="Moving to xy point "+str(xynm)+"/"+str(xyt)+" equal to:" 
		rch_msg+="\t"+"X["+str(xa_n)+"]["+str(ya_m)+"]="+"{:.5f}".format(xya[0])
		rch_msg+="\t"+"Y["+str(xa_n)+"]["+str(ya_m)+"]="+"{:.5f}".format(xya[1])
		rch_msg+=" ..."
		His_Upt(his_fil,2,rch_msg)
		if x_del<0: pico_cmd=self.XY_Set("X","B","M",srv_xm_tim,his_fil)
		elif x_del>0: pico_cmd=self.XY_Set("X","F","M",srv_xm_tim,his_fil)
		if y_del<0: pico_cmd=self.XY_Set("Y","B","M",srv_ym_tim,his_fil)
		elif y_del>0: pico_cmd=self.XY_Set("Y","F","M",srv_ym_tim,his_fil)
		His_Upt(his_fil,2,"...completed")
		return
		
	#Tht_Set=Theta Set.
	#Parameters.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.	
	def Tht_Set(self,t_n,his_fil):
		T_pico_cmd="T"+"\t"+str(self.srv_pht_pul[t_n])+"\t"+str(self.srv_lsr_pul[t_n])+"\n"
		self.Pico_Write(T_pico_cmd)
		pico_cmd=self.Pico_Read(8)
		if pico_cmd!="": His_Upt(his_fil,3,"")
		else: His_Upt(his_fil,3,"")
		return 
		
	#Tht_Ref=Theta Reference.
	#Parameters.
		#his_fil=history file. String parameter. This parameter indicates the path to find the history file.	
	def Tht_Ref(self,his_fil):
		T_pico_cmd="T"+"\t"+str(self.srv_pht_ref_pul[0])+"\t"+str(self.srv_lsr_ref_pul[0])+"\n"
		self.Pico_Write(T_pico_cmd)
		pico_cmd=self.Pico_Read(8)
		if pico_cmd!="": His_Upt(his_fil,3,"")
		else: His_Upt(his_fil,3,"")
		return 
