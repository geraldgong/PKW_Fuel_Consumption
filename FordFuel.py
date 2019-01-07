
# coding: utf-8

# In[10]:

import pandas as pd
dataOld = pd.read_csv("bigfu.csv", sep =';')
dataOld = dataOld.drop(['BenutzerNr', 'FahrzeugNr', 'Strecke', 'KraftstoffNr',  \
                  		'Kraftstoff', 'Notiz', 'Verbrauch', 'Sparsam', \
                  		'Normal', 'Schnell', 'Winter', 'Sommer', 'Ganzjahr',  \
                  		'Stadt', 'Land', 'Autobahn', 'Klima', 'Anhaenger'], axis=1)
dataOld.head()


# In[100]:

dataNew = pd.read_csv("bigfuNew.csv", sep = r'\t', engine='python')
data = pd.concat([dataOld, dataNew])
ordData = data.sort_values(by='Datum')
carInfo = pd.DataFrame(ordData)
carInfo['Datum'] = pd.to_datetime(carInfo.Datum)
carInfo['Tankmenge'] = pd.to_numeric(carInfo.Tankmenge.apply(lambda x: x.replace(',','.')))
carInfo['Kosten'] = pd.to_numeric(carInfo.Kosten.apply(lambda x: x.replace(',','.')))
carInfo['Price'] = (carInfo.Kosten/carInfo.Tankmenge).round(3)
# tank = pd.to_numeric(ordData.Tankmenge.apply(lambda x: x.replace(',','.')))
# kosten = pd.to_numeric(ordData.Kosten.apply(lambda x: x.replace(',','.')))
carInfo = carInfo.set_index('Datum')
carInfo.head()


# In[102]:

d2016 = pd.datetime(2016,1,1)
d2017 = pd.datetime(2017,1,1)
d2018 = pd.datetime(2018,1,1)
d2019 = pd.datetime(2019,1,1)
carInfo[d2016:d2017]


# In[ ]:



