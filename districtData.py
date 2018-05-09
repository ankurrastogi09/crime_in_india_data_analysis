import numpy
import math
from pandas import read_csv
import sys
import matplotlib.pyplot as plt
import collections
from sklearn import linear_model
from numpy import array
import test_series_riots
import male_female_crime

DISTRICT = 'DISTRICT'
YEAR = 'YEAR'
STATE = 'STATE'
METERO = ["chennai", "mumbai commr.", "bengaluru city", "kolkata", "new delhi"]
OTHER_CITIES = ["coimbatore city", "mysuru city", "pune commr.", "darjeeling", "gurgaon"]
PATH = "./"

SP = [2002, 2003, 2004, 2005, 2006]
BSP = [2008, 2009, 2010, 2011, 2012]

COLUMNS_SC = ["STATE/UT", "Murder", "Rape", "Kidnapping and Abduction", "Dacoity", "Robbery", "Arson", "Hurt",
              "Prevention of atrocities (POA) Act", "Protection of Civil Rights (PCR) Act", "Other Crimes Against SCs"]
COLUMNS_ST = ["STATE/UT", "Murder", "Rape", "Kidnapping Abduction", "Dacoity", "Robbery", "Arson", "Hurt",
              "Protection of Civil Rights (PCR) Act", "Prevention of atrocities (POA) Act", "Other Crimes Against STs"]

FilesToRead = ["02_01_District_wise_crimes_committed_against_SC_2001_2012.csv", "02_District_wise_crimes_committed_against_ST_2001_2012.csv"]

COLOR = ['blue', 'red', 'green', 'orange', 'magenta']

BASEPATH = "./"

test_series_riots.GRAPH_FLAG = False
test_series_riots.BASEPATH = BASEPATH

def parseData(file_name, column_names,return_data=dict()):
	column_names.append(DISTRICT)
	column_names.append(YEAR)
	column_names = set(column_names)
	data = read_csv(file_name,usecols=column_names,index_col=False)
	#return_data = {}
	dict_data = data.sort_values(YEAR).to_dict('index')
	for row in dict_data.values():
		for col in row.keys():
			if col != YEAR and col != DISTRICT:
				if return_data.get(row.get(DISTRICT).lower().strip()):
					if return_data.get(row.get(DISTRICT).lower().strip()).get(col.lower().strip()):
						return_data.get(row.get(DISTRICT).lower().strip()).get(col.lower().strip())[row.get(YEAR)] = row.get(col)
					else:
						return_data.get(row.get(DISTRICT).lower().strip())[col.lower().strip()] = {}
						return_data.get(row.get(DISTRICT).lower().strip())[col.lower().strip()][row.get(YEAR)] = row.get(col)
				else:
					return_data[row.get(DISTRICT).lower().strip()] = {}
					return_data[row.get(DISTRICT).lower().strip()][col.lower().strip()] = {}
					return_data[row.get(DISTRICT).lower().strip()][col.lower().strip()][row.get(YEAR)] = row.get(col)

	return return_data


def parseDataByState(file_name, column_names,return_data=dict()):
	column_names = set(column_names)
	data = read_csv(file_name,usecols=column_names,index_col=False)
	return_data = {}
	dict_data = data.to_dict('index')
	for row in dict_data.values():
		for col in row.keys():
			if col != STATE:
				if return_data.get(row.get(STATE)) and return_data.get(row.get(STATE).lower()):
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

def createPopulationIndependentData(superDict, dict):
    newDistricts = []
    for district, value in superDict.items():
        if district.lower() in dict:

            for typeOfCrime,data in value.items():
                for year,val in data.items():
                    popYearArray = dict[district.lower()]
                    population =  popYearArray[year - 2001]
                    superDict[district][typeOfCrime][year] = (val*100000)/population
        else:
            newDistricts.append(district)
    for newDistrict in newDistricts:
        superDict.pop(newDistrict)
    return superDict

def stateWiseWaldTest(state1, state2, superDict, stateDict):
    districts1 = stateDict[state1]
    districts2 = stateDict[state2]
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            population1 = superDict[district1]['rape'].get(2011)
            if population1 is not None:
                poparray1.append(population1)
    for district2 in districts2:
        if district2 in superDict.keys():
            population2 = superDict[district2]['rape'].get(2011)
            if population2 is not None:
                poparray2.append(population2)
    #print(poparray1)
    #print(poparray2)
    waldsTwoPopulation(poparray1,poparray2)


#   Number of Rapes reported in North India, Delhi, NCR before and after Nirbhaya’s case for 2011 and 2013-
#   H0 - More awareness of the crime against rapes in Delhi before and after Nirbhaya’s case.
#   Paired T- Test (since the data is dependent)
def stateWisePairedTest(state1,superDict, stateDict):
    districts1 = stateDict[state1]
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            population1 = superDict[district1]['rape'].get(2011)
            population2 = superDict[district1]['rape'].get(2013)
            if population1 is not None:
                poparray1.append(population1)
            if population2 is not None:
                poparray2.append(population2)

    #print(poparray1)
    #print(poparray2)
    pairedTTest(poparray1,poparray2)
    PlotWrapper({'Cases in 2011': [[range(0, len(poparray1))], poparray1],
                 'Cases in 2013': [[range(0, len(poparray2))], poparray2]}, 'Districts', 'Crime Rate',
                'Rapes reported in Delhi, NCR before and after Nirbhaya''s case')

#Number of riots is 2001 in comparison to 2003 in Gujarat
def stateWisePairedTestRiots(state1,superDict, stateDict):
    districts1 = stateDict[state1]
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            population1 = superDict[district1]['riots'].get(2001)
            population2 = superDict[district1]['riots'].get(2003)
            if population1 is not None:
                poparray1.append(population1)
            if population2 is not None:
                poparray2.append(population2)

    #print(poparray1)
    #print(poparray2)
    pairedTTest(poparray1,poparray2)


#Rate of increase of Rape in 2 state(Delhi and Maha) (The impact of Nirbhaya case had pan india impact) (y-x)/x * 100 y = 2013 x = 2011
def pairedTTestGujarat(state1,state2,superDict, stateDict):
    districts1 = stateDict[state1]
    districts2 = stateDict[state2]
    #print(districts1)
    #print(districts2)
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            #print(district1)

            count1 = superDict[district1]['rape'].get(2011)
            count2 = superDict[district1]['rape'].get(2013)
            if (count1 is not None) and (count2 is not None):
                if not count1 == 0:
                    poparray1.append((count2 - count1)/count1)
    for district2 in districts2:
        if district2 in superDict.keys():
            #print(district2)
            count1 = superDict[district2]['rape'].get(2011)
            count2 = superDict[district2]['rape'].get(2013)
            if (count1 is not None) and (count2 is not None):
                if not count1 == 0:
                    poparray2.append((count2 - count1)/count1)
    waldsTwoPopulation(poparray1, poparray2)

#Comparison of police efficiency between Gujarat and UP between 2011- 2013.
def pairedTTestGujaratRiots(state1,state2,superDict, stateDict):
    districts1 = stateDict[state1]
    districts2 = stateDict[state2]
    #print(districts1)
    #print(districts2)
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            #print(district1)
            if 'total ipc crimes' in superDict[district1].keys():
                count1 = superDict[district1]['total ipc crimes'].get(2011)
                count2 = superDict[district1]['total ipc crimes'].get(2013)
            if (count1 is not None) and (count2 is not None):
                if not count1 == 0:
                    poparray1.append((count2 - count1)/count1)
    for district2 in districts2:
        if district2 in superDict.keys():
            #print(district2)
            if 'total ipc crimes' in superDict[district2].keys():
                count1 = superDict[district2]['total ipc crimes'].get(2011)
                count2 = superDict[district2]['total ipc crimes'].get(2013)
            if (count1 is not None) and (count2 is not None):
                if not count1 == 0:
                    poparray2.append((count2 - count1)/count1)
    waldsTwoPopulation(poparray1, poparray2)


#H0 - Kidnapping crimes more in SP government then in BSP government.
#SP - 2002 - 2007 BSP - 2007 - 2012
def kidnappingInUPunderSPandBSP(state1,superDict, stateDict):
    districts1 = stateDict[state1]
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            #print(district1)
            #print(superDict[district1])
            if 'kidnapping & abduction' in superDict[district1].keys():
                population1 = superDict[district1]['kidnapping & abduction'].get(2002)
                population2 = superDict[district1]['kidnapping & abduction'].get(2003)
                population3 = superDict[district1]['kidnapping & abduction'].get(2004)
                population4 = superDict[district1]['kidnapping & abduction'].get(2005)
                population5 = superDict[district1]['kidnapping & abduction'].get(2006)

                population6 = superDict[district1]['kidnapping & abduction'].get(2008)
                population7 = superDict[district1]['kidnapping & abduction'].get(2009)
                population8 = superDict[district1]['kidnapping & abduction'].get(2010)
                population9 = superDict[district1]['kidnapping & abduction'].get(2011)
                population10 = superDict[district1]['kidnapping & abduction'].get(2012)
                if (population1 is not None) and (population2 is not None) and (population3 is not None) and (population4 is not None) and (population5 is not None) and (population6 is not None) and (population7 is not None) and (population8 is not None) and (population9 is not None) and (population10 is not None):
                    poparray1.append(population1 + population2 + population3 + population4 + population5)
                    poparray2.append(population6 + population7 + population8 + population9 + population10)

    #print(poparray1)
    #print(poparray2)
    pairedTTest(poparray1, poparray2)

# Number of Riots happened under congress ruled state and BJP ruled states under specific year or years. (4 and 4 major states 2012)
def riotsUnderCongressAndBJP(state1, state2, state3, state4, state5, state6, state7, state8):
    districts1 = stateDict[state1]
    districts2 = stateDict[state2]
    districts3 = stateDict[state3]
    districts4 = stateDict[state4]
    districts5 = stateDict[state5]
    districts6 = stateDict[state6]
    districts7 = stateDict[state7]
    districts8 = stateDict[state8]
    poparray1 = []
    poparray2 = []
    for district1 in districts1:
        if district1 in superDict.keys():
            population1 = superDict[district1]['riots'].get(2012)
            if population1 is not None:
                poparray1.append(population1)
    for district2 in districts2:
        if district2 in superDict.keys():
            population2 = superDict[district2]['riots'].get(2012)
            if population2 is not None:
                poparray1.append(population2)
    for district3 in districts3:
        if district3 in superDict.keys():
            population3 = superDict[district3]['riots'].get(2012)
            if population3 is not None:
                poparray1.append(population3)
    for district4 in districts4:
        if district4 in superDict.keys():
            population4 = superDict[district4]['riots'].get(2012)
            if population4 is not None:
                poparray1.append(population4)
    for district5 in districts5:
        if district5 in superDict.keys():
            population5 = superDict[district5]['riots'].get(2012)
            if population5 is not None:
                poparray2.append(population5)
    for district6 in districts6:
        if district6 in superDict.keys():
            population6 = superDict[district6]['riots'].get(2012)
            if population6 is not None:
                poparray2.append(population6)
    for district7 in districts7:
        if district7 in superDict.keys():
            population7 = superDict[district7]['riots'].get(2012)
            if population7 is not None:
                poparray2.append(population7)
    for district8 in districts8:
        if district8 in superDict.keys():
            population8 = superDict[district8]['riots'].get(2012)
            if population8 is not None:
                poparray2.append(population8)

    # print(poparray1)
    # print(poparray2)
    waldsTwoPopulation(poparray1, poparray2)
    return


def pairedTTest(X_Arr, Y_Arr):
    diff = []

    # finding the distribution of difference of two independent normal distributions
    for i in range(0, len(X_Arr)):
        diff.append(X_Arr[i] - Y_Arr[i])

    # Calculating Mean
    x_diff = numpy.mean(diff)

    # Calculating Variance
    var_diff = numpy.var(diff)

    # Calculating Standard Deviation
    s_diff = math.sqrt(var_diff)

    # Calculating Paired T-Test value
    pTTest = abs(x_diff / (s_diff / math.sqrt(len(diff))))

    print(pTTest)


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

def hypo_top_bottom_literacy(fname, superDict, stateDict, dict):
    f = open(fname, "r")
    #print(superDict)
    #sys.exit(0)
    literacyRate = []
    for line in f:
        values = line.split(',')
        st = values[0].lower().strip()
        if st in dict.keys():
            val = float(values[1])*100/dict[st][10]
            literacyRate.append((val, values[0]))

    # print(literacyRate)
    literacyRate.sort(reverse=True)
    toplist = []
    topcount = 0
    for i in range(0, 150):
        dis = literacyRate[i][1]
        dis = dis.lower().strip()
        # print(dis, literacyRate[i][0])
        if dis in superDict.keys():
            if superDict.get(dis) and superDict.get(dis).get('total ipc crimes') and \
                           superDict.get(dis).get('total ipc crimes').get(2011):
                val = superDict[dis]['total ipc crimes'][2011]
                if(val < 600):
                    #print(dis, val)
                    topcount = topcount + 1
                    toplist.append(val)
                    if topcount > 100:
                        break
    #print(toplist)

    literacyRate.sort()
    bottomlist = []
    bottomcount = 0
    for i in range(0, 150):
        dis = literacyRate[i][1]
        dis = dis.lower().strip()
        # print(dis, literacyRate[i][0])
        if dis in superDict.keys():
            if superDict.get(dis) and superDict.get(dis).get('total ipc crimes') and \
                    superDict.get(dis).get('total ipc crimes').get(2011):
                val = superDict[dis]['total ipc crimes'][2011]
                bottomlist.append(val)
                bottomcount = bottomcount + 1
                if bottomcount > 100:
                    break
    #print(bottomlist)
    #print("literacy rate hypo - W value between 100 top literate districts vs 100 bottom literate districts")
    waldsTwoPopulation(toplist, bottomlist)
    #print("Top:",len(toplist))
    #print("Bottom:",len(bottomlist))
    PlotWrapper({'Top 100 Literate Districts':[[range(0,len(toplist))], toplist], 'Bottom 100 Literate Districts': [[range(0,len(bottomlist))], bottomlist]}, 'Districts', 'Crime Rate', 'Correlation between Literacy and Crime rate ')
    return

def hypo_kerala_up_riots(fname, superDict, stateDict, dict):
    state1 = "kerala"
    state2 = "uttar pradesh"

    f = open(fname, "r")
    literacyRate = []

    districts1 = stateDict[state1]
    districts2 = stateDict[state2]
    #print(districts1)
    #print(districts2)
    poparray1 = []
    poparray2 = []

    for line in f:
        values = line.split(',')
        st = values[0].lower().strip()
        for dis1 in districts1:
            if(st == dis1):
                if superDict.get(st) and superDict.get(st).get('riots') and \
                        superDict.get(st).get('riots').get(2011):
                    val = superDict[st]['riots'].get(2011)
                    poparray1.append(val)

        for dis2 in districts2:
            if (st == dis2):
                if superDict.get(st) and superDict.get(st).get('riots') and \
                        superDict.get(st).get('riots').get(2011):
                    val = superDict[st]['riots'].get(2011)
                    poparray2.append(val)

    #print(poparray1)
    #print(poparray2)
    #print("Hyp - Riots comparison between Kerala and Uttar pradesh")
    waldsTwoPopulation(poparray1, poparray2)
    return


def womenTtest(superDict, stateDict):

    poparray1 = []
    poparray2 = []
    stsum2004 = 0
    stsum2006 = 0
    for state in stateDict.keys():
        # print(state)
        dis = stateDict[state]
        # print(dis)
        stsum2004 = 0
        stsum2006 = 0
        for d in dis:
            if d in superDict.keys():
                #print(d)
                #Rape","Kidnapping and Abduction","Dowry Deaths","Assault on women with intent to outrage her modesty","Insult to modesty of Women","Cruelty by Husband or his Relatives","Importation of Girls"
                '''if superDict.get(d).get('rape') and \
                        superDict.get(d).get('rape').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['rape'].get(2004)
                if superDict.get(d).get('rape') and \
                        superDict.get(d).get('rape').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['rape'].get(2006)

                if superDict.get(d).get('kidnapping and abduction') and \
                        superDict.get(d).get('kidnapping and abduction').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['kidnapping and abduction'].get(2004)
                if superDict.get(d).get('kidnapping and abduction') and \
                        superDict.get(d).get('kidnapping and abduction').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['kidnapping and abduction'].get(2006)'''

                if superDict.get(d).get('dowry deaths') and \
                        superDict.get(d).get('dowry deaths').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['dowry deaths'].get(2004)
                if superDict.get(d).get('dowry deaths') and \
                        superDict.get(d).get('dowry deaths').get(2003):
                    stsum2004 = stsum2004 + superDict[d]['dowry deaths'].get(2003)
                if superDict.get(d).get('dowry deaths') and \
                        superDict.get(d).get('dowry deaths').get(2002):
                    stsum2004 = stsum2004 + superDict[d]['dowry deaths'].get(2002)

                if superDict.get(d).get('dowry deaths') and \
                        superDict.get(d).get('dowry deaths').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['dowry deaths'].get(2006)
                if superDict.get(d).get('dowry deaths') and \
                        superDict.get(d).get('dowry deaths').get(2007):
                    stsum2006 = stsum2006 + superDict[d]['dowry deaths'].get(2007)
                if superDict.get(d).get('dowry deaths') and \
                        superDict.get(d).get('dowry deaths').get(2008):
                    stsum2006 = stsum2006 + superDict[d]['dowry deaths'].get(2008)

                '''if superDict.get(d).get('assault on women with intent to outrage her modesty') and \
                        superDict.get(d).get('assault on women with intent to outrage her modesty').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['assault on women with intent to outrage her modesty'].get(2004)
                if superDict.get(d).get('assault on women with intent to outrage her modesty') and \
                        superDict.get(d).get('assault on women with intent to outrage her modesty').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['assault on women with intent to outrage her modesty'].get(2006)'''

                '''if superDict.get(d).get('insult to modesty of women') and \
                        superDict.get(d).get('insult to modesty of women').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['insult to modesty of women'].get(2004)
                if superDict.get(d).get('insult to modesty of women') and \
                        superDict.get(d).get('insult to modesty of women').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['insult to modesty of women'].get(2006)'''

                if superDict.get(d).get('cruelty by husband or his relatives') and \
                        superDict.get(d).get('cruelty by husband or his relatives').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['cruelty by husband or his relatives'].get(2004)
                if superDict.get(d).get('cruelty by husband or his relatives') and \
                        superDict.get(d).get('cruelty by husband or his relatives').get(2003):
                    stsum2004 = stsum2004 + superDict[d]['cruelty by husband or his relatives'].get(2003)
                if superDict.get(d).get('cruelty by husband or his relatives') and \
                        superDict.get(d).get('cruelty by husband or his relatives').get(2002):
                    stsum2004 = stsum2004 + superDict[d]['cruelty by husband or his relatives'].get(2002)

                if superDict.get(d).get('cruelty by husband or his relatives') and \
                        superDict.get(d).get('cruelty by husband or his relatives').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['cruelty by husband or his relatives'].get(2006)
                if superDict.get(d).get('cruelty by husband or his relatives') and \
                        superDict.get(d).get('cruelty by husband or his relatives').get(2007):
                    stsum2006 = stsum2006 + superDict[d]['cruelty by husband or his relatives'].get(2007)
                if superDict.get(d).get('cruelty by husband or his relatives') and \
                        superDict.get(d).get('cruelty by husband or his relatives').get(2008):
                    stsum2006 = stsum2006 + superDict[d]['cruelty by husband or his relatives'].get(2008)

                '''if superDict.get(d).get('importation of girls') and \
                        superDict.get(d).get('importation of girls').get(2004):
                    stsum2004 = stsum2004 + superDict[d]['importation of girls'].get(2004)
                if superDict.get(d).get('importation of girls') and \
                        superDict.get(d).get('importation of girls').get(2006):
                    stsum2006 = stsum2006 + superDict[d]['importation of girls'].get(2006)'''
        poparray1.append(stsum2004)
        poparray2.append(stsum2006)
        #print(state, stsum2004, stsum2006)

    # print(poparray1)
    # print(poparray2)
    #print("Protection of Women from Domestic violence law(2005) - Compare 2004 & 2006")
    pairedTTest(poparray1, poparray2)

    PlotWrapper({'Crime Rate during 2002<->2004': [[range(0,len(poparray1))], poparray1], 'Crime Rate during 2006<->2008': [[range(0,len(poparray2))], poparray2]},'State','Crime Rate','Domestic Violence Against Women')


def collectData(data, metro, other):
    for key, value in data.items():
        if key in METERO:
            for crime, years in value.items():
                for year, count in years.items():
                    metro.append(count)
        elif key in OTHER_CITIES:
            for crime, years in value.items():
                for year, count in years.items():
                    metro.append(count)

    return metro, other


def top_metropolitan():
    data = {}
    parseData(PATH + "01_District_wise_crimes_committed_IPC_2014_updated.csv", ["Rape"], data)
    metro = [0] * 5
    other = [0] * 5
    collectData(data, metro, other)
    print(ksTest(metro, other))


def cdf(data):
    data_sorted_keys = sorted(set(data))

    # Taking final bucket
    buckets = numpy.append(data_sorted_keys, data_sorted_keys[-1] + 1)

    frequency, bin_buckets = numpy.histogram(data, bins=buckets, density=False)
    frequency = frequency / len(data)

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
    plt.plot(cdfObject1.keys(), cdfObject1.values(), linestyle='--', marker="o", color='b')
    plt.plot(cdfObject2.keys(), cdfObject2.values(), linestyle='-', marker="o", color='y')
    plt.ylim((0, 1))
    plt.ylabel("CDF")
    plt.grid(True)

    plt.show()

    return maxDiff




def summateCrimes(data, total_dict_1={}, total_dict_2={}):
    for key, value in data.items():
        if 'UTTAR PRADESH' in value.get('state/ut').values():
            for crime, years in value.items():
                if crime != 'state/ut' and crime != 'year':
                    for year, count in years.items():
                        if int(year) in SP:
                            if total_dict_1.get(key):
                                total_dict_1[key] += count
                            else:
                                total_dict_1[key] = count
                        elif int(year) in BSP:
                            if total_dict_2.get(key):
                                total_dict_2[key] += count
                            else:
                                total_dict_2[key] = count

    return total_dict_1, total_dict_2


def scst():
    data = {}
    total_dict_1 = {}
    total_dict_2 = {}

    parseData(PATH + FilesToRead[0], COLUMNS_SC, data)
    parseData(PATH + FilesToRead[1], COLUMNS_ST, data)

    total_dict_1, total_dict_2 = summateCrimes(data)

    pairedTTest(list(total_dict_1.values()), list(total_dict_2.values()))
    PlotWrapper({'Under SP rule': [[range(0, len(list(total_dict_1.values())))], list(total_dict_1.values())],
                 'Under BSP rule': [[range(0, len(list(total_dict_2.values())))], list(total_dict_2.values())]}, 'District', 'Crime Rate',
                'Crime against SC/ST under SP(2002-06) and BSP(2008-12) in Uttar Pradesh')

def computeSSE(y_data, y_pred):
	sse = 0
	for i in range(0,len(y_data)):
		sse += (y_pred[i][0]-y_data[i][0])**2

	print("SSE:",sse)

def linearRegression(x,y):

	reg = linear_model.LinearRegression()
	x_data = array(x).reshape(-1,1)
	y_data = array(y).reshape(-1,1)
	reg.fit(x_data[:14],y_data)
	yPredict = reg.predict(x_data[10:])
	plt.scatter(x_data[:14], y_data,  color='black')
	plt.plot(x_data[10:], yPredict, color='blue', linewidth=3)
	plt.show()

def computeLinearRegression(data, total_crime,district=None):

	for key,value in data.items():
		if district:
			if key.upper() in district:
				for crime,years in value.items():
					for year,count in years.items():
						total_crime[int(year) - 2001] += count
		else:
			for crime,years in value.items():
				for year,count in years.items():
					total_crime[int(year) - 2001] += count

	return total_crime

def linearRegressionWrapper():

	total_crime = [0]*14
	total_rape = [0]*14

	data = {}
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2001_2012.csv",["TOTAL IPC CRIMES"],data)
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2013.csv",["TOTAL IPC CRIMES"],data)
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2014_updated.csv",["Total Cognizable IPC crimes"],data)
	computeLinearRegression(data,total_crime)

	# data = {}
	# parseData(PATH+"01_District_wise_crimes_committed_IPC_2001_2012.csv",["RAPE"],data)
	# parseData(PATH+"01_District_wise_crimes_committed_IPC_2013.csv",["RAPE"],data)
	# print(computeLinearRegression(data,total_rape))

	#computeLinearRegression(data,total_crime,["MUMBAI COMMR.", "MUMBAI RLY.", "NAVI MUMBAI", "MUMBAI"])
	linearRegression([range(1,20)],total_crime)
	#PlotWrapper({0: [[range(1,15)],total_crime], 1: [[range(1,15)],[total_rape]]},"SCATTER")




def scatterPlot(data_obj,title, xlabel, ylabel):
    for k, v in data_obj.items():
        plt.scatter(array(v[0]).reshape(-1, 1), array(v[1]).reshape(-1, 1), color=COLOR[k])
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def linePlot(data_obj, title, xlabel, ylabel):
    c = 0
    for k, v in data_obj.items():
        plt.plot(array(v[0]).reshape(-1, 1), array(v[1]).reshape(-1, 1), color=COLOR[c], linewidth=3, label = k)
        c = c + 1
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


# data_obj:
# {	0: [[range(1,15)],total_crime],
# 	1: [[range(1,15)],[total_rape]]
# }
def PlotWrapper(data_obj, xlable, ylabel, title, plot_type="LINE"):
    if plot_type == "LINE":
        linePlot(data_obj,title, xlable, ylabel)
    else:
        # SCATTER PLOT
        scatterPlot(data_obj, title, xlable, ylabel)

if __name__ == '__main__':
    path = "./states"
    rootPath = "./states_data/"
    literary = "./literacy_districtwise.csv"

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
            districts.append(name.lower().strip())
            populations = []
            start = int(values[1])
            end =  int(values[2])
            diff = end - start;
            for x in range(0,14):
                val = start + ((diff * x)/10)
                tempDict = {}
                tempDict[2001+x] = val
                populations.append(val)
            dict[name.lower().strip()] = populations
        stateDict[state.lower().strip()] = districts
    superDict = parseData("./01_District_wise_crimes_committed_IPC_2001_2012.csv", ["RAPE", "TOTAL IPC CRIMES", "RIOTS"])
    superDict = parseData("./01_District_wise_crimes_committed_IPC_2013.csv", ["RAPE", "TOTAL IPC CRIMES", "RIOTS"],superDict)
    superDict = parseData("./01_District_wise_crimes_committed_IPC_2014_updated.csv", ["Rape", "Total Cognizable IPC crimes", "Riots"], superDict)

    superDict = createPopulationIndependentData(superDict, dict)

    womenDict = parseData("./42_District_wise_crimes_committed_against_women_2001_2012.csv", ["Rape","Kidnapping and Abduction","Dowry Deaths","Assault on women with intent to outrage her modesty","Insult to modesty of Women","Cruelty by Husband or his Relatives","Importation of Girls"])

    womenDict = createPopulationIndependentData(womenDict, dict)

    #print(superDict)
    #print(stateDict)

    hyp_n = 1

    print("\n\nTopic 1 - RAPE -----------------------------------")
    print(hyp_n, "\nNumber of Rapes reported in North India, Delhi, NCR before and after Nirbhaya’s case for 2011 and 2013")
    stateWisePairedTest("delhi", superDict, stateDict)
    hyp_n += 1

    print(hyp_n, "\nRate of increase of Rape in 2 state(Delhi and Maha) (The impact of Nirbhaya case had pan india impact)")
    pairedTTestGujarat("delhi", "maharashtra", superDict, stateDict)
    hyp_n += 1

    print(hyp_n, "\nComparison of top 10 metropolitan districts vs other 10 districts rape crime KS test")
    top_metropolitan()
    hyp_n += 1

    print("\n\nTopic 2 - POLITICS -----------------------------------")
    print(hyp_n, "\nNumber of Riots happened under congress ruled state and BJP ruled states under specific year or years. (4 and 4 major states 2012)")
    riotsUnderCongressAndBJP("uttarakhand", "gujarat", "madhya pradesh", "karnataka", "rajasthan", "maharashtra", "andhra pradesh", "kerala")
    hyp_n += 1

    print(hyp_n, "\nNumber of crime reports for SC/ST Atrocities increased during BSP compared to SP.")
    scst()
    hyp_n += 1

    print(hyp_n, "\nNumber of riots is 2001 in comparison to 2003 in Gujarat.")
    stateWisePairedTestRiots("gujarat", superDict, stateDict)
    hyp_n += 1

    print(hyp_n, "\nKerala and UP literacy rate vs riots for a particular year")
    hypo_kerala_up_riots(literary, superDict, stateDict, dict)
    hyp_n += 1

    print("\n\nTopic 3 - POLICE -----------------------------------")
    print(hyp_n, "\nComparison of police efficiency between Gujarat and UP between 2011- 2013")
    pairedTTestGujaratRiots("gujarat", "uttar pradesh", superDict, stateDict)
    hyp_n += 1

    print(hyp_n, "\nProtection of Women from Domestic violence law - 2005. We compare domestic violence cases between 2004 and 2006 (pan India)")
    womenTtest(womenDict, stateDict)
    hyp_n += 1

    print(hyp_n, "\nPredicting the number of riots to start recruitments of police to scale up. - Time Series Analysis.")
    test_series_riots.initRiotsPrediction()
    hyp_n += 1

    print("\n\nTopic 4 - DEMOGRAPHICS -----------------------------------")
    print(hyp_n, "\nLinear regression for total crime data training data from 2001 - 2010, error testing 2010- 2014. Prediction till 2020.")
    print("Please see the graph")
    linearRegressionWrapper()
    hyp_n += 1

    print(hyp_n, "\nNormal distribution comparison KS - Test. [MLE is required] Total crime across all district for 1 year - 2013")
    print("To be figured out")
    hyp_n += 1

    print(hyp_n, "\nTop 100 literate district comparison with bottom 100 illerate district crime rate comparison")
    hypo_top_bottom_literacy(literary, superDict, stateDict, dict)
    hyp_n += 1


    print(hyp_n, "\nCDF of x (men distribution) = Number of districts having crime committed by Men <= x / Total number of districts - KS Test")
    male_female_crime.GRAPH_FLAG = False
    male_female_crime.BASEPATH = BASEPATH
    male_female_crime.initMaleFemaleKSTest()
    hyp_n += 1

    print(hyp_n, "\nTime Series for total crime data training data from 2001 - 2010, error testing 2010- 2014. Prediction till 2020")
    test_series_riots.initCrimesPrediction()
    hyp_n += 1


    #stateWiseWaldTest("delhi","rajasthan",superDict,stateDict)

    #kidnappingInUPunderSPandBSP("uttar pradesh",superDict, stateDict)




