
from parse_data import parseData
import numpy
import matplotlib.pyplot as plt
import collections
import math
from pandas import read_csv
import json

METERO = ["chennai","mumbai commr.","bengaluru city","kolkata","new delhi"]
OTHER_CITIES = ["coimbatore city","mysuru city", "pune commr.","darjeeling","gurgaon"]
PATH = "/Users/vineeth/SBU/SEM-2/Probability/crime-in-india/crime/"

def collectData(data, metro, other):

	for key,value in data.items():
		if key in METERO:
			for crime,years in value.items():
				for year,count in years.items():
					metro.append(count)
		elif key in OTHER_CITIES:
			for crime,years in value.items():
				for year,count in years.items():
					metro.append(count)

	return metro,other


def top_metropolitan():
	data = dict()
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2014.csv",["Rape"],data)
	metro = [0]*5
	other = [0]*5
	collectData(data,metro,other)
	ksTest(metro,other)

def cdf(data):
    
    data_sorted_keys = sorted(set(data))
    
    #Taking final bucket
    buckets = numpy.append(data_sorted_keys,data_sorted_keys[-1] + 1)
    
    frequency, bin_buckets = numpy.histogram(data, bins=buckets, density=False)
    frequency = frequency/len(data)
    
    cdf = numpy.cumsum(frequency)
    
    cdf_dict = collections.OrderedDict()
    
    for index, item in enumerate(cdf):
        cdf_dict[bin_buckets[index]] = item
    
#     print(cdf_dict)
    
    return cdf_dict

def ksTest(list1, list2):
    
    cdfObject1 = cdf(list1)
    cdfObject2 = cdf(list2)
    
    combinedKeys = list(cdfObject1.keys()) + list(cdfObject2.keys())
    totalKeys = list(set(combinedKeys))

    prevValue1 = 0
    prevValue2 = 0
    maxDiff = 0
    for item in totalKeys:
        cdfValue1 = prevValue1
        cdfValue2 = prevValue2
        
        if item in cdfObject1:
            cdfValue1 = cdfObject1[item]
        
        if item in cdfObject2:
            cdfValue2 = cdfObject2[item]
        
        maxDiff = max(maxDiff, abs(cdfValue1 - cdfValue2))
        
        prevValue1 = cdfValue1
        prevValue2 = cdfValue2
    
    # Plot the cdf
    plt.plot(cdfObject1.keys(), cdfObject1.values(),linestyle='--', marker="o", color='b')
    plt.plot(cdfObject2.keys(), cdfObject2.values(),linestyle='-', marker="o", color='y')
    plt.ylim((0,1))
    plt.ylabel("CDF")
    plt.grid(True)

    plt.show()
    
    return maxDiff

top_metropolitan()
