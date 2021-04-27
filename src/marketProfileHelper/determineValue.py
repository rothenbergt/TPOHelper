# A file which can determine the value areas for a given TPO\
    
import pandas
import datetime
import matplotlib.pyplot as plt
import time
import numpy
import operator
import functools
from itertools import chain

# Read in data
es = pandas.read_csv("EPM21 - 30 min - RTH.csv")

# Create 30 minute periods from data

print(es)
# es = es.dropna()
# Using data, calculate value areas and POC

times = es['T']
# The times are exported as yyyyMMdd HHmmss

# print([es['T'].str.contains("20210416")])

def convertTime(times):
    return datetime.datetime.strptime(times, '%Y%m%d %H%M%S')


def createVolumeProfile(df):
    price = df[df.columns[1]]
    volume = df[df.columns[4]]
    
    my_dict = {}

    for idx, p in enumerate(price):
        if p in my_dict:
            my_dict[p] += volume[idx]
        else:
            my_dict[p] = volume[idx]

    # Turn into a list as the keys and values are dictionary objects
    plt.barh(list(my_dict.keys()), list(my_dict.values()), color='g')
    plt.show()

def createTPO(df):
    

    # For each 30 minutes, keep track of where price has been
    
    # Can breakup data and multithread

    # Name, Series
    
    A = pandas.Series()
    # B = pandas.Series()
    # C = pandas.Series()

    df['T'] = df['T'].apply(lambda x: convertTime(x))
    

    periodastart = datetime.datetime.strptime('20210416 9300', '%Y%m%d %H%M%S')
    periodaend = datetime.datetime.strptime('20210416 10000', '%Y%m%d %H%M%S')
    periodbend = datetime.datetime.strptime('20210416 10300', '%Y%m%d %H%M%S')
    periodcend = datetime.datetime.strptime('20210416 11000', '%Y%m%d %H%M%S')
    perioddend = datetime.datetime.strptime('20210416 11300', '%Y%m%d %H%M%S')
    periodeend = datetime.datetime.strptime('20210416 12000', '%Y%m%d %H%M%S')
    periodfend = datetime.datetime.strptime('20210416 12300', '%Y%m%d %H%M%S')
    periodgend = datetime.datetime.strptime('20210416 13000', '%Y%m%d %H%M%S')
    periodhend = datetime.datetime.strptime('20210416 13300', '%Y%m%d %H%M%S')
    periodiend = datetime.datetime.strptime('20210416 14000', '%Y%m%d %H%M%S')
    periodjend = datetime.datetime.strptime('20210416 14300', '%Y%m%d %H%M%S')
    periodkend = datetime.datetime.strptime('20210416 15000', '%Y%m%d %H%M%S')
    periodlend = datetime.datetime.strptime('20210416 15300', '%Y%m%d %H%M%S')
    periodmend = datetime.datetime.strptime('20210416 16000', '%Y%m%d %H%M%S')

    startIndex = int(df.index[df['T'] == periodastart].tolist()[0])

    indexes = []
    indexes.append(int(df.index[df['T'] == periodastart].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodaend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodbend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodcend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == perioddend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodeend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodfend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodgend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodhend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodiend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodjend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodkend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodlend].tolist()[0]))
    indexes.append(int(df.index[df['T'] == periodmend].tolist()[0]))

    print(indexes)

    print("Period A Start: " + str(df.index[df['T'] == periodastart].tolist()[0]))
    print("Period A End: " + str(df.index[df['T'] == periodaend].tolist()[0]))
    print("Period B End: " + str(df.index[df['T'] == periodbend].tolist()[0]))
    print("Period C End: " + str(df.index[df['T'] == periodcend].tolist()[0]))
    print("Period D End: " + str(df.index[df['T'] == perioddend].tolist()[0]))
    print("Period E End: " + str(df.index[df['T'] == periodeend].tolist()[0]))
    print("Period F End: " + str(df.index[df['T'] == periodfend].tolist()[0]))
    print("Period G End: " + str(df.index[df['T'] == periodgend].tolist()[0]))
    print("Period H End: " + str(df.index[df['T'] == periodhend].tolist()[0]))
    print("Period I End: " + str(df.index[df['T'] == periodiend].tolist()[0]))
    print("Period J End: " + str(df.index[df['T'] == periodjend].tolist()[0]))
    print("Period K End: " + str(df.index[df['T'] == periodkend].tolist()[0]))
    print("Period L End: " + str(df.index[df['T'] == periodlend].tolist()[0]))
    print("Period M End: " + str(df.index[df['T'] == periodmend].tolist()[0]))
    
    singlePrints = set()
    listOfSets = []
    listOfNumpy = []
    
    for i in range(0, len(indexes) - 1):
        start = i-1
        stop = i
        tempSet = set()
        
        # Get the High and Low for each
        high = float(df.loc[i+1][df.columns[2]])
        low = float(df.loc[i][df.columns[3]])
        print("Period " + chr((i % 14) + 97))
        print("High = " + str(high) + " Low = " + str(low))
        print(numpy.arange(low, high, 0.25))
        listOfNumpy.append(numpy.arange(low, high, 0.25))
        listOfSets.append(set(numpy.arange(low, high, 0.25)))

        
    # print(listOfNumpy)
    
    print("A")
    print(listOfSets[0])
    print("B")
    print(listOfSets[1])
    
    print("Single Prints")
    
    tempSet=set()
    
    for i in range(0, len(listOfSets)):
        tempSet = tempSet ^ listOfSets[i]
    
    print(sorted(tempSet))

    quit()
    
    print(singlePrints)
    print("SERIUJHSER")
    print(set.difference(*listOfSets))

    
    my_list = []
    
    print("The maximum value is" )
    
    start = df.index[df['T'] == periodastart].tolist()[0]
    end = df.index[df['T'] == periodaend].tolist()[0]
    print(df[start:end][df.columns[1]].max())
    print("The minimum value is" )

    print(df[start:end][df.columns[1]].min())
    
    # t1 = set(frozenset(i) for i in t) TODO look this up
    
    listOfLists = []
    my_list = []
    aset = set()
    bset = set()

    # # From period a start to period a end + 1 ?, create the series
    for i in range(df.index[df['T'] == periodastart].tolist()[0], df.index[df['T'] == periodaend].tolist()[0] + 1):
        aset.add(df.loc[i][df.columns[1]])
        

    # # From period a start to period a end + 1 ?, create the series
    for i in range(df.index[df['T'] == periodaend].tolist()[0] + 1, df.index[df['T'] == periodbend].tolist()[0] + 1):
        bset.add(df.loc[i][df.columns[1]])
    
 
    
    print("Single prints for inital balance range is")


    print(aset.symmetric_difference(bset))
    print()
    print(aset)
    print()
    print(bset)
    # print(pandas.Series(my_list))
    # print(new_df)

    # A (9:30-10) : 4173, 4173.25
    # B (10:00-10:30) : 4173, 4173.25
    # .
    # .
    # .


# print(es.columns)

# Takes ~2.3 seconds to process on desktop... 
createTPO(es)
createVolumeProfile(es)



# print(my_dict.keys())
# print(type(my_dict.keys()))
# print(type(my_dict.values()))
# print(my_dict.items())

# date_time_obj = datetime.datetime.strptime(times[0], '%Y%m%d %H%M%S')

# print('Date:', date_time_obj.date())
# print('Time:', date_time_obj.time())
# print('Date-time:', date_time_obj)