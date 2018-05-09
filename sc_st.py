from parse_data import parseData

FilesToRead = ["02_01_District_wise_crimes_committed_against_SC_2001_2012.csv", "02_District_wise_crimes_committed_against_ST_2001_2012.csv"]

PATH = "/Users/vineeth/SBU/SEM-2/Probability/crime-in-india/crime/"

SP = [2002,2003,2004,2005,2006]
BSP = [2008,2009,2010,2011,2012]

COLUMNS_SC = ["STATE/UT","Murder","Rape","Kidnapping and Abduction","Dacoity","Robbery","Arson","Hurt","Prevention of atrocities (POA) Act","Protection of Civil Rights (PCR) Act","Other Crimes Against SCs"]
COLUMNS_ST = ["STATE/UT","Murder","Rape","Kidnapping Abduction","Dacoity","Robbery","Arson","Hurt","Protection of Civil Rights (PCR) Act","Prevention of atrocities (POA) Act","Other Crimes Against STs"]

def summateCrimes(data,total_dict_1=dict(),total_dict_2=dict()):

	for key,value in data.items():
		if 'UTTAR PRADESH' in value.get('state/ut').values():
			for crime,years in value.items():
				if crime != 'state/ut' and crime != 'year':
					for year,count in years.items():
						if int(year) in SP:
							if total_dict_1.get(key):
								total_dict_1[key]+= count
							else:
								total_dict_1[key] = count
						elif int(year) in BSP:
							if total_dict_2.get(key):
								total_dict_2[key]+= count
							else:
								total_dict_2[key] = count

	return total_dict_1, total_dict_2

def scst():
	data = dict()
	total_dict_1 = dict()
	total_dict_2 = dict()
	
	parseData(PATH+FilesToRead[0],COLUMNS_SC,data)
	parseData(PATH+FilesToRead[1],COLUMNS_ST,data)

	total_dict_1,total_dict_2 = summateCrimes(data)

scst()