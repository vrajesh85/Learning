import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

myDataSet = {
    'cars' : ['BMW','Audi','Honda'],
    'years' : [2026, 2025, 2024]
}

# print(f'the version of pandas is {pd.__version__}')
myVar = pd.DataFrame(myDataSet, index = ['car1','car2','car3'])

# print(myVar)
# print(myVar.loc[['car1','car2']])

# Series is like column in a table and it represents one dimensional array. It can be 
arr = [10, 20, 30, 'Rajesh']

myVar = pd.Series(arr, index = ["A","B","C","D"])

# print(myVar)

# print(myVar['C'])

calories = {
    'day1' : 100,
    'day2' : 200,
    'day3' : 300
}

myVar = pd.Series(calories, index = ['day1','day2'])

# print(myVar)

dataFile = pd.read_csv(r"C:\Users\rvemula1\Downloads\data.csv")

# by default pandas returns first 5 rows and last 5 rows, now with this setting we can change that
pd.options.display.max_rows = 10

# print(dataFile)
# print(dataFile.to_string())

# print(f'total duplicates are {dataFile.duplicated()}')

dataFile = pd.read_json(r"C:\Users\rvemula1\Downloads\data.json")
# print('reading JSON')
# print(dataFile.to_string())


data = {
  "Duration":{
    "0":60,
    "1":60,
    "2":60,
    "3":45,
    "4":45,
    "5":60
  },
  "Pulse":{
    "0":110,
    "1":117,
    "2":103,
    "3":109,
    "4":117,
    "5":102
  },
  "Maxpulse":{
    "0":130,
    "1":145,
    "2":135,
    "3":175,
    "4":148,
    "5":127
  },
  "Calories":{
    "0":409,
    "1":479,
    "2":340,
    "3":282,
    "4":406
  }
}

df = pd.DataFrame(data)

print(df)

print('data info')

print(df.info())

df.plot()

plot.show()