# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from Path import Path
from Location import Location

BIGM=100000

class Solution(object):
    def __init__(self, nCandidates, startLocationId):
        self.nVehicles=0
        self.lastArrived=0
        self.addedCandidates=0
        self.nCandidates=nCandidates
        self.startLocationId=startLocationId
        self.isFeasible = True
        
        # The solution consists on a set of sets of paths. Evert set of sets 
        # represents a vehicle.
        self.solution=[]
        
    def addCandidate(self, candidate):
        assert self.nCandidates < self.addedCandidates, "Solution Error: You \
            can not add more candidates to the solution. There is already a valid one"
            
        newArrivingTime = candidate.getSource().getarrivingTime() + \
                          candidate.getSource().getWaitingTime() + \
                          candidate.getSource().getTask() + \
                          candidate.getDistance()
                          
        if newArrivingTime > 720:
            self.isFeasible = False
            return False # No feasible
        
        if candidate.getDestination().getId() == self.startLocationId:
            nVehicles+=1
            
            # Let's start a new cycle
            self.solution.append([candidate])
            if newArrivingTime > self.lastArrived:
                self.lastArrived = newArrivingTime
            
        else:
            candidate.getDestination().arrivingTime = newArrivingTime
            self.solution[nVehicles].append(candidate)
        addedCandidates+=1
        
    def getnVehicles(self):
        return nVehicles
        
    def getlastArrived(self):
        return self.lastArrived
        
    def getQuality(self):
        return self.nVehicles*BIGM  + self.lastArrived
        
    def isDone(self):
        return self.addedCandidates == self.nCandidates
        
    def isFeasible(self):
        return self.isFeasible
        
    def str(self):
        pass

