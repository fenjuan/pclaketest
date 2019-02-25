# 1. Introduction
 This is repository for running model test for manuscript titled "The influence of hydrodynamics on lake ecosystem model simulations: a model experiment using three coupled hydrodynamic-biogeochemical models for four different lake types " registered with (gmd doi)
# 2. The source code 
For those who would like to compile their own code, and for Linux and Mac users, you can follow the guide on (https://github.com/fabm-model/fabm/wiki) to compile your own models used in the simulations. We compiled the three hydrodyanmic model drivers with FABM code (https://github.com/fabm-model/fabm): FABM-0d driver(https://github.com/fabm-model/fabm/tree/master/src/drivers/0d), GOTM (https://github.com/gotm-model/code) and GOTM-lake(https://github.com/gotm-model/code/tree/lake). Within the FABM model option, point the PCLake-model to the code repository from https://github.com/fenjuan/pclaketestsrc. 
# 3. Run the simulation
## 3.1 for windows users
1. click 1-run-gotm-lake.bat, and it will run gotm-lake model for the 4 simulations in *gotm-lake* directory.
2. click 1-run-gotm.bat, and it will run gotm model for the 4 simulations with gotm model in the *gotm* directory. *This **MUST** run before fabm0d is run*
3. click 2-extract-env0d.bat, and it will extract the temperature, shear stress from gotm models from the match depth, these will be used as input for fabm0d model.
4. click 3-run-fabm0d.bat, and it will run fabm0d for the 4 simulations in *fabm0d* directory.
5. click 4-gen-output.bat, then it will generate the figure 02-06 and table2 that presented in the manuscript.
*(The output netcdf files :nc, are in the folder output, together the python scripts that generate the figures and table, as well as the following output figures)*
## 3.2 for linux and Mac users
1. follow step 1 to compile the code for three coupled hydrodyanmic-biogeochemical models described in the manuscript. 
2. Following the order of gotm-lake, gotm, generate environment forcing for fabm0d, running fabm0d, finish the model run. You can see the *.bat files as reference. Finally use the python scripts in output directory to generate the figures and table.
# 4. Overview of the simulated hypothetic lakes
| Lakes         | depth(m)      | Water voulm m-3| Residence time (day)| Layer number of 1D model|
| ------------- |:-------------:| -------------- |:--------------------|:-----------------------:|
| Lake 1        | 2m            | 2 * 2e06       | 100                 |  5                      | 
| Lake 2        | 5m            | 5 * 2e06       | 100                 |  13                     | 
| Lake 3        | 10m           | 10 * 2e06      | 100                 |  25                     | 
| Lake 4        | 20m           | 20 * 2e06      | 100                 |  50                     | 



