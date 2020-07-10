#%%
import datetime as dt
import glob

import matplotlib as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from datetime import timezone
import plotly
import plotly.graph_objects as go
#%%
ny_data=pd.read_csv("ny_data.csv")
end=pd.read_csv("newyork_end.csv")
start=pd.read_csv("newyork_start.csv")
ny_data.rename(columns={" Start station" :"Start station"}, inplace=True)

#%%
ny_covid=pd.read_csv("newyorkcovid.csv")
print(ny_covid.head())
#%% 
print(len(ny_data))
#%%
ny_data.columns
#%%
#ny_data["start_hour"]= ny_data["start_dto"].dt.hour
ny_data["start_hour"]= pd.DatetimeIndex(ny_data['start_dto']).hour

#ny pandemic frame 
ny_pandemic= ny_data["pandemic"]== True
ny_pandemic= ny_data[ny_pandemic]
ny_pandemic=ny_pandemic[ny_pandemic["end_dto"].between("2020-02-29","2020-07-01",inclusive= True)]
print(len(ny_pandemic))


# ny non Pandemic Frame 
ny_nonpandemic= ny_data["pandemic"]== False
ny_nonpandemic= ny_data[ny_nonpandemic]
ny_nonpandemic=ny_nonpandemic[ny_nonpandemic["end_dto"].between("2019-03-01","2019-07-01",inclusive= True)]
print(len(ny_nonpandemic))
#%%

def draw_commuting_share(df):
    dfg = df.groupby('pandemic-commuter').count().reset_index()
    dfg = dfg.rename(columns={"start_date": "Users"})
    fig = px.bar(dfg, x='pandemic-commuter', y='Users', 
                 title= "Commuter versus Noncommuter Riders- Nonpandemic & Pandemic", color_discrete_sequence =['#0000ff']*len(dfg))
    fig.show()
    fig.write_html("./templated-transitive/graphs/fig80ny.html")
draw_commuting_share(df = ny_data[ny_data['pandemic']==True])
draw_commuting_share(ny_data)

def draw_weekend_share(df):
    dfwk = df.groupby('pandemic-weekday').count().reset_index()
    dfwk = dfwk.rename(columns={"start_date": "Users"})
    fig1 = px.bar(dfwk, x='pandemic-weekday', y='Users', title= "Weekday vs Weekend Riders- Nonpandemic & Pandemic", 
    color_discrete_sequence =['#0000ff']*len(dfwk))
    fig1.show()
    fig1.write_html("./templated-transitive/graphs/fig61ny.html")
draw_weekend_share(df = ny_data[ny_data['pandemic']==True])
draw_weekend_share(ny_data)
print("complete - ready to continue")  

#%%# violin plot showing duration of rides pandemic 

'''
fig = px.violin(ny_pandemic, y="Duration", title= "Duration of Ride- Pandemic")
fig.show()

print("complete - ready to continue")  
'''
#%%
# violin plot showing duration of rides non pandemic 
'''
fig1 = px.violin(ny_nonpandemic, y="Duration", title= "Duration of Ride- Nonpandemic")
fig1.show()
'''


#%%
#filter for sub 5000 pandemic

ny_pandemicsub5000=ny_pandemic[ny_pandemic["Duration"]<5000]

#%%

#box plot for sub 5000 Pandemic
'''
fig = px.box(ny_pandemicsub5000, y="Duration", title= "Duration of Ride- Pandemic")
fig.show()

print("complete - ready to continue")  
'''
#%%

#filter for sub 5000 non pandemic
ny_nonpandemicsub5000=ny_nonpandemic[ny_nonpandemic["Duration"]<5000]
#box plot for sub 5000 non pandemic 

#fig = px.box(ny_nonpandemicsub5000, y="Duration", title= "Duration of Ride- Nonpandemic")
#fig.show()

print("complete - ready to continue")  


#%%

# member type duration pandemic 
'''
fig = px.box(ny_pandemicsub5000, y="Duration", x="day_of_week", color="Member type",
             title= "Duration by Member Type- Pandemic")
fig.update_traces(marker_color="#33ff99")
fig.show()
'''
#%%
# member type duration nonpandemic 
'''
fig1 = px.box(ny_nonpandemicsub5000, y="Duration", x="Member type", title= "Duration by Member Type- Nonpandemic")
fig1.show()

'''
#%%
#histogram of pandemic rides per hour 
fighist = px.histogram(ny_pandemic, x="start_hour", title= "Start Hour of Ride- Pandemic")
fighist.update_traces(marker_color="#0000ff")
fighist.update_layout(xaxis_title='Start Hour',
                   yaxis_title='Users')   
fighist.show()
fighist.write_html("./templated-transitive/graphs/fig2ny.html")


#%%
#histogram of nonpandemic rides per hour
fighist = px.histogram(ny_nonpandemic, x="start_hour",  title= "Start Hour of Ride- Nonpandemic")
fighist.update_traces(marker_color="#33ff99")
fighist.update_layout(xaxis_title='Start Hour',
                   yaxis_title='Users')   
fighist.show()
fighist.write_html("./templated-transitive/graphs/fig3ny.html")


#%%
# rides each day of the week total 
# day of week rides during pandemic
cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dfpanweek = ny_pandemic.groupby('day_of_week').count().reindex(cats)
dfpanweek["day_of_week"]=dfpanweek.index
fig = px.bar(dfpanweek, x='day_of_week', y='start_date', title='Total Rides Per Day of the Week- Pandemic',
                    labels={'day_of_week': "Day of the Week", 'start_date':'Total Rides'},
                    color_discrete_sequence =['#0000ff']*len(dfpanweek))
fig.show()
fig.write_html("./templated-transitive/graphs/fig4ny.html")
#%%
dfnonpanweek = ny_nonpandemic.groupby('day_of_week').count().reindex(cats)
dfnonpanweek["day_of_week"]=dfnonpanweek.index
fig = px.bar(dfnonpanweek, x='day_of_week', y='start_date',  
                       title='Total Rides Per Day of the Week- Nonpandemic',
                       labels={'day_of_week': "Day of the Week", 'start_date':'Total Rides'},
                       color_discrete_sequence =['#33ff99']*len(dfnonpanweek),
                        )
fig.show()
fig.write_html("./templated-transitive/graphs/fig5ny.html")





#%%
#pie chart
dfpanpie = ny_pandemic.groupby('Member type').count().reset_index()
dfnonpanpie = ny_nonpandemic.groupby('Member type').count().reset_index()
 
#%%
#pie charts of members versus casual 
fig = px.pie(dfpanpie, values='pandemic', names='Member type', color= "Member type", labels= "Member type",title='Percent of Rider Type During Pandemic',
              color_discrete_map={'Member':'#0000ff',
                                 'Casual':'royalblue'})
fig.show()
fig.write_html("./templated-transitive/graphs/fig8ny.html")
fig = px.pie(dfnonpanpie, values='pandemic', names='Member type', color= "Member type", labels= "Member type",title='Percent of Rider Type During Non-Pandemic',
              color_discrete_map={'Member':'#33ff99',
                                 'Casual':'#009900'})
fig.show()
fig.write_html("./templated-transitive/graphs/fig9ny.html")


#%%
#line graphs 
# rides per day pandemic
ny_pandemicline=ny_pandemic.groupby('end_date_formatted').count().reset_index()
ny_pandemicline = ny_pandemicline.rename(columns={"start_date": "Users"})
fig = px.line(ny_pandemicline, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic', 
              color_discrete_sequence =['#0000ff']*len(dfpanweek))
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1week", step="day", stepmode="todate"),
            dict(count=1, label="1m", step="month", stepmode="todate"),
            dict(count=3, label="3m", step="month", stepmode="todate"),
            dict(step="all")
        ])
    ))
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/fig10ny.html")
#%%
#
# rides per day non pandemic
ny_nonpandemicline=ny_nonpandemic.groupby('end_date_formatted').count().reset_index()
ny_nonpandemicline = ny_nonpandemicline.rename(columns={"start_date": "Users"})
fig = px.line(ny_nonpandemicline, x="end_date_formatted", y="Users",title='Total Rides Per Day- Nonpandemic',
              color_discrete_sequence =['#33ff99']*len(dfnonpanweek))
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1week", step="day", stepmode="todate"),
            dict(count=1, label="1m", step="month", stepmode="todate"),
            dict(count=3, label="3m", step="month", stepmode="todate"),
            dict(step="all")
        ])
    ))
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/fig11ny.html")
#%%
#make data frame of first week pandemic started to spread
ny_pandemicline1stweek=ny_pandemic[ny_pandemic["end_date_formatted"].between("2020-03-01","2020-03-30",inclusive= True)]

ny_pandemicline1stweek=ny_pandemicline1stweek.groupby('end_date_formatted').count().reset_index()
ny_pandemicline1stweek = ny_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(ny_pandemicline1stweek, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic (Around time of Shutdown)', 
              color_discrete_sequence =['#0000ff']*len(dfpanweek))
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1day", step="day", stepmode="todate"),
            dict(count=7, label="1week", step="day", stepmode="todate"),
            dict(step="all")
        ])
    ))
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/fig12ny.html")

#%%
#make data frame of first week after George Floyd was killed 
ny_pandemicline1stweek=ny_pandemic[ny_pandemic["end_dto"].between("2020-05-18","2020-06-09",inclusive= True)]

ny_pandemicline1stweek=ny_pandemicline1stweek.groupby('end_dto').count().reset_index()
ny_pandemicline1stweek = ny_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(ny_pandemicline1stweek, x="end_dto", y="Users", title= 'Total Rides-Pandemic (before and after the death of George Floyd hourly Breakdown)',
              color_discrete_sequence =['#0000ff']*len(dfnonpanweek))
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1day", step="day", stepmode="todate"),
            dict(count=7, label="1week", step="day", stepmode="todate"),
            dict(count=1, label="1m", step="month", stepmode="todate"),
            dict(step="all")
        ])
    ))
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/fig13ny.html")
#%%
ny_pandemicline1stweek=ny_pandemic[ny_pandemic["end_date_formatted"].between("2020-05-18","2020-06-09",inclusive= True)]

ny_pandemicline1stweek=ny_pandemicline1stweek.groupby('end_date_formatted').count().reset_index()
ny_pandemicline1stweek = ny_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(ny_pandemicline1stweek, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic (before and after the death of George Floyd)')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1day", step="day", stepmode="todate"),
            dict(count=7, label="1week", step="day", stepmode="todate"),
            dict(step="all")
        ])
    ))
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/fig14ny.html")
#%%
ny_pandemicline1stweek=ny_pandemic[ny_pandemic["end_dto"].between("2020-05-18","2020-06-09",inclusive= True)]

ny_pandemicline1stweek=ny_pandemicline1stweek.groupby('end_dto').count().reset_index()
ny_pandemicline1stweek = ny_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(ny_pandemicline1stweek, x="end_dto", y="Users", title= 'Total Rides Per Day- Pandemic (before and after the death of George Floyd)')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=12, label="12hour", step="hour", stepmode="todate"),
            dict(count=1, label="1day", step="day", stepmode="todate"),
            dict(count=7, label="1week", step="day", stepmode="todate"),
            dict(step="all")
        ])
    ))
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/fig15ny.html")



#%%


#%%
ny_pandemic["Ride_taken"]=1


#%%# animation 
 #animation 
nypangroup=ny_pandemic.groupby(['start_hour','Member type']).count().reset_index()


fig = px.bar(nypangroup, x="Member type", y="Ride_taken", title= 'Total Rides Per Day- Pandemic', 
             animation_frame= "start_hour")
fig.show()

 #animation_frame="year", a"nimation_group="country,


#%%
ny_pandemic=ny_pandemic.dropna(subset=["End station number"])



#%%
# prepare data frame for end station pandemic 
endst_vc = ny_pandemic['End station'].value_counts()
endst_vc_df = pd.DataFrame({'End station' : endst_vc.index, 'Counts' : endst_vc.values})
endst_vc_df = endst_vc_df.merge(end, on="End station", how="left")
print(endst_vc_df[endst_vc_df['End station']=='Lincoln Memorial'])

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(endst_vc_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    hover_name="End station",
    title= "Ending Station of Rides Taken- Pandemic",
    #size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig16ny.html")
print("complete - ready to continue")  



#%%

# prepare data frame for start station pandemic 
stast_vc = ny_pandemic['Start station'].value_counts()
stast_vc_df = pd.DataFrame({'Start station' : stast_vc.index, 'Counts' : stast_vc.values})
stast_vc_df = stast_vc_df.merge(start, on="Start station", how="left")
#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(stast_vc_df,
    lat="start_lat_y",
    lon="start_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    hover_name="Start station",
    title= "Start Station of Rides Taken- Pandemic",
    #size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig17ny.html")
print("complete - ready to continue")  

#%%
#Nonpandemic Maps 

#%%
# prepare data frame for end station nonpandemic 
non_end_st_vc = ny_nonpandemic['End station'].value_counts()
non_end_st_vc_df = pd.DataFrame({'End station' : non_end_st_vc.index, 'Counts' : non_end_st_vc.values})
non_end_st_vc_df = non_end_st_vc_df.merge(end, on="End station", how="left")
print(non_end_st_vc_df[non_end_st_vc_df['End station']=='Lincoln Memorial'])

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(non_end_st_vc_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
     hover_name="End station",
    title= "Ending Station of Rides Taken- Nonpandemic",
    color_continuous_scale=px.colors.diverging.Portland,
    #size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig18ny.html")
print("complete - ready to continue")  



#%%

# prepare data frame for start station nonpandemic 
stast_vc = ny_nonpandemic['Start station'].value_counts()
stast_vc_df = pd.DataFrame({'Start station' : stast_vc.index, 'Counts' : stast_vc.values})
stast_vc_df = stast_vc_df.merge(start, on="Start station", how="left")
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(stast_vc_df,
    lat="start_lat_y",
    lon="start_lng_y",
    color="Counts",
    hover_name="Start station",
    title= "Starting Station of Rides Taken- Nonpandemic",
    color_continuous_scale=px.colors.diverging.Portland,
    #size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig19ny.html")
print("complete - ready to continue")  


#%%
#covid related graphs 
 
ny_pandemiclinecovid = ny_pandemic['end_date_formatted'].value_counts()
ny_pandemiclinecovid = pd.DataFrame({'end_date_formatted' : ny_pandemiclinecovid.index, 'Counts' : ny_pandemiclinecovid.values})

ny_pandemiclinecovid = ny_pandemiclinecovid.merge(ny_covid, on="end_date_formatted", how="left")
ny_pandemiclinecovid=ny_pandemiclinecovid.sort_values("end_date_formatted")
print(ny_pandemiclinecovid.head())
#%%
'''
print(ny_pandemiclinecovid['end_date_formatted'].dtypes)
#ny_pandemiclinecovid=int(ny_pandemicline["end_date_formatted"])
ny_pandemiclinecovid["graph_time"]=ny_pandemiclinecovid[ny_pandemiclinecovid["end_date_formatted"]].strftime('%m-%d-%y')

ny_pandemiclinecovid = ny_pandemiclinecovid.rename(columns={"end_date_formatted": "Users"})
fig = px.line(ny_pandemicline, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic')

fig = px.line(ny_pandemicline, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic')
fig.show()
fig.write_html("./templated-transitive/graphs/fig20ny.html")
print("complete - ready to continue")  
'''


#%%
# rides vs covid cases line and bar 
fig = go.Figure()

fig.add_trace(
    go.Bar(
      x=ny_pandemiclinecovid["end_date_formatted"], y=ny_pandemiclinecovid["Cases"], name= "Total Covid Cases Diagnosed",

))

fig.add_trace(
  go.Scatter(
        x=ny_pandemiclinecovid["end_date_formatted"], y=ny_pandemiclinecovid["Counts"],name= "Total Rides", line=dict(color="#7afbf9")
    ))
fig.update_layout(
    title = 'Time Series against Total Cases of Covid-19',
    xaxis_tickformat = '%Y-%m-%d',
)
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Instances')   
fig.write_html("./templated-transitive/graphs/fig21ny.html")
fig.show()
#%%
# rides vs covid cases line and bar- scatter bubble chart 
fig=px.scatter(ny_pandemiclinecovid, x="end_date_formatted", y="Counts", size= "Counts", color="Cases", animation_group= "Counts", 
               title="Total rides vs Total cases of Covid-19 Diagnosed", color_continuous_scale=px.colors.diverging.Portland
               #animation_frame= "end_date_formatted"
           )
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Rides')  
fig.write_html("./templated-transitive/graphs/fig22ny.html")
fig.show()

#%%
# prepare data frame for start station pandemic before george floyd demonstrations 
ny_panmay=ny_pandemic[ny_pandemic["start_date_formatted"]=="2020-05-23"]
ny_panmay = ny_panmay['Start station'].value_counts()
ny_panmay_df = pd.DataFrame({'Start station' : ny_panmay.index, 'Counts' : ny_panmay.values})
ny_panmay_df = ny_panmay_df.merge(start, on="Start station", how="left")
print(ny_panmay_df.head())
#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(ny_panmay_df,
    lat="start_lat_y",
    lon="start_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    hover_name="Start station",
    title="Total Rides by Start Station May 23, 2020", 
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig26ny.html")
print("complete - ready to continue")  




#%%
# end stations for protest time in june
bikeamounts=ny_pandemic[ny_pandemic["end_date_formatted"].between("2020-06-07","2020-06-25",inclusive= True)]
bikeamounts = bikeamounts['End station'].value_counts()
bikeamountsdf = pd.DataFrame({'End station' : bikeamounts.index, 'Counts' : bikeamounts.values})
bikeamountsdf = bikeamountsdf.merge(end, on="End station", how="left")

#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(bikeamountsdf,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    title="Total Rides by End station 2020", 
    hover_name="End station",
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/figtotal.html")
print("complete - ready to continue") 




#%%
# ending stations June 10
ny_panjun20st=ny_pandemic[ny_pandemic["end_date_formatted"]=="2020-06-10"]
ny_panjun20st = ny_panjun20st['End station'].value_counts()
ny_panjun20st_df = pd.DataFrame({'End station' : ny_panjun20st.index, 'Counts' : ny_panjun20st.values})
ny_panjun20st_df = ny_panjun20st_df.merge(end, on="End station", how="left")

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(ny_panjun20st_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    title="Total Rides by End station June 10, 2020", 
    hover_name="End station",
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/figjun10.html")
print("complete - ready to continue")  


#%%
#ending stations for June 19
ny_panjun7st=ny_pandemic[ny_pandemic["end_date_formatted"]=="2020-06-19"]
ny_panjun7st = ny_panjun7st['End station'].value_counts()
ny_panjun7st_df = pd.DataFrame({'End station' : ny_panjun7st.index, 'Counts' : ny_panjun7st.values})
ny_panjun7st_df = ny_panjun7st_df.merge(end, on="End station", how="left")

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(ny_panjun7st_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    title="Total Rides by End station June 19, 2020", 
    hover_name="End station",
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/figjun19.html")
print("complete - ready to continue")  



# %%
# animation maps of all rides pandemic & non pandemic 
ny_animmap = ny_pandemic.groupby(["end_date_formatted", "End station"]).size()

# ny_animmap = pd.DataFrame({"idx": ny_animmap.index, "val": ny_animmap.values})
ny_animmap = ny_animmap.to_frame().reset_index()
ny_animmap.rename(inplace=True, columns={0:"Counts"})
print(ny_animmap.columns)
print(ny_animmap.head())

# ny_animmap = pd.DataFrame({'Start station' : ny_animmap.index, 'Counts' : ny_animmap.values})
ny_animmap = ny_animmap.merge(ny_pandemic, on=["end_date_formatted", "End station"], how="left", suffixes=('', '_right'))
print(ny_animmap.columns)
print(ny_animmap.head())

#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(ny_animmap,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    title="Total Rides by End Station Pandemic", 
    hover_name="End station",
    size="Counts",
    animation_frame= "end_date_formatted",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig99ny.html")

# %%
ny_animmapnon = ny_nonpandemic.groupby(["end_date_formatted", "End station"]).size()

# ny_animmap = pd.DataFrame({"idx": ny_animmap.index, "val": ny_animmap.values})
ny_animmapnon = ny_animmapnon.to_frame().reset_index()
ny_animmapnon.rename(inplace=True, columns={0:"Counts"})


# ny_animmap = pd.DataFrame({'Start station' : ny_animmap.index, 'Counts' : ny_animmap.values})
ny_animmapnon = ny_animmapnon.merge(ny_nonpandemic, on=["end_date_formatted", "End station"], how="left", suffixes=('', '_right'))
print(ny_animmapnon.head())

#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(ny_animmapnon,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    title="Total Rides by End Station Nonpandemic", 
    hover_name="End station",
    size="Counts",
    animation_frame= "end_date_formatted",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig100ny.html")