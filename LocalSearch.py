# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from Path import Path
from Location import Location
from Solution import Solution

import copy
        
class LocalSearch(object):
    def __init__(self, problem, solution):
        self.problem = problem
        self.solution = copy.deepcopy(solution)
        
    def exploreNeighborhoodExchange(self, strategy): 
        # The exchange consist on change two locations. The most loaded of the most
        # loaded vehicle with the less loaded of the less loaded vehicle.
        # With this strategy we'll never imprive the number of vehicles but we could
        # improve the lasArrival vehicle.
        
        vehicles = filter(lambda x: len(x) > 0, self.solution.getSolution()) 
        
        # Sort from most loaded vehicle to less loaded one
        vehicles = sorted(vehicles, key=self.__calculeArrivalTime, reverse=True)
        mostLoadedVehicle = vehicle[0]
        lessLoadedVehicle = vehicle[-1]
        
        i_bigLocation, dummy = self.__getMaxMinLoadedLocation(mostLoadedVehicle)
        dummy, i_smallLocation = self.__getMaxMinLoadedLocation(lessLoadedVehicle)
        
        # NOTE: The most loaded location never will be the startingLocatin
        # because the task for this one must be 0
        
        # Exchanging locations
        bigLocation = mostLoadedVehicle[i_bigLocation].getSource()
        smallLocation = lessLoadedVehicle[i_smallLocation].getSource()
        
        ### Putting small location to most loaded vehicle
        bigPreviousLocation = mostLoadedVehicle[i_bigLocation-1].getSource()
        bigLaterLocation = mostLoadedVehicle[i_bigLocation].getDestination()
        
        bigToPath = self.problem.getPathsFromTo(bigPreviousLocation, smallLocation)
        bigFromPath = self.problem.getPathsFromTo(smallLocation, bigLaterLocation)
        mostLoadedVehicle[i_bigLocation-1] = bigToPath
        mostLoadedVehicle[i_bigLocation] = bigFromPath
        
        ### Putting big location to most idle vehicle
        smallPreviousLocation = lessLoadedVehicle[i_smallLocation-1].getSource()
        smallLaterLocation = lessLoadedVehicle[i_smallLocation].getDestination()
        
        smallToPath = self.problem.getPathsFromTo(smallPreviousLocation, bigLocation)
        smallFromPath = self.problem.getPathsFromTo(bigLocation, smallLaterLocation)
        lessLoadedVehicle[i_smallLocation-1] = smallToPath
        lessLoadedVehicle[i_smallLocation] = smallFromPath
        
        
        feasible  = self.__recalculeSolutionFrom(mostLoadedVehicle, i_bigLocation-1)
        feasible &= self.__recalculeSolutionFrom(lessLoadedVehicle, i_smallLocation-1)
        
        
    def __recalculeSolution(self, vehicle, from_location):
        max_load = 0

        for i in range(from_location, len(vehicle))
            arriving_time = vehicle[i].getSource().getarrivingTime() + \
                            vehicle[i].getSource().getWaitingTime() + \
                            vehicle[i].getSource().getTask() + \
                            vehicle[i].getDistance()
            
            if arriving_time > 720: return False
            if arriving_time > vehicle[i].getDestination().getmaxW(): return False
            
            vehicle[i].getDestination().arrivingTime = arriving_time
            
        return True
        
    def exploreNeighborhoodReassignement(self, strategy):
        
        pass
        
    def __calculeArrivalTime(self,vehicle):
        if len(vehicle) == 0: return 0
        lastPath = vehicle[-1]
        
        return  lastPath.getSource().getarrivingTime() + \
                lastPath.getSource().getWaitingTime() + \
                lastPath.getSource().getTask() + \
                lastPath.getDistance()
        
    def __getMaxMinLoadedLocation(self, vehicle):
        min_load = float.inf
        min_load_loc_i = 0
        max_load = 0
        max_load_loc_i = 0
        
        # NOTE: We are avoiding the starting location. We do not care about its task
        # duration
        i = 0
        for i in range(1,len(vehicle):
            p = vehicle[i]
            
            if p.getSource().getTask() > max_load:
                max_load = p.getSource().getTask()
                max_load_loc = i
            if p.getSource().getTask() < min_load:
                min_load = p.getSource().getTask()
                min_load_loc = i
                
        return max_load_loc, min_load_loc