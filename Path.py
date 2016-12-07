# -*- coding: utf-8 -*-
# vim:fenc=utf-8

class Path(object):
    def __init__(self, _id, sourceLoc, destLoc, distance):
        self._id = _id
        self.sourceLoc = sourceLoc
        self.destLoc = destLoc
        self.distance = distance

    def getId(self):
        return self._id
        
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


