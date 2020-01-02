from random import randint
from operator import attrgetter
import Event

INCREMENT = 3

class Competitor:
    def __init__(self, name):
        self.name = name
        self.events = {}
        self.grade = 0
        self.occupied = []

         # Only used when the probability parameter of bestInEvent() is set to high
        self.weightedEvents = {}

    def __repr__(self):
        string = f"{{ name: {self.name}, grade: {self.grade}, weightedSum: {self.weightedEvents}}}"
        return string

    def getRanking(self, eventName):
        if eventName in self.events:
            return self.events[eventName]
        return 0

    def getWeightedRanking(self, eventName):
        if eventName in self.weightedEvents:
            return self.weightedEvents[eventName]
        return 0

    def getWeightedSum(self):
        return self.weightedSum

    def setRanking(self, eventName, eventRanking):
        self.events[eventName] = eventRanking

    def setWeightedRanking(self, eventName, weightedRanking):
        self.weightedEvents[eventName] = weightedRanking

# This function will find the "best" competitor in a given event. Called by getBestCompetitor()
def bestInEvent(competitors, eventName, excludedSeniors, probability):
    # probability parameter is none, low, or high
    best_ranking = 0
    best_competitor = Competitor("defaultA")

    # Takes the best available competitor in the event every time
    if probability == "off":
        for c in competitors:
            ranking = c.getRanking(eventName)
            if ranking >= best_ranking and c not in excludedSeniors:
                best_ranking = ranking
                best_competitor = c
        return best_competitor

    # Takes the best available competitor if that competitor's ranking is great than a randomly
    # generated value within a specific range
    if probability == "on":
        for c in competitors:
            ranking = c.getRanking(eventName)
            if ranking >= best_ranking and c not in excludedSeniors:
                # A greater INCREMENT value will result in more unique schedules, potentially resulting in a better
                # final schedule but it also takes longer
                value = randint(0, 100 + INCREMENT)
                if ranking > value:
                    best_ranking = ranking
                    best_competitor = c
        return best_competitor

    # # Chooses a competitor at "random" where the each competitors score in an event 
    # # is correlated their probability
    # if probability == "high":
    #     from Main import readEvents
    #     from Main import getSum
    #     from reader import POWER
    #     rand = randint(0, getSum(eventName))

    #     # for c in competitors:
    #     #     ranking = c.getWeightedRanking(eventName)
    #     #     if ranking >= 
    #     return best_competitor


def getBestCompetitor(competitors, eventName, period, seniors, maxGrade, maxQuantity):
    competitor = Competitor("defaultB")
    excludedSeniors = []
    excludedMembers = []

    while True:
        current = bestInEvent(competitors, eventName, excludedSeniors, "on")
        if isValid(current, seniors, period, maxGrade, maxQuantity):
            competitor = current
            break
        else:
            excludedSeniors.append(current)
            excludedMembers.append(current)

    return competitor



def isValid(c, seniors, period, maxGrade, maxQuantity):
    if period not in c.occupied:
        if len(seniors) < maxQuantity:
            return True
        else:
            if c.grade == maxGrade and c.name in seniors:
                return True
            elif c.grade < maxGrade:
                return True
            else:
                return False


