
# %%
import datetime as dt
#%%

import glob

import matplotlib as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from datetime import timezone


# Standard quick checks
def dfChkBasics(dframe, valCnt = False): 
  cnt = 1
  print('\ndataframe Basic Check function -')
  
  try:
    print(f'\n{cnt}: info(): ')
    cnt+=1
    print(dframe.info())
  except: pass

  print(f'\n{cnt}: describe(): ')
  cnt+=1
  print(dframe.describe())

  print(f'\n{cnt}: dtypes: ')
  cnt+=1
  print(dframe.dtypes)

  try:
    print(f'\n{cnt}: columns: ')
    cnt+=1
    print(dframe.columns)
  except: pass

  print(f'\n{cnt}: head() -- ')
  cnt+=1
  print(dframe.head())

  print(f'\n{cnt}: shape: ')
  cnt+=1
  print(dframe.shape)

  if (valCnt):
    print('\nValue Counts for each feature -')
    for colname in dframe.columns :
      print(f'\n{cnt}: {colname} value_counts(): ')
      print(dframe[colname].value_counts())
      cnt +=1

# examples:
#dfChkBasics(df)
#%%
## DC data clean up and shaping 
#read in data sets for DC
#%%


mar19= pd.read_csv("DC_Mar19.csv")
print("mar")
print(mar19.columns)
april19= pd.read_csv("DC_Apr19.csv")
print("apr")
print(april19.columns)
may19= pd.read_csv("DC_May19.csv")
print("may")
print(may19.columns)
june19= pd.read_csv("DC_Jun19.csv")
print("june")
print(june19.columns)
march20= pd.read_csv("DC_Mar20.csv")
print("mar")
print(march20.columns)
april20= pd.read_csv("DC_Apr20.csv")
print("april")
print(april20.columns)
may20=pd.read_csv("DC_May20.csv")
print("May")
print(may20.columns)
jun20= pd.read_csv("DC_jun20.csv")
end_stat=pd.read_csv("end.csv")
start_stat=pd.read_csv("start.csv")

#%%
print(len(may20))
print(len(may19))
print(len(april19))
print(len(april20))
print(len(mar19))
print(len(march20))
#%%

#print data sets to take a look # seems that april has different columns names


print("_____break_______")
#Rename columns 
april20.rename(columns={'started_at': 'Start date', 'ended_at': 'End date','start_station_name': 'Start station','start_station_id': 'Start station number','end_station_name': 'End station','end_station_id': 'End station number','member_casual': 'Member type', }, inplace=True)
may20.rename(columns={'started_at': 'Start date', 'ended_at': 'End date','start_station_name': 'Start station','start_station_id': 'Start station number','end_station_name': 'End station','end_station_id': 'End station number','member_casual': 'Member type', }, inplace=True)
jun20.rename(columns={'started_at': 'Start date', 'ended_at': 'End date','start_station_name': 'Start station','start_station_id': 'Start station number','end_station_name': 'End station','end_station_id': 'End station number','member_casual': 'Member type', }, inplace=True)

#%%
#check for column renaming 
april20_head= april20.head()
print(april20_head)



#%%
print(april20.head())
#%%

#%%
#make the df's ready for concatination 
frames=[mar19, april19, may19, june19, march20, april20, may20, jun20]

#concat all the dataframes and drop column that won't be used 
dc_data = pd.concat(frames)
 

#%%
#dc_data=dc_data.merge(april20, on="Start station", how="inner")

dc_data=dc_data.merge(start_stat, on="Start station", how="left")

dc_data=dc_data.merge(end_stat, on="End station", how="left")
print("complete - ready to continue")  



#null_data=dc_data.isnull.sum()

#print("ready")
#print(null_data)



#%% # Function to get percents of missing values 
def missing_values_table(df):
    # Utility function, identify missing data and show percentages.
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
    columns = {0 : 'Missing Values', 1 : '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\nThere are " + str(mis_val_table_ren_columns.shape[0]) + " columns that have missing values.")
    return mis_val_table_ren_columns




#%%
#function to determine if data is missing 
missing_values_table(dc_data)



# %%
print(len(dc_data))

# %%
#dc_data=dc_data.drop(columns=["end_lat", "end_lng", "start_lat", "start_lng"])	 
# drop small na's
dc_data=dc_data.dropna(subset=["End station number"])
dc_data=dc_data.dropna(subset=["Start date"])
dc_data=dc_data.dropna(subset=["End date"])
dc_data=dc_data.dropna(subset=["Member type"])
dc_data=dc_data.dropna(subset=["end_lat_y"])
dc_data=dc_data.dropna(subset=["end_lng_y"])
dc_data=dc_data.dropna(subset=["start_lat_y"])
dc_data=dc_data.dropna(subset=["start_lng_y"])
dc_data=dc_data.dropna(subset=["Start station number"])
dc_data=dc_data.dropna(subset=["Start station"])

# %%
missing_values_table(dc_data)




#%%
dfChkBasics(dc_data)
print(len(dc_data))
# %%
# standardize categorical columns/ and date time columns create new categorical columns
dc_data.rename(columns={"Start date": "start_date", "End date": "end_date",}, inplace=True)
dc_data["Member type"].replace({"member": "Member", "casual": "Casual"}, inplace=True)


#%%
def create_dto(row, colname):
# for index, row in dc_data.iterrows():
    if type(row[colname]) is not str:
        return "Unknown"
    else:
        # Try the various known time formats.
        dtFormat = [
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%y %H:%M',
        ]
        # save cell data to local variable
        cell_contents = row[colname]
        # Drop decimal timestamp precision, if it exists.
        cell_contents = cell_contents.split('.')[0]
        for i in dtFormat:
            try:
                dto = dt.datetime.strptime(cell_contents,i)
                return (
                    dto,
                    dto.strftime("%Y-%m-%d"),
                    dto.strftime("%H:%M")
                 )
            except ValueError:
                pass
        else:
            print("Failed to parse: {:s}".format(cell_contents))
dc_data['start_dto'], dc_data['start_date_formatted'], dc_data['start_time_formatted'] \
    = zip(*dc_data.apply(lambda row: create_dto(row,"start_date"), axis=1))
dc_data['end_dto'], dc_data['end_date_formatted'], dc_data['end_time_formatted'] \
    = zip(*dc_data.apply(lambda row: create_dto(row,"end_date"), axis=1))
    
print(dc_data.tail())

dc_data['weekday'] = dc_data.apply(lambda row: row["start_dto"].weekday() < 5, axis=1)

#%%

print(len(dc_data))
# %%
def determine_pandemic(row):
# for index, row in dc_data.iterrows():
    dto = row["start_dto"]
    if dto.year == 2020:
        return True
    return False
dc_data['pandemic'] = dc_data.apply(lambda row: determine_pandemic(row), axis=1)
#%%
def determine_commuter(row):
# for index, row in dc_data.iterrows():
    dto = row["start_dto"]
    weekday=row["weekday"]
    if (dto.hour in range(6, 10) or dto.hour in range(16, 19)) and weekday:
        return True
    return False
dc_data['commuter'] = dc_data.apply(lambda row: determine_commuter(row), axis=1)

#%%
print(dc_data.head())
#%%
dc_data['Duration'] = dc_data.apply(lambda row: (row["end_dto"] - row["start_dto"]).total_seconds(), axis=1)
#%%
# drop excessive duration 
dc_data=dc_data[dc_data["Duration"]<18000]
dc_data=dc_data[dc_data["Duration"]>60]

print(len(dc_data))



#%%
missing_values_table(dc_data)


#%%
# add year/month column 
dc_data['Month_Year'] = dc_data['end_dto'].dt.strftime('%Y-%m')

dc_data['day_of_week'] = dc_data['end_dto'].dt.day_name()
print("complete - ready to continue")  
#%%
missing_values_table(dc_data)
#%%
print(dc_data.columns)


#%%
# function to make commuter/pandemic column 
def make_pandemic_commuter(row):
    if row['pandemic'] and row['commuter']:
        return "Pandemic Commuter"
    elif row['pandemic'] and not row['commuter']:
        return "Pandemic Noncommuter"
    elif not row['pandemic'] and row['commuter']:
        return "Nonpandemic Commuter"
    elif not row['pandemic'] and not row['commuter']:
        return "Nonpandemic Noncommuter"
dc_data['pandemic-commuter'] = dc_data.apply(lambda row: make_pandemic_commuter(row), axis=1)


#%%
# function to make weekend column
def make_pandemic_weekend(row):
    if row['pandemic'] and row['weekday']:
        return "Pandemic Weekday"
    elif row['pandemic'] and not row['weekday']:
        return "Pandemic Nonweekday"
    elif not row['pandemic'] and row['weekday']:
        return "Nonpandemic Weekday"
    elif not row['pandemic'] and not row['weekday']:
        return "Nonpandemic Nonweekday"
dc_data['pandemic-weekday'] = dc_data.apply(lambda row: make_pandemic_weekend(row), axis=1)


#%%

dc_data.to_csv("dc_data.csv")
#%%
colum=dc_data[dc_data["Start station"]== "Yuma St & Tenley Circle NW"]
#%%


#%%
len(colum)





# %%
