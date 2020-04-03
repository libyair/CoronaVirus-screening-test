#!/usr/bin/env python
# coding: utf-8

# In[35]:


import numpy as np
import pandas as pd
import pandas_gbq
from pandas.io import gbq
#Download a timeseries of daily deaths per country
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
death = pd.read_csv(url, error_bad_lines=False)
death['Country/Region']= death['Country/Region'].str.replace("Mainland China", "China")
death['Country/Region']= death['Country/Region'].str.replace("US", "United States")
death.rename(columns = {'Country/Region':'Country_Name'}, inplace=True)
death = death.groupby(['Country_Name'], sort=False).sum()
death=death.reset_index()
#Converting the death table so that each country and each day is a separate row 
death = death.melt(id_vars=["Country_Name","Lat","Long"], var_name="Date",  value_name="Death_Toll")
death = death.sort_values(["Country_Name", "Date"])
death = death.reset_index(drop=1)
#death = death.drop(col=death.index)
death.head()



# In[ ]:





# In[36]:


#Uploading the table from step 2 into an SQL table named deaths_total
death.to_gbq(destination_table = 'deaths_total.death_tolls', project_id = 'application-data-scientist', if_exists='replace')


# In[37]:


#Calculating the daily change in deaths for each country
Death_daily_change = pd.DataFrame({
                        'Country_Name': death.Country_Name,'Date':death.Date,                                         
                        'death_daily_change': death.groupby(['Country_Name'])['Death_Toll'].transform(lambda x: x.diff())
                                    })
Death_daily_change.head()


# In[38]:


#Uploading the table from step 4 into an SQL table named deaths_change_python
Death_daily_change.to_gbq(destination_table = 'deaths_total.deaths_change_python',
                          project_id = 'application-data-scientist', if_exists='replace')

