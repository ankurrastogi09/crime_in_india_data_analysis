import numpy
import math
from pandas import read_csv

DISTRICT = 'DISTRICT'
YEAR = 'YEAR'

def parseData(file_name,column_names):
    column_names.append(DISTRICT)
    column_names.append(YEAR)
    column_names = set(column_names)
    data = read_csv(file_name,usecols=column_names,index_col=False)
    return_data = {}
    dict_data = data.sort_values(YEAR).to_dict('index')
    for row in dict_data.values():
        for col in row.keys():
            if col != YEAR and col != DISTRICT:
                if return_data.get(row.get(DISTRICT)):
                    if return_data.get(row.get(DISTRICT)).get(col):#and return_data.get(row.get(DISTRICT)).get(col).get(row.get(YEAR)):
                        return_data.get(row.get(DISTRICT)).get(col)[row.get(YEAR)] = row.get(col)
                    else:
                        return_data.get(row.get(DISTRICT))[col] = {}
                        return_data.get(row.get(DISTRICT))[col][row.get(YEAR)] = row.get(col)
                else:
                    return_data[row.get(DISTRICT)] = {}
                    return_data[row.get(DISTRICT)][col] = {}
                    return_data[row.get(DISTRICT)][col][row.get(YEAR)] = row.get(col)
    return(return_data)

def createPopulationIndependentData(superDict, dict):
    for district, value in superDict.items():
        if district.lower() in dict:
            for typeOfCrime,data in value.items():
                for year,val in data.items():
                    popYearArray = dict[district.lower()]
                    population =  popYearArray[year - 2001]
                    superDict[district][typeOfCrime][year] = (val*100000)/population

    return superDict

def waldsTwoPopulation(X_Arr, Y_Arr):
    alpha = 0.05
    Z = 1.96

    # Calculating mean values
    p1_c = numpy.mean(X_Arr)
    p2_c = numpy.mean(Y_Arr)

    # Calculating Variances
    var_p1 = numpy.var(X_Arr)
    var_p2 = numpy.var(Y_Arr)

    # calculataing w value of wald's test by using formula abs((p1_cap - p2_cap)/math.sqrt(variance(p1)/N1 + variance(p2)/N))
    w = abs((p1_c - p2_c) / math.sqrt(var_p1 / len(X_Arr) + var_p2 / len(Y_Arr)))
    print(w)



if __name__ == '__main__':
    path = "/Users/anand/Desktop/PS_PROJECT/states"
    rootPath = "/Users/anand/Desktop/PS_PROJECT/"
    file = open(path,"r")
    sts = ""
    for line in file:
        sts = line
    states = sts.split(',')
    dict = {}
    stateDict = {}
    for state in states:
        file = open(rootPath + state, "r")
        districts = []
        for line in file:
            values = line.split(',')
            name = values[0]
            districts.append(name.lower())
            populations = []
            start = int(values[1])
            end =  int(values[2])
            diff = end - start;
            for x in range(0,14):
                val = start + ((diff * x)/10)
                tempDict = {}
                tempDict[2001+x] = val
                populations.append(val)
            dict[name.lower()] = populations
        stateDict[state] = districts
    #print(stateDict)
    #print(dict)
    superDict = parseData("/Users/anand/Downloads/crime-in-india/crime/01_District_wise_crimes_committed_IPC_2001_2012.csv", ["RAPE", "TOTAL IPC CRIMES"])
    print(superDict)
    superDict = createPopulationIndependentData(superDict,dict)
    print(superDict)

