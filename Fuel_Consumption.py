import streamlit as st


import pandas as pd
import numpy as np
import datetime as datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import six
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
import warnings


dataOld = pd.read_csv("bigfu.csv", sep =';')
dataOld = dataOld.drop(['BenutzerNr', 'FahrzeugNr', 'Strecke', 'KraftstoffNr',  
                  'Kraftstoff', 'Notiz', 'Verbrauch', 'Sparsam', 
                  'Normal', 'Schnell', 'Winter', 'Sommer', 'Ganzjahr', 
                  'Stadt', 'Land', 'Autobahn', 'Klima', 'Anhaenger'], axis=1)
dataNew = pd.read_csv("bigfuNew.csv", sep = r'\t', engine='python')
data = pd.concat([dataOld, dataNew])
ordData = data.sort_values(by='Datum')
carInfo = pd.DataFrame(ordData)
carInfo['Datum'] = pd.to_datetime(carInfo.Datum)
carInfo['Tankmenge'] = pd.to_numeric(carInfo.Tankmenge
                                     .apply(lambda x: x.replace(',','.')))
carInfo['Kosten'] = pd.to_numeric(carInfo.Kosten
                                  .apply(lambda x: x.replace(',','.')))
carInfo['Preis'] = (carInfo.Kosten/carInfo.Tankmenge).round(3)
carInfo = carInfo.set_index('Datum')

# Change tires dates
SummerTires = pd.DataFrame({'year': [2016, 2017, 2018, 2019],
                            'month': [4, 3, 4, 4],
                            'day': [1, 29, 3, 3]})
SummerTires = pd.to_datetime(SummerTires)
WinterTires = pd.DataFrame({'year': [2016, 2017, 2018, 2019],
                            'month': [10, 11, 10, 9],
                            'day': [12, 6, 19, 28]})
WinterTires = pd.to_datetime(WinterTires)

d2016 = pd.datetime(2016,1,1)
d2017 = pd.datetime(2017,1,1)
d2018 = pd.datetime(2018,1,1)
d2019 = pd.datetime(2019,1,1)
d2020 = pd.datetime(2020,1,1)

# Diesel Price (euro/L)
dist = []
[dist.append(carInfo.Laufleistung[i+1] - carInfo.Laufleistung[i]) 
 for i in range(0, len(carInfo)-1)]
dist.insert(0,0) # Erstbetankung
carInfo['Distanz'] = dist
print("Annual Distance (km): ")
print(carInfo.groupby(pd.PeriodIndex(carInfo.index, freq='A'),
                      axis=0)['Distanz'].sum())
print("---------------------------------------------------------------------------------")

fig0 = plt.figure(figsize=(10,6))
ax0 = plt.subplot(111)
carInfo['Preis'].plot(ax=ax0, kind = 'line')
ax0.xaxis_date()
plt.xticks(rotation=60, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("date", fontsize=14)
plt.ylabel("Fuel Price (Euro/L)", fontsize=14)
plt.grid(b=None, which='major', axis='x')
plt.title("Diesel Price", fontsize=16)
# plt.savefig('FuelPrice.pdf', bbox_inches='tight',dpi=300)

AvgConsp = sum(carInfo.Tankmenge)/sum(carInfo.Distanz)*100
print("Average fuel consumption is %.2f L/100km." % AvgConsp)
print("---------------------------------------------------------------------------------")

# get index of the not fully fuelled records
idx = [i for i in range(0, len(carInfo)) if carInfo.ArtNr[i] == 2] 
idx_next = [item + 1 for item in idx]

carInfo.ix[idx_next, 'Tankmenge'] = carInfo.ix[idx_next, 'Tankmenge'].values + carInfo.ix[idx, 'Tankmenge'].values
carInfo.ix[idx_next, 'Distanz'] = carInfo.ix[idx_next, 'Distanz'].values + carInfo.ix[idx, 'Distanz'].values

carInfo = carInfo.drop(carInfo[carInfo.ArtNr != 1].index)
carInfo['Verbrauch'] = (carInfo.Tankmenge/carInfo.Distanz*100).round(2)

print("Situation since 2020: ")
print(carInfo[d2020:])
print("---------------------------------------------------------------------------------")


# # Machine Learning Model

# In[3]:


carInfo.head()
X = (carInfo.index - carInfo.index[0]).days.values.reshape(-1,1)
sc = StandardScaler()
sc.fit(X)
X_std = sc.transform(X)
y = carInfo['Verbrauch'].values
svr = SVR(kernel='rbf', C=1e2, gamma= 2).fit(X_std, y)
y_fit = svr.predict(X_std)

fig = plt.figure(figsize=(10,6))
ax = plt.subplot(111)
plt.plot(carInfo.index, y_fit, 
         label="Regression Model", color = 'r')
plt.scatter(carInfo.index, y, edgecolor='b', s=15, label="Data")
plt.axhline(y = AvgConsp, linestyle='--', color = 'k', alpha = 0.6, 
            label = "Average Consumption")
# format
xlabel = ax.get_xticks().tolist()
ax.xaxis_date()
plt.xticks(rotation=60, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc="lower left")
plt.xlabel("Date", fontsize=14)
plt.ylabel("Fuel Consumption (L/100km)", fontsize=14)
for i in range(len(SummerTires)):
    plt.axvline(x=SummerTires[i], linewidth = 1, color = 'y',
                alpha = 0.3, label = "Summer Tires")
for i in range(len(WinterTires)):
    plt.axvline(x=WinterTires[i], linewidth = 1, color = 'c', 
                alpha = 0.3, label = "Winter Tires")

plt.savefig('FuelConsumption.pdf', bbox_inches='tight', dpi = 300)


# In[ ]:




