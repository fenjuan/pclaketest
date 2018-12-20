rem first go to every directory, delete the exiting env files
cd fabm0d
cd 2m
del /f env_2m.dat
cd ../5m
del /f env_5m.dat
cd ../10m
del /f env_10m.dat
cd ../20m
del /f env_20m.dat
rem go to env_0d directory and extract environment variables for 0d model
cd ../env_0d
rem gotm_to_0d extract colums of: column1:shortwave radiation;
rem column2: temperature;column3: slinity. 
python gotm_to_0d_env.py env-2m.nc --lvl 4 >>  ..\2m\env_2m.dat
python gotm_to_0d_env.py env-5m.nc --lvl 12 >>  ..\5m\env_5m.dat
python gotm_to_0d_env.py env-10m.nc --lvl 24 >>  ..\10m\env_10m.dat
python gotm_to_0d_env.py env-20m.nc --lvl 49 >>  ..\20m\env_20m.dat
rem shear stress should be provided seperately
python gotm_to_0d_shear.py env-2m.nc >>  ..\2m\shear_2m.dat
python gotm_to_0d_shear.py env-5m.nc  >>  ..\5m\shear_5m.dat
python gotm_to_0d_shear.py env-10m.nc  >>  ..\10m\shear_10m.dat
python gotm_to_0d_shear.py env-20m.nc  >>  ..\20m\shear_20m.dat
cd ../..

PAUSE...
