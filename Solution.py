# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from Path import Path
from Location import Location

BIGM=100000
WIDTH_PRINT=80
LEFT_MARGIN=3

QUALITY_STR="Quality: "
NVEHICLES_STR="N of vehicles: "
LASTDONE_STR="Last done @: "

class Solution(object):
    def __init__(self, nLocations, startLocationId):
        self.nVehicles=0
        self.lastArrived=0
        self.visitedLocations=0
        self.nLocations=nLocations
        self.startLocationId=startLocationId
        self.is_feasible=False
        
        # The travel time for the actual cycle.
        self.TravelTime=0
        
        # The solution consists on a set of sets of paths. Evert set of sets 
        # represents a vehicle.
        self.solution= [[] for i in range(nLocations)]
        
        
        
    def addCandidate(self, candidate):
        assert self.solution != None, "Solution is not initialized. Please call " \
            + "initSolution(nLocations) function"
        #assert (self.nLocations-1) > self.visitedLocations, "Solution Error: You " \
        #    + "can not add more candidates to the solution. There is already a valid one"
            
        newArrivingTime = candidate.getSource().getarrivingTime() + \
                          candidate.getSource().getWaitingTime() + \
                          candidate.getSource().getTask() + \
                          candidate.getDistance()
                          
        self.TravelTime = newArrivingTime
                          
        if newArrivingTime > 720:
            return
        
        if candidate.getDestination().getId() == self.startLocationId:            
            self.solution[self.nVehicles].append(candidate)
            self.nVehicles+=1

            if self.TravelTime > self.lastArrived:
                self.lastArrived = self.TravelTime
            self.TravelTime = 0
            
        else:
            candidate.getDestination().arrivingTime = newArrivingTime
            self.solution[self.nVehicles].append(candidate)
        
            # Potentially, we can visit the start location more than one time
            self.visitedLocations+=1
        
        if self.visitedLocations==(self.nLocations-1):
            self.is_feasible = True
        
    def getTravelTime(self):
        return self.TravelTime
    
    def getnVehicles(self):
        return self.nVehicles
        
    def getlastArrived(self):
        return self.lastArrived
        
    def getQuality(self):
        return self.nVehicles*BIGM  + self.lastArrived
        
    def isDone(self):
        return self.visitedLocations == (self.nLocations-1)
        
    def isFeasible(self):
        return self.is_feasible
        
    def str(self):
        sol_quality=self.getQuality()
        n_vehicles=self.getnVehicles()
        last_done=self.getlastArrived()
        
        # Values
        res="\n"
        res+= "*"*WIDTH_PRINT
        res+= "\n*"+" "*(WIDTH_PRINT-2)+"*"
        res+= "\n*{0}{1}{2}{3}*" .format(
            " "*LEFT_MARGIN,QUALITY_STR, 
            str(sol_quality),
            " "*(WIDTH_PRINT-2-LEFT_MARGIN-len(str(sol_quality))-len(QUALITY_STR)))
            
        res+= "\n*{0}{1}{2}{3}*" .format(
            " "*LEFT_MARGIN,NVEHICLES_STR, 
            str(n_vehicles),
            " "*(WIDTH_PRINT-2-LEFT_MARGIN-len(str(n_vehicles))-len(NVEHICLES_STR)))
            
        res+= "\n*{0}{1}{2}{3}*\n" .format(
            " "*LEFT_MARGIN,LASTDONE_STR, 
            str(last_done),
            " "*(WIDTH_PRINT-2-LEFT_MARGIN-len(str(last_done))-len(LASTDONE_STR)))
        
        res+= "*"+" "*(WIDTH_PRINT-2)+"*\n"        
        res+= "*"*WIDTH_PRINT
        res+= "\n"
        
        # Routes
        
        for vehicle in self.solution:
            res+= "*"+" "*(WIDTH_PRINT-2)+"*\n"        
            for path in vehicle:
                loc_s=str(path.getSource().getId())
                loc_d=str(path.getDestination().getId())
                
                res+= "*{0}{1}->{2}{3}*\n" .format(
                    " "*LEFT_MARGIN,
                    loc_s, 
                    loc_d,
                    " "*(WIDTH_PRINT-4-LEFT_MARGIN-len(loc_s)-len(loc_d)))
                    
        res+= "*"*WIDTH_PRINT      
        res+="\n"
        
        return res

