# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import random

from Solution import Solution
from Problem import Problem
from LocalSearch import LocalSearch

class Solver_GRASP(object):
    def __init__(self, problem):
        #random.seed(123123)
        self.problem=problem
        self.visitedLocations=[]
        self.solution=Solution(problem.getnLocations(), 
                               problem.getStartLocationId())
        
    def Solve(self, alfa):
        last_location=self.problem.getStartLocationId()
        while not self.solution.isDone():
            travel_time = self.solution.getTravelTime()
            cset=self.__construct_cs(
                    last_location, 
                    travel_time)
            
            if len(cset) == 0:
                print ("GRASP: No more candidates but solution is not done.")
                break
                
            # Generating RCL
            #qmin=min(cset, key=lambda x: self.__greedy_value(x, travel_time))
            #qmax=max(cset, key=lambda x: self.__greedy_value(x, travel_time))
            
            # TODO: I think that cset is already sorted!!!!
            path_qmin=sorted(cset, key=lambda x: self.__greedy_value(x, travel_time), 
                        reverse=False)[0]
            path_qmax=sorted(cset, key=lambda x: self.__greedy_value(x, travel_time), 
                        reverse=False)[-1]
            
            qmin=self.__greedy_value(path_qmin, travel_time)
            qmax=self.__greedy_value(path_qmax, travel_time)
            
            threshold=qmin + alfa*(qmax-qmin)
            RCL=filter(lambda x: self.__greedy_value(x,travel_time) <= threshold,
                       cset)
            # Pick one randomly
            random_pick=random.randrange(len(RCL))
            candidate=RCL[random_pick]
            '''
            # DEBUG
            print "--CSET--"
            for c in cset:
                print "| {0}: {1}({2})->{3} distance: {4} greedy:{5}".format(c.getId(), c.getSource().getId(),c.getSource().getarrivingTime(), 
                    c.getDestination().getId(), c.getDistance(), self.__greedy_value(c, travel_time))
            print "---------"
            print "--RCL--"
            for c in RCL:
                print "| {0}: {1}->{2} distance:{3} greedy:{4}".format(c.getId(), c.getSource().getId(), 
                    c.getDestination().getId(), c.getDistance(), self.__greedy_value(c, travel_time))
            print "---------"
            print "-------------"
            print "QMAX: {0}".format(qmax)
            print "QMIN: {0}".format(qmin)
            print "THRE: {0}".format(threshold)
            print "RNDP: {0}".format(random_pick)
            print "-------------"
            
            print "--CANDIDATE--"
            print "| {0}: {1}({2})->{3} distance: {4} greedy:{5}".format(candidate.getId(), candidate.getSource().getId(), candidate.getSource().getarrivingTime(),
                candidate.getDestination().getId(), candidate.getDistance(), self.__greedy_value(candidate, travel_time))
            print "-------------"
            '''
            
            # Add candidate to solution
            self.solution.addCandidate(candidate)
            
            # We always can return to the startLocation (+1 vehicle)
            if candidate.getDestination().getId() != self.problem.getStartLocationId():
                self.visitedLocations.append(candidate.getDestination().getId())
            
            last_location=candidate.getDestination().getId()
            
        # Now is mandatory to add to solution the last path in order to return
        # to the startLocation
        from_location=candidate.getDestination().getId()
        to_location=self.problem.getStartLocationId()
        
        last_path=self.problem.getPathsFromTo(from_location, to_location)
        self.solution.addCandidate(last_path)

    def doLocalSearch(self, neighborhood, strategy):
        LS=LocalSearch(self.problem, self.solution)
        
        if neighborhood == "exchange":
            self.solution = LS.exploreNeighborhoodExchange(strategy)
        elif neighborhood == "reassignement":
            self.solution = LS.exploreNeighborhoodReassignement(strategy)

    def getSolution(self):
        return self.solution
        
    def isFeasible(self):
        return self.solution.isFeasible()

    def __construct_cs(self, from_location_id, travel_time):
        # Get all candidate paths filtered by start location
        paths = self.problem.getPathsFrom(from_location_id)
        
        cs = []
        # Get all candidate paths filtered by time
        # TODO: Look for add task and distance to travel_time 
        for p in paths:
            if p.getDestination().getmaxW() >= travel_time:
                cs.append(p)
            
            
        # Get all candidate paths filtered by already visitedLocations
        cs=filter(lambda x: not x.getDestination().getId() in self.visitedLocations, cs)
        
        # We always want the posibility to return to the startLocation
        # then, we have to filter those locations that if we go at there
        # it'll be imposible to return to the startLocation
        def can_return_to_sl(element):
            location_id=element.getDestination().getId()
            floc=self.problem.getLocationById(from_location_id)
            tloc=self.problem.getLocationById(location_id)
       
            slid=self.problem.getStartLocationId()
            # We will always want the posibility to go to sl
            if location_id == slid:
                return True
            
            toLo=self.problem.getPathsFromTo(from_location_id, location_id).getDistance()
            toSl=self.problem.getPathsFromTo(location_id, slid).getDistance()
            
            time_to_lo=max(travel_time, floc.getminW())+floc.getTask()+toLo
            time_to_sl=max(time_to_lo, tloc.getminW())+tloc.getTask()+toSl

            return (time_to_sl < 720)
            
        cs=filter(can_return_to_sl, cs)
        
        # Sort by waiting time. The waiting time is not only from the
        # point of view of the worker, but also from the point of view
        # of the customer.

        cs = sorted(cs, 
                key=lambda x: self.__greedy_value(x, travel_time),
                reverse=False)
        return cs

    def printSolution(self):
        print self.solution.str()
        
    def __greedy_value(self, candidate, travel_time):
        return abs(travel_time+candidate.getDistance()-candidate.getDestination().getminW()+candidate.getSource().getTask())



