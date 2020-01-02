import xlrd
from xlrd import open_workbook, cellname
from Event import Event
from Competitor import Competitor

POWER = 3

def readEvents(path):
    generalEvents = []
    # Read Excel datasets - https://www.geeksforgeeks.org/reading-excel-file-using-python/
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    rankingsSheet = wb.sheet_by_index(1)

    # Create event elements
    for rows in range(1, sheet.nrows):
        eventRankings = []
        weightedRankings = []
        for columns in range(3, rankingsSheet.ncols):
            eventRankings.append(round(rankingsSheet.cell_value(rows, columns)))
            weightedRankings.append(round(rankingsSheet.cell_value(rows, columns))**POWER)
        generalEvents.append(Event(sheet.cell_value(rows, 0), sheet.cell_value(rows, 1), sheet.cell_value(rows, 2), int(sheet.cell_value(rows, 3)), eventRankings))
        generalEvents[rows - 1].sum = sum(weightedRankings)
    return generalEvents
 
def readTeamMembers(path):
    team = []
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(1)

    for i in range(3, sheet.ncols):
        team.append(sheet.cell_value(0, i))

    return team

def populateCompetitors(path):
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(1)
    grades =  wb.sheet_by_index(3)
    eventAbbreviations = []
    competitorList = []

    for row in range(1, sheet.nrows):
        eventAbbreviations.append(sheet.cell_value(row, 0))

    for column in range(3, sheet.ncols):
        activeCompetitor = Competitor(sheet.cell_value(0, column))
        activeCompetitor.grade = int(grades.cell_value(1, column - 3))
        weightedRanking = 0
        for row in range(1, sheet.nrows - 1):
            eventName = eventAbbreviations[row - 1]
            eventRanking = sheet.cell_value(row, column)
            weightedRanking = eventRanking**POWER + weightedRanking
            activeCompetitor.setRanking(eventName, eventRanking)
            activeCompetitor.setWeightedRanking(eventName, weightedRanking)
        competitorList.append(activeCompetitor)
        
    return competitorList