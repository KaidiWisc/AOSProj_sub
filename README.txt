How Much Can Motion Vector Explain the Movement of Precipitation Field

Main.ipynb: It is the main file written in jupyter notebook. Step-by-step descriptions of this experiment are included.

AOSproject.py: functions used in Main.ipynb

Projenv_all.yml: Full yml exported from my environment (windows system) directly
Projenv_simple.yml: Only packages used in this experiment

Data used:

1. MERRA2_0.1.2018.5_9.hourly.nc is hourly, 0.5 by 0.625 deg dataset, with U850, V850 and TQV stored. The time span is from 5/1/2018 to 9/30/2018. the coverage is 45N-35N and 100W-85W. It was downlaoded from https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/. 
U850: eastward wind speed at 850 hPa  m/s
V850: northward wind speed at 850 hPa  m/s
TQV: total precipitable water vapor kg/m2

2. STAGEIV2018_0.1deg.5_9.hourly.nc is hourly, 0.1 by 0.1 deg precipitation data, with the same coverage as MERRA-2. It is from 5/1/2018 to 9/29/2018. It was downloaded from https://data.eol.ucar.edu/dataset/21.093. Reprojection was conducted.
prcp: surface precipitation mm/hr

3. The packages I use are Numpy, Xarray, Cartopy, Scipy, Pysteps and Matplotlib.

Background:

IMERG (https://gpm.nasa.gov/data/imerg) is global near-real-time (four-hour latency) satellite precipitation product. It is a combination of several passive microwave (PMW) and Infrared observations. To make full use of PMW observations, backward and forward interpolation is used. 

In IMERG V06 Final Run, the Modern-Era Retrospective Analysis for Research and Applications Version 2 (MERRA-2) reanalysis product is used to propagate the passive microwave observations over time and space to obtain global observation on precipitation. This interpolation method is called morph (https://doi.org/10.1175/JTECH-D-19-0114.1). This experiment is to evaluate the role of two types of motion vectors: total precipitable water vapor (TQV) and winds speed at 850 mb (U850, V850) in the movement of actual precipitation field. Stage IV is a combination of ground radar and gauge precipitation observations. It ia used as actual surface precipitation.


Experiments descriptions:

1. ALL used data is interpolated to 0.5 by 0.5 degree for less computation load.
2. Motion vectors representing TQV movement are derived. Pixels in 5.5 × 5.5 degrees box are compared to the next half hour fields with different spatial offsets. The offset with the highest correlation forms the motion vector for that grid box. For U850 and V850, the wind speed is transformed to number of grid in one time step (one hour). 
3. These motion vectors are used to propagate precipitation over areas. We use Stage IV data here. A semi-lagrangian scheme is used.
4. The propagated precipitation field are compared with the actual Stage IV data. Heidke skill score (HSS), Pearson correlation coefficient and the normalized root-mean-square error (NRMSE) are used to evaluate our results.
5. The motion vector are compared with the actual movement of Stage IV. The latter is calculated based on optical flow in Pysteps. Magnitude and speed in both the longitudinal and latitudinal directions are evulated.

Conclusions:

1. Winds spped at 850 mb is a better explantion for precipitation data movement, compared with TQV. This also has been proved in pevious research (https://doi.org/10.1175/JTECH-D-19-0114.1).

2. Winds spped at 850 mb can explain about 30% of precipitation field movement.

3. The changes in precipitation magitide, not only the advection of water volume, is important.

4. Morph technique is still under developing by scientists at NASA. They are considering using sophisticated motion vectors hierarchically, from model precipitation (PRECTOT), then total precipitable liquid water (TQL) next, then globally complete TQV, based on the data availablility. 

