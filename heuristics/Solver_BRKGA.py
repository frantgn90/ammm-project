'''
AMMM Lab Heuristics v1.1
BRKGA solver.
Copyright 2016 Luis Velasco and Lluis Gifre.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import random, time
from Solution import Solution
from Problem import Problem

# Configuration 

config_pElites = 0.25
config_pMutants = 0.15
config_numIndividuals = 1024
config_maxExecTime = 0.5
config_pInheritanceElite = 0.5

# Some pre-calculations
numGenes = 0
numElites = int(round(config_pElites * config_numIndividuals))
numMutants = int(round(config_pMutants * config_numIndividuals))
numCrossOvers = config_numIndividuals - numElites - numMutants

class BRKGA_Individual(object):
    def __init__(self, solution, chromosome, fitness):
        self.chromosome = chromosome
        self.fitness = fitness
        self.solution = solution
    
    @classmethod
    def initGreedy(cls, problem):
        solution = Solution(problem.getnLocations(), problem.getStartLocationId())
        visitedLocations=[]
        
        last_location=problem.getStartLocationId()
        while not solution.isDone():
            travel_time = solution.getTravelTime()
            cset=cls.__construct_cs(
                    last_location, 
                    travel_time, visitedLocations, problem)
            
            assert len(cset) > 0, ("BRKGA [initGreedy]: No more candidates but " \
                "solution is not done.")
            
            candidate=sorted(cset, key=lambda x: cls.__greedy_value(x, travel_time), 
                        reverse=False)[0]

            # Add candidate to solution
            solution.addCandidate(candidate)
            
            # We always can return to the startLocation (+1 vehicle)
            if candidate.getDestination().getId() != problem.getStartLocationId():
                visitedLocations.append(candidate.getDestination().getId())
            
            last_location=candidate.getDestination().getId()
            
        # Now is mandatory to add to solution the last path in order to return
        # to the startLocation
        from_location=candidate.getDestination().getId()
        to_location=problem.getStartLocationId()
        
        last_path=problem.getPathsFromTo(from_location, to_location)
        solution.addCandidate(last_path)
        
        chromosome = solution.encodeToBRKGA()
        
        # instantiate the new Individual with chromosome and an undefined fitness
        return(cls(solution, chromosome, solution.getQuality()))
    
    @classmethod
    def initMutant(cls, problem):
        numGenes = problem.getnLocations()
        
        # generate a chromosome (vector of floats)
        # fill it with random values [0.0 .. 1.0]
        chromosome = []
        for numGene in xrange(0, numGenes):
            chromosome.append(random.uniform(0, 1))
            
        solution = Solution(problem.getnLocations(), problem.getStartLocationId())
        solution.fromChromosome(chromosome, problem)
        
        return(cls(solution, chromosome, solution.getQuality()))
    
    @classmethod
    def initCrossOver(cls, elite, nonElite, problem):
        numGenes = problem.getnLocations()
        pInheritanceElite = config_pInheritanceElite
        
        # chromosomes from parents (elite and non-elite) must have the same size to be crossed
        if(len(elite.chromosome) != len(nonElite.chromosome)):
            raise Exception('Unable to cross-over individuals with different chromosome size')
        
        # generate a chromosome (vector of floats)
        # initialize the chromosome by crossing over the parents
        chromosome = []
        for numGene in xrange(0, numGenes):
            # pick genes from parents
            eliteGen = elite.chromosome[numGene]
            nonEliteGen = nonElite.chromosome[numGene]
            
            # pick the gene from elite or non-elite
            # pInheritanceElite: probability of picking the gene from the elite parent
            pInheritance = random.uniform(0.0, 1.0);
            if(pInheritance < pInheritanceElite):
                gene = eliteGen
            else:
                gene = nonEliteGen
            chromosome.append(gene)
            
        solution = Solution(problem.getnLocations(), problem.getStartLocationId())
        solution.fromChromosome(chromosome, problem)
            
        return(cls(solution, chromosome, solution.getQuality()))
      
    ######################################
    ## Some problem-dependant functions ##
    ######################################
    
    @classmethod
    def __construct_cs(cls, from_location_id, travel_time, visitedLocations, problem):
        # Get all candidate paths filtered by start location
        paths = problem.getPathsFrom(from_location_id)
        
        cs = []
        # Get all candidate paths filtered by time
        for p in paths:
            if p.getDestination().getmaxW() >= travel_time:
                cs.append(p)
            
            
        # Get all candidate paths filtered by already visitedLocations
        cs=filter(lambda x: not x.getDestination().getId() in visitedLocations, cs)
        
        # We always want the posibility to return to the startLocation
        # then, we have to filter those locations that if we go at there
        # it'll be imposible to return to the startLocation
        def can_return_to_sl(element):
            location_id=element.getDestination().getId()
            floc=problem.getLocationById(from_location_id)
            tloc=problem.getLocationById(location_id)
       
            slid=problem.getStartLocationId()
            # We will always want the posibility to go to sl
            if location_id == slid:
                return True
            
            toLo=problem.getPathsFromTo(from_location_id, location_id).getDistance()
            toSl=problem.getPathsFromTo(location_id, slid).getDistance()
            
            time_to_lo=max(travel_time, floc.getminW())+floc.getTask()+toLo
            time_to_sl=max(time_to_lo, tloc.getminW())+tloc.getTask()+toSl

            return (time_to_sl < 720)
            
        cs=filter(can_return_to_sl, cs)
        
        # Sort by waiting time. The waiting time is not only from the
        # point of view of the worker, but also from the point of view
        # of the customer.

        cs = sorted(cs, 
                key=lambda x: cls.__greedy_value(x, travel_time),
                reverse=False)
        return cs
        
    @classmethod
    def __greedy_value(self, candidate, travel_time):
        return abs(travel_time+candidate.getDistance()-candidate.getDestination()\
            .getminW()+candidate.getSource().getTask())

# An abstract BRKGA decoder
class BRKGA_Decoder(object):
    def __init__(self):
        raise Exception('Abstract method cannot be called')
    
    def getNumGenes(self):
        raise Exception('Abstract method cannot be called')
    
    def decode(self, individual):
        raise Exception('Abstract method cannot be called')

# Inherits from a parent abstract solver.
class Solver_BRKGA(object):
    def __init__(self, problem):
        self.problem = problem
        numGenes = self.problem.getnLocations()
        
        assert numElites > 0
        assert numMutants > 0
        assert numCrossOvers > 0
        
    def initializeIndividuals(self):
        # create a population with numIndividuals individuals created at random
        population = []
        
        individual = BRKGA_Individual.initGreedy(self.problem)
        population.append(individual)
        
        for numIndividual in xrange(1, config_numIndividuals):
            individual = BRKGA_Individual.initMutant(self.problem)
            population.append(individual)
        return(population)
    
    def decodeIndividuals(self, population, decoder):
        # decode individuals not already decoded, i.e. with undefined fitness, with a specific decoder
        it_decodedIndividuals = 0
        startTime = time.time()
        
        for individual in population:
            if(individual.fitness is not None): continue
            decoder.decode(individual)
            it_decodedIndividuals += 1
        
        it_elapsedDecodingTime = time.time() - startTime
        return(it_elapsedDecodingTime, it_decodedIndividuals)
    
    def sortIndividuals(self, population):
        # sort individuals in a population by their fitness in ascending order
        population.sort(key=lambda individual: individual.fitness)
    
    def evolveIndividuals(self, population):
        # get elites and non-elites from current population
        elites = population[0:numElites]            # elites: sublist from 0 to (numElites-1)
        nonElites = population[numElites:]          # nonElites: sublist from numElites to the end

        newPopulation = []
        
        # direct copy the numElites elite individuals to the new population
        newPopulation[0:numElites] = elites
        
        # create numCrossOvers individuals by crossing randomly selected parents
        for numCrossOver in xrange(0, numCrossOvers):
            elite = random.choice(elites)           # pick an elite individual at random
            nonElite = random.choice(nonElites)     # pick a non-elite individual at random
            
            # crossover them parents (elite and non-elite) to produce a new individual
            # pick each gene from elite or non-elite with a specific inheritance probability 
            individual = BRKGA_Individual.initCrossOver(elite, nonElite, self.problem)
            newPopulation.append(individual)
        
        # create numMutants individuals are created at random
        for numMutant in xrange(0, numMutants):
            individual = BRKGA_Individual.initMutant(self.problem)
            newPopulation.append(individual)
        
        return(newPopulation)
    
    def Solve(self):
        bestSolution = self.solution=Solution(self.problem.getnLocations(), self.problem.getStartLocationId())
        population = self.initializeIndividuals()
        
        generation = 0
        startTime = time.time()
        bestHighestLoad = float("inf")
        
        while(time.time() - startTime < config_maxExecTime):
            generation += 1
            
            # decode the individuals using the decoder
            # NOTE: They are already decoded
            # it_elapsedDecodingTime, it_decodedIndividuals = self.decodeIndividuals(population, decoder)
            
            # sort them by their fitness
            self.sortIndividuals(population)
            
            # update statistics
            bestIndividual = population[0]
            newBestHighestLoad = bestIndividual.fitness
            if(newBestHighestLoad < bestHighestLoad):
                self.bestSolution = bestIndividual.solution
                bestHighestLoad = newBestHighestLoad
            
            # evolve the population
            population = self.evolveIndividuals(population)
        
        return(bestSolution)
        
    def isFeasible(self):
        return self.bestSolution.isFeasible()
        
    def printSolution(self):
        print self.bestSolution.str()
