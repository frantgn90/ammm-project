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
        
    #################################
    ## Special functions for BRKGA ##
    #################################
    
    #####################################################################################
    ## The mapping from chromosome to solution space is not an immediat mapping,       ##
    ## but needs some transformations, because a random chromosome can not be mapped   ##
    ## directly to a trivial solution.                                                 ##
    ##                                                                                 ##
    ## If the chromosome is obtained via <encodeToBRKA> the representation is:         ##
    ## - Every position gen of the chromosome represents one location                  ##
    ## - The value of the chromose indicates the previous source location from where   ##
    ##   the vehicle is comming.                                                       ##
    ## - The starting location does not have any previoues location, i.e. 0.           ##
    #####################################################################################
    
    def encodeToBRKGA(self):
        chromosome = [0]*self.nLocations
        order_divisor = 0
        locs = self.nLocations
        while locs > 0:
            order_divisor += 1
            locs /= 10
        
        for vehicle in self.solution:
            # The last path is not taked into account intetionally in order to
            # keep the gen for the startLocation as 0
            for i in range(len(vehicle)-1):
                path = vehicle[i]
                from_location = path.getSource().getId()
                to_location = path.getDestination().getId()
                chromosome[(to_location-1)] = from_location/10**order_divisor # Should be from 0 to 1.0
            
        return chromosome
        
    def fromChromosome(self, chromosome, problem):
        # Chromosome pre-process: The first step of the decoder is to do the 
        # needed transformations from the raw chromosome in order to obtain a 
        # depurated one that can be mapped to a solution in terms of graph constraints.
        
        # Step 1: Get a natural value from chromosome.
        
        order_divisor = 0
        locs = self.nLocations
        while locs > 0: order_divisor += 1; locs /= 10
            
        d_chromosome = [int(x * 10**order_divisor) for x in chromosome]
        
        #print d_chromosome
        
        # Step 2: All predecessors should exists in the problem, then have to be
        # less or equal the number of locations
        d_chromosome = [x % (self.nLocations+1) for x in d_chromosome]
        
        #print d_chromosome
        
        # Step 3: The only origin that can be repeated is the starting location
        not_seen = list(range(self.nLocations+1))
        seen = []
        
        i = 0
        for loc in d_chromosome:
            if loc in seen:
                d_chromosome[i] = not_seen[0]
                seen.append(not_seen[0])
                del not_seen[0]
            elif loc != self.startLocationId:
                seen.append(loc)
                del not_seen[not_seen.index(loc)]
                
            i += 1
            
        #print d_chromosome
        
        # Step 4: There can not be cycles that implies just one location. Then
        # gens with a value equal to its index must be forbidden.
        i = 0
        for loc in d_chromosome:
            if loc == (i+1):
                to_swap = (i+1)%len(d_chromosome)
                d_chromosome[i] = d_chromosome[to_swap]
                d_chromosome[to_swap] = (i+1)
            i+=1
        
        #print d_chromosome
        
        # Step 5: The chromosome only have to have one 0 i.e. one startLocation.
        # In this step, if there is a 0 then a swap ins performed if needed, if not
        # a 0 is injected in the startLocation gen.
        
        if not 0 in d_chromosome:
            d_chromosome[(self.startLocationId-1)] = 0
        else:
            d_chromosome[d_chromosome.index(0)] = d_chromosome[(self.startLocationId-1)]
            d_chromosome[(self.startLocationId-1)] = 0
        
        #print d_chromosome        
        
        # Step 6: Cycles that are not implying the startLocation are not allowed
        # Since the path from the last location to the start location is not coded
        # explicitly, then the chromosome can not have any cycle. If there is any
        # cycle it means that this cycle is not impying the startingLocation. Then
        # it should be broken with the startingLocation.
        visited_locations = []
        
        i = 0
        for i in range(len(d_chromosome)):
            current_location = (i+1)
            if current_location in visited_locations: 
                continue
            
            while current_location != self.startLocationId:
                if current_location in visited_locations:
                    # It means there is a cycle here that does not imply startLocation
                    # Just remove this cycle and connect it with the starting location
                    d_chromosome[(current_location-1)] = self.startLocationId
                    
                visited_locations.append(current_location)
                previous_location = d_chromosome[(current_location-1)]
                current_location = previous_location
        
        #print d_chromosome
        
        # Once the chromosome has been adapted (deterministically) in order to fulfill
        # the graph constraints, let's try to build up the solution taking into account
        # the time constraints. If the time constraints cannot be fullfiled, more
        # modifications will be done.
        
        solution_paths_sl = []
        solution_paths = [None]*self.nLocations
        are_not_predecesors = [(i+1) for i in range(self.nLocations)]
        
        for gen_i in range(len(d_chromosome)):
            path_from = d_chromosome[gen_i]
            path_to = (gen_i+1)
            
            # If this locations has not predecesor => startingLocation
            if path_from == 0:
                continue 
                
            # Remove from are_not_predecesors
            are_not_predecesors[(path_from-1)] = -1
                
            path = problem.getPathsFromTo(path_from, path_to)
            
            if path_from == self.startLocationId:
                solution_paths_sl.append(path)
            else:
                solution_paths[(path_from-1)] = path
        
        # Now, we have to add all paths that have as destination the startingLocation
        # i.e. we have to look for locations that are not predecesor of any other.
        for from_location in are_not_predecesors:
            if from_location == -1: continue
            
            path = problem.getPathsFromTo(from_location, self.startLocationId)
            solution_paths[(from_location-1)] = path
        
        # Sort all paths and add them to solution
        self.solution = []
        for path in solution_paths_sl:
            vehicle = [path]
            
            from_location = path.getDestination().getId()
            while from_location != self.startLocationId:
                next_path = solution_paths[(from_location-1)]
                vehicle.append(next_path)
                from_location = next_path.getDestination().getId()
                
            self.solution.append(vehicle)
            
        # Now, if this solution is not feasible because the time constraints
        # change it (deterministically) 
        
        lastArrival = 0
        i_vehicle = 0
        for vehicle in self.solution:
            vehicleArrival = 0
            last_time_arrive_home = 0
            last_time_arrive_home_path = None
            last_time_arrive_home_time = 0
            i_path = 0
            for path in vehicle:
                path_source = path.getSource()
                path_destination = path.getDestination()
                    
                vehicleArrival += path.getSource().getTask()
                vehicleArrival += path.getDistance()
                vehicleArrival = max(vehicleArrival, path.getDestination().getminW())
                
                if path_destination.getId() != self.startLocationId:
                    path_to_home = problem.getPathsFromTo(path_destination.getId(), self.startLocationId)
                    time_to_home = vehicleArrival + path_destination.getTask() + path_to_home.getDistance()
                    if time_to_home <= 720:
                        last_time_arrive_home = i_path
                        last_time_arrive_home_path = path_to_home
                        last_time_arrive_home_time = time_to_home
                

                # Then we have to split the path into two vehicles
                if vehicleArrival > 720 or vehicleArrival > path_destination.getmaxW():
                    #print "SPLIT: v={0}, p={1}".format(i_vehicle, i_path)
                    assert last_time_arrive_home_path != None
                    
                    new_path = problem.getPathsFromTo(self.startLocationId, vehicle[last_time_arrive_home+1].getDestination().getId())
                    new_vehicle = [new_path]
                    new_vehicle.extend(vehicle[last_time_arrive_home+2:])
                    self.solution.append(new_vehicle)
                    
                    self.solution[i_vehicle] = vehicle[:last_time_arrive_home+1]
                    self.solution[i_vehicle].append(last_time_arrive_home_path)
                    
                    vehicleArrival = last_time_arrive_home_time
                    break
                
                i_path += 1
                
            if vehicleArrival > lastArrival:
                    lastArrival = vehicleArrival
            
            i_vehicle += 1
                    
        self.lastArrived = lastArrival
        self.nVehicles = len(self.solution)
        self.is_feasible = True
        
        #print self.str()
            
        
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