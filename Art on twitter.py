#!/usr/bin/env python
# coding: utf-8

# Goal: gauge ingagement between tradition and digital art on twitter

# In[1]:


import requests
import pandas as pd
import json
import urllib
import matplotlib


# Linking to the Twitter API

# In[2]:


bearer_token = pd.read_csv("twitterApp.txt", header = 0)


# In[3]:


token = bearer_token['Bearer Token'].iloc[0]


# In[4]:


header = {'Authorization' : 'Bearer {}'.format(token)}


# In[5]:


endpoint_url = 'https://api.twitter.com/2/tweets/search/recent'


# Query to display posts using the hashtags of digital and traditional art

# In[6]:


query = urllib.parse.quote('(#digitalart OR #traditionalart) -is:retweet')


# In[7]:


tweet_fields = 'author_id,id,text,public_metrics,created_at,entities'


# In[8]:


url = endpoint_url + '?query={}&tweet.fields={}&user.fields={}&max_results=100'.format(query,tweet_fields,"username")


# In[9]:


response_1 = requests.request("GET", url, headers=header)


# In[10]:


response_1_dict = json.loads(response_1.text)


# In[15]:


page1 = pd.DataFrame(response_1_dict['data'])


# In[23]:


page1


# In[21]:


metrics = pd.DataFrame(list(page1['public_metrics']))


# In[22]:


metrics


# In[ ]:




