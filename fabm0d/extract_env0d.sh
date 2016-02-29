#!/bin/sh

cd 2m
rm env_2m.dat
cd ../5m
rm env_5m.dat
cd ../10m
rm env_10m.dat
cd ../20m
rm env_20m.dat
cd ../env
python gotm_to_0d_env.py env-2m.nc --lvl 4 >>  ../2m/env_2m.dat
python gotm_to_0d_env.py env-5m.nc --lvl 12 >>  ../5m/env_5m.dat
python gotm_to_0d_env.py env-10m.nc --lvl 24 >>  ../10m/env_10m.dat
python gotm_to_0d_env.py env-20m.nc --lvl 49 >>  ../20m/env_20m.dat


#python gotm_to_0d_env.py ../../output/pclake-gotm1d-2m.nc --lvl 4 >>  ../2m/env_2m.dat
#python gotm_to_0d_env.py ../../output/pclake-gotm1d-5m.nc --lvl 12 >>  ../5m/env_5m.dat
#python gotm_to_0d_env.py ../../output/pclake-gotm1d-10m.nc --lvl 24 >>  ../10m/env_10m.dat
#python gotm_to_0d_env.py ../../output/pclake-gotm1d-20m.nc --lvl 49 >>  ../20m/env_20m.dat

cd ..
