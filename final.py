from skyfield.api import load, wgs84
from datetime import date
import matplotlib.pyplot as plt
import sqlite3
import math
import time 
import random
import serial

ardData=serial.Serial('com3',9600)

start=time.perf_counter()

TrackObject=""

conn=sqlite3.connect('table.db')

cursor=conn.cursor()
dataAzi=[]
dataAl=[]
sat=[]

#with conn:
#    cursor.execute("DROP TABLE data")
    
cursor.execute("""CREATE TABLE IF NOT EXISTS data (
               name string,
               azi real,
               al real,
               rd real
                ) """)
conn.commit()

def clearTable():
    with conn:
        cursor.execute("DELETE FROM data")

def insertQ(name,azi,al):
    cursor.execute("SELECT * FROM data WHERE name = ? ",(name,))
    res=cursor.fetchone()
    conn.commit()
    with conn:
        if(res):
            cursor.execute("UPDATE data SET azi=?,al=? WHERE name = ?",(azi,al,name))
        else:
            cursor.execute("INSERT INTO data (name,azi,al) VALUES (?,?,?)",(name,azi,al))

def deleteQ(name):
    cursor.execute("SELECT * FROM data WHERE name = ? ",(name,))
    res=cursor.fetchone()
    conn.commit()
    with conn:
        if(res):
            if(name==TrackObject):
                    switchObject()
            cursor.execute("DELETE FROM data WHERE name = ? ",(name,))

def calculateRD(target):
    cursor.execute("SELECT * FROM data WHERE name = ? ",(target,))
    res=cursor.fetchone()
    print(res)
    if(res==None): 
        switchObject()
        return
    tempAz=res[1]
    tempAl=res[2]
    conn.commit()
    with conn:
            cursor.execute('SELECT * FROM data')
            temp=cursor.fetchall()
            print("AZIMUTH: "+str(tempAz)+" , ALTITUDE:"+str(tempAl))
    for t in temp:
        try:
            theta=math.radians(tempAz-t[1])
            rd=math.sqrt(tempAl**2+t[2]**2-2*tempAl*t[2]*math.cos(theta))
            cursor.execute("UPDATE data SET rd=? WHERE name = ?",(rd,t[0]))
        except ValueError as e:
            print("Exception")

def displayTable():
    with conn:
        cursor.execute("SELECT * FROM data ")
        tem=cursor.fetchall()
        for t in tem:
         print(t[3])

def get1st():
    with conn:
        cursor.execute("SELECT * FROM data ORDER BY al DESC")
        return cursor.fetchone()[0]        

def switchObject():
    global TrackObject
    cursor.execute("SELECT * FROM data ORDER BY rd ASC")
    temp=cursor.fetchall()
    conn.commit()
    if(temp[1][3]!= None):
        calculateRD(TrackObject)
        if(temp[1][3]>10): 
            return
    
    global sat
    TrackObject=temp[1][0]
    sat.append(TrackObject)
    print(TrackObject)
    calculateRD(TrackObject)

def getValue():
    global TrackObject
    with conn:
        cursor.execute("SELECT * FROM data WHERE name = ?",(TrackObject,))
        return cursor.fetchone()
    
with open('gp.php','r') as file:
    content=file.readlines()
    print('Loaded', int(len(content)/3), 'satellites')

satellites = load.tle_file('gp.php')
by_number = {sat.name: sat for sat in satellites}
count=0
bluffton = wgs84.latlon(12.933851, 77.691874,920)
clearTable()
ts = load.timescale()
for k in range(60):
    t=ts.now()
    #t=ts.utc(2024,1,17,17,k,0)

    for i in by_number:
            
            satellite = by_number[i]
            
            difference = satellite - bluffton
            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            count=count+1
            if alt.degrees > 20:
                insertQ(i,az.degrees,alt.degrees)
            else:
               # if(i==TrackObject):
                # switchObject()
                deleteQ(i)
                #calculateRD(TrackObject)
    #num=random.randint(1,10)   
    if(k==0):
        TrackObject=get1st()    
    calculateRD(TrackObject)
    tempList=getValue()
    azi=int(tempList[1])
    al=int(tempList[2])
    azi=azi-azi%5
    al=al-al%5
    if(azi%5==0 and al%5==0 ):
        cmd=str(azi)+'+'+str(al)+'\r'
        print(cmd)
        ardData.write(cmd.encode())
    dataAzi.append(tempList[1])
    dataAl.append(tempList[2])
    #displayTable()        
        
print(dataAl)
print(dataAzi)
print(sat)
sat=list(set(sat))
x=list(range(len(dataAzi)))
cmd="0+90"+'\r'
ardData.write(cmd.encode())
final=time.perf_counter()
print('Finished in',round(final-start,2),'seconds')

plt.plot(x,dataAzi,label='AZIMUTH')
plt.plot(x,dataAl,label='ALTITUDE')
plt.xlabel('TIME')
plt.ylabel('ANGLE')
plt.title('SATELLITE TRACKING GRAPH')
plt.ticklabel_format(style='plain', axis='both')
plt.legend()
plt.show()

conn.close()