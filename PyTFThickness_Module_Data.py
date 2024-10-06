import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
import PyTFThickness_Module_Read_Write as mod_raw #mod_raw=module read and write.

from numpy import linspace,zeros,meshgrid,NaN

def Dat_Ini():
	tim_grd=2*mod_ipr.Lsr_StS*linspace(start=1,stop=mod_ipr.Pht_Scns,num=mod_ipr.Pht_Scns)
	tht_grd=linspace(start=mod_ipr.R_Ang_Rng[0],stop=mod_ipr.R_Ang_Rng[1],num=mod_ipr.R_Ang_Num)
	tht_grd_ext=linspace(start=mod_ipr.R_Ang_Rng[0],stop=mod_ipr.R_Ang_Rng[1],num=mod_ipr.R_Ext_Ang_Num)
	vtim_grd=zeros(shape=(2,mod_ipr.Pht_Scns),dtype=float)
	vtht_grd=zeros(shape=(2,mod_ipr.R_Ang_Num),dtype=float)
	x_grd=linspace(start=mod_ipr.X_Range[0],stop=mod_ipr.X_Range[1],num=mod_ipr.X_Pnts)
	y_grd=linspace(start=mod_ipr.Y_Range[0],stop=mod_ipr.Y_Range[1],num=mod_ipr.Y_Pnts)
	xy_grd=zeros(shape=(5,mod_ipr.X_Pnts*mod_ipr.Y_Pnts),dtype=float)
	x_msh,y_msh=meshgrid(x_grd,y_grd,indexing="ij")
	z_msh=zeros(shape=(mod_ipr.X_Pnts,mod_ipr.Y_Pnts),dtype=float)
	zerr_msh=zeros(shape=(mod_ipr.X_Pnts,mod_ipr.Y_Pnts),dtype=float)
	n_msh=zeros(shape=(mod_ipr.X_Pnts,mod_ipr.Y_Pnts),dtype=float)
	nerr_msh=zeros(shape=(mod_ipr.X_Pnts,mod_ipr.Y_Pnts),dtype=float)
	xyzn=zeros(shape=(7),dtype=float)
	xy_pnt=0
	for x_n in range(0,mod_ipr.X_Pnts,2):
		for y_m in range(0,mod_ipr.Y_Pnts,1):
			xy_grd[0][xy_pnt]=x_n
			xy_grd[1][xy_pnt]=y_m
			xy_grd[2][xy_pnt]=x_msh[x_n][y_m]
			xy_grd[3][xy_pnt]=NaN#y_grd[x_n][y_m]
			xy_grd[4][xy_pnt]=y_msh[x_n][y_m]
			xy_pnt+=1
		if x_n+1<mod_ipr.X_Pnts:
			for y_m in range(0,mod_ipr.Y_Pnts,1):
				xy_grd[0][xy_pnt]=x_n+1
				xy_grd[1][xy_pnt]=mod_ipr.Y_Pnts-1-y_m
				xy_grd[2][xy_pnt]=x_msh[x_n+1][mod_ipr.Y_Pnts-1-y_m]
				xy_grd[3][xy_pnt]=NaN#y_grd[x_n+1][mod_ipr.Y_Pnts-1-y_m]
				xy_grd[4][xy_pnt]=y_msh[x_n+1][mod_ipr.Y_Pnts-1-y_m]
				xy_pnt+=1
	return tim_grd,tht_grd,tht_grd_ext,vtim_grd,vtht_grd,xy_grd,x_msh,y_msh,z_msh,zerr_msh,n_msh,nerr_msh,xyzn

def Dat_Cln_1D(dat_pnt,dat_val):
	for dat_n in range(dat_pnt): 
		dat_val[0][dat_n]=NaN
		dat_val[1][dat_n]=NaN
	return dat_val

def Dat_Cln_3D(dat_pnt,dat_val):
	for dat_n in range(dat_pnt):
		for dat_m in range(dat_pnt): 
			dat_val[dat_n][dat_m]=NaN
	return dat_val
