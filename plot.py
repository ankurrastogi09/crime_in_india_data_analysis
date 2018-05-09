import matplotlib.pyplot as plt
from numpy import array

COLOR = ['blue', 'red', 'green', 'orange', 'magenta']

def scatterPlot(data_obj):

	for k,v in data_obj.items():
		plt.scatter(array(v[0]).reshape(-1,1), array(v[1]).reshape(-1,1),  color=COLOR[k])
	plt.show()

def linePlot(data_obj):

	for k,v in data_obj.items():
		plt.plot(array(v[0]).reshape(-1,1), array(v[1]).reshape(-1,1), color=COLOR[k], linewidth=3)
	plt.show()
	

# data_obj: 
# {	0: [[range(1,15)],total_crime], 
# 	1: [[range(1,15)],[total_rape]]
# }
def PlotWrapper(data_obj, plot_type="LINE"):

		if plot_type == "LINE":
			linePlot(data_obj)
		else:
			#SCATTER PLOT
			scatterPlot(data_obj)