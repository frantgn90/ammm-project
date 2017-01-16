'''
Project AMMM
Result Visualizer

Juan Francisco Martinez Vera
juan.francisco.martinez@est.fib.upc.edu
'''

import sys
import math
import tkinter as tk
import random

startLocation=4

WSIZE=750
RADIUS=WSIZE/2-50

CITY_RADIUS=25
CITY_FONT_SIZE=20

assert RADIUS < WSIZE/2, "Bad windows configuration"

class Result(object):
    def __init__(self, file):
        self._file=file
        self.__parseResult()
        
    def __parseResult(self):
        ofile=open(self._file, "r")
        
        infield=None
        fieldVal=""
        
        for line in ofile:
            if line[:2] == "//": continue
            if "=" in line:
                fieldVal=' '.join(fieldVal.split())
                fieldVal=fieldVal.replace(";","")
                
                if infield == "nVehicles":
                    self._nvehicles=eval(fieldVal)
                elif infield == "lastDone":
                    self._lastdone=eval(fieldVal)
                elif infield == "tracked":
                    fieldVal=fieldVal.replace(" ", ",").replace("\n",",")
                    self._tracked=eval(fieldVal)
                elif infield == "arrivingTime":
                    fieldVal=fieldVal.replace("\n",",").replace(" ", ",")
                    self._arriving_time=eval(fieldVal)
                
                fieldVal=""
                split_line=line.split(" ")
                infield=split_line[0]
                line=" ".join(split_line[2:])
            fieldVal+=line

        # For last field
        fieldVal=' '.join(fieldVal.split())
        fieldVal=fieldVal.replace(";","")
        
        if infield == "nVehicles":
            self._nvehicles=eval(fieldVal)
        elif infield == "lastDone":
            self._lastdone=eval(fieldVal)
        elif infield == "tracked":
            fieldVal=fieldVal.replace(" ", ",").replace("\n",",")
            self._tracked=eval(fieldVal)
        elif infield == "arrivingTime":
            fieldVal=fieldVal.replace("\n",",").replace(" ", ",")
            self._arriving_time=eval(fieldVal)

            
    def getnVehicles(self):
        return self._nvehicles
        
    def getLastDone(self):
        return self._lastdone
        
    def getArrivingTime(self, city):
        return self._arriving_time[city]
        
    def getTracked(self, citya, cityb):
        return self._tracked[citya][cityb]
        
    def getnCities(self):
        return len(self._arriving_time)

        
def drawCanvas(result):
    master = tk.Tk()

    w = tk.Canvas(master, width=WSIZE, height=WSIZE)

    bground = tk.PhotoImage(file="./spain_map.gif")

    w.pack()
    w.create_image(0, 0, image=bground, anchor='nw')

    cities_degrees=[0]*result.getnCities()
    cities_degrees[0]=0
    for i in range(1,result.getnCities()):
        cities_degrees[i]=cities_degrees[i-1] + 360/result.getnCities()

    
    center=[WSIZE/2, WSIZE/2]
    cities_positions=[]
    for i in range(len(cities_degrees)):
        city_center_x=center[0]+RADIUS*math.cos(math.radians(cities_degrees[i]))
        city_center_y=center[1]+RADIUS*math.sin(math.radians(cities_degrees[i]))
        cities_positions.append([city_center_x, city_center_y])

    icity=1
    for city in cities_positions:
        if icity==startLocation:
            color_oval="black"
            color_text="white"
        else:
            color_oval="white"
            color_text="black"

        w.create_oval(city[0]-CITY_RADIUS,
                      city[1]+CITY_RADIUS, 
                      city[0]+CITY_RADIUS,
                      city[1]-CITY_RADIUS,fill=color_oval)
        w.create_text(city[0],city[1], 
                      text=str(icity), fill=color_text, font=("Purisa", CITY_FONT_SIZE))
        icity+=1

    for i in range(result.getnCities()):
        for j in range(result.getnCities()):
            if result.getTracked(i,j):
                toffset_x=0
                toffset_y=0
                
                w.create_line(cities_positions[i][0], cities_positions[i][1],
                              cities_positions[j][0]+toffset_x, 
                              cities_positions[j][1]+toffset_y,
                              fill="red", arrow="last", width="2", 
                              arrowshape=(15, 15, 8), dash=(4))
                              
    for i in range(result.getnCities()):
        w.create_text(cities_positions[i][0], cities_positions[i][1]-CITY_RADIUS-10, 
                      text=str(result.getArrivingTime(i)))

    tk.mainloop()
    
def Usage(name):
    print("{0}: AMMM Project result visualizer v0.1".format(name))
    print("{0} <result.txt>".format(name))
    
def main(argc, argv):
    if argc < 2:
        #Usage(argv[0])
        #exit(1)
        result_file="result.txt"
    else:
        result_file=argv[1]
    result=Result(result_file)
    drawCanvas(result)
    
if __name__=="__main__":
    main(len(sys.argv), sys.argv)
