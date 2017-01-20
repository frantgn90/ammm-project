#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys
from Problem import Problem
from Solver_GRASP import Solver_GRASP
from Solver_BRKGA import Solver_BRKGA
from Solution import Solution

LS_ALFA=0.3

LS_NB="reassignement" #      exchange
LS_ST="best-improvement" # "first-improvement"

GRASP_ITERATIONS=3

def main(argc, argv):
    def Usage(cmd):
        print("Usage():{0} <GRASP|BRKGA> input.dat".format(cmd))
        print
        exit(1)

    if argc < 3: Usage(" ".join(argv))
    
    heuristic = argv[1]
    if argc == 4:
        LS_ALFA=float(argv[2])
        input_data_file = argv[3]
    else:
        input_data_file = argv[2]

    problem = Problem(input_data_file)
    #problem.print_test()
    
    if heuristic == "GRASP":

        bestQuality = float("inf")
        bestSolution = None
        for i in range(GRASP_ITERATIONS):
            grasp=Solver_GRASP(problem)
            grasp.Solve(0.25)
            if not grasp.isFeasible():
                print("GRASP: Solution not feasible")
                exit(0)
            
            grasp.doLocalSearch(LS_NB, LS_ST)
                
            print "ITERATION {0}: {1}".format(i, grasp.solution.getQuality())
            if grasp.solution.getQuality() < bestQuality:
                bestQuality = grasp.solution.getQuality()
                bestSolution = grasp.solution
                
        print "GRASP DONE"
        print "=========="
        print "Quality: {0}".format(grasp.solution.getQuality())

    elif heuristic == "BRKGA":
        brkga=Solver_BRKGA(problem)
        brkga.Solve()
        if brkga.isFeasible():
            #print brkga.printSolution()
            print "BRKGA DONE"
            print "=========="
            print "Quality: {0}".format(brkga.bestSolution.getQuality())
        else:
            print("BRKGA: Solution not feasible")
            exit(0)
        
    else:
        assert False, "{0} heuristic is not developed".format(heuristic)

    #input_data_file_name = input_data_file.split(".")[:-1]
    #output_data_file = input_data_file_name + ".sol"
    #solution.write(output_data_file)

    return 0


if __name__ == "__main__":
    exit(main(len(sys.argv), sys.argv))
