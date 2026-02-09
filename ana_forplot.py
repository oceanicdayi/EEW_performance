# import MySQLdb
import time
import os
import subprocess
from subprocess import PIPE
import math

import numpy as np
import matplotlib.pyplot as plt
import numpy

import sys

def delaz( elat, elon, slat,  slon):
	avlat=0.5*(elat+slat);
	a=1.840708+avlat*(.0015269+avlat*(-.00034+avlat*(1.02337e-6)));
	b=1.843404+avlat*(-6.93799e-5+avlat*(8.79993e-6+avlat*(-6.47527e-8)));
	dlat=slat-elat;
	dlon=slon-elon;
	dx=a*dlon*60.0;
	dy=b*dlat*60.0;
	delta=math.sqrt(dx*dx+dy*dy);
	return delta;

def check_seis_r(tlon, tlat, elon, elat, num_boundary, r):
	sta=[]
	result=0
	for	 i in range(1,num_boundary):
		x=tlon[i]-elon
		y=tlat[i]-elat
		dist=delaz(elat,elon,tlat[i],tlon[i])
			
		for j in range(1,6):
			sta.append(0)
		
		if x>0 and y>0:
			sta[0]=1
		if x<0 and y<0:
			sta[1]=1
		if x>0 and y<0:
			sta[2]=1
		if x<0 and y>0:
			sta[3]=1
		if dist<r:
			sta[4]=1		
	
		check = sta[0]*sta[1]*sta[2]*sta[3]
		
		if check==1 or sta[4]==1:
			result=1
			break
	return result	
	
tlon=[]
tlat=[]
g = open("taiwan.txt","r")
n=0
for j in g.readlines():
	data = j.split()	
	n = n + 1
	dd = float(data[0])
	tlon.append(dd)
	dd = float(data[1])
	tlat.append(dd)	
	# print '--%5d %8s %8s' %(n,data[0],data[1])
# print 'n = ', n
num_boundary = n;
g.close()
	
# file = open("0206-tcpd-aftershock.txt","r")
# file = open("0206-tcpd-new.txt","r")
# file = open("0206-tcpd-new-cwb24.txt","r")
# file = open("0206-fst-ori-equal-fst.txt","r")

# file = open("EEW_ALL-new-ver.txt","r")

# file = open("EEW_ALL-20200406-2020.txt","r")

# file = open("EEW-2021.txt","r")
# file = open("EEW_ALL-202005-2021.txt","r")
#file = open("EEW-2019-01-06-M5-230.txt","r")
# file = open("EEW-2019-01-06-M5-grd.txt","r")


# file = open("EEW-201905-07-230.txt","r")
# file = open("EEW-201905-07-236.txt","r")
# file = open("EEW-201905-07-grd.txt","r")
# file = open("EEW-201905-07-ofs.txt","r")

# file = open("EEW_ALL-20200406-2020.txt","r")
# file = open("EEW_F42-20200406-2021.txt","r")

# file = open("EEW_ALL-2021-2022-EOS-F42.txt","r")
# file = open("EEW_ALL-2014-2024.txt","r",encoding="utf-8")

file = open("EEW-2024.txt","r",encoding="utf-8")


#EEW_ALL-2021-2022-EOS-F42.txt
#EEW_ALL-2021-2022-EOS-230.txt
#EEW_ALL-2014-2021.txt



f1 = open("dis_pro_time","w")
f2 = open("dot","w")
f3 = open("miss","w")
f4 = open("dis_loc_err","w")
f5 = open("no","w")
f6 = open("yes","w")
f7 = open("dot_dis_err","w")
f8 = open("cmag_emag","w")

f9 = open("dis_loc_err_last","w")   # f4
f10 = open("cmag_emag_last","w")    # f8
f11 = open("dis_pro_time_last","w") # f1


f_all_time_05 = open("pro_time_05","w")
f_all_time_10 = open("pro_time_10","w")
f_all_time_15 = open("pro_time_15","w")
f_all_time_20 = open("pro_time_20","w")
f_all_time_25 = open("pro_time_25","w")
f_all_time_30 = open("pro_time_30","w")


aa=0
fac=0.03
fac_dis_err=0.018

all_time=[]
inland_time=[]
offshore_time=[]

all_time_f42=[]
inland_time_f42=[]
offshore_time_f42=[]

inland_loc=[]
offshore_loc=[]

inland_loc_f42=[]
offshore_loc_f42=[]


miss_mag=[]
miss_dep=[]
count_Y=0
count_N=0
count_L=0
loc_err=[]
mag_err=[]

loc_inland_err=[]
mag_inland_err=[]
loc_offshore_err=[]
mag_offshore_err=[]

loc_inland_err_f42=[]
mag_inland_err_f42=[]
loc_offshore_err_f42=[]
mag_offshore_err_f42=[]


arrmag_sd=[]

near_coast_line_dis = 1.0

for rr in file.readlines():
	# rr = rr.strip()

	print ("---"+rr)
	
	
	qq11 = rr.split()
	# print qq11
	
	print("len: qq11 : ", len(qq11))
	
	lonn1 = float(qq11[3])
	latt1 = float(qq11[4])
	magg1 = float(qq11[5])	
	depp1 = float(qq11[6])
	# if lonn1 < 119:
		# continue		
	# if latt1 <= 21:
		# continue		
        
	if magg1 < 5.0:
		continue		
	if depp1 > 40.0:
		continue
		
	if rr[1]== 'Y':
		# print rr        rr=rr.strip('\n')

		qq = rr.split()
		lon1 = float(qq[3])
		lat1 = float(qq[4])
		mag1 = float(qq[5])		
		dep1 = float(qq[6])
		lon2 = float(qq[7])
		lat2 = float(qq[8])			
		mag2 = float(qq[9])	
		
		if lat1 < 21.0:
			continue
			
		if lat1 > 26.0:
			continue			

		if lon1 < 119:
			continue	
		
		if lon1 > 123:
			continue		
		
		if dep1 > 40:
			continue
			
		if mag1 < 5.0:
			continue	

            
		# print( rr)
        
		# if mag1 < 4.0:
			# continue		        
	
		pro_time = float(qq[11] )	
        
        
	        
        
		if len(qq)>12:
			pro_time1 = float(qq[12])
		else:
			pro_time1 = 0.0
            
            
		# if pro_time > 11.0:
			# continue            
            
		dis = delaz( lat1, lon1, lat2, lon2)
		diff = abs(mag1-mag2)
		arrmag_sd.append(diff*diff)
		
		flag=check_seis_r(tlon, tlat, lon1, lat1, num_boundary, near_coast_line_dis)
		
		# if flag!=1:
			# continue
            
		# if flag==1:
			# continue            
		
		# if pro_time < 30:
			# continue        
        
		# if pro_time >= 11:
			# continue
            
		# if pro_time < 40:
			# continue            
			
		if pro_time > 15 and lon1 > 121 and lat1 > 23  and lat1 < 23.7:
			print ("-----------")
			print (rr)
			print (pro_time)
			print ("-----------")
		if dis > 50 :
			print ("-----------")
			print (rr)
			print (dis)
			print ("-----------")            
		count_Y +=1			
		# print count_Y,qq[1],lon1,lat1,mag1,lon2,lat2,mag2, dis, diff, pro_time
		# if dis < 10:
		# print(rr)
		
		with open ("data.dat","a") as fp:
			fp.write(rr)
		
		
		f1.write("%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time));
		f4.write("%8.3f %8.3f %5.2f %5.2f %8.3f %8.3f \n"%(lon1,lat1,fac_dis_err*dis,dis,dep1, mag1));	
		f6.write("%8.3f %8.3f %8.3f %8.3f \n"%(lon1,lat1,dep1, mag1));		
		f8.write("%8.3f %8.3f \n"%(mag1, mag2));	

		if pro_time<= 10:
			f_all_time_05.write( "%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time) )
            
		if pro_time> 10 and pro_time<=15:
			f_all_time_10.write( "%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time) )
            
		if pro_time> 15 and pro_time<=20:
			f_all_time_15.write( "%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time) )
            
		if pro_time> 20 and pro_time<=25:
			f_all_time_20.write( "%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time) ) 
            
		if pro_time> 25 and pro_time<=30:
			f_all_time_25.write( "%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time) )
            
		if pro_time> 30:
			f_all_time_30.write( "%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time) )
            
		# if rr[0]=='o':
			# gg = rr.split()
			# print gg
			# lon3 = float(gg[12])
			# lat3 = float(gg[13])
			# mag3 = float(gg[14])				
			# pro_time3 = float(gg[16])
			
			# dis_last = delaz( lat1, lon1, lat3, lon3)
			# diff = abs(mag1-mag2)	
			
			# f11.write("%8.3f %8.3f %5.2f \n"%(lon1,lat1,fac*pro_time3));
			# f9.write("%8.3f %8.3f %5.2f %5.2f %8.3f %8.3f \n"%(lon1,lat1,fac_dis_err*dis_last,dis_last,dep1, mag1));			
			# f10.write("%8.3f %8.3f \n"%(mag1, mag2));
		
		loc_err.append(dis)
		mag_err.append(diff)		
		
		all_time.append(pro_time)
		if pro_time1<0.1:
			pass
		else:
			all_time_f42.append(pro_time1)
		
		if flag==1:
			inland_time.append(pro_time)
			inland_loc.append(dis)
			loc_inland_err.append(dis)
			mag_inland_err.append(diff*diff)
			
			if pro_time1<0.1:
				pass
			else:
				inland_time_f42.append(pro_time1) 
				loc_inland_err_f42.append(dis)
				mag_inland_err_f42.append(diff*diff)            
		
		if flag!=1:
			offshore_time.append(pro_time)
			offshore_loc.append(dis)
			loc_offshore_err.append(dis)
			mag_offshore_err.append(diff*diff)			
			
			if pro_time1<0.1:
				pass
			else:
				offshore_time_f42.append(pro_time1)      
				loc_offshore_err_f42.append(dis)
				mag_offshore_err_f42.append(diff*diff)           
		
		
	if rr[1]== 'N':


		qq = rr.split()
		lon1 = float(qq[3])
		lat1 = float(qq[4])	
		mag1 = float(qq[5])		
		dep1 = float(qq[6])
		count_N +=1		
		f5.write("%8.3f %8.3f %8.3f %8.3f \n"%(lon1,lat1,dep1, mag1));		
		# print count_N,qq[1],lon1,lat1,mag1,dep1	
		
	if rr[1]== 'L':
		# print rr
		
		# print '-----1'
		# print (rr )
		# print '-----2'
		
		qq = rr.split()
		lon1 = float(qq[3])
		lat1 = float(qq[4])	
		mag1 = float(qq[5])		
		dep1 = float(qq[6])
		
		# if mag1 < 5.0:
			# continue	
			
		count_L +=1			
		print( '-------------------===========================',count_L,qq[1],lon1,lat1,mag1,dep1		)
		f3.write("%8.3f %8.3f %8.3f %8.3f \n"%(lon1,lat1,dep1, mag1));
		miss_mag.append(mag1)
		miss_dep.append(dep1)

f2.write('120.03 25.20 %f \n'% ( 15 * fac) )
f2.write('120.03 24.95 %f \n'% ( 20 * fac) )
f2.write('120.03 24.70 %f \n'% ( 25 * fac) )
f2.write('120.03 24.45 %f \n'% ( 30 * fac) )

f7.write('120.03 25.20 %f \n'% ( 10 * fac_dis_err) )
f7.write('120.03 24.95 %f \n'% ( 20 * fac_dis_err) )
f7.write('120.03 24.70 %f \n'% ( 40 * fac_dis_err) )
f7.write('120.03 24.45 %f \n'% ( 80 * fac_dis_err) )
		
file.close()
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()

f9.close()
f10.close()
f11.close()

f_all_time_05.close()
f_all_time_10.close()
f_all_time_15.close()
f_all_time_20.close()
f_all_time_25.close()
f_all_time_30.close()


print ('\n\n')
print ('1_inland: ',inland_time)
print ('2_offshore: ',offshore_time)
print ('3_inland: ',inland_time_f42)
print ('4_offshore: ',offshore_time_f42)
print ('\n\n')
print ('count_Y,N,L: ', count_Y, count_N, count_L)
print ('\n\n')
print ('miss_mag: ',miss_mag)
print ('AVG: ',numpy.mean(miss_mag), 'STD: ',numpy.std(miss_mag))
# print 'miss_dep: ',miss_dep
# print 'AVG: ',numpy.mean(miss_dep), 'STD: ',numpy.std(miss_dep)
print ('\n\n')
print ('loc_err AVG: ',numpy.mean(loc_err), 'loc_err STD: ',numpy.std(loc_err))
print ('mag_err AVG: ',numpy.mean(mag_err), 'STD: ',numpy.std(mag_err))

# print 'loc_err: ', loc_err

arr1 = numpy.array(inland_time)
arr2 = numpy.array(offshore_time)
f1=open("time_txt1","w")
f1.write("119.991 21.77 14.5 0 9 ML Inland Average: %.1f \261 %.1f sec\n"%(numpy.mean(arr1),numpy.std(arr1)))
f1.write("119.991 21.63 14.5 0 9 ML Offshore Average: %.1f \261 %.1f sec\n"%(numpy.mean(arr2),numpy.std(arr2)))
f1.close()




# arr1 = numpy.array(loc_inland_err)
# arr2 = numpy.array(loc_offshore_err)
# print "loc_inland_err Inland Average: %.1f \261 %.1f sec\n"%(numpy.mean(loc_inland_err),numpy.std(loc_inland_err)))
# print "loc_offshore_err Offshore Average: %.1f \261 %.1f sec\n"%(numpy.mean(loc_offshore_err),numpy.std(loc_offshore_err)))

print ("\n\n")
arr1 = numpy.array(loc_inland_err)
arr2 = numpy.array(loc_offshore_err)
print ("loc_inland_err Inland Average: ", numpy.mean(loc_inland_err), "   ",numpy.std(loc_inland_err))
print ("loc_offshore_err Offshore Average: ", numpy.mean(loc_offshore_err),"   ", numpy.std(loc_offshore_err))


print ("\n\n")
arr1 = numpy.array(loc_inland_err)
arr2 = numpy.array(loc_offshore_err)
print ("loc_inland_err Inland Average f42: ", numpy.mean(loc_inland_err_f42), "   ",numpy.std(loc_inland_err_f42))
print ("loc_offshore_err Offshore Average f42: ", numpy.mean(loc_offshore_err_f42),"   ", numpy.std(loc_offshore_err_f42))

print ("\n\n")
# arr1 = numpy.array(mag_inland_err)
# arr2 = numpy.array(mag_offshore_err)


arr1 = np.array(mag_inland_err)
ss1_in = np.mean(arr1)
ss2_in = np.sqrt(ss1_in)

arr2 = np.array(mag_offshore_err)
ss1_off = np.mean(arr2)
ss2_off = np.sqrt(ss1_off)

print ("mag_inland_err Inland Average: ", ss2_in)
print ("mag_offshore_err Offshore Average: ", ss2_off)



arr1 = np.array(mag_inland_err_f42)
ss1_in = np.mean(arr1)
ss2_in = np.sqrt(ss1_in)

arr2 = np.array(mag_offshore_err_f42)
ss1_off = np.mean(arr2)
ss2_off = np.sqrt(ss1_off)

print ("mag_inland_err_f42 Inland Average: ", ss2_in)
print ("mag_offshore_err_f42 Offshore Average: ", ss2_off)




print ('\n\n')
arr1 = numpy.array(inland_time)
arr2 = numpy.array(offshore_time)
arr3 = numpy.array(all_time)
print ('Process Time Inland AVG: ',numpy.mean(arr1), ' STD: ',numpy.std(arr1),numpy.shape(arr1))
print ('Process Time Offshore AVG: ',numpy.mean(arr2), 'STD: ',numpy.std(arr2),numpy.shape(arr2))
print ('Process Time  AVG: ',numpy.mean(arr3), 'STD: ',numpy.std(arr3),numpy.shape(arr3))

print ("inland number: "+str(len(inland_time)))
print ("offshore number: "+str(len(offshore_time)))
print ("total number", len(inland_time)+len(offshore_time))


print ('\n\n')
arr1 = numpy.array(inland_time_f42)
arr2 = numpy.array(offshore_time_f42)
arr3 = numpy.array(all_time_f42)
print ('Process Time Inland_f42 AVG: ',numpy.mean(arr1), ' STD: ',numpy.std(arr1),numpy.shape(arr1))
print ('Process Time Offshore_f42 AVG: ',numpy.mean(arr2), 'STD: ',numpy.std(arr2),numpy.shape(arr2))
print ('Process Time f42 AVG: ',numpy.mean(arr3), 'STD: ',numpy.std(arr3),numpy.shape(arr3))

print ("inland_f42 number: "+str(len(inland_time_f42)))
print ("offshore_f42 number: "+str(len(offshore_time_f42)))
print ("total_f42 number", len(inland_time_f42)+len(offshore_time_f42))


f1=open("mag_line_std","w")

arr = np.array(arrmag_sd)
ss1 = np.mean(arr)
ss2 = np.sqrt(ss1)

print ('-----------------ss2:', ss2)

f1.write("0 %f \n"%(0+ss2))
f1.write("8 %f \n"%(8+ss2))
f1.write(">> \n")
f1.write("0 %f \n"%(0-ss2))
f1.write("8 %f \n"%(8-ss2))
f1.write(">> \n")
f1.close()
f1=open("mag_txt","w")
f1.write("5.5 4.6 12 0 9 ML M@-L @-= M@-Pd @-SDV: %.1f \n"%(ss2))
f1.close()