import ast
import json

def exportTestOptions(l):
    with open("Data\\testOptionsList.json", "w") as file:
        json.dump(l, file, indent=2)

def importTestOptions():
    with open("Data\\testOptionsList.json", "r") as file:
        return ast.literal_eval(file.read().replace("null","None"))
    
def exportLockOutput(l):
    with open('ReactApp\\optiondealsfinder\\src\\data\\lockOutput.json', "w") as file:
        json.dump(l, file, indent=2)