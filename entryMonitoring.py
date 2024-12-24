import optionCodes
import dataProcess

options = optionCodes.importWeeklyFiltered()


dividedOptions = dataProcess.divideOptionTypes(input_data[1:])
calls, puts, nextCalls, nextPuts = dividedOptions['calls'], dividedOptions['puts'], dividedOptions['nextCalls'], dividedOptions['nextPuts']
    

def analyzeUpdate(symbol, buyPrice, sellPrice):
    print