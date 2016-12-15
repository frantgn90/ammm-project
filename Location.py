# -*- coding: utf-8 -*-
# vim:fenc=utf-8

class Location(object):
    def __init__(self, _id, task, minW, maxW):
        self._id=_id
        self.task=task
        self.minW=minW
        self.maxW=maxW
        self.arrivingTime=None

    def getTask(self):
        return self.task

    def getminW(self):
        return self.minW

    def getmaxW(self):
        return self.maxW

    def getId(self):
        return self._id
        
    def getarrivingTime(self):
        return self.arrivingTime
       
    def getWaitingTime(self):
        assert self.arrivingTime != None, ("Location {0} error: Arriving time " \
            + "must be set before get the waiting time.").format(self._id)
        return max(0, self.minW-self.arrivingTime)

