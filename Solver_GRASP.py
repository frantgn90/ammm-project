# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import random

from Solution import Solution
from Problem import Problem

class Solver_GRASP(object):
    def __init__(self, problem):
        self.problem=problem
        self.visitedLocations=[]
        self.solution=Solution(len(problem.getPaths()), 
                               problem.getStartLocation().getId())
        
    def Solve(self, alfa):
        last_location=self.problem.getStartLocation()
        while not self.solution.isDone():
            travel_time = self.solution.getTravelTime()
            cset=self.__construct_cs(
                    last_location, 
                    travel_time)
                    
            # Generating RCL
            qmin=min(cset, key=lambda x: self.__greedy_value(x, travel_time))
            qmax=max(cset, key=lambda x: self.__greedy_value(x, travel_time))
            threshold=qmin + alfa*(qmax-qmin)
            RCL=filter(lambda x: self.__greedy_value(x,travel_time) <= threshold,
                       cset)
            # Pick one randomly
            random_pick=random.randrange(len(RCL))
            candidate=RCL[random_pick]
            
            self.visitedLocations.append(candidate)
            feasible = self.solution.addCandidate(candidate)
            if not feasible:
                break
            last_location=candidate.getDestination()

    def LocalSearch(self, neighborhood, strategy):
        assert False, "TODO: This feature is not done yet."

    def getSolution(self):
        return self.solution
        
    def isFeasible(self):
        return self.solution.isFeasible()

    def __construct_cs(self, from_location, travel_time):
        # Get all candidate paths filtered by start location
        paths = self.problem.getPathsFrom(from_location)

        cs = []
        # Get all candidate paths filtered by time
        for p in paths:
            if p.getDestination().getmaxW() <= travel_time:
                cs.append(p)
                
        # Get all candidate paths filtered by already visitedLocations
        filter(lambda x: not x.getId() in self.visitedLocations, cs)

        # Sort by waiting time. The waiting time is not only from the
        # point of view of the worker, but also from the point of view
        # of the customer.

        cs = sort(cs, 
                key=lambda x: self.__greedy_value(x, travel_time),
                reverse=False)
        return cs

    def printSolution(self):
        print self.solution.str()
        
    def __greedy_value(self, candidate, travel_time):
        abs(travel_time+candidate.getDistance()-candidate.getDestination.getminW()),



