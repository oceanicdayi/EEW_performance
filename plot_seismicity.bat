@ echo off
rem   GMT Environment
 SET NETCDF=C:\NETCDF
 SET GMTHOME=C:\gmt341
 SET HOME=C:\gmt341
 SET INCLUDE=%INCLUDE%;%NETCDF%\INCLUDE
 SET LIB=%LIB%;%NETCDF%\LIB;%GMTHOME%\LIB
 SET PATH=%PATH%;%GMTHOME%\BIN;%NETCDF%\BIN
rem GMT Instructions
rem gmtset ANNOT_FONT_SIZE 3p


rem grdimage asia.grd -R114/130/10/30 -B1:."2012 Seismic Network": -Cex1.cpt -JM8 -P -K -V > ex1.ps

REM grdcontour taiwan.grd -Cex1.cpt -R -J -K -V >> ex1.ps

pscoast -R119.85/123.1/21.3/25.5 -B1WSne -JM15 -Di -W3  -K  -V -P > ex1.ps

REM gmtset	FRAME_PEN		= 0.01p
REM gmtset	BASEMAP_FRAME_RGB	= 255/255/255

REM psbasemap -R -JX15/19.8 -B:Longitude(E):/WSne:Latitude(N): -K -O -V >> ex1.ps
rem psbasemap -R -JM -B:"Longitude(E)":/WSne:"Latitude(N\260)": -K -O -V >> ex1.ps
REM psbasemap -R -JM -B:Longitude:/WSne:Latitude: -K -O -V >> ex1.ps

REM gmtset	FRAME_PEN		= 1.25p
REM gmtset	BASEMAP_FRAME_RGB	= 0/0/0







REM echo 120.15 21.7 13.5 0 9 ML Station > sta_text
REM pstext sta_text     -R  -JM -W0.1/0/0/0  -K -O -V >> ex1.ps

REM echo 122.86  24.31  13.5 0 9 ML YOJ > YOJ
REM pstext YOJ     -R  -JM -W0.1/0/0/0  -K -O -V >> ex1.ps

REM echo 122.18  24.62 13.5 0 9 ML EOS1 > OBS
REM pstext OBS     -R  -JM -W0.1/0/0/0  -K -O -V >> ex1.ps

echo 122.86  24.31  13.5 0 9 ML YOJ > YOJ
REM pstext YOJ     -R  -JM -W0.1/0/0/0  -K -O -V >> ex1.ps

echo 122.18  24.62 13.5 0 9 ML EOS1 > OBS
REM pstext OBS     -R  -JM -W0.1/0/0/0  -K -O -V >> ex1.ps
REM psxy sta1     -R -JM -W0.1 -G125  -St0.4 -K -O -V >> ex1.ps
REM psxy legend_time1   -R -JM -W2/0/0/0  -Sc -K  -O -V >> ex1.ps

psxy eve.txt  -R -JM -W5/255/0/0  -Sc0.5  -G255/255/0 -O -V >> ex1.ps
REM psxy dis_loc_err_last  -R -JM -W5/255/0/0  -Sc -K  -G255/255/255 -O -V >> ex1.ps




ps2raster ex1.ps -GC:\gs\gs9.18\bin\gswin64c -A -Tg -V

ex1.png