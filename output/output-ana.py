
# coding: utf-8
"""
****************Section for import all needed libraries************************
"""
# numpy arrary manipulation module
import numpy as np
# matplotlib plot library and its formating modules
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
# Pandas library, for data storage and manipulation
import pandas as pd
from pandas import DataFrame
from pandas import Series
# NetCDF library for reading model output and interface for exporting
# NC file to normal arrays and pandas dataset
from netCDF4 import Dataset
from netCDF4 import num2date
from netCDF4 import date2num
# Normal system modules, for reading file path
import os
import sys
import os.path
import glob
import datetime
"""
*************************End of library section********************************
"""


"""
*************************File reading section**********************************
files names for each type of model simulation is store as string array,
 fabm0d[], gotm1d[], gotmlake[], respectively
"""
# Reading in model output files, from three different applications, fabm0d,
# gotm1d and gotmlake
output_dir= os.path.normpath(os.getcwd() + os.sep + os.pardir+"/output")
# fabm0d files
#fabm0d=['pclake-fabm0d-2m.nc','pclake-fabm0d-5m.nc','pclake-fabm0d-10m.nc' \
#        'pclake-fabm0d-20m.nc']
#gotm1d=['pclake-gotm1d-2m.nc','pclake-gotm1d-5m.nc','pclake-gotm1d-10m.nc', \
#        'pclake-gotm1d-20m.nc']
#gotmlake=['pclake-gotmlake-2m.nc','pclake-gotmlake-5m.nc',\
#         'pclake-gotmlake-10m.nc','pclake-gotmlake-20m.nc']
fabm0d=[];gotm1d=[];gotmlake=[]
for f_0d in glob.glob("*fabm0d*.nc"):
    fabm0d.append(f_0d)
# gotm1d files
for f_1d in glob.glob("*gotm1d*.nc"):
    gotm1d.append(f_1d)
# gotm-lake files
for f_lake in glob.glob("*gotmlake*.nc"):
    gotmlake.append(f_lake)

"""
**********************End of file reading section******************************
"""
"""
********************Section for setting up analized period*********************
Since 3 applications has the same time intervals, so use anyone of them is fine
"""
# Set ploting time intervals(keep matplotlib datetime format)
path=os.path.join(output_dir, fabm0d[0])
# convert NetCDF data to Dataset, to read time
time_nc=Dataset(path, mode='r')
time        = time_nc.variables['time']
units       = time_nc.variables['time'].units
valid_times = num2date(time[:], units=units).tolist()
# Set the start and stop point for ploting interval
start=valid_times.index(datetime.datetime(2015, 1, 1))
stop=valid_times.index(datetime.datetime(2016, 1, 1))
# Time for extracting data
time=valid_times[start:stop]
# ploting x axis
dt=datetime.date
# Setting period, and model output intervals is 1day
time_t=mdates.drange(dt(2015,1,1), dt(2016,1,1), datetime.timedelta(days=1))
"""
*****************End of Section for setting up analized period*****************
"""

"""
*****************Sectin for reading line plot data*****************************
line plotting data are comparison with 3 different model set-ups: with 0D output
(one value for whole water columne), 1D avaraged value(layer avaraged mean) and
lake volumn avaraged value
"""
# Read in gotm1d data, get the vertical avarage value, and store in nc Dataset form
df_fabm0d={};df_gotm1d={};df_gotmlake={}
for f_0d in fabm0d:
    path=os.path.join(output_dir, f_0d)
    fabm0d_nc=Dataset(path, mode='r')
# create empty lists for storging extracted and treated variables
    temperature=fabm0d_nc.variables['temp'][start:stop,0,0]
    PAR=fabm0d_nc.variables['phytoplankton_water_partop'][start:stop,0,0]
    Oxygen=fabm0d_nc.variables['abiotic_water_sO2W'][start:stop,0,0]
    TP=fabm0d_nc.variables['pclake_totP_calculator_result'][start:stop,0,0]
    TN=fabm0d_nc.variables['pclake_totN_calculator_result'][start:stop,0,0]
    Phyto=fabm0d_nc.variables['phytoplankton_water_aDPhytW'][start:stop,0,0]
    Zoo=fabm0d_nc.variables['foodweb_water_sDZoo'][start:stop,0,0]
    Fish=fabm0d_nc.variables['foodweb_water_sDFiAd'][start:stop,0,0]+\
     fabm0d_nc.variables['foodweb_water_sDFiJv'][start:stop,0,0]
    Veg=fabm0d_nc.variables['macrophytes_sDVeg'][start:stop,0,0]
    Ben=fabm0d_nc.variables['foodweb_sediment_sDBent'][start:stop,0,0]
# put list into pandas dataframe format
    temp=DataFrame(temperature,index=time,columns=['temp'])
    PAR=DataFrame(PAR,index=time,columns=['PAR'])
    O2=DataFrame(Oxygen,index=time,columns=['O2'])
    totP=DataFrame(TP,index=time,columns=['totP'])
    totN=DataFrame(TN,index=time,columns=['totN'])
    aDPhytW=DataFrame(Phyto,index=time,columns=['aDPhytW'])
    sDZoo=DataFrame(Zoo,index=time,columns=['sDZoo'])
    aDFish=DataFrame(Fish,index=time,columns=['aDFish'])
    sDVeg=DataFrame(Veg,index=time,columns=['sDVeg'])
    sDBent=DataFrame(Ben,index=time,columns=['sDBent'])
# put data into dict for future usage
    df_fabm0d[f_0d]=pd.concat([temp,PAR,O2,totP,totN,aDPhytW,sDZoo,aDFish,\
                              sDVeg,sDBent],axis=1)

# Read in gotm1d data, get the vertical avarage value, and store in nc Dataset form
# Loop over gotm1d files and get the netcdf data
for f_1d in gotm1d:
    path=os.path.join(output_dir, f_1d)
    gotm1d_nc=Dataset(path, mode='r')
# create empty lists for storging extracted and treated variables
    temperature=[];PAR=[];Oxygen=[];TP=[];TN=[]
    Phyto=[];Zoo=[];Fish=[];Veg=[];Ben=[]
# loop over time and put the variable in lists
    i=0
    for t in time:
        temperature.append(np.mean(gotm1d_nc.variables['temp'][i,:,0,0]))
        Oxygen.append(np.mean(gotm1d_nc.variables['abiotic_water_sO2W'][i,:,0,0]))
        TP.append(np.mean(gotm1d_nc.variables['pclake_totP_calculator_result'][i,:,0,0]))
        TN.append(np.mean(gotm1d_nc.variables['pclake_totN_calculator_result'][i,:,0,0]))
        Phyto.append(np.mean(gotm1d_nc.variables['phytoplankton_water_aDPhytW'][i,:,0,0]))
        Zoo.append(np.mean(gotm1d_nc.variables['foodweb_water_sDZoo'][i,:,0,0]))
        Fish.append(np.mean(gotm1d_nc.variables['foodweb_water_sDFiAd'][i,:,0,0])+
                    np.mean(gotm1d_nc.variables['foodweb_water_sDFiJv'][i,:,0,0]))
        PAR.append(gotm1d_nc.variables['phytoplankton_water_partop'][i,-1,0,0])
        Veg.append(gotm1d_nc.variables['macrophytes_sDVeg'][i,0,0])
        Ben.append(gotm1d_nc.variables['foodweb_sediment_sDBent'][i,0,0])
        i=i+1
# put list into pandas dataframe format
    temp=DataFrame(temperature,index=time,columns=['temp'],)
    PAR=DataFrame(PAR,index=time,columns=['PAR'])
    O2=DataFrame(Oxygen,index=time,columns=['O2'])
    totP=DataFrame(TP,index=time,columns=['totP'])
    totN=DataFrame(TN,index=time,columns=['totN'])
    aDPhytW=DataFrame(Phyto,index=time,columns=['aDPhytW'])
    sDZoo=DataFrame(Zoo,index=time,columns=['sDZoo'])
    aDFish=DataFrame(Fish,index=time,columns=['aDFish'])
    sDVeg=DataFrame(Veg,index=time,columns=['sDVeg'])
    sDBent=DataFrame(Ben,index=time,columns=['sDBent'])
# put data into dict for future usage
    df_gotm1d[f_1d]=pd.concat([temp,PAR,O2,totP,totN,aDPhytW,sDZoo,aDFish,sDVeg,sDBent],axis=1)


# Reading gotmlake data, get the volumn weigted avarage value
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
# Loop over gotmlake files and get the netcdf data
for f_lake in gotmlake:
    path=os.path.join(output_dir, f_lake)
    gotmlake_nc=Dataset(path, mode='r')
# Get the f_lvl for different depth
    lvl=len(gotmlake_nc.variables['temp'][0])
    if lvl==5:
        f_lvl=f_Vn_2m
    elif lvl== 13:
        f_lvl=f_Vn_5m
    elif lvl==25:
        f_lvl=f_Vn_10m
    elif lvl==50:
        f_lvl=f_Vn_20m
#    else:
#        print*, "I can't find f_lvl"
# create empty lists for storging extracted and treated variables
    temperature=[];PAR=[];Oxygen=[];TP=[];TN=[];Phyto=[];Zoo=[]
    Fish=[];Veg=[];Ben=[]
# Loop over time, treat the data and put variables in lists
    i=0
    for t in time:
# get the volume average data from gotmlake
        temperature.append(np.sum(gotmlake_nc.variables['temp'][i,:,0,0]*f_lvl[:]))
        Oxygen.append(np.sum(gotmlake_nc.variables['abiotic_water_sO2W'][i,:,0,0]*f_lvl[:]))
        TP.append(np.sum(gotmlake_nc.variables['pclake_totP_calculator_result'][i,:,0,0]*f_lvl[:]))
        TN.append(np.sum(gotmlake_nc.variables['pclake_totN_calculator_result'][i,:,0,0]*f_lvl[:]))
        Phyto.append(np.sum(gotmlake_nc.variables['phytoplankton_water_aDPhytW'][i,:,0,0]*f_lvl[:]))
        Zoo.append(np.sum(gotmlake_nc.variables['foodweb_water_sDZoo'][i,:,0,0]*f_lvl[:]))
        Fish.append(np.sum(gotmlake_nc.variables['foodweb_water_sDFiAd'][i,:,0,0]*f_lvl[:])+
                           np.sum(gotmlake_nc.variables['foodweb_water_sDFiJv'][i,:,0,0]*f_lvl[:]))
# PAR is stil the top layer data
        PAR.append(gotmlake_nc.variables['phytoplankton_water_partop'][i,-1,0,0])
# Get gotmlake sediment data, now it's 1D for state variables
        Veg.append(np.mean(gotmlake_nc.variables['macrophytes_sDVeg'][i,:,0,0]))
        Ben.append(np.mean(gotmlake_nc.variables['foodweb_sediment_sDBent'][i,:,0,0]))
        i=i+1
# Convert data into pandas dataframework
    temp=DataFrame(temperature,index=time,columns=['temp'])
    PAR=DataFrame(PAR,index=time,columns=['PAR'])
    O2=DataFrame(Oxygen,index=time,columns=['O2'])
    totP=DataFrame(TP,index=time,columns=['totP'])
    totN=DataFrame(TN,index=time,columns=['totN'])
    aDPhytW=DataFrame(Phyto,index=time,columns=['aDPhytW'])
    sDZoo=DataFrame(Zoo,index=time,columns=['sDZoo'])
    aDFish=DataFrame(Fish,index=time,columns=['aDFish'])
    sDVeg=DataFrame(Veg,index=time,columns=['sDVeg'])
    sDBent=DataFrame(Ben,index=time,columns=['sDBent'])
# Store gotmlake data into dict for future usage
    df_gotmlake[f_lake]=pd.concat([temp,PAR,O2,totP,totN,aDPhytW,sDZoo,aDFish,sDVeg,sDBent],axis=1)


# join dataframe according to depths
df_2m= pd.concat([df_fabm0d['pclake-fabm0d-2m.nc'],df_gotm1d['pclake-gotm1d-2m.nc'],
                  df_gotmlake['pclake-gotmlake-2m.nc']],axis=1,keys=['fabm0d', 'gotm1d', 'gotmlake'])
df_5m= pd.concat([df_fabm0d['pclake-fabm0d-5m.nc'],df_gotm1d['pclake-gotm1d-5m.nc'],
                  df_gotmlake['pclake-gotmlake-5m.nc']],axis=1,keys=['fabm0d', 'gotm1d', 'gotmlake'])
df_10m= pd.concat([df_fabm0d['pclake-fabm0d-10m.nc'],df_gotm1d['pclake-gotm1d-10m.nc'],
                   df_gotmlake['pclake-gotmlake-10m.nc']],axis=1,keys=['fabm0d', 'gotm1d', 'gotmlake'])
df_20m= pd.concat([df_fabm0d['pclake-fabm0d-20m.nc'],df_gotm1d['pclake-gotm1d-20m.nc'],
                   df_gotmlake['pclake-gotmlake-20m.nc']],axis=1,keys=['fabm0d', 'gotm1d', 'gotmlake'])
# Joined all data together for plot
results= pd.concat([df_2m,df_5m,df_10m,df_20m],axis=1,keys=['2m','5m','10m','20m'])
"""
***************Section for line plotting**************************************
"""
# Give the lables of variables for plotting
models=['fabm0d','gotm1d','gotmlake']
variables_group1 = ['temp', 'totN', 'totP',  'O2']
variables_group2= ['PAR','aDPhytW','sDZoo','aDFish']
depths=['2m','5m','10m','20m']
xticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct',',Nov','Dec']
colors=['b','g','r']
lines=['--','-','-.']
#get y-lim range for each variable
ymin_1=[];ymax_1=[];ymin_2=[];ymax_2=[]
for var in variables_group1:
    ymin_depths=[];ymax_depths=[]
    for depth in depths:
        ymin_models=[];ymax_models=[]
        for model in models:
            ymin_models.append(np.min(np.min(results[depth][model][var])))
            ymax_models.append(np.max(np.max(results[depth][model][var])))
        ymin_depths.append(np.min(ymin_models))
        ymax_depths.append(np.max(ymax_models))
    ymin_1.append(np.min(ymin_depths))
    ymax_1.append(np.max(ymax_depths))
for var in variables_group2:
    ymin_depths=[];ymax_depths=[]
    for depth in depths:
        ymin_models=[];ymax_models=[]
        for model in models:
            ymin_models.append(np.min(np.min(results[depth][model][var])))
            ymax_models.append(np.max(np.max(results[depth][model][var])))
        ymin_depths.append(np.min(ymin_models))
        ymax_depths.append(np.max(ymax_models))
    ymin_2.append(np.min(ymin_depths))
    ymax_2.append(np.max(ymax_depths))


# Library for legends(only used here)
# draw lengend according to the upper right corner
# Variables for ploting legend
fontP = FontProperties()
fontP.set_size('xx-small')
# Plot line plots with three different model output
# Plot group one variables
fig1 = plt.figure(figsize=(8.27, 11.69), dpi=1200)
fig1, axs = plt.subplots(4,4,sharex=True,squeeze=True, )
# adjust the space between subplots
fig1.subplots_adjust(hspace = 0.07)
#plt.subplots_adjust(hspace = .1)
j=0
for depth in depths:
    ymin=ymin_1[j];ymax=ymax_1[j]
    i=0
    for var in variables_group1:
        k=0
        for model in models:
            axs[j,i].plot(time_t,results[depth][model][var], color=colors[k],linestyle=lines[k],label=model)
            axs[i,j].set_ylim(ymin,ymax)
            k=k+1
# Set x-axis and y-axis ticks
# Set x-axis for subplots
            axs[i,j].xaxis_date()
            axs[i,j].xaxis.set_major_locator(mdates.MonthLocator())
            axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            for xtick in axs[i,j].xaxis.get_major_ticks():
                xtick.label.set_fontsize(5)
        for ytick in axs[j,i].yaxis.get_major_ticks():
            ytick.label.set_fontsize(5)
        i=i+1
    j=j+1
# loc[x,y], y is vertial positon, y, 1 is top
# x is horizontal positon, 1 is the right
# The following is setting legends and labels for the picture
# i.e making the picture look beautiful
# Make legend, accoring to subplot [2,3], place it on the right side of the figure
legend = axs[2,3].legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1.65,1.4),
                         prop = fontP,fancybox=True,shadow=False)
legend.draw_frame(False)
plt.setp(legend.get_title(),fontsize='xx-small')
# Add text for variables
fig1.text(0.15,0.92,'Temperature',**{'fontsize':10})
fig1.text(0.38,0.92,'Oxygen',**{'fontsize':10})
fig1.text(0.55,0.92,'Total Nitrogen',**{'fontsize':10})
fig1.text(0.75,0.92,'Total Phosphorus',**{'fontsize':10})
# Add text for depth
fig1.text(0.05,0.8,'2m',**{'fontsize':10})
fig1.text(0.05,0.6,'5m',**{'fontsize':10})
fig1.text(0.05,0.4,'10m',**{'fontsize':10})
fig1.text(0.05,0.2,'20m',**{'fontsize':10})
fig1.autofmt_xdate(rotation=90)
# Save figure, and reduce the margins
fig1.savefig('fig1.png',bbox_inches='tight')
plt.close()
# plot group two variables
fig2 = plt.figure(figsize=(8.27, 11.69), dpi=1200)
fig2, axs = plt.subplots(4,4,sharex=True)
j=0
for depth in depths:
    ymin=ymin_2[j];ymax=ymax_2[j]
    i=0
    for var in variables_group2:
        k=0
        for model in models:
            axs[j,i].plot(time_t,results[depth][model][var], color=colors[k],linestyle=lines[k],label=model)
            axs[i,j].set_ylim(ymin,ymax)
            k=k+1
# Set x-axis and y-axis ticks
# Set x-axis for subplots
            axs[i,j].xaxis_date()
            axs[i,j].xaxis.set_major_locator(mdates.MonthLocator())
            axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            for xtick in axs[i,j].xaxis.get_major_ticks():
                xtick.label.set_fontsize(5)
        for ytick in axs[j,i].yaxis.get_major_ticks():
            ytick.label.set_fontsize(5)
        i=i+1
    j=j+1
# The following is setting legends and labels for the picture
# i.e making the picture look beautiful
# Make legend, accoring to subplot [2,3], place it on the right side of the figure
legend = axs[2,3].legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1.65,1.4),
                         prop = fontP,fancybox=True,shadow=False)
legend.draw_frame(False)
plt.setp(legend.get_title(),fontsize='xx-small')
# Add text for variables
fig2.text(0.19,0.92,'PAR',**{'fontsize':10})
fig2.text(0.35,0.92,'Phytoplankton',**{'fontsize':10})
fig2.text(0.56,0.92,'Zooplankton',**{'fontsize':10})
fig2.text(0.79,0.92,'Fish',**{'fontsize':10})
# Add text for depth
fig2.text(0.05,0.8,'2m',**{'fontsize':10})
fig2.text(0.05,0.6,'5m',**{'fontsize':10})
fig2.text(0.05,0.4,'10m',**{'fontsize':10})
fig2.text(0.05,0.2,'20m',**{'fontsize':10})
fig2.autofmt_xdate(rotation=90)
# Save figure, and reduce the margins
fig2.savefig('fig2.png',bbox_inches='tight')
plt.close()

"""
***************End of line plotting Section***********************************
"""

"""
***********Section for read in 2D data from gotm 1d and gotm lake****************
"""

df_1d={};df_lake={}
for f_lake in gotmlake:
    path_lake=os.path.join(output_dir, f_lake)
    gotmlake_nc=Dataset(path_lake, mode='r')
# Get the f_lvl for different depth
    lvl=len(gotmlake_nc.variables['temp'][0])
#GOTM-lake data
    tm_lake=gotmlake_nc.variables['temp'][start:stop,:,0,0].T
    O2_lake=gotmlake_nc.variables['abiotic_water_sO2W'][start:stop,:,0,0].T
    TP_lake=gotmlake_nc.variables['pclake_totP_calculator_result'][start:stop,:,0,0].T
    TN_lake=gotmlake_nc.variables['pclake_totN_calculator_result'][start:stop,:,0,0].T
    PAR_lake=gotmlake_nc.variables['phytoplankton_water_partop'][start:stop,:,0,0].T
    Phyto_lake=gotmlake_nc.variables['phytoplankton_water_aDPhytW'][start:stop,:,0,0].T
    Zoo_lake=gotmlake_nc.variables['foodweb_water_sDZoo'][start:stop,:,0,0].T
    Fish_lake=gotmlake_nc.variables['foodweb_water_sDFiAd'][start:stop,:,0,0].T \
              +gotmlake_nc.variables['foodweb_water_sDFiJv'][start:stop,:,0,0].T
    df_tm_lake=DataFrame(tm_lake,index=np.arange(lvl),columns=[time])
    df_O2_lake=DataFrame(O2_lake,index=np.arange(lvl), columns=[time])
    df_TN_lake=DataFrame(TN_lake,index=np.arange(lvl),columns=[time])
    df_TP_lake=DataFrame(TP_lake,index=np.arange(lvl), columns=[time])
    df_PAR_lake=DataFrame(PAR_lake,index=np.arange(lvl), columns=[time])
    df_Phyto_lake=DataFrame(Phyto_lake,index=np.arange(lvl), columns=[time])
    df_Zoo_lake=DataFrame(Zoo_lake,index=np.arange(lvl), columns=[time])
    df_Fish_lake=DataFrame(Fish_lake,index=np.arange(lvl), columns=[time])

    df_lake[f_lake]=pd.concat([df_tm_lake,df_O2_lake,df_TN_lake,df_TP_lake, \
                                    df_PAR_lake,df_Phyto_lake,df_Zoo_lake, \
                                     df_Fish_lake],axis=1,keys=['tm','O2','TN','TP',\
                                                               'PAR','Phy','Zoo','Fis'])

for f_1d in gotm1d:
    path_1d=os.path.join(output_dir, f_1d)
    gotm1d_nc=Dataset(path_1d, mode='r')
    lvl=len(gotm1d_nc.variables['temp'][0])
#   get the variables array
    tm_1d=gotm1d_nc.variables['temp'][start:stop,:,0,0].T
    O2_1d=gotm1d_nc.variables['abiotic_water_sO2W'][start:stop,:,0,0].T
    TP_1d=gotm1d_nc.variables['pclake_totP_calculator_result'][start:stop,:,0,0].T
    TN_1d=gotm1d_nc.variables['pclake_totN_calculator_result'][start:stop,:,0,0].T
    PAR_1d=gotm1d_nc.variables['phytoplankton_water_partop'][start:stop,:,0,0].T
    Phyto_1d=gotm1d_nc.variables['phytoplankton_water_aDPhytW'][start:stop,:,0,0].T
    Zoo_1d=gotm1d_nc.variables['foodweb_water_sDZoo'][start:stop,:,0,0].T
    Fish_1d=gotm1d_nc.variables['foodweb_water_sDFiAd'][start:stop,:,0,0].T     +gotm1d_nc.variables['foodweb_water_sDFiJv'][start:stop,:,0,0].T
    df_tm_1d=DataFrame(tm_1d,index=np.arange(lvl), columns=[time])
    df_O2_1d=DataFrame(O2_1d,index=np.arange(lvl), columns=[time])
    df_TN_1d=DataFrame(TN_1d,index=np.arange(lvl), columns=[time])
    df_TP_1d=DataFrame(TP_1d,index=np.arange(lvl), columns=[time])
    df_PAR_1d=DataFrame(PAR_1d,index=np.arange(lvl), columns=[time])
    df_Phyto_1d=DataFrame(Phyto_1d,index=np.arange(lvl), columns=[time])
    df_Zoo_1d=DataFrame(Zoo_1d,index=np.arange(lvl), columns=[time])
    df_Fish_1d=DataFrame(Fish_1d,index=np.arange(lvl), columns=[time])
    df_1d[f_1d]= pd.concat([df_tm_1d,df_O2_1d,df_TN_1d,df_TP_1d,df_PAR_1d,                                 df_Phyto_1d, df_Zoo_1d,df_Fish_1d],axis=1,keys=                                 ['tm','O2','TN','TP','PAR','Phy','Zoo','Fis'])


# In[21]:

df_2D_2m=pd.concat([df_1d['pclake-gotm1d-2m.nc'],df_lake['pclake-gotmlake-2m.nc']],axis=1,keys=['gotm-1d','gotm-lake'])
df_2D_5m=pd.concat([df_1d['pclake-gotm1d-5m.nc'],df_lake['pclake-gotmlake-5m.nc']],axis=1,keys=['gotm-1d','gotm-lake'])
df_2D_10m=pd.concat([df_1d['pclake-gotm1d-10m.nc'],df_lake['pclake-gotmlake-10m.nc']],axis=1,keys=['gotm-1d','gotm-lake'])
df_2D_20m=pd.concat([df_1d['pclake-gotm1d-20m.nc'],df_lake['pclake-gotmlake-20m.nc']],axis=1,keys=['gotm-1d','gotm-lake'])
"""
********************End of 2D data reading section*****************************
"""


"""
**************************Section for 2D plotting******************************
"""
# get plot groups
models=['gotm-1d','gotm-lake']
group1=['tm','O2','TN','TP']
group2=['PAR','Phy','Zoo','Fis']
outputs=[df_2D_2m,df_2D_5m,df_2D_10m,df_2D_20m]
depth=['2m','5m','10m','20m']


# In[23]:

#get color range for each variables
vmin_1=[];vmax_1=[];vmin_2=[];vmax_2=[]
for var in group1:
    vmin_depths=[]
    vmax_depths=[]
    for output in outputs:
        vmin_models=[]
        vmax_models=[]
        for model in models:
            vmin_models.append(np.min(np.min(output[model][var])))
            vmax_models.append(np.max(np.max(output[model][var])))
        vmin_depths.append(np.min(vmin_models))
        vmax_depths.append(np.max(vmax_models))
    vmin_1.append(np.min(vmin_depths))
    vmax_1.append(np.max(vmax_depths))
for var in group2:
    vmin_depths=[]
    vmax_depths=[]
    for output in outputs:
        vmin_models=[]
        vmax_models=[]
        for model in models:
            vmin_models.append(np.min(np.min(output[model][var])))
            vmax_models.append(np.max(np.max(output[model][var])))
        vmin_depths.append(np.min(vmin_models))
        vmax_depths.append(np.max(vmax_models))
    vmin_2.append(np.min(vmin_depths))
    vmax_2.append(np.max(vmax_depths))

# starting plot group1 variables
com_1d1 = plt.figure(figsize=(8.27, 11.69), dpi=1200)
com_1d1, axs = plt.subplots(8,4,sharex=True,squeeze=True)
# add color bar postions
# add color bar, for group 1
cbposition1=[]
cbposition_1=com_1d1.add_axes([0.13, 0.93, 0.15,0.01])
cbposition1.append(cbposition_1)
cbposition_2=com_1d1.add_axes([0.33, 0.93, 0.15,0.01])
cbposition1.append(cbposition_2)
cbposition_3=com_1d1.add_axes([0.53, 0.93, 0.15,0.01])
cbposition1.append(cbposition_3)
cbposition_4=com_1d1.add_axes([0.73, 0.93, 0.15,0.01])
cbposition1.append(cbposition_4)
# j for column location
j=0
for var in group1:
    vmin=vmin_1[j]
    vmax=vmax_1[j]
# i for row location
# k for depths index
    i=0
    k=0
    for output in outputs:
        wd=np.arange(len(output.index))+1
        extent=[time_t.min(), time_t.max(),wd.min(),wd.max()]
        for model in models:
            cbmap = axs[i,j].imshow(output[model][var],extent = extent,origin ='lower',\
                                    aspect='auto',vmin=vmin, vmax=vmax)
# Set x-axis for subplots
            axs[i,j].xaxis_date()
            axs[i,j].xaxis.set_major_locator(mdates.MonthLocator())
            axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            for xtick in axs[i,j].xaxis.get_major_ticks():
                xtick.label.set_fontsize(5)
# Set y-axis for subplots
            axs[i,j].yaxis.set_major_locator(ticker.FixedLocator([wd.min(),wd.max()]))
            axs[i,j].set_yticklabels(['0',depth[k]])
            for ytick in axs[i,j].yaxis.get_major_ticks():
                ytick.label.set_fontsize(5)
# set labels for different model output
            if j==0:
                axs[i,j].set_ylabel(model,fontsize=8,rotation='horizontal')
                axs[i,j].yaxis.set_label_coords(-0.25, 0.5)
# plotting color bar
            if i==0:
                cb=com_1d1.colorbar(cbmap,cax=cbposition1[j],orientation='horizontal')
                # set color bar location
                cblocator=[];step=(vmax-vmin)/5;
                cblocator=[vmin,vmin+step,vmin+2*step,vmin+3*step,vmin+4*step,vmin+5*step]
                cb.set_ticks(cblocator)
                cb.formatter=ticker.FormatStrFormatter(('%0.1f'))
                cb.update_ticks()
                cb.ax.tick_params(labelsize=5)
            i=i+1
        k=k+1
    j=j+1
# add columns for variables
com_1d1.text(0.15,0.95,'Temperature',**{'fontsize':8})
com_1d1.text(0.38,0.95,'Oxygen',**{'fontsize':8})
com_1d1.text(0.55,0.95,'Total Nitrogen',**{'fontsize':8})
com_1d1.text(0.75,0.95,'Total Phosphorus',**{'fontsize':8})
com_1d1.autofmt_xdate(rotation=90)
#save fig
com_1d1.savefig('comp_1d_1.png',bbox_inches='tight')
plt.close()

# Plotting variables group2
com_1d2 = plt.figure(figsize=(8.27, 11.69), dpi=1200)
com_1d2, axs = plt.subplots(8,4,sharex=True,squeeze=True)
# add color bar postions
# add color bar, for group 1
cbposition2=[]
cbposition_1=com_1d2.add_axes([0.13, 0.93, 0.15,0.01])
cbposition2.append(cbposition_1)
cbposition_2=com_1d2.add_axes([0.33, 0.93, 0.15,0.01])
cbposition2.append(cbposition_2)
cbposition_3=com_1d2.add_axes([0.53, 0.93, 0.15,0.01])
cbposition2.append(cbposition_3)
cbposition_4=com_1d2.add_axes([0.73, 0.93, 0.15,0.01])
cbposition2.append(cbposition_4)
# j for column location
j=0
for var in group2:
    vmin=vmin_2[j];vmax=vmax_2[j]
# i for row location
# k for depths index
    i=0;k=0
    for output in outputs:
        wd=np.arange(len(output.index))+1
        extent=[time_t.min(), time_t.max(),wd.min(),wd.max()]
        for model in models:
            cbmap=axs[i,j].imshow(output[model][var],extent = extent,origin ='lower',\
                                  aspect='auto',vmin=vmin, vmax=vmax)
            axs[i,j].xaxis_date()
            axs[i,j].xaxis.set_major_locator(mdates.MonthLocator())
            axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            for xtick in axs[i,j].xaxis.get_major_ticks():
                xtick.label.set_fontsize(5)
# Set y-axis for subplots
            axs[i,j].yaxis.set_major_locator(ticker.FixedLocator([wd.min(),wd.max()]))
            axs[i,j].set_yticklabels(['0',depth[k]])
            for ytick in axs[i,j].yaxis.get_major_ticks():
                ytick.label.set_fontsize(5)
# set labels for different model output
            if j==0:
                axs[i,j].set_ylabel(model,fontsize=8,rotation='horizontal')
                axs[i,j].yaxis.set_label_coords(-0.25, 0.5)
# plotting color bar
            if i==0:
                cb=com_1d2.colorbar(cbmap,cax=cbposition2[j],orientation='horizontal')
                # set color bar location
                cblocator=[];step=(vmax-vmin)/5;
                cblocator=[vmin,vmin+step,vmin+2*step,vmin+3*step,vmin+4*step,vmin+5*step]
                cb.set_ticks(cblocator)
                cb.formatter=ticker.FormatStrFormatter(('%0.1f'))
                cb.update_ticks()
                cb.ax.tick_params(labelsize=5)
            i=i+1
        k=k+1
    j=j+1
# adjust a-axis labels
# add columns for variables
com_1d2.text(0.17,0.95,'PAR',**{'fontsize':8})
com_1d2.text(0.36,0.95,'Phytoplankton',**{'fontsize':8})
com_1d2.text(0.55,0.95,'Zooplankton',**{'fontsize':8})
com_1d2.text(0.77,0.95,'Fish',**{'fontsize':8})
com_1d2.autofmt_xdate(rotation=90)

com_1d2.savefig('comp_1d_2.png',bbox_inches='tight')

"""
**************************End of 2D plotting section***************************
"""
