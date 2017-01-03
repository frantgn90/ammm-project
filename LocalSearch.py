# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from Path import Path
from Location import Location
from Solution import Solution

import copy
        
class LocalSearch(object):
    def __init__(self, problem, solution):
        self.problem = problem
        self.solution = solution
       
    '''
    The exchange consist on change two locations. The most loaded of the most
    loaded vehicle with the less loaded of the less loaded vehicle.
    With this strategy we'll never imprive the number of vehicles but we could
    improve the lasArrival vehicle.
    '''
    def exploreNeighborhoodExchange(self, strategy): 
        # Sort from most loaded vehicle to less loaded one
        vehicles = filter(lambda x: len(x) > 0, self.solution.getSolution())
        
        vehicles = sorted(vehicles, key=self.__calculeArrivalTime, reverse=True)
        mostLoadedVehicle = vehicles[0]
        
        # Every location visited by the most lodead vehicle is prone to be exchanged
        # but the most desirable situation is that the location with the highest task
        # will be changed
        mostLoadedVehicleLocations = []
        for path in mostLoadedVehicle: 
            if path.getSource().getId() != self.problem.getStartLocationId():
                mostLoadedVehicleLocations.append(path.getSource())
                    
        mostLoadedVehicleLocations = sorted(mostLoadedVehicleLocations, 
            key=lambda x: x.getTask(), 
            reverse=True)
        
        # The rest of the locations for the other vehicles that are prone to be exchanged
        # ordered from small to big task
        restOfLocations = []
        for v_i in range(1, len(vehicles)): 
            for p in vehicles[v_i]: 
                if p.getSource().getId() != self.problem.getStartLocationId():
                    restOfLocations.append(p.getSource())
            
        restOfLocations = sorted(restOfLocations, 
            key=lambda x: x.getTask(), 
            reverse=False)
        
        # Look for all the neighborhood
        best_solution = self.solution
        for loc_a in mostLoadedVehicleLocations:
            for loc_b in restOfLocations:
                if loc_b.getId() == self.problem.getStartLocationId: continue
                
                change = ("exchange", loc_a, loc_b)
                feasible, q = self.solution.evaluateNeighbor(change, self.problem)
                '''
                print ("Exchanging {0}<->{1} . Feasible: {2} . Quality: {3}"
                    .format(loc_a.getId(), loc_b.getId(), str(feasible), q))
                '''
                if not feasible: continue
                
                if q < best_solution.getQuality():
                    new_solution = copy.deepcopy(self.solution)
                    new_solution.performChange(change, self.problem)
                    
                    if strategy == "first-improvement":
                        return new_solution
                    elif strategy == "best-improvement":
                        best_solution = new_solution
                        
        return best_solution
        
    '''
    The reassignement consists on move locations visited by one vehicle to 
    other vehicle. With this strategy we could minimize the number of needed
    vehicles
    '''
    def exploreNeighborhoodReassignement(self, strategy):                
        # Sort from most loaded vehicle to less loaded one
        vehicles = filter(lambda x: len(x) > 0, self.solution.getSolution())
        vehiclesByLoad = sorted(vehicles, key=self.__calculeArrivalTime, reverse=False)
        vehiclesByLocations = sorted(vehicles, key=lambda x: len(x), reverse=False)
        
        # Will try to reassign the locations for the vehicles with less locations to
        # vehicles with less load
        
        best_solution = self.solution
        for vFewLocations in vehiclesByLocations:
            for p in vFewLocations:
                locationToReassign = p.getSource()
                if locationToReassign.getId() == self.problem.getStartLocationId(): 
                    continue
                    
                for vLessLoaded in vehiclesByLoad:
                    if p in vLessLoaded: continue # Is the same vehicle
                    
                    # Try to put the location to some place of the vehicle route
                    for pathToInject in vLessLoaded:
                        change = ("reassignement", locationToReassign, pathToInject)
                        feasible, q = self.solution.evaluateNeighbor(change, self.problem)
                        
                        if not feasible: continue
                        
                        if q < best_solution.getQuality():                                    
                            new_solution = copy.deepcopy(self.solution)
                            new_solution.performChange(change, self.problem)
                            '''
                            print ("Reassignement {0} -> ({1}->{2}) . Feasible: {3} . Quality: {4}"
                            .format(locationToReassign.getId(), 
                                    pathToInject.getSource().getId(), 
                                    pathToInject.getDestination().getId(),
                                    feasible, new_solution.getQuality()))
                            '''
                            if strategy == "first-improvement":
                                return new_solution
                            elif strategy == "best-improvement":
                                best_solution = new_solution
        return best_solution
    '''
    Auxiliar function just for sort vehicles
    '''
    def __calculeArrivalTime(self, vehicle):
        if len(vehicle) == 0: return 0
        lastPath = vehicle[-1]
        
        return  lastPath.getSource().getarrivingTime() + \
                lastPath.getSource().getWaitingTime() + \
                lastPath.getSource().getTask() + \
                lastPath.getDistance()