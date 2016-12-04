# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from Solution import Solution
from Problem import Problem

class Solver_GRASP(object):
    def __init__(self, problem):
        self.problem=problem
        self.visitedLocations=[]
        self.solution=Solution()
        
    def Solve(self, alfa):
        
        while not self.solution.isDone():
            travel_time = self.solution.getTravelTime()
            cset=self.__construct_cs(
                    self.problem.getStartLocation(), 
                    travel_time)
                    
            # Constructing RCL
            qmin=min(cset, key=lambda x: self.__greedy_value(x, travel_time))
            qmax=max(cset, key=lambda x: self.__greedy_value(x, travel_time))
            


    





    def LocalSearch(self, neighborhood, strategy):
        pass

    def getSolution(self):
        return self.solution

    def __construct_cs(self, from_location, travel_time):
        # Get all candidate paths filtered by start location
        paths = self.problem.getPathsFrom(from_location)

        cs = []
        # Get all candidate paths filtered by time
        for p in paths:
            if p.getDestination().getmaxW() <= travel_time:
                cs.append(p)

        # Sort by waiting time. The waiting time is not only from the
        # point of view of the worker, but also from the point of view
        # of the customer.

        cs = sort(cs, 
                key=lambda x: self.__greedy_value(x, travel_time)
                reverse=False)
        return cs

    def __greedy_value(self, candidate, travel_time):
        abs(travel_time+candidate.getDistance()-candidate.getDestination.getminW()),



