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
    
    def evaluateNeighbor(self, change, problem):
        assert self.is_feasible == True, "Error trying to evaluate a neighbor " \
            " without having a feasible solution."
            
        neighbor = change[0]
        if neighbor == "exchange":
            a_location = change[1]
            b_location = change[2]
            
            lastArrival = 0
            for vehicle in self.solution:
                vehicleArrival = 0
                for path in vehicle:
                    the_path = path
                    path_source = path.getSource()
                    path_destination = path.getDestination()
                    
                    same_path = True
                    
                    # Replace path_source if needed
                    # Replace path_destination if needed
                    if path_source.getId() == a_location.getId():
                        path_source = b_location
                        same_path = False
                    elif path_source.getId() == b_location.getId():
                        path_source = a_location
                        same_path = False
                        
                    if path_destination.getId() == a_location.getId():
                        path_destination = b_location
                        same_path = False
                    elif path_destination.getId() == b_location.getId():
                        path_destination = a_location
                        same_path = False
                
                    if not same_path:
                        the_path = problem.getPathsFromTo(path_source.getId(),path_destination.getId())
                        
                    vehicleArrival += path_source.getTask()
                    vehicleArrival += the_path.getDistance()
                    vehicleArrival = max(vehicleArrival, path_destination.getminW())
                    
                    if vehicleArrival > 720:
                        return False, None
                    elif vehicleArrival > path_destination.getmaxW():
                        return False, None
                    
                if vehicleArrival > lastArrival:
                    lastArrival = vehicleArrival
                    
            return True, self.nVehicles*BIGM + lastArrival
                
        elif neighbor == "reassignement":
            location_to_reassign = change[1]
            path_to_inject = change[2] 
            
            # e.g. loc = 1, pti = 4->5
            # neighbor = 4->1->5
            
            evalVehicles = self.nVehicles
            lastArrival = 0
            for vehicle in self.solution:
                vehicleArrival = 0
                waiting_source = None
                
                for path in vehicle:
                    the_path = path
                    path_source = path.getSource()
                    path_destination = path.getDestination()
                    
                    # Remove the location_to_reassign from its original place
                    if path_destination.getId() == location_to_reassign.getId():
                        waiting_source = path_source
                        continue
                    elif path.getSource().getId() == location_to_reassign.getId():
                        assert waiting_source != None, "ERROR: Something wrong :: {0}"\
                            .format(path.getSource().getId())
                        
                        # It means that the reassignement have achieved the reduction of one vehicle.
                        if waiting_source.getId() == path_destination.getId():
                            evalVehicles -= 1
                            break
                            
                        the_path = problem.getPathsFromTo(waiting_source.getId(),path_destination.getId())
                        waiting_source = None
                        
                    if path.getId() == path_to_inject.getId():
                        path_1 = problem.getPathsFromTo(path_source.getId(), location_to_reassign.getId())
                        the_path = problem.getPathsFromTo(location_to_reassign.getId(), path_destination.getId())
                        
                        vehicleArrival += path_1.getSource().getTask()
                        vehicleArrival += path_1.getDistance()
                        vehicleArrival = max(vehicleArrival, path_1.getDestination().getminW())
                        
                    vehicleArrival += the_path.getSource().getTask()
                    vehicleArrival += the_path.getDistance()
                    vehicleArrival = max(vehicleArrival, the_path.getDestination().getminW())
                    
                    if vehicleArrival > 720:
                        return False, None
                    elif vehicleArrival > the_path.getDestination().getmaxW():
                        return False, None
                    
                if vehicleArrival > lastArrival:
                    lastArrival = vehicleArrival
                    
            return True, evalVehicles*BIGM + lastArrival
            
        else:
            assert False, "The neighborhood {0} does not exist.".format(neighbor)
        
    def performChange(self, change, problem):
        neighbor = change[0]
        
        if neighbor == "exchange":
            a_location = change[1]
            b_location = change[2]
            
            lastArrival = 0
            for vehicle in self.solution:
                vehicleArrival = 0
                p_counter = 0
                for path in vehicle:
                    the_path = path
                    path_source = path.getSource()
                    path_destination = path.getDestination()
                    
                    same_path = True
                    
                    # Replace path_source if needed
                    # Replace path_destination if needed
                    if path_source.getId() == a_location.getId():
                        path_source = b_location
                        same_path = False
                    elif path_source.getId() == b_location.getId():
                        path_source = a_location
                        same_path = False
                    
                    if path_destination.getId() == a_location.getId():
                        path_destination = b_location
                        same_path = False
                    elif path_destination.getId() == b_location.getId():
                        path_destination = a_location
                        same_path = False
                
                    if not same_path:
                        the_path = problem.getPathsFromTo(path_source.getId(),path_destination.getId())
                    
                    # Perform the change
                    vehicle[p_counter] = the_path
                    
                    vehicleArrival += path_source.getTask()
                    vehicleArrival += the_path.getDistance()
                    vehicleArrival = max(vehicleArrival, path_destination.getminW())
                    
                    if vehicleArrival > 720:
                        assert False, "ERROR: Before perform change you have to ensure" \
                            + " that this change is feasible."
                    elif vehicleArrival > path_destination.getmaxW():
                        assert False, "ERROR: Before perform change you have to ensure" \
                            + " that this change is feasible."
                    
                    p_counter += 1
                    
                if vehicleArrival > lastArrival:
                    lastArrival = vehicleArrival
                    
            # The number of vehicles is always the same
            self.lastArrived = lastArrival
        elif neighbor == "reassignement":
            location_to_reassign = change[1]
            path_to_inject = change[2] 
            
            # e.g. loc = 1, pti = 4->5
            # neighbor = 4->1->5
            
            lastArrival = 0
            i_vehicle = 0
            vehicles_to_del = []
            for vehicle in self.solution:
                vehicleArrival = 0
                waiting_source = None
                path_added = False
                i_path = 0
                for path in vehicle:
                    if path_added: path_added=False; continue
                    
                    the_path = path
                    path_source = path.getSource()
                    path_destination = path.getDestination()
                    
                    # Remove the location_to_reassign from its original place
                    if path_destination.getId() == location_to_reassign.getId():
                        waiting_source = path_source
                        continue
                    elif path.getSource().getId() == location_to_reassign.getId() and waiting_source != None:
                        assert waiting_source != None, "ERROR: Something wrong :: {0}"\
                            .format(path.getSource().getId())
                        
                        if waiting_source.getId() == path_destination.getId():
                            vehicles_to_del.append(i_vehicle)
                            break
                            
                        the_path = problem.getPathsFromTo(waiting_source.getId(),path_destination.getId())
                        self.solution[i_vehicle][i_path] = the_path
                        del self.solution[i_vehicle][i_path-1]
                        waiting_source = None
                        
                    if path.getId() == path_to_inject.getId():
                        path_1 = problem.getPathsFromTo(path_source.getId(), location_to_reassign.getId())
                        the_path = problem.getPathsFromTo(location_to_reassign.getId(), path_destination.getId())
                        
                        self.solution[i_vehicle][i_path] = path_1
                        self.solution[i_vehicle].insert(i_path+1, the_path)
                        
                        path_added = True
                        
                        vehicleArrival += path_1.getSource().getTask()
                        vehicleArrival += path_1.getDistance()
                        vehicleArrival = max(vehicleArrival, path_1.getDestination().getminW())
                        
                    vehicleArrival += the_path.getSource().getTask()
                    vehicleArrival += the_path.getDistance()
                    vehicleArrival = max(vehicleArrival, the_path.getDestination().getminW())
                    
                    if vehicleArrival > 720:
                        assert False, "ERROR: Before perform change you have to ensure" \
                            + " that this change is feasible."
                    elif vehicleArrival > the_path.getDestination().getmaxW():
                        assert False, "ERROR: Before perform change you have to ensure" \
                            + " that this change is feasible."
                        
                    i_path += 1
                    
                if vehicleArrival > lastArrival:
                    lastArrival = vehicleArrival
                    
                i_vehicle += 1
                    
            # Updating solution quality
            self.lastArrived = lastArrival
            for v in vehicles_to_del:
                del self.solution[v]
                self.nVehicles -= 1
                
        else:
            assert False, "The neighborhood {0} does not exist.".format(neighbor)
        
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
    
    def getSolution(self):
        return self.solution
        
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
        '''
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
        '''
        
        return res