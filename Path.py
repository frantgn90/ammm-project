# -*- coding: utf-8 -*-
# vim:fenc=utf-8

class Path(object):
    def __init__(self, sourceLoc, destLoc, distance):
        self.sourceLoc = sourceLoc
        self.destLoc = destLoc
        self.distance = distance

    def getSource(self):
        return self.sourceLoc

    def getDestination(self):
        return self.destLoc

    def getDistance(self):
        return self.distance

    def str(self):
        text="From {0} to {1} are {2} min."\
                .format(self.sourceLoc.getId(),
                        self.destLoc.getId(),
                        self.distance)

        return text


