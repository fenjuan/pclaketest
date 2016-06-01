
# coding: utf-8

# In[17]:

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from netCDF4 import num2date
from netCDF4 import date2num
import datetime
import os
import sys
import os.path
import glob
import argparse

parser = argparse.ArgumentParser(description='converts CSV to NETCDF')
parser.add_argument("inputfilename",help="Model NETCDF file name lake_fure_daily_surface.nc")
parser.add_argument("outputfilename1",help="Observations NETCDF file name Fure_surface.nc")
parser.add_argument("outputfilename2",help="Output file name Performance_surf.pdf")


args        = parser.parse_args()
In_file    = args.inputfilename
Out_file1    = args.outputfilename1
Out_file2     = args.outputfilename2


Script_folder   = os.path.normpath(os.getcwd() + os.sep + os.pardir)
sed_file = os.path.join(Script_folder,In_file)
output_file1 = os.path.join(Script_folder,Out_file1)
output_file2 = os.path.join(Script_folder,Out_file2)


# In[24]:
# Read in Data_sed
Data_sed=pd.read_table(sed_file,names=['aLLimShootVeg','aNutLimVeg'],sep=r"\s*")
# get day numbers
days=np.asarray(Data_sed.index.get_level_values(0))
daycount=np.max(days)
# put scaler into arreay. since day starts at 0, so acutally days need +1
oxy=np.asarray(Data_sed['aLLimShootVeg'])
oxy_year=np.reshape(oxy,(daycount+1,36))
oxy_plot=oxy_year.T
SorpIM= np.asarray(Data_sed['aNutLimVeg'])
SorpIM= SorpIM*86400
SorpIM_year= np.reshape(SorpIM,(daycount+1,36))
SorpIM_plot= SorpIM_year.T


# In[27]:

# set the plot area
# ploting x axis
dt=datetime.date
# Setting period, and model output intervals is 1day
time_t=mdates.drange(dt(1989,1,2), dt(2013,1,1), datetime.timedelta(days=1))
extent=[time_t.min(), time_t.max(),1,36]
vmin1= np.min(oxy);vmax1=np.max(oxy)
#vmin2= np.min(SorpIM); vmax2=np.max(SorpIM)
vmin2= -0.18; vmax2=np.max(SorpIM)


# In[21]:

# plot vertial profile afoxysed
fig1,ax= plt.subplots()
cbmap1 =ax.imshow(oxy_plot,extent= extent, vmin=vmin1, vmax=vmax1, origin ='lower',aspect='auto')
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# formating x-axis
ax.tick_params(axis='x',which='both',top='off',bottom='off')
plt.setp( ax.xaxis.get_majorticklabels(), rotation=90 )
for xtick in ax.xaxis.get_major_ticks():
    xtick.label.set_fontsize(10)
# add colorbar
cb1=fig1.colorbar(cbmap1)

fig1.savefig(output_file1)


# In[28]:

# plot vertial profile afoxysed
fig2,ax= plt.subplots()
cbmap2=ax.imshow(SorpIM_plot,extent= extent, vmin=vmin2, vmax=vmax2, origin ='lower',aspect='auto')
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# formating x-axis
ax.tick_params(axis='x',which='both',top='off',bottom='off')
plt.setp( ax.xaxis.get_majorticklabels(), rotation=90 )
for xtick in ax.xaxis.get_major_ticks():
    xtick.label.set_fontsize(10)
# add colorbar
cb2=fig2.colorbar(cbmap2)

fig2.savefig(output_file2)


# In[ ]:
