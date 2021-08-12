import numpy as np
import pandas as pd
#from pandas import Series, DataFrame
import csv
from numpy import arange

address = 'C:/Users/Lillian/Desktop/ExerciseFiles/Data/mtcars.csv'

cars = pd.read_csv(address)

cars.columns = ['car_names', 'mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
cars.head()

df = pd.read_excel("C:/Users/ying.fan/Downloads/OBD2_Reporting.xlsx", sheet_name="OBD2")
mylist = df['SerialNumber'].tolist()
print(mylist)

def remove(listA, listB):
    for item in listB:
        listA.remove(item)
    return listA

listA = [1, 1, 2, 3, 4]
listB = [1, 2, 3]
remove(listA, listB)

xl = pd.ExcelFile("C:/Users/ying.fan/Downloads/pandas_multiple.xlsx")
dfs = {sheet_name: xl.parse(sheet_name) 
          for sheet_name in xl.sheet_names}
#df00= pd.DataFrame(['Weekly Update', 'Total No.', 'HW/FW revision'], columns=['0'])
df = dfs['summary']

def color_red(val):
    color = 'black'
    if type(val)==str and val.endswith('%'):
        val_num = val.strip('%').replace('.','',1)
        if val_num.isdigit():
            if int(val_num)>500:
                color ='red'
            else:
                color = 'green' 
    return 'color: %s' % color

def color_red2(val):     
    color = 'black'
    try:
        if not val.endswith('%'): 
            pass
        elif float(val.rstrip('%')) > 5:
            color ='red'
        else:
            color = 'green'
    except:
        pass
    
    return 'color: %s' % color

#df.style.apply(lambda x: ['font-weight:bold' if x.name == 'A' or i < 6 else '' for i,_ in x. iteritems()])
#df.style.apply(lambda x: ['background-color:#a9b2bc'  if i<3 else '' for i,_ in x. iteritems()])\
#.apply(lambda x: ['background-color:	#8c99a6'  if 2<i < 5 else '' for i,_ in x. iteritems()])\
#.apply(lambda x: ['background-color:	#c5ccd2'  if x.name == 'A' else '' for i,_ in x. iteritems()])\
df.style.applymap(color_red2)
#'10.00%'.strip('%').replace('.','',1).isdigit()
