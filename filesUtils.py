import ast
import json

def exportTestOptions(l):
    with open("Data\\testOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def importTestOptions():
    with open("Data\\testOptionsList.json", "r") as file:
        return ast.literal_eval(file.read().replace("null","None"))
    
def importTestPrices():
    with open("Data\\testPrices.json", "r") as file:
        return ast.literal_eval(file.read().replace("null","None"))
    
def importMockList():
    with open("Data\\mockList.json", "r") as file:
        return ast.literal_eval(file.read().replace("null","None"))

def importCurrent():
    with open("Data\\currentOptionsList.json", "r") as file:
        return ast.literal_eval(file.read())
    
def importWeeklyCurrent():
    with open("Data\\weeklyCurrentOptionsList.json", "r") as file:
        return ast.literal_eval(file.read())
    
def importWeeklyCurrentForTHL():
    with open("Data\\weeklyCurrentOptionsList.json", "r") as file:
        return ast.literal_eval(file.read())

def importPrices():
    with open("Data\\testPrices.json", "r") as file:
        return ast.literal_eval(file.read().replace("null","None"))

def importFiltered():
    with open("Data\\filteredOptionsList.json", "r") as file:
        return ast.literal_eval(file.read())

def importWeeklyFiltered():
    with open("Data\\weeklyFilteredOptionsList.json", "r") as file:
        return ast.literal_eval(file.read())

def exportCurrentOptionsList(l):
    with open("Data\\currentOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def exportWeeklyCurrentOptionsList(l):
    with open("Data\\weeklyCurrentOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def exportWeeklyCurrentOptionsListForTHL(l):
    with open("Data\\weeklyCurrentOptionsListForTHL.json", "w") as file:
        json.dump(l, file, indent=2)

def exportFilteredOptions(l):
    with open("Data\\filteredOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def exportWeeklyFilteredOptions(l):
    with open("Data\\weeklyFilteredOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def exportWeeklyFilteredOptionsForTHL(l):
    with open("Data\\weeklyFilteredOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def exportTestPrices(l):
    with open("Data\\testPrices.json", "w") as file:
        json.dump(l, file, indent=1)

def exportLockOutput(l):
    with open('ReactApp\\optiondealsfinder\\src\\data\\lockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

def exportWeeklyLockOutput(l):
    with open('Data\\weeklyLockOutput.json', "w") as file:
        json.dump(l, file, indent=2)