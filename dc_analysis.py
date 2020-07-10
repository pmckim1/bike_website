

#%%
import datetime as dt
import glob

import matplotlib as plt
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import timezone
import plotly
import plotly.graph_objects as go
#%%
dc_data=pd.read_csv("dc_data.csv")
end=pd.read_csv("end.csv")
start=pd.read_csv("start.csv")
#%%
dc_covid=pd.read_csv("dccovid.csv")
print(dc_covid.head())
#%%
dc_data.columns

print(dc_data.tail())
#%%
print(len(dc_data))
#%%

dc_data["start_hour"]= pd.DatetimeIndex(dc_data['start_dto']).hour
dc_data["Ride_taken"]=1

#%%

def draw_commuting_share(df):
    dfg = df.groupby('pandemic-commuter').count().reset_index()
    dfg = dfg.rename(columns={"start_date": "Users"})
    fig = px.bar(dfg, x='pandemic-commuter', y='Users', title= "Commuter versus Noncommuter Riders- Nonpandemic & Pandemic", color_discrete_sequence =['#0000ff']*len(dfg))
    fig.show()
    fig.write_html("./templated-transitive/graphs/fig31dc.html")
    
draw_commuting_share(df = dc_data[dc_data['pandemic']==True])
draw_commuting_share(dc_data)


#%%

def draw_weekend_share(df):
    dfwk = df.groupby('pandemic-weekday').count().reset_index()
    dfwk = dfwk.rename(columns={"start_date": "Users"})
    fig1 = px.bar(dfwk, x='pandemic-weekday', y='Users', title= "Weekday vs Weekend Riders- Nonpandemic & Pandemic", 
    color_discrete_sequence =['#0000ff']*len(dfwk))
    fig1.show()
    fig1.write_html("./templated-transitive/graphs/fig32dc.html")
draw_weekend_share(df = dc_data[dc_data['pandemic']==True])
draw_weekend_share(dc_data)

#%%
#DC pandemic frame 
dc_pandemic= dc_data["pandemic"]== True
dc_pandemic= dc_data[dc_pandemic]
dc_pandemic=dc_pandemic[dc_pandemic["end_dto"].between("2020-02-29","2020-07-01",inclusive= True)]
print(len(dc_pandemic))
print(len(dc_data))

# DC non Pandemic Frame 
dc_nonpandemic= dc_data["pandemic"]== False
dc_nonpandemic= dc_data[dc_nonpandemic]
dc_nonpandemic=dc_nonpandemic[dc_nonpandemic["end_dto"].between("2019-02-28","2019-07-01",inclusive= True)]
print(len(dc_nonpandemic))


#%%
# table of timelines for both cities  
timeline=pd.read_csv("timeline.csv")

#%%
fig = go.Figure(data=[go.Table(
    header=dict(values=list(timeline.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[timeline.WhenOccured, timeline.Event, timeline.City],
               fill_color='light gray',
               align='left'))
])
fig.update_layout(title="Timeline of Events")   
fig.show()
fig.write_html("./templated-transitive/graphs/fig1.html")





#%%
#filter for sub 5000 pandemic
dc_datasub5000=dc_data[dc_data["Duration"]<5000]

fig = px.box(dc_datasub5000, y="Duration", x="pandemic",
             title= "Duration by Pandemic or Non")
labels={'true': "pandemic", 'false':'Nonpandemic'},
fig.show()
fig.write_html("./templated-transitive/graphs/figboxdc.html")

#%%



dc_pandemicsub5000=dc_pandemic[dc_pandemic["Duration"]<5000]

#%%

#box plot for sub 5000 Pandemic

fig = px.box(dc_pandemicsub5000, y="Duration", title= "Duration of Ride- Pandemic")
fig.show()

print("complete - ready to continue")  

#%%

#filter for sub 5000 non pandemic
dc_nonpandemicsub5000=dc_nonpandemic[dc_nonpandemic["Duration"]<5000]
#box plot for sub 5000 non pandemic 

fig = px.box(dc_nonpandemicsub5000, y="Duration", title= "Duration of Ride- Nonpandemic")
fig.show()

print("complete - ready to continue")  


#%%

# member type duration pandemic 

fig = px.box(dc_pandemicsub5000, y="Duration", x="day_of_week",
             title= "Duration by Member Type- Pandemic")
fig.update_traces(marker_color="#0000ff")
fig.show()

#%%
# member type duration nonpandemic 


#%%
dcpangroup=dc_pandemic.groupby(['Duration','Member type']).count().reset_index()
dcpangroup=dcpangroup[["end_date_formatted", "Member type", "Ride_taken"]]
print(dc_pandemic.columns)
print(dc_pandemic.head())
print(dcpangroup.columns)
print(dcpangroup.head())

fig = px.bar(dcpangroup, 
            x="Member type",
            y="Ride_taken",
            title='Total Rides Per Day', 
            animation_frame="end_date_formatted",
        )
fig.write_html("./templated-transitive/graphs/fig102dc.html")
fig.show()


#%%
#histogram of pandemic rides per hour 

fighist = px.histogram(dc_pandemic, x="start_hour", title= "Start Hour of Ride- Pandemic")
fighist.update_traces(marker_color="#0000ff")
fighist.update_layout(xaxis_title='Start Hour',
                   yaxis_title='Users')   
fighist.show()
fighist.write_html("./templated-transitive/graphs/fig2dc.html")


#%%
#histogram of nonpandemic rides per hour
fighist = px.histogram(dc_nonpandemic, x="start_hour",  title= "Start Hour of Ride- Nonpandemic")
fighist.update_traces(marker_color="#33ff99")
fighist.update_layout(xaxis_title='Start Hour',
                   yaxis_title='Users')   
fighist.show()
fighist.write_html("./templated-transitive/graphs/fig3dc.html")

#%%

#histogram of both together

import plotly.graph_objects as go
x1= dc_pandemic["start_hour"]
x2= dc_nonpandemic["start_hour"]
fig = go.Figure()
fig.add_trace(go.Histogram(x=x2, name='Nonpandemic', marker_color="#33ff99"))
fig.add_trace(go.Histogram(x=x1, name= "Pandemic", marker_color= "#0000ff"))
# Overlay both histograms
fig.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
fig.update_layout(title= "Start Hour of Ride- Pandemic and Nonpandemic",
    xaxis_title='Start Hour',
                   yaxis_title='Users')   
fig.show()
fig.write_html("./templated-transitive/graphs/doublehisto.html")


#%%

# rides each day of the week total 
# day of week rides during pandemic
cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dfpanweek = dc_pandemic.groupby('day_of_week').count().reindex(cats)
dfpanweek["day_of_week"]=dfpanweek.index
figpanweek = px.bar(dfpanweek, x='day_of_week', y='start_date', title='Total Rides Per Day of the Week- Pandemic',
                    labels={'day_of_week': "Day of the Week", 'start_date':'Total Rides'},
                    color_discrete_sequence =['#0000ff']*len(dfpanweek))
figpanweek.show()
figpanweek.write_html("./templated-transitive/graphs/fig50dc.html")
#%%
# rides each day of the week nonpan
dfnonpanweek = dc_nonpandemic.groupby('day_of_week').count().reindex(cats)
dfnonpanweek["day_of_week"]=dfnonpanweek.index
fig = px.bar(dfnonpanweek, x='day_of_week', y='start_date',  
                       title='Total Rides Per Day of the Week- Nonpandemic',
                       labels={'day_of_week': "Day of the Week", 'start_date':'Total Rides'},
                       color_discrete_sequence =['#33ff99']*len(dfnonpanweek),
                        )
fig.show()
fig.write_html("./templated-transitive/graphs/fig5dc.html")



#%%

#pie chart
dfpanpie = dc_pandemic.groupby('Member type').count().reset_index()
dfnonpanpie = dc_nonpandemic.groupby('Member type').count().reset_index()
 
#pie charts of members versus casual 
fig = px.pie(dfpanpie, values='pandemic', names='Member type', color= "Member type", labels= "Member type",title='Percent of Rider Type During Pandemic',
              color_discrete_map={'Member':'#0000ff',
                                 'Casual':'royalblue'})
fig.show()
fig.write_html("./templated-transitive/graphs/fig8dc.html")
fig = px.pie(dfnonpanpie, values='pandemic', names='Member type', color= "Member type", labels= "Member type",title='Percent of Rider Type During Non-Pandemic',
              color_discrete_map={'Member':'#33ff99',
                                 'Casual':'#009900'})
fig.show()
fig.write_html("./templated-transitive/graphs/fig9dc.html")


#%%

#line graphs 
# rides per day pandemic
dc_pandemicline=dc_pandemic.groupby('end_date_formatted').count().reset_index()
dc_pandemicline = dc_pandemicline.rename(columns={"start_date": "Users"})
fig = px.line(dc_pandemicline, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic', 
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
fig.write_html("./templated-transitive/graphs/fig10dc.html")

#%%
#
# rides per day non pandemic
dc_nonpandemicline=dc_nonpandemic.groupby('end_date_formatted').count().reset_index()
dc_nonpandemicline = dc_nonpandemicline.rename(columns={"start_date": "Users"})
fig = px.line(dc_nonpandemicline, x="end_date_formatted", y="Users",title='Total Rides Per Day- Nonpandemic',
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
fig.write_html("./templated-transitive/graphs/fig11dc.html")

#%%
#make data frame of first weeks pandemic started to spread
dc_pandemicline1stweek=dc_pandemic[dc_pandemic["end_date_formatted"].between("2020-03-09","2020-03-30",inclusive= True)]

dc_pandemicline1stweek=dc_pandemicline1stweek.groupby('end_date_formatted').count().reset_index()
dc_pandemicline1stweek = dc_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(dc_pandemicline1stweek, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic (Around time of Shutdown)', 
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
fig.write_html("./templated-transitive/graphs/fig12dc.html")


#%%
#make data frame of before & after George Floyd was killed 

dc_pandemicline1stweek=dc_pandemic[dc_pandemic["end_dto"].between("2020-05-18","2020-06-09",inclusive= True)]

dc_pandemicline1stweek=dc_pandemicline1stweek.groupby('end_dto').count().reset_index()
dc_pandemicline1stweek = dc_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(dc_pandemicline1stweek, x="end_dto", y="Users", title= 'Total Rides-Pandemic (before and after the death of George Floyd Hourly Breakdown)',
              color_discrete_sequence =['#0000ff']*len(dc_pandemicline1stweek))
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
fig.write_html("./templated-transitive/graphs/fig13dc.html")
#%%
# line graph for before and after death of George floyd 
dc_pandemicline1stweek=dc_pandemic[dc_pandemic["end_date_formatted"].between("2020-05-18","2020-06-09",inclusive= True)]

dc_pandemicline1stweek=dc_pandemicline1stweek.groupby('end_date_formatted').count().reset_index()
dc_pandemicline1stweek = dc_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(dc_pandemicline1stweek, x="end_date_formatted", y="Users", title= 'Total Rides Per Day- Pandemic (before and after the death of George Floyd)',   
              color_discrete_sequence =['#0000ff']*len(dc_pandemicline1stweek))
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
fig.write_html("./templated-transitive/graphs/fig14dc.html")

#%%
# hours histo for days and weeks after george Floyd was killed
dc_pandemicline1stweek=dc_pandemic[dc_pandemic["end_dto"].between("2020-05-18","2020-06-09",inclusive= True)]

dc_pandemicline1stweek=dc_pandemicline1stweek.groupby('end_dto').count().reset_index()
dc_pandemicline1stweek = dc_pandemicline1stweek.rename(columns={"start_date": "Users"})
fig = px.line(dc_pandemicline1stweek, x="end_dto", y="Users", title= 'Total Rides Per Day- Pandemic (before and after the death of George Floyd)')
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
fig.write_html("./templated-transitive/graphs/fig15dc.html")


#%%# animation 
 
dcpangroup=dc_pandemic.groupby(['start_hour','Member type']).count().reset_index()
dcpangroup=dcpangroup[["start_hour", "Member type", "Ride_taken"]]
print(dc_pandemic.columns)
print(dc_pandemic.head())
print(dcpangroup.columns)
print(dcpangroup.head())

fig = px.bar(dcpangroup, 
            x="Member type",
            y="Ride_taken",
            title='Total Rides Per Day - Pandemic', 
            animation_frame="start_hour",
        )
fig.write_html("./templated-transitive/graphs/fig98dc.html")
fig.show()




#%%

fig = px.bar(dcpangroup, 
            x="Member type",
            y="Ride_taken",
            title='Total Rides Per Day', 
            animation_frame="start_hour",
            range_y=[0,2500],
        )
fig.show()

 #animation_frame="year", a"nimation_group="country,


#%%
dc_pandemic=dc_pandemic.dropna(subset=["End station number"])



#%%

# prepare data frame for end station pandemic 
endst_vc = dc_pandemic['End station'].value_counts()
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
fig.write_html("./templated-transitive/graphs/fig16dc.html")
print("complete - ready to continue")  



#%%

# prepare data frame for start station pandemic 

stast_vc = dc_pandemic['Start station'].value_counts()
stast_vc_df = pd.DataFrame({'Start station' : stast_vc.index, 'Counts' : stast_vc.values})
stast_vc_df = stast_vc_df.merge(start, on="Start station", how="left")

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
fig.write_html("./templated-transitive/graphs/fig17dc.html")
print("complete - ready to continue")  

#%%
#Nonpandemic Maps 

# prepare data frame for end station nonpandemic 
non_end_st_vc = dc_nonpandemic['End station'].value_counts()
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
fig.write_html("./templated-transitive/graphs/fig18dc.html")
print("complete - ready to continue")  



#%%

# prepare data frame for start station nonpandemic 
stast_vc = dc_nonpandemic['Start station'].value_counts()
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
fig.write_html("./templated-transitive/graphs/fig19dc.html")
print("complete - ready to continue")  


#%%
#covid related graphs 
dc_pandemiclinecovid = dc_pandemic['end_date_formatted'].value_counts()
dc_pandemiclinecovid = pd.DataFrame({'end_date_formatted' : dc_pandemiclinecovid.index, 'Counts' : dc_pandemiclinecovid.values})
dc_pandemiclinecovid = dc_pandemiclinecovid.merge(dc_covid, on="end_date_formatted", how="left")
dc_pandemiclinecovid=dc_pandemiclinecovid.sort_values("end_date_formatted")

print("complete - ready to continue")  



#%%
# rides vs covid cases line and bar 

fig = go.Figure()

fig.add_trace(
    go.Bar(
      x=dc_pandemiclinecovid["end_date_formatted"], y=dc_pandemiclinecovid["Cases"], name= "Total Covid Cases Diagnosed",

))

fig.add_trace(
  go.Scatter(
        x=dc_pandemiclinecovid["end_date_formatted"], y=dc_pandemiclinecovid["Counts"],name= "Total Rides", line=dict(color="#7afbf9")
    ))
fig.update_layout(
    title = 'Time Series against Total Cases of Covid-19',
    xaxis_tickformat = '%Y-%m-%d',
)
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Instances')   
fig.write_html("./templated-transitive/graphs/fig21dc.html")
fig.show()
#%%
# rides vs covid cases line and bar- scatter bubble chart 
fig=px.scatter(dc_pandemiclinecovid, x="end_date_formatted", y="Counts", size= "Counts", color="Cases", animation_group= "Counts", 
               title="Total rides vs Total cases of Covid-19 Diagnosed",  color_continuous_scale=px.colors.diverging.Portland,
               #animation_frame= "end_date_formatted"
           )
fig.update_layout(xaxis_title='Date',
                   yaxis_title='Rides')  
fig.write_html("./templated-transitive/graphs/fig22dc.html")
fig.show()




#%%
# prepare data frame for end station pandemic after george floyd death-- same time as   demonstrations 
dc_panjun5=dc_pandemic[dc_pandemic["end_date_formatted"]=="2020-06-05"]
dc_panjun5 = dc_panjun5['End station'].value_counts()
dc_panjun5_df = pd.DataFrame({'End station' : dc_panjun5.index, 'Counts' : dc_panjun5.values})
dc_panjun5_df = dc_panjun5_df.merge(end, on="End station", how="left")
#print(endst_vc_df[endst_vc_df['End station']=='Lincoln Memorial'])
#print(endst_vc_df.head(500))
#print(dc_data.head(500))

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(dc_panjun5_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    title="Total Rides by End Station June 5, 2020", 
    color_continuous_scale=px.colors.diverging.Portland,
    hover_name="End station",
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig23dc.html")
print("complete - ready to continue")  


#%%
# prepare data frames & maps for end station pandemic after george floyd death-- same time as  demonstrations 
dc_panjun6=dc_pandemic[dc_pandemic["end_date_formatted"]=="2020-06-06"]
dc_panjun6 = dc_panjun6['End station'].value_counts()
dc_panjun6_df = pd.DataFrame({'End station' : dc_panjun6.index, 'Counts' : dc_panjun6.values})
dc_panjun6_df = dc_panjun6_df.merge(end, on="End station", how="left")
#print(endst_vc_df[endst_vc_df['End station']=='Lincoln Memorial'])
#print(endst_vc_df.head(500))
#print(dc_data.head(500))

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(dc_panjun6_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    title="Total Rides by End Station June 6, 2020", 
    color_continuous_scale=px.colors.diverging.Portland,
    hover_name="End station",
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig24dc.html")
print("complete - ready to continue")  

#%%
# prepare data frames & maps for end station pandemic after george floyd death-- same time as  demonstrations 
dc_panjun7=dc_pandemic[dc_pandemic["end_date_formatted"]=="2020-06-07"]
dc_panjun7 = dc_panjun7['End station'].value_counts()
dc_panjun7_df = pd.DataFrame({'End station' : dc_panjun7.index, 'Counts' : dc_panjun7.values})
dc_panjun7_df = dc_panjun7_df.merge(end, on="End station", how="left")

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(dc_panjun7_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    title="Total Rides by End Station June 7, 2020", 
    hover_name="End station",
    size="Counts",
    zoom=10.2
)
fig.show()
fig.write_html("./templated-transitive/graphs/fig25dc.html")
print("complete - ready to continue")  


#%%
# prepare data frame for end station pandemic before george floyd demonstrations 
dc_panmay=dc_pandemic[dc_pandemic["end_date_formatted"]=="2020-05-23"]
dc_panmay = dc_panmay['End station'].value_counts()
dc_panmay_df = pd.DataFrame({'End station' : dc_panmay.index, 'Counts' : dc_panmay.values})
dc_panmay_df = dc_panmay_df.merge(end, on="End station", how="left")

px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig4 = px.scatter_mapbox(dc_panmay_df,
    lat="end_lat_y",
    lon="end_lng_y",
    color="Counts",
    color_continuous_scale=px.colors.diverging.Portland,
    hover_name="End station",
    title="Total Rides by End Station May 23, 2020", 
    size="Counts",
    zoom=10.2
)
fig4.show()
fig4.write_html("./templated-transitive/graphs/fig26dc.html")
print("complete - ready to continue")  



#%%
print("Just run!")
#%%
#Map of end stations pandemic- animated map 
#dc_animmap = dc_pandemic['Start station'].value_counts()
dc_animmap = dc_pandemic.groupby(["end_date_formatted", "End station"]).size()

# dc_animmap = pd.DataFrame({"idx": dc_animmap.index, "val": dc_animmap.values})
dc_animmap = dc_animmap.to_frame().reset_index()
dc_animmap.rename(inplace=True, columns={0:"Counts"})
print(dc_animmap.columns)
print(dc_animmap.head())

# dc_animmap = pd.DataFrame({'Start station' : dc_animmap.index, 'Counts' : dc_animmap.values})
dc_animmap = dc_animmap.merge(dc_pandemic, on=["end_date_formatted", "End station"], how="left", suffixes=('', '_right'))
print(dc_animmap.columns)
print(dc_animmap.head())

#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(dc_animmap,
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
fig.write_html("./templated-transitive/graphs/fig99dc.html")

# %%
dc_animmapnon = dc_nonpandemic.groupby(["end_date_formatted", "End station"]).size()

# dc_animmap = pd.DataFrame({"idx": dc_animmap.index, "val": dc_animmap.values})
dc_animmapnon = dc_animmapnon.to_frame().reset_index()
dc_animmapnon.rename(inplace=True, columns={0:"Counts"})
print(dc_animmapnon.columns)
print(dc_animmapnon.head())

# dc_animmap = pd.DataFrame({'Start station' : dc_animmap.index, 'Counts' : dc_animmap.values})
dc_animmapnon = dc_animmapnon.merge(dc_nonpandemic, on=["end_date_formatted", "End station"], how="left", suffixes=('', '_right'))
print(dc_animmapnon.columns)
print(dc_animmapnon.head())

#%%
px.set_mapbox_access_token("pk.eyJ1IjoibWNraW1wYyIsImEiOiJja2J2MndscTMwMjE3MnFud2diMnZjaWR1In0.2kGSzHfnYe94CesoZi0i7Q")
fig = px.scatter_mapbox(dc_animmapnon,
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
fig.write_html("./templated-transitive/graphs/fig100dc.html")

# %%
