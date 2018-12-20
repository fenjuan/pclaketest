# import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
from pandas import DataFrame
from pandas import Series
from netCDF4 import Dataset
from netCDF4 import num2date
from netCDF4 import date2num
import datetime
import os
import sys
import os.path
import glob


# Reading in model output files, from three different applications, fabm0d,
# gotm1d and gotmlake
output_dir= os.path.normpath(os.getcwd() + os.sep + os.pardir+"/output")
fabm0d=['pclake-fabm0d-2m.nc','pclake-fabm0d-5m.nc','pclake-fabm0d-10m.nc','pclake-fabm0d-20m.nc']
gotm1d=['pclake-gotm1d-2m.nc','pclake-gotm1d-5m.nc','pclake-gotm1d-10m.nc','pclake-gotm1d-20m.nc']
gotmlake=['pclake-gotmlake-2m.nc','pclake-gotmlake-5m.nc','pclake-gotmlake-10m.nc','pclake-gotmlake-20m.nc']


# Set ploting time intervals(keep matplotlib datetime format)
# Since 3 applications has the same time intervals, so use anyone of them is fine
# Set ploting time intervals(keep matplotlib datetime format)
path=os.path.join(output_dir, fabm0d[0])
# convert NetCDF data to Dataset, to read time
time_nc=Dataset(path, mode='r')
time        = time_nc.variables['time']
units       = time_nc.variables['time'].units
valid_times = num2date(time[:], units=units).tolist()
# Set the start and stop point for ploting interval
start=valid_times.index(datetime.datetime(2015, 6, 1))
stop=valid_times.index(datetime.datetime(2016, 9, 1))
# Time for extracting data
time=valid_times[start:stop]
# ploting x axis
dt=datetime.date
# Setting period, and model output intervals is 1day
time_t=mdates.drange(dt(2015,6,1), dt(2016,9,1), datetime.timedelta(days=1))

# Read in gotm1d data, get the vertical avarage value, and store in nc Dataset form
# creat dict for store output of wanted fabm0d data
Tm_0d=[];PAR_0d=[];O2_0d=[];TN_0d=[];TP_0d=[];
Phy_0d=[];Zoo_0d=[];Fish_0d=[]
for f_0d in fabm0d:
    path=os.path.join(output_dir, f_0d)
    fabm0d_nc=Dataset(path, mode='r')
# depths for calculating fish biomass
    if f_0d=='pclake-fabm0d-2m.nc':
        d=2.0
    elif f_0d=='pclake-fabm0d-5m.nc':
        d=5.0
    elif f_0d=='pclake-fabm0d-10m.nc':
        d=10.0
    elif f_0d=='pclake-fabm0d-20m.nc':
        d=20.0
# create empty lists for storging extracted and treated variables
    Tm   = fabm0d_nc.variables['temp'][start:stop,0,0]
    PAR  = fabm0d_nc.variables['phytoplankton_water_phypar'][start:stop,0,0]
    O2   = fabm0d_nc.variables['abiotic_water_sO2W'][start:stop,0,0]
    TN   = fabm0d_nc.variables['pclake_totN_calculator_result'][start:stop,0,0]
    TP   = fabm0d_nc.variables['pclake_totP_calculator_result'][start:stop,0,0]
    Blue = fabm0d_nc.variables['phytoplankton_water_sDBlueW'][start:stop,0,0]
    Gren = fabm0d_nc.variables['phytoplankton_water_sDGrenW'][start:stop,0,0]
    Diat = fabm0d_nc.variables['phytoplankton_water_sDDiatW'][start:stop,0,0]
    Phy  = np.add(np.add(Blue,Gren),Diat)
    Zoo  = fabm0d_nc.variables['zooplankton_sDZoo'][start:stop,0,0]
    Fish = fabm0d_nc.variables['fish_sDFiAd'][start:stop,0,0]*d+     fabm0d_nc.variables['fish_sDFiJv'][start:stop,0,0]*d
# Get anually average values
    Tm_0d.append(np.mean(Tm[:]))
    PAR_0d.append(np.mean(PAR[:]))
    O2_0d.append(np.mean(O2[:]))
    TN_0d.append(np.mean(TN[:]))
    TP_0d.append(np.mean(TP[:]))
    Phy_0d.append(np.mean(Phy[:]))
    Zoo_0d.append(np.mean(Zoo[:]))
    Fish_0d.append(np.mean(Fish[:]))    
Ave_0d = np.row_stack((Tm_0d,PAR_0d,O2_0d,TN_0d,TP_0d,Phy_0d,Zoo_0d,Fish_0d))
df_0d  = DataFrame(Ave_0d,columns=['2m','5m','10m','20m'],index=['Tm','PAR','O2','TN','TP','Phy','Zoo','Fish'])


# Get gotm1d data
Tm_1d_surf=[];Tm_1d_bott=[];Tm_1d_mean=[];
PAR_1d_surf=[];PAR_1d_bott=[];PAR_1d_mean=[];
O2_1d_surf=[];O2_1d_bott=[];O2_1d_mean=[];
TN_1d_surf=[];TN_1d_bott=[];TN_1d_mean=[];
TP_1d_surf=[];TP_1d_bott=[];TP_1d_mean=[];
Phy_1d_surf=[];Phy_1d_bott=[];Phy_1d_mean=[];
Zoo_1d_surf=[];Zoo_1d_bott=[];Zoo_1d_mean=[];
Fish_1d_surf=[];Fish_1d_bott=[];Fish_1d_mean=[];
# depths for calculating fish biomass
 
for f_1d in gotm1d:
    if f_1d=='pclake-gotm1d-2m.nc':
        d=2.0
    elif f_1d=='pclake-gotm1d-5m.nc':
        d=5.0
    elif f_1d=='pclake-gotm1d-10m.nc':
        d=10.0
    elif f_1d=='pclake-gotm1d-20m.nc':
        d=20.0
    path=os.path.join(output_dir, f_1d)
    gotm1d_nc=Dataset(path, mode='r')
#   Get surface value   
    Tm_surf   = gotm1d_nc.variables['temp'][start:stop,-1,0,0]
    PAR_surf  = gotm1d_nc.variables['phytoplankton_water_phypar'][start:stop,-1,0,0]
    O2_surf   = gotm1d_nc.variables['abiotic_water_sO2W'][start:stop,-1,0,0]
    TN_surf   = gotm1d_nc.variables['pclake_totN_calculator_result'][start:stop,-1,0,0]
    TP_surf   = gotm1d_nc.variables['pclake_totP_calculator_result'][start:stop,-1,0,0]
    Blue_surf  = gotm1d_nc.variables['phytoplankton_water_sDBlueW'][start:stop,-1,0,0]
    Gren_surf  = gotm1d_nc.variables['phytoplankton_water_sDGrenW'][start:stop,-1,0,0]
    Diat_surf  = gotm1d_nc.variables['phytoplankton_water_sDDiatW'][start:stop,-1,0,0]    
    Phy_surf  = np.add(Blue_surf,np.add(Gren_surf,Diat_surf))
    Zoo_surf  = gotm1d_nc.variables['zooplankton_sDZoo'][start:stop,-1,0,0]
    Fish_surf = gotm1d_nc.variables['fish_sDFiAd'][start:stop,-1,0,0]*d + gotm1d_nc.variables['fish_sDFiJv'][start:stop,-1,0,0]*d    
#   Get bottom value
    Tm_bott   = gotm1d_nc.variables['temp'][start:stop,0,0,0]
    PAR_bott  = gotm1d_nc.variables['phytoplankton_water_phypar'][start:stop,0,0,0]
    O2_bott   = gotm1d_nc.variables['abiotic_water_sO2W'][start:stop,0,0,0]
    TN_bott   = gotm1d_nc.variables['pclake_totN_calculator_result'][start:stop,0,0,0]
    TP_bott   = gotm1d_nc.variables['pclake_totP_calculator_result'][start:stop,0,0,0]
    Blue_bott = gotm1d_nc.variables['phytoplankton_water_sDBlueW'][start:stop,0,0,0]
    Gren_bott = gotm1d_nc.variables['phytoplankton_water_sDGrenW'][start:stop,0,0,0]
    Diat_bott = gotm1d_nc.variables['phytoplankton_water_sDDiatW'][start:stop,0,0,0]
    Phy_bott  = np.add(Blue_bott,np.add(Gren_bott,Diat_bott)) 
    Zoo_bott  = gotm1d_nc.variables['zooplankton_sDZoo'][start:stop,0,0,0]
    Fish_bott = gotm1d_nc.variables['fish_sDFiAd'][start:stop,0,0,0]*d + gotm1d_nc.variables['fish_sDFiJv'][start:stop,0,0,0]*d    
#  Get vertical average    
    Tm_mean=[];PAR_mean=[];O2_mean=[];TN_mean=[];TP_mean=[];Zoo_mean=[];Fish_mean=[]
    Blue_mean=[]; Gren_mean=[];Diat_mean=[]
    i=start
    for t in time:
        Tm_mean.append(np.mean(gotm1d_nc.variables['temp'][i,:,0,0]))
        PAR_mean.append(np.mean(gotm1d_nc.variables['phytoplankton_water_phypar'][i,:,0,0]))
        O2_mean.append(np.mean(gotm1d_nc.variables['abiotic_water_sO2W'][i,:,0,0]))
        TN_mean.append(np.mean(gotm1d_nc.variables['pclake_totN_calculator_result'][i,:,0,0]))
        TP_mean.append(np.mean(gotm1d_nc.variables['pclake_totP_calculator_result'][i,:,0,0]))
        Blue_mean.append(np.mean(gotm1d_nc.variables['phytoplankton_water_sDBlueW'][i,:,0,0]))
        Gren_mean.append(np.mean(gotm1d_nc.variables['phytoplankton_water_sDGrenW'][i,:,0,0]))
        Diat_mean.append(np.mean(gotm1d_nc.variables['phytoplankton_water_sDDiatW'][i,:,0,0]))
        Zoo_mean.append(np.mean(gotm1d_nc.variables['zooplankton_sDZoo'][i,:,0,0]))
        Fish_mean.append(np.sum(gotm1d_nc.variables['fish_sDFiAd'][i,:,0,0]*0.4) +                     np.sum(gotm1d_nc.variables['fish_sDFiJv'][i,:,0,0]*0.4))
        i=i+1
    Phy_mean = np.add(Blue_mean, np.add(Gren_mean, Diat_mean))    
# Assemble surface variables
    Tm_1d_surf.append(np.mean(Tm_surf[:]))
    PAR_1d_surf.append(np.mean(PAR_surf[:]))
    O2_1d_surf.append(np.mean(O2_surf[:]))
    TN_1d_surf.append(np.mean(TN_surf[:]))
    TP_1d_surf.append(np.mean(TP_surf[:]))
    Phy_1d_surf.append(np.mean(Phy_surf[:]))
    Zoo_1d_surf.append(np.mean(Zoo_surf[:]))
    Fish_1d_surf.append(np.mean(Fish_surf[:]))
    
# Assemble bottom variables    
    Tm_1d_bott.append(np.mean(Tm_bott[:])) 
    PAR_1d_bott.append(np.mean(PAR_bott[:]))
    O2_1d_bott.append(np.mean(O2_bott[:]))
    TN_1d_bott.append(np.mean(TN_bott[:]))
    TP_1d_bott.append(np.mean(TP_bott[:]))
    Phy_1d_bott.append(np.mean(Phy_bott[:]))
    Zoo_1d_bott.append(np.mean(Zoo_bott[:]))
    Fish_1d_bott.append(np.mean(Fish_bott[:]))
# Assemble mean values
    Tm_1d_mean.append(np.mean(Tm_mean[:]))
    PAR_1d_mean.append(np.mean(PAR_mean[:]))
    O2_1d_mean.append(np.mean(O2_mean[:]))
    TN_1d_mean.append(np.mean(TN_mean[:]))    
    TP_1d_mean.append(np.mean(TP_mean[:]))
    Phy_1d_mean.append(np.mean(Phy_mean[:]))
    Zoo_1d_mean.append(np.mean(Zoo_mean[:]))
    Fish_1d_mean.append(np.mean(Fish_mean[:]))
# Put three different layer together   
Tm_1d= np.row_stack((Tm_1d_mean,Tm_1d_surf,Tm_1d_bott))
PAR_1d= np.row_stack((PAR_1d_mean,PAR_1d_surf,PAR_1d_bott))
O2_1d= np.row_stack((O2_1d_mean,O2_1d_surf,O2_1d_bott))
TN_1d= np.row_stack((TN_1d_mean,TN_1d_surf,TN_1d_bott))
TP_1d= np.row_stack((TP_1d_mean,TP_1d_surf,TP_1d_bott))    
Phy_1d= np.row_stack((Phy_1d_mean,Phy_1d_surf,Phy_1d_bott))
Zoo_1d= np.row_stack((Zoo_1d_mean,Zoo_1d_surf,Zoo_1d_bott))
Fish_1d= np.row_stack((Fish_1d_mean,Fish_1d_surf,Fish_1d_bott))

# assemble all data together
Ave_1d = np.row_stack((Tm_1d,PAR_1d,O2_1d,TN_1d,TP_1d,Phy_1d,Zoo_1d,Fish_1d))
df_1d  = DataFrame(Ave_1d,columns=['2m','5m','10m','20m'],index=['Tm','Tm_surf','Tm_bott',
                                                                 'PAR','PAR_surf','PAR_bott',
                                                                 'O2','O2_surf','O2_bott',
                                                                 'TN','TN_surf','TN_bott',
                                                                 'TP','TP_surf','TP_bott',
                                                                 'Phy','Phy_surf','Phy_bott',
                                                                 'Zoo','Zoo_surf','Zoo_bott',
                                                                 'Fish','Fish_surf','Fish_bott'])



# get gotmlake data
Tm_lake_surf=[];Tm_lake_bott=[];Tm_lake_mean=[];
PAR_lake_surf=[];PAR_lake_bott=[];PAR_lake_mean=[];
O2_lake_surf=[];O2_lake_bott=[];O2_lake_mean=[];
TN_lake_surf=[];TN_lake_bott=[];TN_lake_mean=[];
TP_lake_surf=[];TP_lake_bott=[];TP_lake_mean=[];
Phy_lake_surf=[];Phy_lake_bott=[];Phy_lake_mean=[];
Zoo_lake_surf=[];Zoo_lake_bott=[];Zoo_lake_mean=[];
Fish_lake_surf=[];Fish_lake_bott=[];Fish_lake_mean=[];
# Get the volumn fraction for each depth in gotmlake
# calculated according to hypsograph data in excel.
f_Vn_2m=[0.04,0.12,0.20,0.28,0.36]
f_Vn_5m=[0.01,0.02,0.03,0.04,0.05,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.15]
f_Vn_10m=[0.0025,0.0056,0.0087,0.0119,0.0150,0.0181,0.0212,0.0244,0.0275,
          0.0306,0.0337,0.0369,0.0400,0.0431,0.0463,0.0494,0.0525,0.0556,
          0.0588,0.0619,0.0650,0.0681,0.0713,0.0744,0.0775]
f_Vn_20m=[0.000854443,0.001635895,0.002417346,0.003198797,0.003980249,0.0047617,
          0.005543151,0.006324602,0.007106054,0.007887505,0.008668956,0.009450408,
          0.010231859,0.01101331,0.011794761,0.012576213,0.013357664,0.014139115,
          0.014920567,0.015702018,0.016483469,0.01726492,0.018046372,0.018827823,
          0.019609274,0.020390726,0.021172177,0.021953628,0.02273508,0.023516531,
          0.024297982,0.025079433,0.025860885,0.026642336,0.027423787,0.028205239,
          0.02898669,0.029768141,0.030549592,0.031331044,0.032112495,0.032893946,
          0.033675398,0.034456849,0.0352383,0.036019751,0.036801203,0.037582654,
          0.038364105,0.039145557]

for f_lake in gotmlake:
    path=os.path.join(output_dir, f_lake)
    gotmlake_nc=Dataset(path, mode='r')
    # Get the f_lvl for different depth
    lvl=len(gotmlake_nc.variables['temp'][0])
    if lvl==5:
        f_lvl=f_Vn_2m;
        d = 2.0;
    elif lvl== 13:
        f_lvl=f_Vn_5m;
        d = 5;.0
    elif lvl==25:
        f_lvl=f_Vn_10m;
        d = 10.0 ;
    elif lvl==50:
        f_lvl=f_Vn_20m;
        d = 20.0;
#   Get surface value   
    Tm_surf   = gotmlake_nc.variables['temp'][start:stop,-1,0,0]
    PAR_surf  = gotmlake_nc.variables['phytoplankton_water_phypar'][start:stop,-1,0,0]
    O2_surf   = gotmlake_nc.variables['abiotic_water_sO2W'][start:stop,-1,0,0]
    TN_surf   = gotmlake_nc.variables['pclake_totN_calculator_result'][start:stop,-1,0,0]
    TP_surf   = gotmlake_nc.variables['pclake_totP_calculator_result'][start:stop,-1,0,0]
    Blue_surf = gotmlake_nc.variables['phytoplankton_water_sDBlueW'][start:stop,-1,0,0]
    Gren_surf = gotmlake_nc.variables['phytoplankton_water_sDGrenW'][start:stop,-1,0,0]
    Diat_surf = gotmlake_nc.variables['phytoplankton_water_sDDiatW'][start:stop,-1,0,0]
    Phy_surf  = np.add(Blue_surf, np.add(Gren_surf,Diat_surf))
    Zoo_surf  = gotmlake_nc.variables['zooplankton_sDZoo'][start:stop,-1,0,0]
    Fish_surf = gotmlake_nc.variables['fish_sDFiAd'][start:stop,-1,0,0]*d +                 gotmlake_nc.variables['fish_sDFiJv'][start:stop,-1,0,0]*d    
#   Get bottom value
    Tm_bott   = gotmlake_nc.variables['temp'][start:stop,0,0,0]
    PAR_bott  = gotmlake_nc.variables['phytoplankton_water_phypar'][start:stop,0,0,0]
    O2_bott   = gotmlake_nc.variables['abiotic_water_sO2W'][start:stop,0,0,0]
    TN_bott   = gotmlake_nc.variables['pclake_totN_calculator_result'][start:stop,0,0,0]
    TP_bott   = gotmlake_nc.variables['pclake_totP_calculator_result'][start:stop,0,0,0]
    Blue_bott = gotmlake_nc.variables['phytoplankton_water_sDBlueW'][start:stop,0,0,0]
    Gren_bott = gotmlake_nc.variables['phytoplankton_water_sDGrenW'][start:stop,0,0,0]
    Diat_bott = gotmlake_nc.variables['phytoplankton_water_sDDiatW'][start:stop,0,0,0]
    Phy_bott  = np.add (Blue_bott, np.add(Gren_bott, Diat_bott))    
    Zoo_bott  = gotmlake_nc.variables['zooplankton_sDZoo'][start:stop,0,0,0]
    Fish_bott = gotmlake_nc.variables['fish_sDFiAd'][start:stop,0,0,0]*d +                 gotmlake_nc.variables['fish_sDFiJv'][start:stop,0,0,0]*d    
#  Get vertical wieghted average       
    Tm_mean=[];PAR_mean=[];O2_mean=[];TN_mean=[];TP_mean=[];Zoo_mean=[];Fish_mean=[]
    Blue_mean=[]; Diat_mean=[]; Gren_mean=[]
    i=start
    for t in time:
        Tm_mean.append(np.sum(gotmlake_nc.variables['temp'][i,:,0,0]*f_lvl[:]))
        PAR_mean.append(np.sum(gotmlake_nc.variables['phytoplankton_water_phypar'][i,:,0,0]*f_lvl[:]))
        O2_mean.append(np.sum(gotmlake_nc.variables['abiotic_water_sO2W'][i,:,0,0]*f_lvl[:]))
        TN_mean.append(np.sum(gotmlake_nc.variables['pclake_totN_calculator_result'][i,:,0,0]*f_lvl[:]))
        TP_mean.append(np.sum(gotmlake_nc.variables['pclake_totP_calculator_result'][i,:,0,0]*f_lvl[:]))
        Blue_mean.append(np.sum(gotmlake_nc.variables['phytoplankton_water_sDBlueW'][i,:,0,0]*f_lvl[:]))
        Gren_mean.append(np.sum(gotmlake_nc.variables['phytoplankton_water_sDGrenW'][i,:,0,0]*f_lvl[:]))
        Diat_mean.append(np.sum(gotmlake_nc.variables['phytoplankton_water_sDDiatW'][i,:,0,0]*f_lvl[:]))
        Zoo_mean.append(np.sum(gotmlake_nc.variables['zooplankton_sDZoo'][i,:,0,0]*f_lvl[:]))
        Fish_mean.append(np.sum(gotmlake_nc.variables['fish_sDFiAd'][i,:,0,0]*0.4) +                     np.sum(gotmlake_nc.variables['fish_sDFiJv'][i,:,0,0]*0.4))
        i=i+1
    Phy_mean = np.add(Blue_mean, np.add(Gren_mean, Diat_mean))    
# Assemble surface variables
    Tm_lake_surf.append(np.mean(Tm_surf[:]))
    PAR_lake_surf.append(np.mean(PAR_surf[:]))
    O2_lake_surf.append(np.mean(O2_surf[:]))
    TN_lake_surf.append(np.mean(TN_surf[:]))
    TP_lake_surf.append(np.mean(TP_surf[:]))
    Phy_lake_surf.append(np.mean(Phy_surf[:]))
    Zoo_lake_surf.append(np.mean(Zoo_surf[:]))
    Fish_lake_surf.append(np.mean(Fish_surf[:]))
    
# Assemble bottom variables    
    Tm_lake_bott.append(np.mean(Tm_bott[:])) 
    PAR_lake_bott.append(np.mean(PAR_bott[:]))
    O2_lake_bott.append(np.mean(O2_bott[:]))
    TN_lake_bott.append(np.mean(TN_bott[:]))
    TP_lake_bott.append(np.mean(TP_bott[:]))
    Phy_lake_bott.append(np.mean(Phy_bott[:]))
    Zoo_lake_bott.append(np.mean(Zoo_bott[:]))
    Fish_lake_bott.append(np.mean(Fish_bott[:]))
# Assemble mean values
    Tm_lake_mean.append(np.mean(Tm_mean[:]))
    PAR_lake_mean.append(np.mean(PAR_mean[:]))
    O2_lake_mean.append(np.mean(O2_mean[:]))
    TN_lake_mean.append(np.mean(TN_mean[:]))    
    TP_lake_mean.append(np.mean(TP_mean[:]))
    Phy_lake_mean.append(np.mean(Phy_mean[:]))
    Zoo_lake_mean.append(np.mean(Zoo_mean[:]))
    Fish_lake_mean.append(np.mean(Fish_mean[:]))        
        
# Put three different layer together   
Tm_lake= np.row_stack((Tm_lake_mean,Tm_lake_surf,Tm_lake_bott))
PAR_lake= np.row_stack((PAR_lake_mean,PAR_lake_surf,PAR_lake_bott))
O2_lake= np.row_stack((O2_lake_mean,O2_lake_surf,O2_lake_bott))
TN_lake= np.row_stack((TN_lake_mean,TN_lake_surf,TN_lake_bott))
TP_lake= np.row_stack((TP_lake_mean,TP_lake_surf,TP_lake_bott))    
Phy_lake= np.row_stack((Phy_lake_mean,Phy_lake_surf,Phy_lake_bott))
Zoo_lake= np.row_stack((Zoo_lake_mean,Zoo_lake_surf,Zoo_lake_bott))
Fish_lake= np.row_stack((Fish_lake_mean,Fish_lake_surf,Fish_lake_bott))

# assemble all data together
Ave_lake = np.row_stack((Tm_lake,PAR_lake,O2_lake,TN_lake,TP_lake,Phy_lake,Zoo_lake,Fish_lake))
df_lake  = DataFrame(Ave_lake,columns=['2m','5m','10m','20m'],index=['Tm','Tm_surf','Tm_bott',
                                                                 'PAR','PAR_surf','PAR_bott',
                                                                 'O2','O2_surf','O2_bott',
                                                                 'TN','TN_surf','TN_bott',
                                                                 'TP','TP_surf','TP_bott',
                                                                 'Phy','Phy_surf','Phy_bott',
                                                                 'Zoo','Zoo_surf','Zoo_bott',
                                                                 'Fish','Fish_surf','Fish_bott'])



# Re-structure data
sum_2m =  pd.concat([df_0d.loc[:,'2m'],df_1d.loc[:,'2m'],df_lake.loc[:,'2m']],axis=1,keys=['0d','1d','lake'])
sum_5m =  pd.concat([df_0d.loc[:,'5m'],df_1d.loc[:,'5m'],df_lake.loc[:,'5m']],axis=1,keys=['0d','1d','lake'])
sum_10m =  pd.concat([df_0d.loc[:,'10m'],df_1d.loc[:,'10m'],df_lake.loc[:,'10m']],axis=1,keys=['0d','1d','lake'])
sum_20m =  pd.concat([df_0d.loc[:,'20m'],df_1d.loc[:,'20m'],df_lake.loc[:,'20m']],axis=1,keys=['0d','1d','lake'])
# ensemble data and output 
Total_annual=pd.concat([sum_2m,sum_5m,sum_10m,sum_20m],axis=1,keys=['2m','5m','10m','20m'])
Total_annual.to_csv('table1.csv')

