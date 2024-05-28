import json
import requests
import serial
from datetime import datetime,timedelta
from datetime import date
date=date.today()
tomo=date+timedelta(1)
from geopy.geocoders import Nominatim 

arduinoData=serial.Serial('com3',9600)
cmd="placeholder"

loc=Nominatim(user_agent="GetLoc")
getLoc=loc.geocode("Bangalore")

lat=str(getLoc.latitude)
lon=str(getLoc.longitude)
c=0 
a=input("Enter the object name:")
while True:
    if (c>=10): break
    now =datetime.now() 
    current_time=now.strftime("%H:%M:%S") 
    tim=str(current_time) 
    azi=str(0) 
    ali=str(90) 
    print(azi,ali) 
    cmd=azi+'+'+ali+'\r'
    arduinoData.write(cmd.encode())
    c=c+10
print("done")
