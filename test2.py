from skyfield.api import load, wgs84
from datetime import date
import matplotlib.pyplot as plt
import sqlite3
import math
import time 
start=time.perf_counter()

TrackObject=""

conn=sqlite3.connect('table.db')

cursor=conn.cursor()
dataAzi=[]
dataAl=[]
sat=[]

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
            cursor.execute("DELETE FROM data WHERE name = ? ",(name,))

def calculateRD(target):
    cursor.execute("SELECT * FROM data WHERE name = ? ",(target,))
    res=cursor.fetchone()
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
            rd=math.sqrt(tempAl**2+t[2]**2-2*tempAl*t[2]*math.cos(math.radians(tempAz-t[1])))
            cursor.execute("UPDATE data SET rd=? WHERE name = ?",(rd,t[0]))
        except ValueError as e:
            print("Exception")
            switchObject()

def displayTable():
    with conn:
        cursor.execute("SELECT * FROM data ")
        tem=cursor.fetchall()
        for t in tem:
         print(t[3])

def get1st():
    with conn:
        cursor.execute("SELECT * FROM data")
        return cursor.fetchone()[0]        

def switchObject():
    cursor.execute("SELECT * FROM data ORDER BY rd ASC")
    temp=cursor.fetchall()
    conn.commit()
    global TrackObject
    TrackObject=temp[1][0]
    print(TrackObject)
    calculateRD(TrackObject)

def getValue():
    global TrackObject
    with conn:
        cursor.execute("SELECT * FROM data WHERE name = ?",(TrackObject,))
        return cursor.fetchone()

satellites = load.tle_file('gp.php')
print('Loaded', len(satellites), 'satellites')
by_number = {sat.name: sat for sat in satellites}
count=0
bluffton = wgs84.latlon(12.933851, 77.691874,920)
clearTable()
ts = load.timescale()
for k in range(50):
    t=ts.now()
    for i in by_number:
            
            satellite = by_number[i]
            
            difference = satellite - bluffton
            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            count=count+1
            if alt.degrees > 20:
                insertQ(i,az.degrees,alt.degrees)
            else:
                if(i==TrackObject):
                    switchObject()
                deleteQ(i)
                
    if(k==0):
        TrackObject=get1st()    
    calculateRD(TrackObject)
    if(k%10==0):
        switchObject()
    tempList=getValue()
    dataAzi.append(tempList[1])
    dataAl.append(tempList[2])
    #displayTable()            
print(dataAl)
print(len(dataAzi))
print(dataAzi)
sat=list(set(sat))
x=list(range(len(dataAzi)))

final=time.perf_counter()
print(final-start)

#plt.plot(x,dataAzi,label='AZIMUTH')
#plt.plot(x,dataAl,label='ALTIDUDE')
plt.polar(dataAzi,dataAl)
#plt.xlabel('TIME')
#plt.ylabel('MAGNITUDE')
#plt.title('SATELLITE TRACKING GRAPH')
#plt.ticklabel_format(style='plain', axis='both')
#plt.legend()
plt.show()
for a in sat:
    print(a)

conn.close()