
# %%
import datetime as dt
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


#load in NYC data
ny_data1=glob.glob("NY*.csv") 

print("complete")

ny_data = []

for file in ny_data1:
  ny_data.append(pd.read_csv(file))
  
ny_data = pd.concat(ny_data)

print("complete")


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
missing_values_table(ny_data)




# %%
# drop missing values since there are few  
ny_data=ny_data.dropna()	 


# %%
missing_values_table(ny_data)


#%%
dfChkBasics(ny_data)
print(ny_data.tail())
# %%
ny_data.rename(columns={"starttime": "start_date", "stoptime": "end_date","tripduration" :"Duration", "start station id": "Start station number", "start station name" : "Start station", 
                        "start station latitude" : "start_lat_y", "start station longitude" : 'start_lng_y',"end station id" : "End station number","end station name" : "End station" ,
                         "end station latitude" :  "end_lat_y" ,"end station longitude" : "end_lng_y", "bikeid" : "Bike number",
                         "usertype": "Member type" 
  }, inplace=True)
ny_data["Member type"].replace({"Subscriber": "Member", "Customer": "Casual"}, inplace=True)


#%%
print(ny_data.tail())


#%%
def create_dto(row, colname):  # need fix!!!!!
# for index, row in ny_data.iterrows():
    if type(row[colname]) is not str:
        return "Unknown"
    else:
        # Try the various known time formats.
        dtFormat = [
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%y %H:%M',
            '%H:%M:%S %Y-%m-%d',
            '%M: %Y-%m-%d'
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
ny_data['start_dto'], ny_data['start_date_formatted'], ny_data['start_time_formatted'] \
    = zip(*ny_data.apply(lambda row: create_dto(row,"start_date"), axis=1))
ny_data['end_dto'], ny_data['end_date_formatted'], ny_data['end_time_formatted'] \
    = zip(*ny_data.apply(lambda row: create_dto(row,"end_date"), axis=1))
    
print(ny_data.tail())

ny_data['weekday'] = ny_data.apply(lambda row: row["start_dto"].weekday() < 5, axis=1)

# %%
def determine_pandemic(row):
# for index, row in ny_data.iterrows():
    dto = row["start_dto"]
    if dto.year == 2020:
        return True
    return False
ny_data['pandemic'] = ny_data.apply(lambda row: determine_pandemic(row), axis=1)
#%%
def determine_commuter(row):
# for index, row in ny_data.iterrows():
    dto = row["start_dto"]
    weekday=row["weekday"]
    if (dto.hour in range(6, 10) or dto.hour in range(16, 19)) and weekday:
        return True
    return False
ny_data['commuter'] = ny_data.apply(lambda row: determine_commuter(row), axis=1)

#%%
print(ny_data.head())
#%%
ny_data['Duration'] = ny_data.apply(lambda row: (row["end_dto"] - row["start_dto"]).total_seconds(), axis=1)
#%%
# drop excessive duration 
ny_data=ny_data[ny_data["Duration"]<18000]
ny_data=ny_data[ny_data["Duration"]>60]

print(len(ny_data))



#%%
missing_values_table(ny_data)


#%%
# add year/month column 
ny_data['Month_Year'] = ny_data['end_dto'].dt.strftime('%Y-%m')

ny_data['day_of_week'] = ny_data['end_dto'].dt.day_name()
print("complete - ready to continue")  
#%%
missing_values_table(ny_data)
#%%
print(ny_data.columns)


#%%
# function to make commuter/pandemic graph 
def make_pandemic_commuter(row):
    if row['pandemic'] and row['commuter']:
        return "Pandemic Commuter"
    elif row['pandemic'] and not row['commuter']:
        return "Pandemic Noncommuter"
    elif not row['pandemic'] and row['commuter']:
        return "Nonpandemic Commuter"
    elif not row['pandemic'] and not row['commuter']:
        return "Nonpandemic Noncommuter"
ny_data['pandemic-commuter'] = ny_data.apply(lambda row: make_pandemic_commuter(row), axis=1)
#%%
def draw_commuting_share(df):
    dfg = df.groupby('pandemic-commuter').count().reset_index()
    dfg = dfg.rename(columns={"start_date": "Users"})
    fig = px.bar(dfg, x='pandemic-commuter', y='Users')
    fig.show()
draw_commuting_share(df = ny_data[ny_data['pandemic']==True])
draw_commuting_share(ny_data)

#%%
def make_pandemic_weekend(row):
    if row['pandemic'] and row['weekday']:
        return "Pandemic Weekday"
    elif row['pandemic'] and not row['weekday']:
        return "Pandemic Nonweekday"
    elif not row['pandemic'] and row['weekday']:
        return "Nonpandemic Weekday"
    elif not row['pandemic'] and not row['weekday']:
        return "Nonpandemic Nonweekday"
ny_data['pandemic-weekday'] = ny_data.apply(lambda row: make_pandemic_weekend(row), axis=1)
#%%
def draw_weekend_share(df):
    dfwk = df.groupby('pandemic-weekday').count().reset_index()
    dfwk = dfwk.rename(columns={"start_date": "Users"})
    fig1 = px.bar(dfwk, x='pandemic-weekday', y='Users')
    fig1.show()
draw_weekend_share(df = ny_data[ny_data['pandemic']==True])
draw_weekend_share(ny_data)
print("complete - ready to continue")  

#%%

ny_data.to_csv("ny_data.csv")

#%%
#ny pandemic frame 
ny_pandemic= ny_data["pandemic"]== True
ny_pandemic= ny_data[ny_pandemic]
print(len(ny_pandemic))

# ny non Pandemic FRame 
ny_nonpandemic= ny_data["pandemic"]== False
ny_nonpandemic= ny_data[ny_nonpandemic]
print(len(ny_nonpandemic))




