#######################################################################################################
##PyEART Module Read and Write -- Version 1.0                                                        ##
##The funtions on this module are made to read and write data related with the simulation.           ##
#######################################################################################################

import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.

from numpy import zeros

#Cre_Fil_His=Create File History.
#Parameters:
	#his_fil_nam=history file name. String parameter. This parameter indicates the directory and name to create the history file.
	#his_fil_dte=history file date. String parameter. This parameter indicates the date when the history file was created.
	#his_fil_tim=history file time. String parameter. This parameter indicates the time when the history file was created.
def Cre_Fil_His(his_fil_nam,his_fil_dte,his_fil_tim):
	his_fil=open(file=his_fil_nam,mode='w') #his_fil=history file.
	lin_hea='* History file for TFThickness (Thimn Films Thickness by Reflectance Spectroscopy) *' #lin_hea=line header.
	lin_mar=''
	for i_lin_cha in range(0,len(lin_hea),1): lin_mar=lin_mar+'*'
	lin_sta='*****This measurement adquisitions were performed on '+his_fil_dte+' at '+his_fil_tim+'*****' #lin_sta=line start.
	lin_ini='\n'+lin_mar+'\n'+lin_hea+'\n'+lin_mar+'\n\n\n'+lin_sta+'\n\n' #lin_ini=line initialization.
	print(lin_ini)
	his_fil.write(lin_ini)
	his_fil.close()
	return

#His_Fil_Wri=History File Write.
	#This function will write the data given in the history file.
#Parameters.
	#his_fil_nam=history file name. string parameter. This parameter indicates the directory and name of the file to be read.
	#his_msg_str=history file message. string parameter. This parameter indicates the line to be written in the history file.
def His_Fil_Wri(his_fil_nam,his_msg_str):
	his_fil=open(file=his_fil_nam,mode='a') #his_fil=history file.
	his_fil.write(his_msg_str+'\n')
	his_fil.close()
	return

#His_Fil_Mer=History File Merge.
	#This function will merge the data given in the history files.
#Parameters.
	#his_fil_nam=history file names. String array. This parameter indicates the directory and name of the history files to be merged.
	#his_fil_mer=history file merge. String parameter. This parameter indicates the directory and name of the merged history file.
def His_Fil_Mer(his_fil_nam,his_fil_mer):
	with open(his_fil_mer,'w') as his_fil_mer_out: #his_fil_mer_out=history file merged out.
    		for his_fil_nam_act in his_fil_nam: #his_fil_nam_act=history file name actual.
        		with open(his_fil_nam_act) as his_fil_act: #his_fil_act=history file actual.
            			for his_fil_act_lin in his_fil_act: #his_fil_act_lin=history file actual line.
                			his_fil_mer_out.write(his_fil_act_lin)
	return

#Rea_Fil_Txt=Read File Text.
	#This function will open an text file and save its contents in a array.
#Parameters.
	#txt_fil_nam=text file name. string parameter. This parameter indicates the directory and name of the file to be read.
def Rea_Fil_Txt(txt_fil_nam):
	print(txt_fil_nam)
	rea_txt_fil=open(file=txt_fil_nam,mode='r') #rea_txt_fil=read text file.
	rea_dat_num_lin=0 #rea_dat_num_lin=read data number lines.
	rea_dat_num_col=0 #rea_dat_num_col=read data number columns.
	rea_dat=[None] #rea_dat=read data x.
	for i_lin in rea_txt_fil: #i_lin=i-counter line.
		row=i_lin
		cells=row.split()
		if rea_dat_num_lin==0:
			rea_dat_num_col=len(cells)
			rea_dat=[None]*rea_dat_num_col
			for i_col in range(0,rea_dat_num_col,1): #i_col=i-counter column.
				rea_dat[i_col]=[]
		if rea_dat_num_lin>1:
			for i_col in range(0,rea_dat_num_col,1): #i_col=i-counter column.
				rea_dat[i_col].append(cells[i_col])
		rea_dat_num_lin=rea_dat_num_lin+1
	rea_txt_fil.close()
	return rea_dat

def Rea_Fil_Txt_Lst(txt_fil_nam):
	print(txt_fil_nam)
	rea_txt_fil=open(file=txt_fil_nam,mode='r') #rea_txt_fil=read text file.
	rea_lst,rea_lin=0,0
	for row in rea_txt_fil: #i_lin=i-counter line.
		cells=row.split('\t')
		rea_lin+=1
		if len(cells)>1: 
			if rea_lin>1: rea_lst=cells[0]
		else: break
	rea_txt_fil.close()
	if rea_lst=='--' or '#': rea_lst=0
	return int(float(rea_lst))

#Rep_Fil_Txt=Replace File Text.
	#This function will open an text file and save its contents in a array.
#Parameters.
	#txt_fil_nam=text file name. String parameter. This parameter indicates the directory and name of the file to be read.
	#txt_lin_lab= String parameter. This parameter indicates the line which is going to be replaced.
	#txt_lin_rep= String parameter. This parameter indicates the text which is going to be replaced.
def Rep_Fil_Txt(txt_fil_nam,txt_lin_lab,txt_lin_rep):
	ori_txt_fil=open(file=txt_fil_nam,mode='r').read() #rep_txt_fil=replace text file.
	rep_txt=ori_txt_fil.replace(txt_lin_lab,txt_lin_rep)
	rep_ext_fil=open(file=txt_fil_nam,mode='w')
	rep_ext_fil.write(rep_txt)
	rep_ext_fil.close()
	return

#Wri_Dat_Str_Txt=Write Data String Text.
	#This function will write the data given in a text file.
#Parameters.
	#txt_fil_nam=text file name. string parameter. This parameter indicates the directory and name of the file to be read.
	#wri_dat_val=write data values. float array of [wri_dat_col_num][wri_dat_lin_num] dimentions. This parameter has all the data to write.
	#wri_dat_col_num=write data columns number. integer variable. This parameter indicates the number of columns in the data.
	#wri_dat_lin_num=write data lines number. integer variable. This parameter indicates the number of rows in the data.
	#wri_dat_mod=write data mode. string parameter. This parameter indicates the type of writting that will be perform.
def Wri_Dat_Str_Txt(txt_fil_nam,wri_dat_val,wri_dat_col_num,wri_dat_lin_num,wri_dat_mod):
	txt_fil=open(file=txt_fil_nam,mode=wri_dat_mod) #txt_fil=text file.
	for i_wri_dat_lin_num in range(0,wri_dat_lin_num,1): #i_wri_dat_lin_num=i-counter write data lines number. 
		line=''
		#print(i_wri_dat_lin_num)
		for i_wri_dat_col_num in range(0,wri_dat_col_num,1): #i_wri_dat_col_num=i-counter write data columns number.
			#print(i_wri_dat_col_num)
			line=line+wri_dat_val[i_wri_dat_lin_num][i_wri_dat_col_num]+'\t'
		line=line+'\n'
		txt_fil.write(line)
	txt_fil.close()
	return

#His_Fil_Wri=History File Write.
	#This function will write the data given in the history file.
#Parameters.
	#his_fil_nam=history file name. string parameter. This parameter indicates the directory and name of the file to be read.
	#his_msg_str=history file message. string parameter. This parameter indicates the line to be written in the history file.
def His_Fil_Wri(his_fil_nam,his_msg_str):
	his_fil=open(file=his_fil_nam,mode='a') #his_fil=history file.
	his_fil.write(his_msg_str+'\n')
	his_fil.close()
	return

#Rep_Fil_Txt=Replace File Text.
	#This function will open an text file and save its contents in a array.
#Parameters.
	#txt_fil_nam=text file name. String parameter. This parameter indicates the directory and name of the file to be read.
	#txt_lin_lab= String parameter. This parameter indicates the line which is going to be replaced.
	#txt_lin_rep= String parameter. This parameter indicates the text which is going to be replaced.
def Rep_Fil_Txt(txt_fil_nam,txt_lin_lab,txt_lin_rep):
	ori_txt_fil=open(file=txt_fil_nam,mode='r').read() #rep_txt_fil=replace text file.
	rep_txt=ori_txt_fil.replace(txt_lin_lab,txt_lin_rep)
	rep_ext_fil=open(file=txt_fil_nam,mode='w')
	rep_ext_fil.write(rep_txt)
	rep_ext_fil.close()
	return
	
#Wri_Dat_Str_Txt=Write Data String Text.
	#This function will write the data given in a text file.
#Parameters.
	#txt_fil_nam=text file name. string parameter. This parameter indicates the directory and name of the file to be read.
	#wri_dat_val=write data values. float array of [wri_dat_col_num][wri_dat_lin_num] dimentions. This parameter has all the data to write.
	#wri_dat_col_num=write data columns number. integer variable. This parameter indicates the number of columns in the data.
	#wri_dat_mod=write data mode. string parameter. This parameter indicates the type of writting that will be perform.
def Wri_Dat_Flt_1L_Txt(txt_fil_nam,wri_dat_val,wri_dat_col_num,wri_dat_mod):
	txt_fil=open(file=txt_fil_nam,mode=wri_dat_mod) #txt_fil=text file.
	line=''
	for i_col in range(0,wri_dat_col_num-1,1): line+=str(wri_dat_val[i_col])+'\t'
	line+=str(wri_dat_val[wri_dat_col_num-1])+'\n'
	txt_fil.write(line)
	txt_fil.close()
	return
	
#Wri_Dat_Str_Txt=Write Data String Text.
	#This function will write the data given in a text file.
#Parameters.
	#txt_fil_nam=text file name. string parameter. This parameter indicates the directory and name of the file to be read.
	#wri_dat_val=write data values. float array of [wri_dat_col_num][wri_dat_lin_num] dimentions. This parameter has all the data to write.
	#wri_dat_col_num=write data columns number. integer variable. This parameter indicates the number of columns in the data.
	#wri_dat_lin_num=write data lines number. integer variable. This parameter indicates the number of rows in the data.
	#wri_dat_mod=write data mode. string parameter. This parameter indicates the type of writting that will be perform.
def Wri_Dat_Flt_nL_Txt(txt_fil_nam,wri_dat_val,lin_num,col_num,wri_dat_mod):
	txt_fil=open(file=txt_fil_nam,mode=wri_dat_mod) #txt_fil=text file.
	for i_lin_num in range(0,lin_num-1,1):  
		line=''
		for i_col_num in range(0,col_num-1,1): 
			line=line+str(wri_dat_val[i_col_num][i_lin_num])+'\t'
		line=line+str(wri_dat_val[col_num-1][i_lin_num])+'\n'
		txt_fil.write(line)
	line=''
	for i_col_num in range(0,col_num-1,1): line=line+str(wri_dat_val[i_col_num][lin_num-1])+'\t'
	line=line+str(wri_dat_val[col_num-1][lin_num-1])
	txt_fil.write(line)
	txt_fil.close()
	return
