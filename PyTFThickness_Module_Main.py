import PyTFThickness_Module_Initial_Parameters as mod_ipr #mod_ipr=module intial parameters.
from PyTFThickness_Module_Register import Dte_Upt,Tim_Upt,Tim_Upt_Int,His_Upt,Tim_Mea_Sta,Tim_HMS_Dec_Con,Mea_Fol,Tim_Mea_Sta
from PyTFThickness_Module_PicoController import Pico_Brd
from PyTFThickness_Module_Data import Dat_Ini,Dat_Cln_1D,Dat_Cln_3D
from PyTFThickness_Module_Plotting import Plt_Mea_Man_Ini,Plt_Mea_Man_Upd
from PyTFThickness_Module_Fitting import R_plt,Fit_R
from PyTFThickness_Module_Read_Write import Rea_Fil_Txt_Lst,Wri_Dat_Flt_1L_Txt,Wri_Dat_Flt_nL_Txt
from PyTFThickness_Module_PiCamera import CameraStart,Pix_Inten

from multiprocessing import cpu_count,Process
from time import sleep
from os.path import isfile

#********************************************
#Initialize directory paths and history file*
#********************************************

mea_dte=Dte_Upt() #mea_dte=measurements date.
mea_tim=Tim_Upt() #mea_tim=measurements time.
mea_set,mea_cnt_fil,mea_his_fil,mea_dir_pth=Mea_Fol(mea_dte,mea_tim) #mea_set=measurement set. mea_cnt_fil=measurement control file. mea_his_fil=measurements history file. mea_pth=measurement directories path.

#***********************************
#Initialize USB servo-motor devices*
#***********************************

pico_cmd=Pico_Brd(mea_his_fil) #Pico_Brd=Pico object activated.

#********************
#Initialize PiCamera*
#********************

cmr_cmd=CameraStart()

#*************************************************
#Waiting for starting PyTikness Measurements time*
#*************************************************

Tim_Mea_Sta(mea_his_fil)

#*******************************
#Start TFThickness Measurements*
#*******************************
#"""
if __name__ =='__main__':
    #print('Number of CPU cores:',cpu_count())
    His_Upt(mea_his_fil,0,'*****Measurements start*****') 	
    mea_stp=False #mea_stp=measurements stop.
    Tim,Tht,ThtE,VTim,VTht,XY,X,Y,Z,Z_err,N,N_err,XYZN=Dat_Ini()
    VTim=Dat_Cln_1D(mod_ipr.Pht_Scns,VTim)
    VTht=Dat_Cln_1D(mod_ipr.R_Ang_Num,VTht)
    plt_obj=Plt_Mea_Man_Ini(Tim,Tht,VTim,VTht,XY,X,Y,Z) #fig_mea=figure measurement. 
    pico_cmd.XY_C(mea_his_fil)
    xy_pnt,xy_tot=0,mod_ipr.X_Pnts**2
    xy_pnt_tot=mod_ipr.X_Pnts*mod_ipr.Y_Pnts
    xy_sta=0
    xy_act,xy_prv=[0,0],[0,0]
    fil_xy,fil_xyt,fil_xyts=None,None,None
    fil_xy_num=0
    fil_uns=True #fil_unp=file unsuitable
    while fil_uns:
        fil_xy_try=mea_dir_pth[3]+"TFT_XYZN_"+str(fil_xy_num)+".txt"
        if isfile(fil_xy_try)==False:
            fil_xy=mea_dir_pth[3]+"TFT_XYZN_"+str(fil_xy_num)+".txt"
            fil_xyt=[mea_dir_pth[2]+"TFT_XYZN_"+str(fil_xy_num)+"_","_Vtheta.txt"]
            fil_xyts=[mea_dir_pth[1]+"TFT_XYZN_"+str(fil_xy_num)+"_","_Vtheta_","_Scans.txt"]
            fil_uns=False
        else:
            pnt_lst=Rea_Fil_Txt_Lst(fil_xy_try)
            if 0<pnt_lst+1 and pnt_lst+1<xy_pnt_tot:
                fil_xy=mea_dir_pth[3]+"TFT_XYZN_"+str(fil_xy_num)+".txt"
                fil_xyt=[mea_dir_pth[2]+"TFT_XYZN_"+str(fil_xy_num)+"_","_Vtheta.txt"]
                fil_xyts=[mea_dir_pth[1]+"TFT_XYZN_"+str(fil_xy_num)+"_","_Vtheta_","_Scans.txt"]
                fil_uns=False 
                xy_sta=pnt_lst+1
        fil_xy_num+=1
    if xy_sta==0:
        Wri_Dat_Flt_1L_Txt(fil_xy,["#","X","Y","Z","Z_e","n","n_e"],7,"w")
        Wri_Dat_Flt_1L_Txt(fil_xy,["--","mm","mm","nm","nm","--","--"],7,"a")
    for xy_pnt in range(0,xy_sta): 
        XY[3][xy_pnt]=XY[4][xy_pnt]
        XY[4][xy_pnt]=XY[3][xy_sta]
    #XY[3][xy_pnt]=XY[4][xy_sta]
    if mod_ipr.R_V_Nrm_Mea==True:
        mvm_tht=pico_cmd.Tht_Ref(mea_his_fil)
        mod_ipr.R_V_Nrm=0
        for i_scn in range(mod_ipr.Pht_Scns):
            cmr_cmd,VTim[0][i_scn]=Pix_Inten(pico_cmd,"D","Test",cmr_cmd,mea_dir_pth[4]+"Test_"+str(i_scn))
            sleep(0.5)
            cmr_cmd,VTim[1][i_scn]=Pix_Inten(pico_cmd,"U","Test",cmr_cmd,mea_dir_pth[4]+"Test_"+str(i_scn))
            mod_ipr.R_V_Nrm+=abs(VTim[1][i_scn]-VTim[0][i_scn])
        mod_ipr.R_V_Nrm=mod_ipr.R_V_Nrm/mod_ipr.Pht_Scns
        fil_xyts_act=fil_xyts[0]+"Ref"+fil_xyts[2]
        Wri_Dat_Flt_1L_Txt(fil_xyts_act,["Time","V_ofs","V_mea"],3,"w")
        Wri_Dat_Flt_1L_Txt(fil_xyts_act,["ms","mV","mV"],3,"a")
        Wri_Dat_Flt_nL_Txt(fil_xyts_act,[Tim,VTim[0],VTim[1]],mod_ipr.Pht_Scns,3,"a")
    for xy_pnt in range(xy_sta,xy_pnt_tot):
        forget=XY[3][xy_pnt]
        x_n,y_m=int(XY[0][xy_pnt]),int(XY[1][xy_pnt])
        xy_act[0],xy_act[1]=X[x_n][y_m],Y[x_n][y_m]
        XY[3][xy_pnt]=xy_act[1]
        xy_lab="Measurement for point "+str(xy_pnt)+"/"+str(xy_pnt_tot)
        plt_obj=Plt_Mea_Man_Upd(plt_obj,3,xy_lab,Tim,Tht,VTim,VTht,xy_act,XY,X,Y,Z)
        pico_cmd.XY_Mvm(xy_prv,xy_act,x_n,y_m,xy_pnt,xy_tot,mea_his_fil)
        VTht=Dat_Cln_1D(mod_ipr.R_Ang_Num,VTht)
        pnt_lab="_pnt_"+str(xy_pnt)+"_"+str(xy_pnt_tot)
        for i_tht in range(mod_ipr.R_Ang_Num):
            VTht[0][i_tht]=0
            VTim=Dat_Cln_1D(mod_ipr.Pht_Scns,VTim)
            mvm_tht=pico_cmd.Tht_Set(i_tht,mea_his_fil)
            pnt_tht_lab=pnt_lab+"_tht_"+str(i_tht)
            for i_scn in range(mod_ipr.Pht_Scns):
                lab_scn="Camera_Offset"+pnt_tht_lab+"_scan_"+str(i_scn)
                cmr_cmd,VTim[0][i_scn]=Pix_Inten(pico_cmd,"D",cmr_cmd,lab_scn,mea_dir_pth[4]+lab_scn)
                scn_lab="Offset for scan "+str(i_scn)+"/"+str(mod_ipr.Pht_Scns)
                plt_obj=Plt_Mea_Man_Upd(plt_obj,0,scn_lab,Tim,Tht,VTim,VTht,xy_act,XY,X,Y,Z)
            for i_scn in range(mod_ipr.Pht_Scns):
                lab_scn="Camera_Measure"+pnt_tht_lab+"_scan_"+str(i_scn)
                cmr_cmd,VTim[1][i_scn]=Pix_Inten(pico_cmd,"U",cmr_cmd,lab_scn,mea_dir_pth[4]+lab_scn)
                scn_lab="Measurement for scan "+str(i_scn)+"/"+str(mod_ipr.Pht_Scns)
                plt_obj=Plt_Mea_Man_Upd(plt_obj,0,scn_lab,Tim,Tht,VTim,VTht,xy_act,XY,X,Y,Z)
            for i_scn in range(mod_ipr.Pht_Scns): VTht[0][i_tht]+=abs(VTim[1][i_scn]-VTim[0][i_scn])
            #print(VTht[0][i_tht],VTim[1][i_scn],VTim[0][i_scn])
            fil_xyts_act=fil_xyts[0]+"X_"+str(x_n)+"_Y_"+str(y_m)+fil_xyts[1]+str(i_tht)+fil_xyts[2]
            Wri_Dat_Flt_1L_Txt(fil_xyts_act,["Time","V_ofs","V_mea"],3,"w")
            Wri_Dat_Flt_1L_Txt(fil_xyts_act,["ms","mV","mV"],3,"a")
            Wri_Dat_Flt_nL_Txt(fil_xyts_act,[Tim,VTim[0],VTim[1]],mod_ipr.Pht_Scns,3,"a")
            tht_lab="Measurement for angle "+str(pico_cmd.r_ang_val[i_tht])+" or "+str(i_tht)+"/"+str(mod_ipr.R_Ang_Num)
            VTht[0][i_tht]=VTht[0][i_tht]/mod_ipr.Pht_Scns
            plt_obj=Plt_Mea_Man_Upd(plt_obj,1,tht_lab,Tim,Tht,VTim,VTht,xy_act,XY,X,Y,Z)
        fil_xyt_act=fil_xyt[0]+"X_"+str(x_n)+"_Y_"+str(y_m)+fil_xyt[1]
        Wri_Dat_Flt_1L_Txt(fil_xyt_act,["Angle","V_mea","V_fit"],3,"w")
        Wri_Dat_Flt_1L_Txt(fil_xyt_act,["degree","mV","mV"],3,"a")
        Wri_Dat_Flt_nL_Txt(fil_xyt_act,[Tht,VTht[0],VTht[1]],mod_ipr.R_Ang_Num,3,"a")
        Z[x_n][y_m],Z_err[x_n][y_m],N[x_n][y_m],N_err[x_n][y_m],A=0,0,0,0,0
        Z_fit,Z_err_fit,N_fit,N_err_fit,A_fit=[],[],[],[],[]
        fit_scs=True #False
        def ZN_append(Z,ZE,N,NE,A,z,ze,n,ne,a):
            Z.append(z)
            ZE.append(ze)
            N.append(n)
            NE.append(ne)
            A.append(a)
            return Z,ZE,N,NE,A
        Fit_Mth,fit_wth="lm",100
        z_chi_tol=1e-3
        while fit_wth<200000: 
            try:
                z,z_err,n,n_fit,a=Fit_R(pico_cmd.r_ang_val,ThtE,VTht[0],Fit_Mth,1.5,fit_wth)
                Z_fit,Z_err_fit,N_fit,N_err_fit,A_fit=ZN_append(Z_fit,Z_err_fit,N_fit,N_err_fit,A_fit,z,z_err,n,n_fit,a)
            except RuntimeError: print("Fitting failed")
            fit_wth=fit_wth*10
            z_chi_act=Z_err_fit[-1]/Z_fit[-1]
            print(z_chi_act)
            if z_chi_act<z_chi_tol:   
                A,z_min=Z_err_fit[-1],A_fit[-1]
                Z[x_n][y_m],Z_err[x_n][y_m]=Z_fit[-1],Z_err_fit[-1]
                N[x_n][y_m],N_err[x_n][y_m]=N_fit[-1],N_err_fit[-1]
                break
        VTht[1]=R_plt(Tht,Z[x_n][y_m],N[x_n][y_m],A)
        XYZN[0],XYZN[1],XYZN[2]=xy_pnt,X[x_n][y_m],Y[x_n][y_m]
        XYZN[3],XYZN[4],XYZN[5],XYZN[6]=Z[x_n][y_m],Z_err[x_n][y_m],N[x_n][y_m],N_err[x_n][y_m]
        Wri_Dat_Flt_1L_Txt(fil_xy,XYZN,7,"a")
        print(Z[x_n][y_m],Z_err[x_n][y_m],N[x_n][y_m],N_err[x_n][y_m],A)
        plt_obj=Plt_Mea_Man_Upd(plt_obj,1,tht_lab,Tim,Tht,VTim,VTht,xy_act,XY,X,Y,Z)
        xy_prv=xy_act
        XY[4][xy_pnt]=forget
    plt_obj=Plt_Mea_Man_Upd(plt_obj,2,xy_lab,Tim,Tht,VTim,VTht,X,Y,Z)
    print('Measurement finished succesfully!!!')
"""
if __name__ =='__main__':
    #print('Number of CPU cores:',cpu_count())
    His_Upt(mea_his_fil,0,'*****Measurements start*****') 	
    mea_stp=False #mea_stp=measurements stop.
    tim_fin=Tim_HMS_Dec_Con(mod_ipr.Cap_Tim_Fin) #tim_fin=time to finish.
    dtm_wav,dtf_wav,dtf_tim,dtm_off,dtm_ref,dtm_itn,dtf_oms,dtf_acs,dtf_scd,dtf_con=Mea_DtB_Ini(mea_his_fil,mea_dte,spc_act,spe_sfn)
    plt_obj=Plt_Mea_Man_Ini(dtm_wav,dtf_wav,dtf_tim,dtm_itn,dtf_oms,dtf_acs,dtf_scd,dtf_con) #fig_mea=figure measurement. axs_itn=axes intensities. axs_oms=axes optical density measurement simulated. axs_acs=axes absorption cross section. axs_scd=axes slant column densities. axs_con=axes concentrations.
    #fig_mea,axs_itn,axs_oms,axs_acs,axs_scd,axs_con,lin_itn,lin_oms,lin_acs,lin_scd,lin_con
    while(mea_stp==False):
        His_Upt(mea_his_fil,1,'Performing set measurement '+str(mea_set)+' ...')
        dtm_off,tim_off=Cap_Off(mea_his_fil,mea_cnt_fil,dtm_wav,mea_dte,mea_set,spc_act,spe_sfn,srv_ctr,mea_dir_pth[2],'Offset')
        Plt_Mea_Man_Upd(dtm_wav,dtf_wav,dtf_tim,dtm_off,dtf_oms,dtf_acs,dtf_scd,dtf_con,plt_obj,'Offset for set '+str(mea_set))
        dtm_ref,tim_ref=Cap_Ref(mea_his_fil,mea_cnt_fil,dtm_wav,mea_dte,mea_set,spc_act,spe_sfn,srv_ctr,mea_dir_pth[3],'Reference_Normal')
        Plt_Mea_Man_Upd(dtm_wav,dtf_wav,dtf_tim,dtm_ref,dtf_oms,dtf_acs,dtf_scd,dtf_con,plt_obj,'Reference normal for set '+str(mea_set))
        if mod_ipr.Sol_Trk_Act==True:
            dtm_rst,tim_rst=Cap_RST(mea_his_fil,mea_cnt_fil,dtm_wav,mea_dte,mea_set,spc_act,spe_sfn,srv_ctr,mea_dir_pth[3],'Reference_Sun_Tracking')
            Plt_Mea_Man_Upd(dtm_wav,dtf_wav,dtf_tim,dtm_rst,dtf_oms,dtf_acs,dtf_scd,dtf_con,plt_obj,'Reference sun tracking for set '+str(mea_set))
        for i_ele_pul in range(0,mod_ipr.Ele_Ang_Num,1): #i_ele_pul=i-counter elevation pulse.
            for i_azi_pul in range(0,mod_ipr.Azi_Ang_Num,1): #i_azi_apul=i-counter azimutal pulse.
                Srv_Tar(mea_his_fil,srv_ctr,[i_azi_pul,i_ele_pul,i_ele_pul])
                dtm_itn,mea_tim=Cap_Mea(mea_his_fil,mea_cnt_fil,dtm_wav,mea_dte,mea_set,spc_act,spe_sfn,mea_dir_pth[1],i_azi_pul,i_ele_pul)
                Plt_Mea_Man_Upd(dtm_wav,dtf_wav,dtf_tim,dtm_itn,dtf_oms,dtf_acs,dtf_scd,dtf_con,plt_obj,'Measurement [Azi='+str(mod_ipr.Azi_Ang_Val[i_azi_pul])+','+'Ele='+str(mod_ipr.Ele_Ang_Val[i_ele_pul])+'] for set '+str(mea_set))
            i_ele_pul+=1
            for i_azi_pul in range(1,mod_ipr.Azi_Ang_Num+1,-1): #i_azi_apul=i-counter azimutal pulse.
                Srv_Tar(mea_his_fil,srv_ctr,[mod_ipr.Azi_Ang_Num-i_azi_pul,i_ele_pul,i_ele_pul])
                dtm_itn,mea_tim=Cap_Mea(mea_his_fil,mea_cnt_fil,dtm_wav,mea_dte,mea_set,spc_act,spe_sfn,mea_dir_pth[1],i_azi_pul,i_ele_pul)
                Plt_Mea_Man_Upd(dtm_wav,dtf_wav,dtf_tim,dtm_itn,dtf_oms,dtf_acs,dtf_scd,dtf_con,plt_obj,'Measurement [Azi='+str(mod_ipr.Azi_Ang_Val[i_azi_pul])+','+'Ele='+str(mod_ipr.Ele_Ang_Val[i_ele_pul])+'] for set '+str(mea_set))
        tim_act=Tim_HMS_Dec_Con(Tim_Upt_Int()) #tim_act=time actual.
        if tim_fin<=tim_act: mea_stp=True
        else: mea_set=mea_set+1
    His_Upt(mea_his_fil,0,'Measurements finished!!!')
    print('Measurement finished succesfully!!!')
"""
