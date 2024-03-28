from skyfield.api import load, wgs84
from datetime import date
import time

start=time.perf_counter()
OldSat=[]
CurrentSat=[]
temp=0
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle'
satellites = load.tle_file(stations_url)
print('Loaded', len(satellites), 'satellites')
by_number = {sat.model.satnum: sat for sat in satellites}
bluffton = wgs84.latlon(12.933851, 77.691874,920)

ts = load.timescale()

while temp <= 95*2:

    for i in by_number:
        
        satellite = by_number[i]
        
        t=ts.utc(2023,12,26,12+int(temp/60),30+int(temp%60),0)
        
        difference = satellite - bluffton
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()

        if alt.degrees > 20:
            CurrentSat.append(satellite)
    print(temp/10+1)   
    temp=temp+10
    OldSat=list(set(OldSat).union(set(CurrentSat)))  
    CurrentSat=[]

GetCat=[]
for i in OldSat:
    temp=str(i)
    for j in range(len(temp)):
        if (temp[j]=='#'):
            GetCat.append(str(temp[j+1]+temp[j+2]+temp[j+3]+temp[j+4]+temp[j+5]))
            j=len(temp)+1
print(GetCat)


content=None
with open('gp.php','r') as file:
    content=file.readlines()

for i in range(2,len(content),3):
    temp=content[i]
    num=str(temp[2]+temp[3]+temp[4]+temp[5]+temp[6])
    for j in GetCat:
        if(num==j):
            with open('gph.php','a') as file:
                file.writelines(content[i-2]+content[i-1]+content[i])
final=time.perf_counter() 
print(final-start)

