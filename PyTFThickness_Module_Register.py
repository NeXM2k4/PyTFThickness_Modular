
import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
import PyTFThickness_Module_Read_Write as mod_raw #mod_raw=module read and write.

from os.path import isdir,isfile,expanduser
from shutil import move 
from os import mkdir,remove
from sys import exit
from datetime import date,datetime
from time import sleep

#Dte_Upt=Date Update.
	#This function will return the actual date of the system.
def Dte_Upt():
	dte_sys=date.today() #dte_sys=date system.
	dte_upt=dte_sys.strftime("%Y"+"_"+"%m"+"_"+"%d") #dte_upt=date update.
	return dte_upt
 
#Tim_Upt=Time Update.
	#This function will return the actual time of the system.
def Tim_Upt():
	tim_sys=datetime.now() #tim_sys=time system.
	tim_upt=tim_sys.strftime("%H:%M:%S") #tim_upt=date update.
	return tim_upt

#Tim_Upt_Int=Time Update Integer.
	#This function will return the actual time of the system.
def Tim_Upt_Int():
	tim_sys=datetime.now() #tim_sys=time system.
	tim_upt=[0,0,0] #tim_upt=date update.
	tim_upt[0]=tim_sys.strftime("%H")
	tim_upt[1]=tim_sys.strftime("%M")
	tim_upt[2]=tim_sys.strftime("%S")
	return tim_upt

#Tim_HMS_Dec_Con=Time Hour Minute Second Decimal Convertion.
	#This function converts form a HMS format to a decimal format.
#Parameters.
	#tim_hms_value=time hour minute second values. Integer array of [3] dimention. This parameter contains the values for the hour, minute and second of a time t.
def Tim_HMS_Dec_Con(tim_hms_value):
	tim_dec_val=float(tim_hms_value[0])+(1/60)*float(tim_hms_value[1])+(1/3600)*float(tim_hms_value[2]) #tim_dec_val=time decimal value.
	return tim_dec_val

#His_Upt=Histoy Update.
	#This function will print relevant information on screen and save it in history file.
#Parameters.
	#his_fil=history file. String parameter. This parameter indicates the path to find the history file.
	#his_lvl=history level. Integer parameter. This parameter indicates the indentation level introduced to the history message.
	#his_msg=history message. String parameter. This parameter indicates the message to be shown and stored.
def His_Upt(his_fil,his_lvl,his_msg):
	his_msg_str='' #his_msg_str=history message string.
	for i_his_lvl in range(0,his_lvl,1): his_msg_str=his_msg_str+'\t' #i_his_lvl=i-counter history message level.
	his_msg_str=his_msg_str+his_msg
	print(his_msg_str)
	mod_raw.His_Fil_Wri(his_fil,his_msg_str)
	return

#Mea_Fol=Measurements Folder.
	#This function will print relevant information on screen and save it in history file.
#Parameters.
	#mea_dte_str=measurement date string. String parameter. This parameter indicates the date when the history file was created.
	#mea_tim_str=measurement time string. String parameter. This parameter indicates the time when the history file was created.
def Mea_Fol(mea_dte_str,mea_tim_str):
	mea_set=0 #mea_set=measurement set.
	his_fil=expanduser("~")+'/'+mod_ipr.Dat_His_Nam+mea_dte_str #his_fil=history file.
	cnt_fil=expanduser("~")+'/'+mod_ipr.Dat_Cnt_Nam+mea_dte_str #cnt_fil=control file.
	sec_pth_nam=[] #sec_pth_nam=secondary path names.
	mod_raw.Cre_Fil_His(his_fil,mea_dte_str,mea_tim_str)
	mod_raw.Wri_Dat_Str_Txt(cnt_fil,mod_ipr.Dat_Cnt_CHe,6,2,'w')		
	His_Upt(his_fil,0,'*****Check directory paths*****')
	His_Upt(his_fil,1,'Checking the existence of the main path ('+mod_ipr.Dir_Sav_Mai_Pth+') for measurements storage...')
	if isdir(mod_ipr.Dir_Sav_Mai_Pth)==True:
		His_Upt(his_fil,1,'Check compleated. The main path ('+mod_ipr.Dir_Sav_Mai_Pth+') for measurements storage was already created. There is no need to create the main path.')
		His_Upt(his_fil,1,'Checking the existence of the secondary paths for measurements storage...')
		sec_pth_nam.append(mod_ipr.Dir_Sav_Mai_Pth+mod_ipr.Dat_Fld_Nam+mea_dte_str)
		sec_pth_nam.append(mod_ipr.Dir_Sav_Scn_Pth)
		sec_pth_nam.append(mod_ipr.Dir_Sav_Tht_Pth)
		sec_pth_nam.append(mod_ipr.Dir_Sav_XYZ_Pth)
		sec_pth_nam.append(mod_ipr.Dir_Sav_Cam_Pth)
		His_Upt(his_fil,2,'Checking path ('+sec_pth_nam[0]+') for measurements storage is going to be checked...')
		for i_sec_pth in range(0,len(sec_pth_nam),1): #i_sec_pth=i-counter secondary paths.
			if i_sec_pth!=0: sec_pth_nam[i_sec_pth]=sec_pth_nam[0]+'/'+sec_pth_nam[i_sec_pth]		
			if isdir(sec_pth_nam[i_sec_pth])==True:
				His_Upt(his_fil,2,'Check compleated. The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage was already created. There is no need to create this secondary path.')
			else:
				His_Upt(his_fil,2,'Check compleated. The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage was not found. Creation of this directory will be attented...')
				mkdir(sec_pth_nam[i_sec_pth])
				if isdir(sec_pth_nam[i_sec_pth])==True: 
					His_Upt(his_fil,3,'The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage was succefully created!!!')
				else:
					His_Upt(his_fil,3,'The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage could not be created!!!')	
					exit('Error path -'+sec_pth_nam[i_sec_pth]+'- could not be created. The  history file will be saved at -'+his_fil+'-.')
			if i_sec_pth==0:
				his_fil_new_pth=sec_pth_nam[0]+'/'+mod_ipr.Dat_His_Nam+mea_dte_str
				cnt_fil_new_pth=sec_pth_nam[0]+'/'+mod_ipr.Dat_Cnt_Nam+mea_dte_str #'.'+mod_ipr.Dat_Cnt_Typ
				if isfile(his_fil_new_pth)==True:
					move(his_fil_new_pth,his_fil_new_pth+'A')
					move(his_fil,his_fil_new_pth+'B')
					mod_raw.His_Fil_Mer([his_fil_new_pth+'A',his_fil_new_pth+'B'],his_fil_new_pth)
					remove(his_fil_new_pth+'A')
					remove(his_fil_new_pth+'B')
					his_fil=his_fil_new_pth
				else:
					move(his_fil,his_fil_new_pth)
					his_fil=his_fil_new_pth
				if isfile(cnt_fil_new_pth)==True:
					cnt_rea=mod_raw.Rea_Fil_Txt(cnt_fil_new_pth) #cnt_rea=control read
					try: set_lst=float(cnt_rea[0][-1])
					except ValueError: mea_Set=0
					else:
						if len(cnt_rea[0])==1: mea_set=int(cnt_rea[0][0])
						else: mea_set=int(cnt_rea[0][-1])
					cnt_fil=cnt_fil_new_pth
				else:
					remove(cnt_fil)
					cnt_fil=cnt_fil_new_pth
		His_Upt(his_fil,1,'Check compleated. All secondary paths are available for measurements storage.'+'\n')
	else:
		His_Upt(his_fil,1,'Check compleated. The main path ('+mod_ipr.Dir_Sav_Mai_Pth+') for measurements storage was not found. Creation of the main path will be attented.')
		mkdir(mod_ipr.Dir_Sav_Mai_Pth)
		if isdir(mod_ipr.Dir_Sav_Mai_Pth)==True: 
			His_Upt(his_fil,2,'The main path ('+mod_ipr.Dir_Sav_Mai_Pth+') for measurements storage was succefully created!!!')
		else:
			His_Upt(his_fil,2,'The main path ('+mod_ipr.Dir_Sav_Mai_Pth+') for measurements storage could not be created!!!')	
			exit('Error path -'+sec_pth_nam[i_sec_pth]+'- could not be created. The  history file will be saved at -'+his_fil+'-.')
		His_Upt(his_fil,1,'Checking the existence of the secondary paths for measurements storage...')
		sec_pth_nam.append(mod_ipr.Dir_Sav_Mai_Pth+mod_ipr.Dat_Fld_Nam+mea_dte_str)
		sec_pth_nam.append(mod_ipr.Dir_Sav_Scn_Pth)
		sec_pth_nam.append(mod_ipr.Dir_Sav_Tht_Pth)
		sec_pth_nam.append(mod_ipr.Dir_Sav_XYZ_Pth)
		sec_pth_nam.append(mod_ipr.Dir_Sav_Cam_Pth)
		His_Upt(his_fil,2,'Checking path ('+sec_pth_nam[0]+') for measurements storage is going to be checked...')
		for i_sec_pth in range(0,4,1): #i_sec_pth=i-counter secondary paths.
			if i_sec_pth!=0: sec_pth_nam[i_sec_pth]=sec_pth_nam[0]+'/'+sec_pth_nam[i_sec_pth]	
			if isdir(sec_pth_nam[i_sec_pth])==True:
				His_Upt(his_fil,2,'Check compleated. The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage was already created. There is no need to create this secondary path.')
			else:
				His_Upt(his_fil,2,'Check compleated. The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage was not found. Creation of this directory will be attented...')
				mkdir(sec_pth_nam[i_sec_pth])
				if isdir(sec_pth_nam[i_sec_pth])==True: 
					His_Upt(his_fil,3,'The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage was succefully created!!!')
				else:
					His_Upt(his_fil,3,'The secondary path ('+sec_pth_nam[i_sec_pth]+') for measurements storage could not be created!!!')	
					exit('Error path -'+sec_pth_nam[i_sec_pth]+'- could not be created. The  history file will be saved at -'+his_fil+'-.')
			if i_sec_pth==0:
				his_fil_new_pth=sec_pth_nam[0]+'/'+mod_ipr.Dat_His_Nam+mea_dte_str
				cnt_fil_new_pth=sec_pth_nam[0]+'/'+mod_ipr.Dat_Cnt_Nam+mea_dte_str #'.'+mod_ipr.Dat_Cnt_Typ
				if isfile(his_fil_new_pth)==True:
					move(his_fil_new_pth,his_fil_new_pth+'A')
					move(his_fil,his_fil_new_pth+'B')
					mod_raw.His_Fil_Mer([his_fil_new_pth+'A',his_fil_new_pth+'B'],his_fil_new_pth)
					remove(his_fil_new_pth+'A')
					remove(his_fil_new_pth+'B')
					his_fil=his_fil_new_pth
				else:
					move(his_fil,his_fil_new_pth)
					his_fil=his_fil_new_pth
				if isfile(cnt_fil_new_pth)==True:
					cnt_rea=mod_raw.Rea_Fil_Txt(cnt_fil_new_pth) #cnt_rea=control read
					try: set_lst=float(cnt_rea[0][-1])
					except ValueError: mea_Set=0
					else:
						if len(cnt_rea[0])==1: mea_set=int(cnt_rea[0][0])
						else: mea_set=int(cnt_rea[0][-1])
					cnt_fil=cnt_fil_new_pth
				else:
					remove(cnt_fil)
					cnt_fil=cnt_fil_new_pth
		His_Upt(his_fil,1,'Check compleated. All secondary paths are available for measurements storage.'+'\n')
	return mea_set,cnt_fil,his_fil,sec_pth_nam

#Tim_Mea_Sta=Time Measurement Start.
	#This function will indicate if the stating time for measurements had been reached.
#Parameters.
	#his_fil=history file. String parameter. This parameter indicates the path to find the history file.
def Tim_Mea_Sta(his_fil):
	His_Upt(his_fil,0,'*****Checking start of measurements time*****') 	
	His_Upt(his_fil,1,'Waiting for set starting measurements time...')
	mea_sta=False #mea_sta=measurements start.
	wai_tim=0 #wai_tim=waiting time.
	while mea_sta==False:
		his_msg_str='The actual time is ' #his_msg_str=history message string.
		act_tim=Tim_Upt()
		his_msg_str=his_msg_str+act_tim
		if Tim_HMS_Dec_Con(mod_ipr.Cap_Tim_Sta)<=Tim_HMS_Dec_Con(Tim_Upt_Int()):
			his_msg_str=his_msg_str+'... measurements will beging.'
			His_Upt(his_fil,2,his_msg_str)
			mea_sta=True
		else:
			his_msg_str=his_msg_str+'... waiting for the set starting measurements time.'
			if wai_tim==0:
				His_Upt(his_fil,2,his_msg_str)
			else: 
				wai_tim=wai_tim+mod_ipr.Cap_Tim_Sta_Wai_Scr
				if 3600*mod_ipr.Cap_Tim_Sta_Wai_His<=wai_tim: wai_tim=0			
			sleep(mod_ipr.Cap_Tim_Sta_Wai_Scr)
	return
