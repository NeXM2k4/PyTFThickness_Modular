import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
import PyTFThickness_Module_Read_Write as mod_raw #mod_raw=module read and write.
from PyTFThickness_Module_Register import Tim_HMS_Dec_Con

from matplotlib.pyplot import fignum_exists,figure,savefig,show,ion
from matplotlib import cm
from numpy import nanmax,isnan

from numpy import min,max

#CREAR UNA FIGURA DEL PLOT 3D SOLITO
def Plt_3d_xyz():
    fig_3d = figure("3D Plot")
    fig_3d.clear()
    
    ax_xyz = None
    
    ax_xyz.set_xlabel("X position (mm)")
    ax_xyz.set_ylabel("Y position (mm)")
    ax_xyz.set_zlabel("Z position (mm)")
    
    #sfc_xyz[1]=ax_xyz[1].plot_surface(x,y,z)
    ax_xyz.set_xlim(0.9*mod_ipr.X_Range[0],1.1*mod_ipr.X_Range[1])
    ax_xyz.set_ylim(0.9*mod_ipr.Y_Range[0],1.1*mod_ipr.Y_Range[1])
    ax_xyz.set_zlim(0,1)
     
    fig_3d.show()
    fig_3d.canvas.draw()
    
    

def Plt_Mea_Man_Ini(time,theta,vtime,vtheta,xy,x,y,z):
    
    #FIGURA SOLO DEL PLOT 3D
    Plt_3d_xyz()
    
    fig_mea=figure('Measurement control panel') #plt_fig_mea=plot figure measurements.
    fig_mea.clear()
    
    n_col,m_col,nd2_col,md2_col=mod_ipr.Plt_N,mod_ipr.Plt_M+1,int((mod_ipr.Plt_N)/2),int((mod_ipr.Plt_M)/2)
    grd=fig_mea.add_gridspec(n_col,m_col,wspace=0.75,hspace=0.75)
    
    #if get_backend()!='TkAgg': switch_backend('TkAgg') 
    ax_vtim=None #ax_vtim=axes voltage time.
    ax_vtht=None #ax_vtht=axes voltage theta.
    ax_xyz=[None,None] #ax_xyz=axes xyz.
    lin_vtim_om=[None,None] #lin_vtim_om=lines voltage offset measurement.
    lin_vtht_mf=[None,None] #lin_vtht_mf=lines voltage theta measurement fit.
    sfc_xyz=[None,None] #sfc_xy_z=surfaces x y z.
    pnt_pfp=[None,None,None] #pnt_pfp=points past present future.
    
    ax_vtim=fig_mea.add_subplot(grd[0:nd2_col-1,0:md2_col])
    ax_vtht=fig_mea.add_subplot(grd[nd2_col:n_col,0:md2_col])
    ax_xyz[0]=fig_mea.add_subplot(grd[0:nd2_col,md2_col+1:m_col-1])
    ax_xyz[1]=fig_mea.add_subplot(grd[nd2_col+1:n_col,md2_col+1:m_col-1],projection='3d')
    
    #Colorbar axis
    ax_cbr=1#fig_mea.add_subplot(grd[n_col,m_col])
    
    #00 Configuring axis for V vs time
    ax_vtim.set_xlabel("time (ms)")
    ax_vtim.set_ylabel("Voltage (mV)")
    lin_vtim_om[0],=ax_vtim.plot(time,vtime[0],lw=2.0,ms=3.0,c="blue",label="Offset angle ")
    lin_vtim_om[1],=ax_vtim.plot(time,vtime[1],lw=2.0,ms=3.0,c="red",label="Voltages angle ")
    ax_vtim.set_xlim(time[0],time[mod_ipr.Pht_Scns-1])
    ax_vtim.set_ylim(0,1)
    ax_vtim.legend()
    
    #10 Configuring axis for V vs theta
    ax_vtht.set_xlabel("Incident angle (degrees)")
    ax_vtht.set_ylabel("Voltage (mV)")
    lin_vtht_mf[1],=ax_vtht.plot(theta,vtheta[1],lw=3.0,ms=0.0,marker=",",c="green",label="Fited line")
    lin_vtht_mf[0],=ax_vtht.plot(theta,vtheta[0],lw=0.0,ms=6.0,marker="o",c="orange",label="Measured points")
    ax_vtht.set_xlim(0.9*mod_ipr.R_Ang_Rng[0],1.1*mod_ipr.R_Ang_Rng[1])
    ax_vtht.set_ylim(0,1)
    ax_vtht.legend()
    
    #11 Configuring axis for XY vs Z
    ax_xyz[0].set_xlabel("X position (mm)")
    ax_xyz[0].set_ylabel("Y position (mm)")
    pnt_pfp[0],=ax_xyz[0].plot(xy[2],xy[3],c='blue',linestyle='-',marker='o',lw=1.0,ms=3.0)
    pnt_pfp[1],=ax_xyz[0].plot(xy[2],xy[4],c='gray',linestyle='-',marker='o',lw=1.0,ms=3.0)
    pnt_pfp[2],=ax_xyz[0].plot(0,0,c='red',linestyle='-',marker='o',lw=1.0,ms=3.0)
    
    #pln_xyz[0]=ax_xyz[0].contourf(x,y)
    ax_xyz[0].set_xlim(1.1*mod_ipr.X_Range[0],1.1*mod_ipr.X_Range[1])
    ax_xyz[0].set_ylim(1.1*mod_ipr.Y_Range[0],1.1*mod_ipr.Y_Range[1])
    ax_xyz[1].set_xlabel("X position (mm)")
    ax_xyz[1].set_ylabel("Y position (mm)")
    ax_xyz[1].set_zlabel("Z position (mm)")
    
    #sfc_xyz[1]=ax_xyz[1].plot_surface(x,y,z)
    ax_xyz[1].set_xlim(0.9*mod_ipr.X_Range[0],1.1*mod_ipr.X_Range[1])
    ax_xyz[1].set_ylim(0.9*mod_ipr.Y_Range[0],1.1*mod_ipr.Y_Range[1])
    ax_xyz[1].set_zlim(0,1)     
    fig_mea.show()
    fig_mea.canvas.draw()
    return [fig_mea,[ax_vtim,ax_vtht,ax_xyz,ax_cbr],[lin_vtim_om,lin_vtht_mf,pnt_pfp,sfc_xyz]]
    
def Plt_Mea_Man_Upd(plt_obj,plt_upd,plt_lab,time,theta,vtime,vtheta,xy_act,xy,x,y,z):
    if fignum_exists("Measurement control panel"):
        if plt_upd==0:
            plt_obj[2][0][0].set_ydata(vtime[0])
            plt_obj[2][0][1].set_ydata(vtime[1])
            #y_max=1.2*nanmax(vtime.flatten())
            #if isnan(y_max): y_max=33000
            plt_obj[1][0].set_ylim(0,1.2*nanmax(vtime.flatten()))
        elif plt_upd==1:
            plt_obj[2][1][0].set_ydata(vtheta[0])
            plt_obj[2][1][1].set_ydata(vtheta[1])
            #y_max=1.2*nanmax(vtime.flatten())
            #if isnan(y_max): y_max=33000
            plt_obj[1][1].set_ylim(0,1.2*nanmax(vtheta.flatten()))
        elif plt_upd==2:
            plt_obj[2][1][1].set_ydata(vtheta)
            #y_max=1.2*nanmax(vtime.flatten())
            #if isnan(y_max): y_max=33000
            #plt_obj[1][1].set_ylim(0,1.2*nanmax(vtheta.flatten()))
        elif plt_upd==3:
            plt_obj[2][2][0].set_ydata(xy[3])
            plt_obj[2][2][1].set_ydata(xy[4])
            plt_obj[2][2][2].set_xdata(xy_act[0])
            plt_obj[2][2][2].set_ydata(xy_act[1])
        elif plt_upd==4:
            z_srf=plt_obj[1][2][0].contourf(x,y,z,cmap=cm.coolwarm,vmin=0,vmax=nanmax(z.flatten()),linewidth=1.0,antialiased=True)
            plt_obj[2][2][0]=z_srf
            plt_obj[2][2][0].set_xlabel("X (mm)")
            plt_obj[2][2][0].set_ylabel("Y (mm)")
            z_pln=plt_obj[1][2][1].plot_surface(x,y,z,cmap=cm.coolwarm,vmin=0,vmax=nanmax(z.flatten()),linewidth=1.0,antialiased=True) 
            plt_obj[2][2][1]=z_pln
            plt_obj[2][2][1].set_xlabel("X (mm)")
            plt_obj[2][2][1].set_ylabel("Y (mm)")
            plt_obj[2][2][1].set_zlabel("Z (nm)")
            #plt_obj[0].colorbar(z_srf,cax=ax_cbr)
        plt_obj[0].suptitle(plt_lab)
        plt_obj[0].canvas.draw()
        plt_obj[0].canvas.flush_events()
        ion()
    else: plt_obj=Plt_Mea_Man_Ini(time,theta,vtime,vtheta,x,y,z)
    return plt_obj

def Plt_Fit_Upd(theta,r_mea,r_fit,fig_fit,lin_fit):
    if fignum_exists("Fitting"):
        ax_fit.set_ydata(r_fit)
        fig_fit.suptitle(plt_lab)
        fig_fit.canvas.draw()
        fig_fit.canvas.flush_events()
        ion()
    else: 
        fig_fit=figure("Fitting")
        fit_grd=fig_fit.add_gridspec(1,1,wspace=0.75,hspace=0.75)
        ax_fit=fig_fit.add_subplot(fit_grd[0,0])        
        ax_fit.set_xlabel("Angle (0)")
        ax_fit.set_ylabel("Voltage (mV)")
        lin_mea,=ax_fit.plot(theta,r_mea,lw=0.0,ms=3.0,c="blue",label="Measured points")
        lin_fit,=ax_fit.plot(theta,r_fit,lw=3.0,ms=0.0,c="red",label="Fitted points")
    return fig_fit,lin_fit
