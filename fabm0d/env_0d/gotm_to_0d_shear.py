#!/usr/bin/env python

"""gotm_to_0d_env.py: Extracts and converts environmental forcing from a GOTM
simulation formatted for the 0d FABM driver"""

__author__ = "Karsten Bolding"
__license__ = "GPL"

# see http://stackoverflow.com/questions/1523427/python-what-is-the-common-header-format

import numpy as np
from netCDF4 import Dataset
from netCDF4 import num2date

import argparse

parser = argparse.ArgumentParser(description='Extract environmental forcing for the 0d FABM driver from a GOTM simulation.')
parser.add_argument("filename",help="GOTM NetCDF file name")
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                   help='cal level to extract - default surfacett
# parser.add_argument('--lvl', dest='lvl', default=-1,
#                    help='vertical level to extract - default surface')
args = parser.parse_args()
fn  = args.filename
# lvl = int(args.lvl)
data = Dataset(fn)
time = data.variables['time']
shearstress=data.variables['auxiliary_shearstress']

valid_times = num2date(time[:], time.units).tolist()
i=0
for t in valid_times:
    print t.strftime('%Y-%m-%d %H:00:00') + \
          "%8.5f" % (shearstress[i])
    i=i+1