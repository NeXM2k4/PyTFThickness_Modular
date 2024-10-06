import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
from PyTFThickness_Module_Fitting import R_plt,Fit_R
from PyTFThickness_Module_Data import Dat_Ini
from PyTFThickness_Module_Read_Write import Rea_Fil_Txt
from numpy import array

Tim,Tht,ThtE,VTim,VTht,XY,X,Y,Z,Z_err,N,N_err,XYZN=Dat_Ini()
V_val=Rea_Fil_Txt("/home/cisneros/Documentos/PyTFThickness/TFT_Measurements_2024_10_04/V_Theta_Points/"+"TFT_XYZN_0_X_0_Y_2_Vtheta.txt")
V_val=array(V_val,dtype=float)
z,z_err,n,n_fit,a=Fit_R(Tht,ThtE,V_val[1],"lm",1.5,100)
