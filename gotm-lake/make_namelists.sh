#!/bin/sh

dirs="2m 5m 10m 20m"

for d in $dirs; do
  cd $d
  make namelist
  mv fabm_input.nml fabm_input.nml.keep
  mv streams.nml streams.nml.keep
  cd ..
done
