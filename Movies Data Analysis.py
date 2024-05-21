#!/usr/bin/env python
# coding: utf-8

# In[62]:


#Import libraries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


# In[63]:


#Import dataset

df = pd.read_csv('movies.csv')
df.head(5)


# In[64]:


#See how many rows and columns the dataset has

df.shape


# In[65]:


df.columns


# In[66]:


#dropping unecessary columns

df.drop(columns = ['id','imdb_id','homepage','cast','tagline','overview','budget_adj'], inplace = True)


# In[67]:


df.head()


# In[68]:


#Drop NULL values from certain columns in the dataset

df.isnull().sum()


# In[69]:


df.dropna(how = 'any', subset = ['genres','director'],
         inplace = True)


# In[70]:


#Fill in NULL values with 0

df['production_companies'] = df['production_companies'].fillna(0)
df['keywords'] = df['keywords'].fillna(0)


# In[71]:


df


# In[72]:


#round popularity and roi columns decimals to 2

df['popularity'] = df['popularity'].round(2)


# In[73]:


df


# In[74]:


#Create additional columns

df.insert(3, 'profit', df.revenue - df.budget)


# In[75]:


df.insert(4, 'roi', df.profit / df.budget)


# In[80]:


df


# In[79]:


df['roi'] = df['roi'].round(2)


# In[91]:


#Creating a histogram using specific columns

df1 = df[['popularity', 'budget', 'revenue', 'profit', 'roi', 'vote_count', 'vote_average', 'release_year']]


# In[92]:


df.isnull().sum()


# In[93]:


df.roi.value_counts()


# In[88]:


non_finite_values = ~np.isfinite(df['roi'])


# In[89]:


non_finite_values.sum()


# In[90]:


df['roi'] = df['roi'].replace([np.inf, -np.inf], np.nan)


# In[95]:


df1.hist(bins = 20, figsize = (14,12))
plt.show


# In[96]:


df.popularity.value_counts()


# In[99]:


df.head(2)


# In[101]:


#Plotting the average of return on investment (roi) over different release years


df2 = df.groupby('release_year')['roi'].mean()
df2.plot(kind = 'line')


# In[127]:


#Plot the total popularity over different release years


df3 = df.groupby('release_year')['popularity'].sum()
df3.plot(kind = 'line', color = 'cornflowerblue')
plt.xlabel('Year', fontsize = 12)
plt.ylabel('Popularity')


# In[128]:


#Visualize the average vote average over different release years


df4 = df.groupby('release_year')['vote_average'].mean()
df4.plot(kind = 'line', color = 'cornflowerblue')
plt.xlabel('Year', fontsize = 12)
plt.ylabel('Rating')


# In[129]:


#Create a scatter plot using the 'popularity' and  'vote_average' to check the dependency



df5 = df.plot.scatter(x = 'popularity', y = 'vote_average', c = 'cornflowerblue', figsize = (6,4))
df5.set_xlabel('popularity', color = 'DarkRed')
df5.set_ylabel('Vote Average', color = 'DarkRed')
df5.set_title('Popularity vs Vote Average', fontsize = 17 )


# In[117]:


#Split the values in  'genres' column  based on a delimiter (in this case, "|")


df.genres.value_counts()


# In[118]:


split = ['genres']
for i in split:
    df[i] = df[i].apply(lambda x: x.split("|"))
df.head(3)


# In[119]:


df = df.explode('genres')
df


# In[123]:


#Check the popularity of movies by genres


df7 = df.groupby('genres')['popularity'].sum().sort_values(ascending = True)
df7


# In[130]:


df7.plot.barh(x = 'genres', y = 'popularity', color = 'cornflowerblue', figsize = (12,6))


# In[133]:


#Check the popularity of movies by months


#converting 'release_date' data type from 'object' to 'date'

df['release_date'] = pd.to_datetime(df['release_date'])


# In[134]:


df.dtypes


# In[135]:


df['extracted_month'] = df['release_date'].dt.month


# In[138]:


df.head()


# In[139]:


df8 = df.groupby('extracted_month')['popularity'].sum()


# In[143]:


df8


# In[144]:


df8.index


# In[146]:


df8.values


# In[147]:


data = {
    'extracted_month': df8.index,
    'popularity': df8.values
       
}
df8 = pd.DataFrame(data)


# In[148]:


df8


# In[149]:


index_to_month = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}


# In[150]:


df8.extracted_month = df8.extracted_month.map(index_to_month)


# In[151]:


df8


# In[153]:


df8.plot(kind = 'bar', x = 'extracted_month', y = 'popularity', color = 'cornflowerblue')


# In[185]:


#Print out the popular movies by revenue 


df9 = df.groupby('extracted_month')['revenue'].sum()


# In[186]:


df9


# In[187]:


data = {
    'extracted_month': df9.index,
    'revenue': df9.values
       
}
df9 = pd.DataFrame(data)


# In[188]:


df9


# In[189]:


index_to_month = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}


# In[190]:


df9.extracted_month = df9.extracted_month.map(index_to_month)


# In[191]:


df9


# In[192]:


df9.plot(kind = 'bar', x = 'extracted_month', y = 'revenue', color = 'cornflowerblue')
plt.title('Revenue by Month')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.show()


# In[194]:


#Print out the most popular titles by profit


df10 = df.groupby('original_title')['profit'].sum().sort_values(ascending = False).head(5)
df10


# In[200]:


df10.plot(kind = 'pie', autopct = '%1.1f%%', startangle = 90, colors = plt.cm.Paired.colors)
plt.title('TOP 5 MOVIES BY PROFIT', color = 'darkred')


# In[228]:


#Visualize the popular production companies 


df11 = df.production_companies.value_counts().head(5)
df11


# In[231]:


df11 = df11.drop(0)


# In[232]:


df11.index


# In[236]:


explode_list = [0.04,0,0,0]
df11.plot(kind = 'pie', figsize = (12,6) ,autopct = '%1.1f%%', startangle = 90, labels = None, pctdistance = 1.14,
         explode = explode_list)
#plt.title('TOP 5 MOVIES BY PROFIT', color = 'darkred')
plt.legend(labels = df11.index, loc = 'upper right' )
plt.axis('equal')
plt.show()


# In[243]:


#Create a treemap to visualize the popular keywords in movies.


df12 = df.keywords.value_counts().head(15)
df12


# In[244]:


df12 = df12.drop(0)


# In[245]:


df12.index


# In[246]:


df12.values


# In[247]:


data = {
    'keywords': df12.index,
    'value': df12.values
       
}
df12 = pd.DataFrame(data)


# In[248]:


df12


# In[249]:


fig = px.treemap(df12, path = ['keywords'], values = 'value')
fig.show()

