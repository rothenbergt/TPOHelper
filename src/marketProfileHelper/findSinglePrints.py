# The purpose of this file is to find single prints for a given day
import yfinance as yf
import pandas as pd
import numpy as np
import collections
import datetime

def convert_to_datetime64(date):
    return np.datetime64(date)

def convert_to_datetime(date):
    return datetime.datetime(date)

def getDataFrame(ticker):
    
    try:
        df = yf.download(ticker, period = "2d", interval = '30m', parse_dates = ['Date'])
        
        # If the dataframe is empty, exit 
        if df.empty:
            print("No data returned from ticker " + str(ticker))
            quit()
            
        # Change the index from datetime 
        df.reset_index(inplace = True)
        
        # Convert the datetime64 north america to datetimen64
        df['Datetime'] = df['Datetime'].apply(convert_to_datetime64)

        start_index = getDataFrameIndex(df, month = 4, day = 27)
        
        findRTHSinglePrints(df[start_index:])
    except ConnectionError:
        print("Data for ticker " + str(ticker) + " could not be downloaded...")
        quit()


def getDataFrameIndex(df, day, month):
    
    # Create the datetime we are referencing
    d1 = np.datetime64(datetime.datetime(2021, month, day, 9, 30, 00))

    # Find the location of this
    start_index = df[df['Datetime'] == d1].index[0]
   
    return start_index

getDataFrame("ES=F")

quit()
# Read in data using Yahoo Finance API. Get rid of ETH data
es = yf.download("ES=F", period = "2d", interval = '30m', parse_dates = ['Date'])
nq = yf.download("NQ=F", period = "2d", interval = '30m')[19:-3]

# Change the index from datetime 
es.reset_index(inplace = True)

print(es.dtypes)


def convert_to_datetime64(date):
    return np.datetime64(date)

def convert_to_datetime(date):
    return datetime.datetime(date)



# TODO do I want to keep this in datetime64, or should i convert everything to datetime?
es['Datetime'] = es['Datetime'].apply(convert_to_datetime64)


# Create the datetime we are referencing
d1 = np.datetime64(datetime.datetime(2021, 4, 27, 9, 30, 00))

# Find the location of this
start_index = es[es['Datetime'] == d1].index[0]

# print(es.dtypes)
# quit()?
# print(nq)

# This method will find the single prints for a day in the past if given
# a dataframe which contains the the periods for 9:30AM - 4:00PM
def findRTHSinglePrints(df, tickSize = 0.25):

    print(df)

    # Create an empty counter
    c = collections.Counter()

    # For each period
    for i in range(start_index, start_index + 14):

        # Get the periods high and low
        periodHigh = df['High'][i]
        periodLow = df['Low'][i]

        # For each high and low, create a numpy series, with tick size intervals
        periodLocations = np.arange(periodLow, periodHigh + tickSize, tickSize)

        # Add the period locatiosn to the running counter
        c.update(periodLocations)

    # Process the counter
    singlePrints = []

    # If any of the keys have a value of 1, they are single prints
    for key in c:
        if c[key] == 1:
            singlePrints.append(key)


    print("The single prints are: ")
    print(singlePrints)

    listOfLists = []
    currentList = []
    listIdx = 0
    temp = 0

    for idx, singlePrint in enumerate(singlePrints):

        print("We are looking at single print value " + str(singlePrint) + " with temp value " + str(temp))

        if idx == 0:
            print("Starting a new list")
            currentList.append(singlePrint)
            temp = singlePrint

        elif idx == len(singlePrints) - 1:

            try:
                listOfLists[listIdx] = currentList
            except IndexError:
                listOfLists.append(currentList)

        else:
            if singlePrint < (temp + tickSize):
                print("We have reached a  division")
                currentList.append(temp)
                try:
                    listOfLists[listIdx] = currentList
                except IndexError:
                    listOfLists.append(currentList)
                listIdx += 1
                currentList = []
                currentList.append(singlePrint)

        currentList.append(singlePrint)
        temp = singlePrint

    for single_print_list in listOfLists:
        print(single_print_list)

    quit()

    # TODO rewrite these loops with more thought out logic
    
    # if max(c) in singlePrints:
    #     print("Excess High:     " + str(max(c)), end = ' ')

    #     for idx, singlePrint in enumerate(reversed(singlePrints)):

    #         if (idx == 0):
    #             temp = singlePrint

    #         if temp > (singlePrint + tickSize):
    #             print("- " + str(temp) + "\t(" + str(max(c) - temp) + ")")
    #             break

    #         temp = singlePrint


    # for currList in reversed(listOfLists):
    #     try:
    #         if (max(c) not in currList and min(c) not in currList):
    #             print("Single Prints:   " + str(currList[len(currList) - 1]) + " - " + str(currList[0]) + "\t(" + str(currList[len(currList) - 1] - currList[0]) + str(")"))
    #     except:
    #         continue




    # if min(c) in singlePrints:
    #     # print("Excess Low:      " + str(min(c)), end = ' ')

    #     for idx, singlePrint in enumerate(singlePrints):

    #         if (idx == 0):
    #             temp = singlePrint

    #         if singlePrint > (temp + tickSize):
    #             print("Excess Low:      " + str(temp) + " - " + str(min(c)) + "\t(" + str(temp - min(c)) + str(")"))
    #             break

    #         temp = singlePrint

    # If our high is in one of the single print distributions, that is an excess high

    # If our low is in one of the single print distributions, that is an excess low


print("\n")
print("--------------------- ES ----------------------")
print("Parameter            Range               Size")
print("-----------------------------------------------")
findRTHSinglePrints(es[start_index:])
# print("")
# print("--------------------- NQ ----------------------")

# print("Parameter            Range               Size")
# print("-----------------------------------------------")
# findRTHSinglePrints(nq)
# print("-----------------------------------------------")
# print("\n")
