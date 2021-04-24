# The purpose of this file is to find single prints for a given day
import yfinance as yf
import pandas as pd
import numpy as np
import collections 
# Read in data
es = pd.read_csv("EPM21 - 30 min - RTH.csv")

es = yf.download("ES=F", period = "1d", interval = '30m')[19:]
nq = yf.download("NQ=F", period = "1d", interval = '30m')[19:]
rty = yf.download("RTY=F", period = "1d", interval = '30m')[19:]

# print(es)
# print(data[19:])

# This method will find the single prints for a day in the past if given 
# a dataframe which contains the the periods for 9:30AM - 4:00PM
def findRTHSinglePrints(df, tickSize = 0.25):

    c = collections.Counter()
    
    # For each period
    for i in range(0, 14):
        
        # Get the periods high and low
        periodHigh = df['High'][i]
        periodLow = df['Low'][i] 

        # For each high and low, create a numpy series, with tick size intervals
        periodLocations = np.arange(periodLow, periodHigh + tickSize, tickSize)
        
        periodLocations = np.round(periodLocations, 2)
        
        # Add the period locatiosn to the running counter
        c.update(periodLocations)
    
    # Process the counter
    singlePrints = []
    
    # If any of the keys have a value of 1, they are single prints
    for key in c:
        if c[key] == 1:
            singlePrints.append(key)
    
    # print(sorted(singlePrints))

    listOfLists = []
    currentList = []
    listIdx = 0
    for idx, singlePrint in enumerate(singlePrints):
        
        if idx == 0:
            # print("We have single prints from: " + str(singlePrint), end = ' ')
            currentList.append(singlePrint)
            temp = singlePrint
        elif idx == len(singlePrints) - 1:
            # print("to " + str(singlePrint))
            try:
                listOfLists[listIdx] = currentList
            except IndexError:
                listOfLists.append(currentList)
            
        else:
            if singlePrint > (temp + tickSize):
                # print("to " + str(temp))
                currentList.append(temp)
                # print(currentList)
                try:
                    listOfLists[listIdx] = currentList
                except IndexError:
                    listOfLists.append(currentList)
                listIdx += 1
                currentList = []
                # print("We have single prints from: " + str(singlePrint), end = ' ')
                currentList.append(singlePrint)
       
 
        currentList.append(singlePrint)
        # print(singlePrint)
        temp = singlePrint
     
    if max(c) in singlePrints:
        print("Excess High:     " + str(max(c)), end = ' ')
        
        for idx, singlePrint in enumerate(reversed(singlePrints)):
            
            if (idx == 0):
                temp = singlePrint
            
            if temp > (singlePrint + tickSize):
                print("- " + str(temp) + "\t(" + str(max(c) - temp) + ")")
                break
                
            temp = singlePrint
     
        
    for currList in listOfLists:
        try:
            if (max(c) not in currList and min(c) not in currList):
                print("Single Prints:   " + str(currList[0]) + " - " + str(currList[len(currList) - 1]) + "\t(" + str(currList[len(currList) - 1] - currList[0]) + str(")"))
        except:
            continue
        
        


    if min(c) in singlePrints:
        print("Excess Low:      " + str(min(c)), end = ' ')
        
        for idx, singlePrint in enumerate(singlePrints):
            
            if (idx == 0):
                temp = singlePrint
            
            if singlePrint > (temp + tickSize):
                print("- " + str(temp) + "\t(" + str(temp - min(c)) + str(")"))
                break
                
            temp = singlePrint

    # If our high is in one of the single print distributions, that is an excess high
    
    # If our low is in one of the single print distributions, that is an excess low
    


print("--------------------- ES ----------------------")
print("Parameter            Range               Size")
print("--------------------- -- ----------------------")
findRTHSinglePrints(es)
print("--------------------- NQ ----------------------")

print("Parameter            Range               Size")
print("--------------------- -- ----------------------")
findRTHSinglePrints(nq)
print("--------------------- -- ----------------------")
