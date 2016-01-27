#!/bin/sh

dirs="2m 5m 10m 20m"

for d in $dirs; do
  cd $d
  export GOTMDIR=~/GOTM/lake
  make namelist
  rm fabm_input.nml
  rm streams.nml
  cd ..
done
