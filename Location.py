# -*- coding: utf-8 -*-
# vim:fenc=utf-8

class Location(object):
    def __init__(self, _id, task, minW, maxW):
        self._id=_id
        self.task=task
        self.minW=minW
        self.maxW=maxW

    def getTask(self):
        return self.task

    def getminW(self):
        return self.minW

    def getmaxW(self):
        return self.maxW

    def getId(self):
        return self._id

