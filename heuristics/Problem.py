# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from Location import Location
from Path import Path

class Problem(object):
    def __init__(self, input_data_file):
        # Parsing file
        self.nLocations=self.__parse_n_locations(input_data_file)
        self.startLocation=self.__parse_start_location(input_data_file)

        # -- Raw data
        distances=self.__parse_distances(input_data_file)
        minimWind=self.__parse_minimWind(input_data_file)
        maximWind=self.__parse_maximWind(input_data_file)
        tasks=self.__parse_tasks(input_data_file)

        # Check the correctness of data
        assert self.startLocation > 0 and self.startLocation <= self.nLocations, \
            "1 < startLocation < nLocations, but 1 < {0} < {1}".format(startLocation,nLocations)

        assert len(distances)*len(distances[0])-len(distances) == self.nLocations**2-self.nLocations, \
            "len(distances)=nLocations, but {0}!={1}".format(len(distances), nLocations**2-nLocations)

        assert len(minimWind) == len(maximWind) and len(maximWind) == self.nLocations, \
            "len(windows)=nLocations, but ({0},{1})!={2}".format(len(minimWind), len(maximWind), nLocations)

        assert len(tasks) == self.nLocations, \
            "len(tasks)=nLocations, but {0}!={1}".format(len(tasks), nLocations)

        # The problem is defined by a set of paths. The paths have the information
        # about the locations that connects.

        # Create locations objects
        self.locations=[]
        for i in range(self.nLocations):
            loc=Location(i+1, tasks[i], minimWind[i], maximWind[i])
            
            # It is needed in order to perform the calculation of the
            # arriving time for the locations that sources from startLocation
            if i+1==self.startLocation:
                loc.arrivingTime=0

            self.locations.append(loc)


        # Create path objects
        self.paths=[]
        paths_count=1
        for i in range(self.nLocations):
            for j in range(self.nLocations):
                if i==j: continue
                pa=Path(paths_count,self.locations[i], self.locations[j], 
                    distances[i][j])
                self.paths.append(pa)
                paths_count+=1

    def getPathsFrom(self, from_location):
        result=[]

        for p in self.paths:
            if p.getSource().getId() == from_location:
                result.append(p)
                
        return result

    def getPathsFromTo(self, from_location, to_location):
        assert from_location != to_location, ("Travels from-to the same Location " \
            + "are not allowed ({0})").format(from_location)
        return filter(lambda x: x.getSource().getId()==from_location and \
                                x.getDestination().getId()==to_location, \
                                self.paths)[0]
                                
    def getStartLocationId(self):
        return self.startLocation

    def getnLocations(self):
        return self.nLocations
        
    def getLocations(self):
        return self.locations

    def getPaths(self):
        return self.paths
        
    def getLocationById(self, location_id):
        return filter(lambda x: x.getId()==location_id, self.locations)[0]

    def print_test(self):
        for p in self.paths:
            print p.str()

    def __parse_n_locations(self, input_data_file):
        data = self.__parse_data("nLocations", input_data_file)
        assert type(data) == int, \
            "Error parsing nLocations: {0}".format(type(data))
        return data

    def __parse_start_location(self, input_data_file):
        data = self.__parse_data("startLocation", input_data_file)
        assert type(data) == int, \
            "Error parsing startLocation: {0}".format(type(data))    
        return data

    def __parse_distances(self, input_data_file):
        data = self.__parse_data("distances", input_data_file)
        assert type(data) == list, \
            "error parsing distances: {0}".format(type(data))
        return data

    def __parse_minimWind(self, input_data_file):
        data = self.__parse_data("minW", input_data_file)
        assert type(data) == list, \
            "error parsing minW: {0}".format(type(data))
        return data

    def __parse_maximWind(self, input_data_file):
        data = self.__parse_data("maxW", input_data_file)
        assert type(data) == list, \
            "error parsing maxW: {0}".format(type(data))
        return data

    def __parse_tasks(self, input_data_file):
        data = self.__parse_data("task", input_data_file)
        assert type(data) == list, \
            "error parsing task: {0}".format(type(data))
        return data

    def __parse_data(self, field_name, input_data_file):
        with open(input_data_file) as infile:
            lines=infile.readlines()

            infield=False
            field_data=""
            for l in lines:
                if infield == False and not "=" in l:
                    continue

                elif infield == False and "=" in l:
                    equal_index=l.index("=")
                    fieldName=l[:equal_index]

                    if fieldName == field_name:
                        infield=True
                        field_data=l[equal_index+1:]

                elif infield == True and "=" not in l:
                    field_data+=l

                elif infield == True and "=" in l:
                    break

            field_data=field_data.replace("\n"," ")
            field_data=field_data.replace(";","")
            field_data=field_data.strip()

            return eval(field_data)
