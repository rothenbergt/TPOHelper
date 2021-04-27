#  findSinglePrints.py
#  ==============
#  Script which will find the single prints for a given day in the past (up to 60 days)

import yfinance as yf
import pandas as pd
import numpy as np
import collections
import datetime
import warnings

# We get a warning because the datetime64 is a deprecated format. 
# I don't feel like recreating for datetime.datetime until a later date.
# The reason it was deprecated had to do with converting timezones which
# we aren't worried about for this script. I will ignore warnings for now.
warnings.filterwarnings("ignore")

# If you want more information to debug the script, you may turn this on
debug = False

# Method which converts a datetime.datetime to a datetime64
def convert_to_datetime64(date):
    return np.datetime64(date)

# Helper method for get_single_prints. Does a lot of the heavy 
# lifting once a dataframe is given. Will find all single prints
# as well as determine excess, weak, and poor highs / lows. 
def get_single_prints_helper(df, start_index,  tick_size = 0.25):

    # Create an empty counter
    c = collections.Counter()

    # For each period
    for i in range(start_index, start_index + 14):

        # Get the periods high and low
        periodHigh = df['High'][i]
        periodLow = df['Low'][i]

        # For each high and low, create a numpy series, with tick size intervals
        periodLocations = np.arange(periodLow, periodHigh + tick_size, tick_size)

        # Add the period locatiosn to the running counter
        c.update(periodLocations)

    # Process the counter
    list_of_single_prints = []

    # If any of the keys have a value of 1, they are single prints
    for key in c:
        if c[key] == 1:
            list_of_single_prints.append(key)

    # If the length is 0, exit
    if len(list_of_single_prints) < 1:
        print("There are no single prints")
        quit()
    
    list_of_lists = []
    current_list = []
    
    # Sort the single prints
    list_of_single_prints = sorted(list_of_single_prints)
    
    if debug: print(list_of_single_prints)
    
    # Prep the previous pointer for the loop
    prev_single_print = list_of_single_prints[0]
    current_list.append(prev_single_print)

    # Go through the all of the single prints
    for idx, single_print in enumerate(list_of_single_prints):
        
        # Skip the first index
        if idx == 0:
            continue
        
        # If the line of single prints are interrupted
        if single_print > (prev_single_print + tick_size):
            
            if (debug): print("A new division was found at " + str(single_print))
            
            # Add the list to a list of lists
            list_of_lists.append(current_list)
            
            # Reset the current list
            current_list = []
            
        if idx == len(list_of_single_prints) - 1:
            
            if (debug): print("The last element found is: " + str(single_print))
            
            # Add the element to the list
            current_list.append(single_print)
            
            # Add the list to a list of lists
            list_of_lists.append(current_list)
            
            # Reset the current list
            current_list = []
            
        # Otherwise, add the single_print to the current list
        current_list.append(single_print)
        
        # Walk the previous pointer 
        prev_single_print = single_print

    high_flag = False
    low_flag = False
    
    if debug: print("The length of the list_of_lists is: " + str(len(list_of_lists)))
    
    for single_print_list in list_of_lists:
        
        if debug: print(single_print_list)
        
        # If the maximum value in the counter is in this list it contains the high
        if max(c) in single_print_list:
            
            # Check if its a weak high (one tick of excess)
            if (len(single_print_list) < 2):
                print("Weak High:\t", end = ' ')
            # Otherwise it is an excess high (two ticks of excess or more)
            else:
                print("Excess High:\t", end = ' ')
                
            # Print the results
            print(single_print_list[0] ,  " - " , single_print_list[-1], end = ' ')
            print("\t(" + str(single_print_list[-1]-single_print_list[0])  + ")")
            
            # Trip the flag
            high_flag = True
            
        # If the minimum value in the counter is in this list it contains the low
        elif min(c) in single_print_list:
            
            # Check if its a weak low (one tick of excess)
            if (len(single_print_list) < 2):
                print("Weak Low:\t", end = ' ')
                
            # Otherwise it is an excess low (two ticks of excess or more)
            else:
                print("Excess Low:\t", end = ' ')            
            
            # Print the results
            print(single_print_list[0] ,  " - " , single_print_list[-1], end = ' ')
            print("\t(" + str(single_print_list[-1]-single_print_list[0])  + ")")    
            
            # Trip the flag
            low_flag = True
            
        # Otherwise, these are single prints
        else:
            # Print the results
            print("Single Prints:\t", end = ' ')
            print(single_print_list[0] ,  " - " , single_print_list[-1], end = ' ')
            print("\t(" + str(single_print_list[-1]-single_print_list[0])  + ")")

    # If we didn't trip the flags, there are no single prints at the highs/lows
    # Therefore, they are poor. 
    if high_flag == False:
        print("Poor High\t" + str(max(c)))
    if low_flag == False:
        print("Poor Low\t" + str(min(c)))
        
# get the single prints for a ticker within the past 60 days
def get_single_prints(ticker, month, day):
    
    try:
        # Get the data from yahoo finance
        df = yf.download(ticker, period = "60d", interval = '30m', progress=False, parse_dates = ['Date'])
        
        # If the dataframe is empty, exit 
        if df.empty:
            print("No data returned from ticker " + str(ticker))
            quit()
            
        # Change the index from datetime 
        df.reset_index(inplace = True)
        
        # Convert the datetime64 north america to datetimen64
        df['Datetime'] = df['Datetime'].apply(convert_to_datetime64)

        # Create the datetime we are referencing
        # I am using 1:30PM as Yahoo finance always uses UTC timezone so I have to account for that
        d1 = np.datetime64(datetime.datetime(2021, month, day, 13, 30, 00))

        # Find the location of this
        start_index = df[df['Datetime'] == d1].index[0]
        
        # Print out the results
        print("----------------------------------------------------")
        print("\t" + ticker + " single prints " + str(month) + "/" + str(day) + "/2021")
        print("----------------------------------------------------")
        print("Parameter\t Range\t\t\tSize")
        print("----------------------------------------------------")
        get_single_prints_helper(df[start_index:], start_index)

    except ConnectionError:
        print("Data for ticker " + str(ticker) + " could not be downloaded...")
        quit()
    except IndexError:
        print("Uh oh! I don't think " + str(month) + "/" + str(day) + " is a trading day")
    except ValueError:
        print("Uh oh! I don't think " + str(month) + "/" + str(day) + " is a trading day")


# Get the single prints for a day within the past 60 days for any ticker
get_single_prints(ticker = "ES=F", month = 4, day = 27)

