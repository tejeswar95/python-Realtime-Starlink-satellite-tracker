import matplotlib.pyplot as plt
import sqlite3
from itertools import count
from matplotlib.animation import FuncAnimation

conn=sqlite3.connect('table.db')
cursor=conn.cursor()

plt.style.use('fivethirtyeight')
index=count()
x_vals=[]
azi=[]
al=[]

def plotter(i):
    with conn:
        cursor.execute("SELECT * FROM data WHERE rd = 0 ")
        t=cursor.fetchone()
        if(t==None): return
        x_vals.append(next(index))
        azi.append(t[1])
        al.append(t[2])
        plt.cla()
        plt.plot(x_vals,azi,label='Azimuth')
        plt.plot(x_vals,al,label='Altitude')
        plt.legend()
        print('Azimuth: '+str(t[1])+' Altitude: '+str(t[2]))

ani=FuncAnimation(plt.gcf(),plotter,interval=1000)

#plt.tight_layout()
plt.show()
