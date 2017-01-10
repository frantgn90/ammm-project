#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys
from Problem import Problem
from Solver_GRASP import Solver_GRASP
from Solver_BRKGA import Solver_BRKGA
from Solution import Solution

LS_NB="reassignement" # "exchange" 
LS_ST="best-improvement" # "first-improvement"
LS_ALFA=0.3

def main(argc, argv):
    def Usage(cmd):
        print("Usage():{0} <GRASP|BRKGA> input.dat".format(cmd))
        print
        exit(1)

    if argc < 3: Usage(" ".join(argv))

    heuristic = argv[1]
    input_data_file = argv[2]

    problem = Problem(input_data_file)
    #problem.print_test()
    
    if heuristic == "GRASP":
        grasp=Solver_GRASP(problem)
        grasp.Solve(LS_ALFA)
        if grasp.isFeasible():
            grasp.doLocalSearch(LS_NB, LS_ST)
            print grasp.printSolution()
        else:
            print("GRASP: Solution not feasible")
            exit(0)

    elif heuristic == "BRKGA":
        brkga=Solver_BRKGA(problem)
        brkga.Solve()
        if brkga.isFeasible():
            print brkga.printSolution()
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
