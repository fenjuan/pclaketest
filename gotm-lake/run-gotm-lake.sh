#!/bin/sh

dirs="2m 5m 10m 20m"

for d in $dirs; do
  cd $d
  gotm-lake
  cd ..
done
