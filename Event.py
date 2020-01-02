# Generic event class
class Event:
    def __init__ (self, name, size, selfSchedule, period, rankings=[], status=0):
        self.name = name
        self.size = size
        self.selfSchedule = selfSchedule
        self.period = period
        self.rankings = rankings
        self.status = 0
        self.competitors = []
        self.sum = 0
    
    def __repr__(self):
        if self.selfSchedule == 1:
            return f"Event{{name: {self.name}, size: {int(self.size)}, period: SELF_SCHEDULE}}, sum: {self.sum}"
        else:
            return f"Event{{name: {self.name}, size: {int(self.size)}, period: {int(self.period)}}}, sum: {self.sum}"

    def fitness(self):
        fitness = 0
        for c in self.competitors:
            fitness += c.getRanking(self.name)

        return fitness

    



