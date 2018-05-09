import numpy
import matplotlib.pyplot as plt
import collections
import math
from pandas import read_csv
import json

DISTRICT = 'DISTRICT'
YEAR = 'YEAR'
STATE = 'STATE/UT'
BASEPATH = "/User/ankurrastogi/sbu_classes/Spring2018/Prob n Stats/Project/crime-in-india/crime/"
GRAPH_FLAG = False

def cdf(data):
    
    data_sorted_keys = sorted(set(data))
    
    #Taking final bucket
    buckets = numpy.append(data_sorted_keys,data_sorted_keys[-1] + 1)
    
    frequency, bin_buckets = numpy.histogram(data, bins=buckets, density=False)
    frequency = frequency/(len(data)*1.0)
    
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
    
    if GRAPH_FLAG is True:
        # Plot the cdf
        plt.plot(cdfObject1.keys(), cdfObject1.values(),linestyle='--', marker="o", color='b')
        plt.plot(cdfObject2.keys(), cdfObject2.values(),linestyle='-', marker="o", color='y')
        plt.ylim((0,1))
        plt.ylabel("CDF")
        plt.grid(True)

        plt.show()
    
    return maxDiff

def parseData(file_name, column_names):
    column_names = set(column_names)
    data = read_csv(file_name,usecols=column_names,index_col=False)
    return_data = dict()
    dict_data = data.to_dict('index')
    for row in dict_data.values():
        for col in row.keys():
            if col != STATE: #and col != DISTRICT: 
                if return_data.get(row.get(STATE).lower()):
                    if return_data.get(row.get(STATE).lower()).get(col.lower()):
                        return_data.get(row.get(STATE).lower()).get(col.lower()).append(row.get(col))
                    else:
                        return_data.get(row.get(STATE).lower())[col.lower()] = []
                        return_data.get(row.get(STATE).lower())[col.lower()].append(row.get(col))
                else:
                    return_data[row.get(STATE).lower()] = {}
                    return_data[row.get(STATE).lower()][col.lower()] = []
                    return_data[row.get(STATE).lower()][col.lower()].append(row.get(col))


    return return_data

def loadPopulationData():
    f = open("./kstest_male_female_data.json","r")
    return json.loads(f.read())


def initMaleFemaleKSTest():
    
    superDict = parseData(BASEPATH + "07_01_Persons_arrested_by_sex_and_age_group_IPC_2012.csv", ["STATE/UT","Male Total","Female Total"])
    
    del superDict['total (uts)']
    del superDict['total (states)']
    del superDict['total (all-india)']
        
    populationData = loadPopulationData()

    FEMALE_TOTAL = 'female total';
    MALE_TOTAL = 'male total';
    
    FEMALE_POPULATION = 'female population';
    MALE_POPULATION = 'male population';
    
    FEMALE_CRIME = 'female_crime';
    MALE_CRIME = 'male_crime';
    
    male_data = []
    female_data = []
    
    for st in superDict:
        superDict[st][FEMALE_TOTAL] = sum(superDict[st][FEMALE_TOTAL])
        superDict[st][MALE_TOTAL] = sum(superDict[st][MALE_TOTAL])

    for item in populationData:
        for state in item:
            superDict[state]["male population"] = item[state]["male population"]
            superDict[state]["female population"] = item[state]["female population"]
            superDict[state]["male_crime"] = (superDict[state]["male total"]/(superDict[state]["male population"]*1.0))*100000
            superDict[state]["female_crime"] = (superDict[state]["female total"]/(superDict[state]["female population"]*1.0))*100000
    
    for st in superDict:
        male_data.append(superDict[st][MALE_CRIME])
        female_data.append(superDict[st][FEMALE_CRIME])
        
    
    max_diff = ksTest(male_data, female_data)
    print(max_diff)

# if __name__ == "__main__":

# 	initMaleFemaleKSTest()

