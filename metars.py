#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob


# # open dataset

# In[2]:


datasets = glob.glob("./*.csv")
datasets


# In[3]:


databases = []
for d in datasets:
    databases.append(pd.read_csv(d))
databases[1].head()


# In[4]:


stations = []
for n in datasets:
    stations.append(n[2:6])
    
stations    


# In[26]:


def rename_col(df):
    for s in df:
        s.rename(columns={'valid' : 'date',
                          'tmpc' : 'temp',
                          'dwpc' : 'dew',
                          'relh' : 'rh',
                          'drct' : 'wind_dir',
                          'sknt' : 'wind_speed',
                          'mslp' : 'p',
                          'vsby' : 'vis',
                          'gust' : 'g',
                          'skyc1' : 'cl1',
                          'skyc2' : 'cl2',
                          'skyc3' : 'cl3',
                          'wxcodes' : 'ww',}, inplace=True)
    return(df)


# In[22]:


databases = rename_col(databases)
databases[0].head()


# In[6]:


for s in databases:
    s['date'] = pd.to_datetime(s['date'])
databases[2].info()


# In[7]:


noOfRaws = {}
i=0
for s in databases:
    noOfRaws[stations[i]] = {'noOfRaws' : s.shape[0],
                             'start_date' : s.loc[0, 'date'],
                             'end_date' : s.loc[len(s['date'])-1, 'date']}
    i += 1
pd.DataFrame(noOfRaws)


# # open another dataset

# In[8]:


datasets2 = glob.glob("./08/*.csv")
datasets2


# In[9]:


databases2 = []
for d in datasets2:
    databases2.append(pd.read_csv(d))
databases2[1].head()


# In[27]:


databases2 = rename_col(databases2)


# # Concate the two datasets

# In[50]:


for i in range(len(databases2)):
    databases[i+1] = pd.concat([databases[i+1], databases2[i]]) 
databases[2].shape


# In[52]:


databases[3].head()


# In[54]:


databases[3].tail()


# # Deling with data
# ## Join the wanted columns
# ### Add suffix for each station within the database

# In[56]:


suffi = []
for n in datasets:
    suffi.append(n[4:6])
    
suffi 


# In[57]:


def suffix(df, suffi):
    df = df.add_suffix("_" + suffi)
    return(df)


# In[58]:


for i in range(len(databases)):
    databases[i] = suffix(databases[i], suffi[i])


# In[60]:


len(databases)


# In[64]:


databases[0].head()


# ### Create another column for date to make the original date the index

# In[65]:


for i in range(len(databases)):
    col = "date" + "_" + suffi[i]
    databases[i]['date'] = databases[i][col]  


# ### Make the original date the index

# In[66]:


for i in range(len(databases)):
    databases[i] = databases[i].set_index('date')
databases[0].head()


# In[67]:


databases[2].head()


# ## Join all databases in one then chose a variable

# In[72]:


result_1 = databases[0].join(databases[1:])
result_1.info()


# In[56]:


result_1.head()


# In[ ]:


df_temp = pd.DataFrame(index=result_1.index)
for str in suffi: 
    col = 'temp' + "_" + str
    df_temp[col] = result_1[col]
df_temp.head()


# # Chose certain variable from the resultant dataset then join them

# In[78]:


var = []
for i in range(len(databases)): 
    col = 'temp' + "_" + suffi[i]
    var.append(pd.DataFrame(databases[i][col]))
var[1]


# In[91]:


# df_temp = pd.DataFrame(index=databases.index)
ind = suffi.index('CA')
df_temp = var[ind].join(var[:])
df_temp.drop(df_temp.columns[ind+1], axis=1, inplace=True)
df_temp.info()


# In[92]:


df_temp.head()


# # Chose certain variable from dataset then concate them

# In[93]:


def date_columns(df):
    df['year'] = pd.DatetimeIndex(df.index).year
    df['month'] = pd.DatetimeIndex(df.index).month
    df['day'] = pd.DatetimeIndex(df.index).day
    df['hour'] = pd.DatetimeIndex(df.index).hour
    df['min'] = pd.DatetimeIndex(df.index).minute
    return (df)


# In[94]:


df_temp = date_columns(df_temp)
df_temp.head()


# In[95]:


df_temp = df_temp[df_temp['min'] == 0]
df_temp.head()


# In[108]:


df_temp.index = pd.to_datetime(df_temp.index)
df_temp2011 = df_temp[df_temp.index > '2010-12-31 23:30:00' ]
df_temp2011.tail(5)


# In[111]:


import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,10)
df_temp2011.groupby(['year', 'month']).max().plot()


# In[112]:


df_temp2011.groupby(['year', 'month'])['temp_CA_x'].max().plot()


# In[26]:


df.loc[14428, 'tmpc'] = 19
df.loc[14428, 'tmpc']


# In[27]:


df.groupby(['year', 'month'])['tmpc'].max().plot()


# In[28]:


df.groupby(['year', 'month'])['tmpc'].min().plot()


# In[34]:


import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,5)

df_max = df.groupby(['year', 'month', 'day'])['tmpc'].max()
df_max.groupby(['year', 'month']).mean().plot()


# In[ ]:




