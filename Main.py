# CENTERVILLE SCIENCE OLYMPIAD SCHEDULE OPTIMIZER
# Peter Hall 2019

# Import necessary libraries
import math
import random
import time
import copy
import os

from Event import Event
from Schedule import Schedule
import Competitor
import reader
import colorama
from progress import ProgressBar
from progress import progress

# DEFINITIONS
path = os.path.abspath("Data.xlsx")

readEvents = reader.readEvents(path) # Read the list of events from the datasheet
competitorList = reader.populateCompetitors(path) # Get the competitors from the datasheet
GENERATIONS = 0
MAX_GRADE = 12
MAX_QUANTITY = 7
DEBUG = False


# FUNCTIONS
def timer(message):
    print(f"{message} {round(time.process_time() - start_time, 5)}s")

def getSum(eventName):
    for i in range(len(readEvents)):
        if eventName == readEvents[i].name:
            return readEvents[i].sum
    return 0

def setup():
    global GENERATIONS
    GENERATIONS = int(input("How many schedules do you want to compare? "))

def generate(eventData, competitors, debug):
    activeSchedule = Schedule() # Create object for initial schedule. Probably add something to store all these objects externally later
    activeSchedule.events = copy.deepcopy(eventData) # Create a local instance of eventData[] 

    seniors = []
    team = []

    # Assign periods randomly for self-schedule eventData
    for obj in activeSchedule.events:
        if (obj.selfSchedule == True):
            obj.period = random.randint(1,6)
    
    # Loop through all the possible competitor slots in an event.
    for phase in range(3):
        # Shuffle the event lsit so that there is no bias as to when the event is
        random.shuffle(activeSchedule.events)
        # Loop through each event in the current schedule
        for event in activeSchedule.events:
            # If the event isn't filled yet
            if len(event.competitors) < event.size:
                # If we can still add people to the team, get the best competitor out of everyone
                if len(team) < 15:
                    competitor = Competitor.getBestCompetitor(competitors, event.name, event.period, seniors, MAX_GRADE, MAX_QUANTITY)
                # If we're full, get the best competitor out of the people on the team already
                else: 
                    competitor = Competitor.getBestCompetitor(team, event.name, event.period, seniors, MAX_GRADE, MAX_QUANTITY)
                # Now that the competitor has been added to this time slot, they are occupied
                competitor.occupied.append(event.period)
                # Add the competitor to the list of poeple competing in the event
                event.competitors.append(competitor)

                # Add the competitor to the list of seniors if they are a senior and aren't already there
                if competitor.grade == MAX_GRADE and competitor.name not in seniors:
                    seniors.append(competitor.name)
                # Add the competitor to the competing team roster if they aren't already there
                if competitor not in team:
                    team.append(competitor)
    
    # Reset the occupied status of the competitors for the next schedule
    for c in competitors:
        c.occupied = []

    activeSchedule.members = team
    return activeSchedule

# Function calls
# MAIN PROCESS
if __name__ == "__main__":
    # Call the function to set appropiate variables values for the specified division
    setup()

    #Mark the starting time for performance tracking
    start_time = time.process_time()
    #Create a list to hold all of the schedules
    allSchedules = []

    #Create a schedule that will hold the best one
    best_schedule = Schedule()
    best_fitness = 0

    #Generate a schedule for each generation
    for i in range(GENERATIONS):
        activeSchedule = generate(readEvents, competitorList, False)
        current_fitness = activeSchedule.fitness()
        if current_fitness > best_fitness:
            best_schedule = activeSchedule
            best_fitness = current_fitness
            if DEBUG:
                print(f"New highest fitness: {best_fitness}")
                print(f"   time: {round(time.process_time(), 4)}")
                print(f"   iteration: {i}/{GENERATIONS}")


        p = (i/GENERATIONS)
        progress(i, GENERATIONS, "optimizing teams")

    best_schedule.sort()
    print(" ")
    print("P | EV | Competitors")
    print(best_schedule)
    print(f"Generations: {GENERATIONS}")
    timer("Elapsed time:")