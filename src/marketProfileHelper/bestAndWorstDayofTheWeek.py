import pandas as pd
import yfinance as yf
from datetime import datetime
import collections 
import matplotlib.pyplot as plt
import numpy as np
def day_of_week(date):
    return date.strftime("%W %A")

es = yf.download("SPY", period = "100y", interval = '1d', parse_dates = ['Date'])

es.reset_index(inplace = True)

es['Date'] = es['Date'].apply(day_of_week)

currMax = 0
day = ""

my_dict = {
  "Monday": 0,
  "Tuesday": 0,
  "Wednesday": 0,
  "Thursday": 0,
  "Friday": 0,
}

min_dict = {
  "Monday": 0,
  "Tuesday": 0,
  "Wednesday": 0,
  "Thursday": 0,
  "Friday": 0,
}

def addToDictionary(day, dictionary):
    
    if day in dictionary:
        dictionary[day] += 1
    else:
        dictionary[day] = 1

prevWeekNumber = 17
currWeekNumber = 17
currMax = 0
currMin = 9999
minDay = ""
maxDay = ""

for index, row in es.iterrows():
    
    week_number, week_day = str.split(row['Date'])
    
    # print(week_number)
    
    currWeekNumber = week_number
    
    # print("Current week number is " + str(currWeekNumber) + " previous week number is " + str(prevWeekNumber))
    
    if currWeekNumber != prevWeekNumber:
        # print("We are on a new week...")
        if (maxDay != ""):
            addToDictionary(maxDay, my_dict)
            currMax = 0


        if (minDay != ""):
            addToDictionary(minDay, min_dict)
            currMin = 9999

    if (row['High'] > currMax):
        currMax = row['High']
        maxDay = week_day
    
    if (row['Low'] < currMin):
        currMin = row['Low']
        minDay = week_day

    prevWeekNumber = week_number
    
print(my_dict)
print(min_dict)

names, counts = zip(*my_dict.items())
x = np.arange(len(names))
plt.bar(x - 0.1, counts, color='g', width = 0.2)

names, counts = zip(*min_dict.items())
x = np.arange(len(names))
plt.bar(x + 0.1, counts, color='r', width = 0.2)

# plt.bar(range(len(min_dict)), min_dict.values(), color='r')
# plt.show()
plt.xticks(x, list(my_dict.keys()))
plt.show()
