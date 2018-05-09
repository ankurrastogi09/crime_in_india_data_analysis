from sklearn import linear_model
from numpy import array
from parse_data import parseData
import matplotlib.pyplot as plt
from plot import scatterPlot, linePlot, PlotWrapper

PATH = "/Users/vineeth/SBU/SEM-2/Probability/crime-in-india/crime/"
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

	data = dict()
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2001_2012.csv",["TOTAL IPC CRIMES"],data)
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2013.csv",["TOTAL IPC CRIMES"],data)
	parseData(PATH+"01_District_wise_crimes_committed_IPC_2014.csv",["Total Cognizable IPC crimes"],data)
	computeLinearRegression(data,total_crime)

	# data = dict()
	# parseData(PATH+"01_District_wise_crimes_committed_IPC_2001_2012.csv",["RAPE"],data)
	# parseData(PATH+"01_District_wise_crimes_committed_IPC_2013.csv",["RAPE"],data)
	# print(computeLinearRegression(data,total_rape))

	#computeLinearRegression(data,total_crime,["MUMBAI COMMR.", "MUMBAI RLY.", "NAVI MUMBAI", "MUMBAI"])
	linearRegression([range(1,20)],total_crime)
	#PlotWrapper({0: [[range(1,15)],total_crime], 1: [[range(1,15)],[total_rape]]},"SCATTER")

linearRegressionWrapper()