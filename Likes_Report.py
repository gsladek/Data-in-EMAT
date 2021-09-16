#!/usr/bin/env python
# coding: utf-8

# # Likes Report

# Gloria Sladek
# 
# 9/15/2021
# 

# Using data downloaded from my instagram, I organized the number of likes by time stamp and presented the information in a data frame.

# The first thing I did was load in the packages I was going to use.

# In[67]:


import pandas as pd
import json


# 1. Next I used the __with__ and __open__ function to open the _liked_posts.json_ file located in the Instagram data folder on my PC. I used the __json.load__ function to load in the file, saving it in a variable I called _dat_. 

# In[68]:


with open(r"C:\Users\glori\OneDrive\Desktop\Classes\Data in EMAT\Instagram Data\likes\liked_posts.json") as j:
    dat = json.load(j)


# I used dot notation to find the keys in the dat file which gave me the output of 'likes_media_likes'

# In[69]:


dat.keys()


# In[70]:


dat['likes_media_likes'][0]


# After calling and reviewing the data under dat, I discovered that the '_timestamp_' value was located in the 'string_list_data' key. 

# Next I used the '__x for x in__' format to create a list using the key values generated in the previous step. I assigned this list to the variable '_likes_'. 

# In[71]:


likes = [x['string_list_data'][0] for x in dat['likes_media_likes']]


# 2. Once I had generated a list, I created a data frame by using the function '__DataFrame__' from the _pandas_ library, and calling columns 1 through 10 on the likes variable I created previously. I then called the data frame to demonstrate what was generated.
# If I were to evaluate this data by creating a graph, the full list would be used. However, for the purposes of this report I have limited the data to only show rows 1-10.

# In[72]:


df_likes = pd.DataFrame(likes[0:10])


# In[73]:


df_likes


# 3. I determined that Instagram Collected the data shown above in order to sell it to advertisers to then create targeted advertisements. In some ways this data is reliable, for example if I were to like a lot of posts relating to a specific brand of clothing, chances are I like that brand of clothing. However it can also be unreliable. For example, I may like items relating to fashion for other reasons such as art references.

# 4. Bellow I took the data I had gathered from the likes report and transfered it into a CSV file using dot notation and the function __to_csv__. I then went on to group that data by "timestamp" using the __groupby__ function and used the __count__ function to make a more readable data frame.

# In[74]:


df_likes.to_csv(r'C:\Users\glori\OneDrive\Desktop\Classes\Data in EMAT\liked.csv')


# In[75]:


dictionary = df_likes.groupby('timestamp').count()


# In[76]:


dictionary


# 5. Due to the amount of art I see on Instagram, I believe that I follow mostly art accounts. With the data provided in the "following" file, I will test my prediction that 70% of my follows are art accounts.
# Ideally a column would be provided in the data that stated the type of account each was; this could include personal, art, business, ect. The quickest way of identifying art or nonart accounts would be to add a column that contained a value of 'yes' or 'no' depending on if an account was an art related account.

# I reviewed previous class notes in order to understand how to use each functions. After looking at the previous demonstrations I was able to understand what each function did and how the data was obtained and organized.
# The main place I struggled was indexing the list and data frame so that I could view specific rows. I used the Panda Docs for this information under their "Indexing and selecting data" page.

# The data presented would be more useful for my hypothesis if each like was related to a category, or if the timestamp was more readable to the human eye. Rather then having a string of numbers this data would be more useful if the time stamp was "5:00" or "14:00" and so on. In the future I will learn how to interpret time related data in order to come to better conclusions.
