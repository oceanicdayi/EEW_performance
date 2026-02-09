@ echo off
rem   GMT Environment
SET NETCDF=C:\NETCDF
SET GMTHOME=C:\gmt341
SET HOME=C:\gmt341
SET INCLUDE=%INCLUDE%;%NETCDF%\INCLUDE
SET LIB=%LIB%;%NETCDF%\LIB;%GMTHOME%\LIB
SET PATH=%PATH%;%GMTHOME%\BIN;%NETCDF%\BIN

psbasemap -R4.3/6.9/4.3/6.9 -JX9/9 -B0.5WSne:M@-L:/0.5WSne:M@-Pd: -K -P -V > ex2.ps
psxy cmag_emag -R -JX -B -W5/255/0/0 -G255/255/0   -Sc0.42 -K -O -V >> ex2.ps
REM psxy cmag_emag_09 -R -JX -B -W5/255/0/0 -G255/255/0   -Sc0.42 -K -O -V >> ex2.ps
REM psxy cmag_emag_last -R -JX -B -W2/255/0/0 -G255/255/255   -Sc0.42 -K -O -V >> ex2.ps
echo 0 0 > mag_line
echo 8 8 >> mag_line
psxy mag_line        -R  -JX -W2/0/0/0  -M -K -O -V >> ex2.ps
psxy mag_line_std    -R  -JX -W2/0/0/0/,-  -M -K -O -V >> ex2.ps
pstext	mag_txt		-R -JX  -O -V >> ex2.ps

ps2raster ex2.ps -GD:\programs\gs\gs9.22\bin\gswin64c -A -Tg -V
ex2.png