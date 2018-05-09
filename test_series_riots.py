import numpy
import matplotlib.pyplot as plt
import math
import json
import collections
from pandas import read_csv
from sklearn import linear_model

DISTRICT = 'DISTRICT'
YEAR = 'YEAR'
STATE = 'STATE/UT'
BASEPATH = "/Users/ankurrastogi/sbu_classes/Spring2018/Prob n Stats/Project/crime-in-india/crime/"
FILE_2001_2012 = "01_District_wise_crimes_committed_IPC_2001_2012.csv"
FILE_2013 = "01_District_wise_crimes_committed_IPC_2013.csv"
FILE_2014 = "01_District_wise_crimes_committed_IPC_2014.csv"
GRAPH_FLAG = True


def fetchYearCrimes(file_name, capsFlag):
    if capsFlag is True:
        superDict = read_csv(BASEPATH + file_name, usecols=["TOTAL IPC CRIMES", "YEAR"], index_col=False).to_dict(
            'index')
    elif capsFlag is False:
        superDict = read_csv(BASEPATH + file_name, usecols=["Total Cognizable IPC crimes", "Year"],
                             index_col=False).to_dict('index')
    return superDict


def fetchYearRiots(file_name, capsFlag):
    if capsFlag is True:
        superDict = read_csv(BASEPATH + file_name, usecols=["RIOTS", "YEAR"], index_col=False).to_dict('index')
    elif capsFlag is False:
        superDict = read_csv(BASEPATH + file_name, usecols=["Riots", "Year"], index_col=False).to_dict('index')
    return superDict


def ewma(year_wise_dict, alpha, extendFlag):
    ewma_predicted_data = {}
    perDiff = 0
    errorDiff = 0

    ewma_predicted_data[2011] = alpha * year_wise_dict[2010] + (1 - alpha) * year_wise_dict[2010]

    for year in range(2012, 2015):
        ewma_predicted_data[year] = alpha * year_wise_dict[year - 1] + (1 - alpha) * ewma_predicted_data[year - 1]

    for year in range(2011, 2015):
        errorDiff = abs(ewma_predicted_data[year] - year_wise_dict[year])
        perDiff += (errorDiff / year_wise_dict[year]) * 100
    print("Error Rate is : ", perDiff / 4)

    if GRAPH_FLAG is True:
        # Plotting graph for moving average
        plt.plot(year_wise_dict.keys(), year_wise_dict.values(), color='b')
        plt.plot(ewma_predicted_data.keys(), ewma_predicted_data.values(), color='y')
        plt.title("EWMA Time Analysis, alpha = " + str(alpha))
        plt.xlabel("Year (2001-2014)")
        plt.ylabel("Number of Riots")
        plt.show()

    return ewma_predicted_data


def ar(year_wise_dict, p, extendFlag):
    x_train = []
    y_train = []
    x_test = []
    # ar_predicted_data = {}
    ar_predicted_data = collections.OrderedDict()
    errorDiff = 0
    perDiff = 0

    for year in range(2001, 2011 - p):
        x_train_item = []
        y_train_item = []
        for x_train_year in range(year, year + p):
            x_train_item.append(year_wise_dict[x_train_year])
        y_train_item.append(year_wise_dict[year + p])
        x_train.append(x_train_item)
        y_train.append(y_train_item)

    model = linear_model.LinearRegression()
    model.fit(x_train, y_train)

    for year in range(2011, 2015):
        x_test_item = []
        for x_test_year in range(year - p, year):
            x_test_item.append(year_wise_dict[x_test_year])

        x_test_item = numpy.array(x_test_item)
        x_test_item = x_test_item.reshape((1, x_test_item.shape[0]))
        ar_predicted_data[year] = model.predict(x_test_item)[0][0]

    for year in range(2011, 2015):
        errorDiff = abs(ar_predicted_data[year] - year_wise_dict[year])
        perDiff += (errorDiff / year_wise_dict[year]) * 100

    print("Error Rate is : ", perDiff / 4)

    if extendFlag is True:
        temp_year_wise_dict = year_wise_dict.copy()

        for year in range(2015, 2021):
            x_test_item = []
            for x_test_year in range(year - p, year):
                x_test_item.append(temp_year_wise_dict[x_test_year])

            x_test_item = numpy.array(x_test_item)
            x_test_item = x_test_item.reshape((1, x_test_item.shape[0]))

            ar_predicted_data[year] = model.predict(x_test_item)[0][0]
            temp_year_wise_dict[year] = ar_predicted_data[year]

    if GRAPH_FLAG is True:
        # Plotting graph for moving average
        plt.plot(year_wise_dict.keys(), year_wise_dict.values(), color='b')
        plt.plot(ar_predicted_data.keys(), ar_predicted_data.values(), color='y')
        plt.title("AR Time Analysis, p = " + str(p))
        plt.xlabel("Year (2001-2014)")
        plt.ylabel("Number of Riots")
        plt.show()

    return ar_predicted_data


def lastObserved(year_wise_dict, extendFlag):
    last_observed_predicted_data = {}
    errorDiff = 0
    perDiff = 0

    for year in range(2011, 2015):
        last_observed_predicted_data[year] = year_wise_dict[year - 1]

    for year in range(2011, 2015):
        errorDiff = abs(last_observed_predicted_data[year] - year_wise_dict[year])
        perDiff += (errorDiff / (year_wise_dict[year] * 1.0)) * 100

    if GRAPH_FLAG is True:
        # Plotting graph for last onserved
        plt.plot(year_wise_dict.keys(), year_wise_dict.values(), color='b')
        plt.plot(last_observed_predicted_data.keys(), last_observed_predicted_data.values(), color='y')
        plt.title("Last Observed Time Analysis")
        plt.xlabel("Year (2001-2014)")
        plt.ylabel("Number of Riots")
        plt.show()

    print("Error Rate is : ", perDiff / 4)

    return last_observed_predicted_data


def movingAverage(year_wise_dict, N, extendFlag):
    moving_average_predicted_data = {}
    perDiff = 0
    errorDiff = 0

    for year in range(2011, 2015):
        total_riots = 0

        for past_year in range(year - N, year):
            total_riots += year_wise_dict[past_year]

        moving_average_predicted_data[year] = total_riots / N

    for year in range(2011, 2015):
        errorDiff = abs(moving_average_predicted_data[year] - year_wise_dict[year])
        perDiff += (errorDiff / (year_wise_dict[year] * 1.0)) * 100

    print("Error Rate is : ", perDiff / 4)

    if GRAPH_FLAG is True:
        # Plotting graph for moving average
        plt.plot(year_wise_dict.keys(), year_wise_dict.values(), color='b')
        plt.plot(moving_average_predicted_data.keys(), moving_average_predicted_data.values(), color='y')
        plt.title("Moving Average Time Analysis, N = " + str(N) + " years")
        plt.xlabel("Year (2001-2014)")
        plt.ylabel("Number of Riots")
        plt.show()

    return moving_average_predicted_data


def returnYearWiseRiots(file_name, year_wise_dict, capsFlag):
    superDict = fetchYearRiots(file_name, capsFlag)

    if capsFlag is True:
        YEAR_COLUMN_NAME = 'YEAR'
        RIOTS_COLUMN_NAME = 'RIOTS'
    else:
        YEAR_COLUMN_NAME = 'Year'
        RIOTS_COLUMN_NAME = 'Riots'

    for item in superDict.values():
        if item[YEAR_COLUMN_NAME] not in year_wise_dict:
            year_wise_dict[item[YEAR_COLUMN_NAME]] = 0
        year_wise_dict[item[YEAR_COLUMN_NAME]] += item[RIOTS_COLUMN_NAME]

    return year_wise_dict;


def returnYearWiseCrimes(file_name, year_wise_dict, capsFlag):
    superDict = fetchYearCrimes(file_name, capsFlag)

    if capsFlag is True:
        YEAR_COLUMN_NAME = 'YEAR'
        CRIMES_COLUMN_NAME = 'TOTAL IPC CRIMES'
    else:
        YEAR_COLUMN_NAME = 'Year'
        CRIMES_COLUMN_NAME = 'Total Cognizable IPC crimes'

    for item in superDict.values():
        if item[YEAR_COLUMN_NAME] not in year_wise_dict:
            year_wise_dict[item[YEAR_COLUMN_NAME]] = 0
        year_wise_dict[item[YEAR_COLUMN_NAME]] += item[CRIMES_COLUMN_NAME]

    return year_wise_dict;


def initRiotsPrediction():
    year_wise_dict = {}

    # collecting the data
    year_wise_dict = returnYearWiseRiots(FILE_2001_2012, year_wise_dict, True)
    year_wise_dict = returnYearWiseRiots(FILE_2013, year_wise_dict, True)
    year_wise_dict = returnYearWiseRiots(FILE_2014, year_wise_dict, False)

    # predicting as per last observed data
    print("=======================Last Observed=========================>")
    last_observed_predicted_data = lastObserved(year_wise_dict, False)

    # predicting as moving average
    print("=======================Moving Average N = 5=========================>")
    moving_average_predicted_data = movingAverage(year_wise_dict, 5, False)

    # predicting as ewma
    print("=======================EWMA, alpha = 0.9=========================>")
    ewma_predicted_data = ewma(year_wise_dict, 0.9, False)

    # predicting as ewma
    print("=======================EWMA, alpha = 0.5=========================>")
    ewma_predicted_data = ewma(year_wise_dict, 0.5, False)

    # predicting as ar
    print("=======================AR, p = 3=========================>")
    ar_predicted_data = ar(year_wise_dict, 3, True)

    # predicting as ar
    print("=======================AR, p = 6=========================>")
    ar_predicted_data = ar(year_wise_dict, 6, False)


def initCrimesPrediction():
    year_wise_dict = {}

    # collecting the data
    year_wise_dict = returnYearWiseCrimes(FILE_2001_2012, year_wise_dict, True)
    year_wise_dict = returnYearWiseCrimes(FILE_2013, year_wise_dict, True)
    year_wise_dict = returnYearWiseCrimes(FILE_2014, year_wise_dict, False)

    # predicting as per last observed data
    print("=======================Last Observed=========================>")
    last_observed_predicted_data = lastObserved(year_wise_dict, False)

    # predicting as moving average
    print("=======================Moving Average N = 5=========================>")
    moving_average_predicted_data = movingAverage(year_wise_dict, 5, False)

    # predicting as ewma
    print("=======================EWMA, alpha = 0.9=========================>")
    ewma_predicted_data = ewma(year_wise_dict, 0.9, False)

    # predicting as ewma
    print("=======================EWMA, alpha = 0.5=========================>")
    ewma_predicted_data = ewma(year_wise_dict, 0.5, False)

    # predicting as ar
    print("=======================AR, p = 6=========================>")
    ar_predicted_data = ar(year_wise_dict, 6, False)

    # predicting as ar
    print("=======================AR, p = 3=========================>")
    ar_predicted_data = ar(year_wise_dict, 3, True)

    # ar(year_wise_dict, 5)


if __name__ == "__main__":
    print("#######################Predicting Riots Till 2020#######################")
    initRiotsPrediction()
    print("\n\n\n\n")
    print("#######################Predicting Crimes Till 2020#######################")
    initCrimesPrediction()
