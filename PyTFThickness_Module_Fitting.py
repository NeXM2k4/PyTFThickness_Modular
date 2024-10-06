import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
#from PyTFThickness_Module_Plotting import Plt_Mea_Man_Upd,Plt_Fit_Upd

from numpy import pi,sin,cos,arcsin,deg2rad,rad2deg,diag,transpose,sqrt
from matplotlib.pyplot import fignum_exists,figure,savefig,show,ion
from scipy.optimize import curve_fit
from scipy.interpolate import PchipInterpolator

def tht_r_fun(tht_i_val,n_val):
	tht_r_val=arcsin(sin(tht_i_val)/n_val)
	return tht_r_val

def r_fun(tht_i_val,tht_r_val):
	r_val=sin(tht_r_val-tht_i_val)/sin(tht_r_val+tht_i_val)
	return r_val

def r2_fun(tht_i_val,tht_r_val):
	r2_val=(sin(tht_r_val-tht_i_val)/sin(tht_r_val+tht_i_val))**2
	return r2_val

def phi_fun(tht_r_val,h_val,n_val):
	phi_val=(4*pi*n_val*h_val/mod_ipr.Lsr_Wav)*cos(tht_r_val)
	return phi_val
	
def R_plt(tht_i_deg_val,h_val,n_val,A):	
	tht_i_val=deg2rad(tht_i_deg_val)
	tht_r_val=tht_r_fun(tht_i_val,n_val)
	r2_val=r2_fun(tht_i_val,tht_r_val)
	phi_val=phi_fun(tht_r_val,h_val,n_val)
	R_val=2*A*r2_val*(1-cos(phi_val))/(1+r2_val*(r2_val-2*cos(phi_val)))
	return R_val
	
def R_dev_fun(r2_val,phi_val):
	R_val=2*r2_val*(1-cos(phi_val))/(1+r2_val*(r2_val-2*cos(phi_val)))
	return R_val
	
def dr_dn_fun(tht_i_val,tht_r_val):
	dr_dn_val=-1*(sin(2*tht_i_val)/sin(tht_i_val+tht_r_val)**2)
	return dr_dn_val
	
def dphi_dn_fun(tht_i_val,tht_r_val,h_val,n_val):
	dphi_dn_val=(4*pi*h_val/mod_ipr.Lsr_Wav)*(cos(tht_r_val)-((n_val**4)*sin(tht_i_val)*sin(tht_r_val))/(sqrt(n_val**2-sin(tht_i_val)**2)))
	return dphi_dn_val
	
def dphi_dh_fun(tht_r_val,n_val):
	dphi_dn_val=(4*pi*n_val/mod_ipr.Lsr_Wav)*cos(tht_r_val)
	return dphi_dn_val

def R_Jac_fun(tht_i_val,h_val,n_val):
	#Evaluates variables
	tht_r_val=tht_r_fun(tht_i_val,n_val)
	r_val=r_fun(tht_i_val,tht_r_val)
	r2_val=r2_fun(tht_i_val,tht_r_val)
	phi_val=phi_fun(tht_r_val,h_val,n_val)
	R_val=R_dev_fun(r2_val,phi_val)
	dr_dn_val=dr_dn_fun(tht_i_val,tht_r_val)
	dphi_dn_val=dphi_dn_fun(tht_i_val,tht_r_val,h_val,n_val)
	dphi_dh_val=dphi_dh_fun(tht_r_val,n_val)
	#Evaluates derivates
	dR_dh_val=R_val*(sin(phi_val)/(1-cos(phi_val)))*(1-R_val/(2*r2_val*(1-cos(phi_val))))*dphi_dh_val
	dR_dn_val=R_val*((1-2*(r2_val-cos(phi_val))/(1-cos(phi_val)))*(R_val/r_val)*dr_dn_val+(1-R_val)*(sin(phi_val)/(1-cos(phi_val)))*dphi_dn_val)
	#Evaluates Jacobian
	R_Jac_val=transpose([dR_dh_val,dR_dn_val])
	return R_Jac_val

def Fit_R(Tht_mea_deg,Tht_mea_ext_deg,R_mea,fit_mth,n_gss,h_gss):
	Tht_mea_rad=deg2rad(Tht_mea_deg)
	Tht_mea_ext_rad=deg2rad(Tht_mea_ext_deg)
	R_mea_nrm=R_mea/max(R_mea)#mod_ipr.R_V_Nrm #max(R_mea)
	R_intp=PchipInterpolator(Tht_mea_deg,R_mea_nrm)
	R_mea_nrm_ext=R_intp(Tht_mea_ext_deg)
	#Plotting fits
	fig_fit=figure("Fitting")
	fig_fit.clear()
	fit_grd=fig_fit.add_gridspec(1,1,wspace=0.75,hspace=0.75)
	ax_fit=fig_fit.add_subplot(fit_grd[0,0])
	ax_fit.set_xlabel("Angle (0)")
	ax_fit.set_ylabel("Voltage (mV)")
	lin_fit,=ax_fit.plot(Tht_mea_ext_deg,R_mea_nrm_ext,lw=3.0,ms=0.0,marker="o",c="red",label="Fitted line")
	lin_mea_ext,=ax_fit.plot(Tht_mea_ext_deg,R_mea_nrm_ext,lw=3.0,ms=0.0,marker="o",c="gray",label="Interpolated line")
	lin_mea,=ax_fit.plot(Tht_mea_deg,R_mea_nrm,lw=0.0,ms=3.0,marker="o",c="blue",label="Measured points")
	fig_fit.legend()
	fig_fit.canvas.draw()
	fig_fit.canvas.flush_events()
	ion()
	show()
	def R_fun(tht_i_val,h_val,n_val):	
		tht_r_val=tht_r_fun(tht_i_val,n_val)
		r2_val=r2_fun(tht_i_val,tht_r_val)
		phi_val=phi_fun(tht_r_val,h_val,n_val)
		R_val=2*r2_val*(1-cos(phi_val))/(1+r2_val*(r2_val-2*cos(phi_val)))
		R_val=R_val/max(R_val)
		lin_fit.set_ydata(R_val)
		fig_fit.suptitle("Fitting for:"+"h="+str(h_val)+" and "+"n="+str(n_val))
		fig_fit.canvas.draw()
		fig_fit.canvas.flush_events()
		ion()
		return R_val
	hna_opt,hna_cov=None,None
	if fit_mth=="lm": hna_opt,hna_cov=curve_fit(R_fun,Tht_mea_ext_rad,R_mea_nrm_ext,p0=[h_gss,n_gss],method=fit_mth,ftol=1e-12,gtol=1e-12,maxfev=1000)
	else: hna_opt,hna_cov=curve_fit(R_fun,Tht_mea_ext_rad,R_mea_nrm_ext,p0=[h_gss,n_gss],bounds=[[1,1],[10000000,2]],jac=R_Jac_fun,method=fit_mth,ftol=1e-12,gtol=1e-12,maxfev=1500,tr_solver="exact")
	hva_err=diag(hna_cov)
	print(hna_opt,hva_err)
	#if : savefig()
	return hna_opt[0],hva_err[0],hna_opt[1],hva_err[1],max(R_mea)
