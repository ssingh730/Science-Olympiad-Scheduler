class Schedule:
    def __init__ (self):
        self.events = []
        self.members = []

    def __str__(self):
        string = ""
        # string = "P | EV | Competitors\n"
        for event in self.events:
            # string += f"{event.period} | {event.name} | {', '.join(event.competitors)}" + "\n"
            competitorsString = [c.name for c in event.competitors]
            string += f"{event.period} | {event.name} | {', '.join(competitorsString)}" + "\n"
        
        # Sort the competitors by name and grade
        self.members.sort(key=lambda x:x.name, reverse = False)
        self.members.sort(key=lambda x:x.grade, reverse = True)

         # Add the competitor names to the list to display
        string += "Team: "
        for i in range(len(self.members)):
            string += f"{self.members[i].name}"

            # Formatting (not actually important)
            if i < len(self.members) - 1:
                string += "; "

        # Add the fitness to the string
        string += f"\nFitness: {round(self.fitness()/4900*100,4)}"
        return string

    def sort(self):
        self.events.sort(key=lambda x: x.period, reverse = False) # Sort the schedule in period order for display/readability
    
    def fitness(self):
        fitness  = 0
        for event in self.events:
            fitness += event.fitness()

        return fitness
