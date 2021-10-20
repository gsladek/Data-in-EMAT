#!/usr/bin/env python
# coding: utf-8

# # Twitter API
# By: Gloria Sladek

# Using Twitter Data I hope to answer the question of how artists are using twitter as a platform. More specifically I would like to identify the types of art being posted: Ie traditional vs. Digital.

# ## Gathering Data

# In[1]:


import requests
import pandas as pd
import json
import urllib


# I imported the different libraries I would be using.
# 
# Then I called in my _twitter API_ text files as _csv_ and assigned them to a variable called __bearer_token.__ 
# 
#     The bearer token is used to access the twitter API

# In[2]:


bearer_token = pd.read_csv("twitterApp.txt", header = 0)


# I isolated the Bearer Token from its label using _iloc_ then formated a line that included the header of Authorization and 'Bearer' followed by the token value.

# In[ ]:


bearer_token['Bearer Token'].iloc[0]


# In[4]:


header = {'Authorization' : 'Bearer {}'.format(bearer_token['Bearer Token'].iloc[0])}


# I then set the endpoint url to a variable. This will allow me to use a query to search twitter for specified content.

# In[5]:


endpoint_url = 'https://api.twitter.com/2/tweets/search/recent'


# ## Creating a Query

# Next I built my query and assigned it to a variable. The function _urllib.parse.quote_ takes the search that I put in quotes and replaces the symbols with _%xx_.
#         
#         The query I chose is ment to identify tweets with one or more of the hastags listed. I added #art AND #digitalart 
#         rather than OR because in my experiece #art is used alot out of the context of what I am looking for.

# In[6]:


query = urllib.parse.quote('( #art #digitalart OR #digitalart OR #traditionalart OR #myart OR #Inktober) lang:en')


# I created a variable to hold the tweet fields I wanted to get back from my query. Then I added my query to the end_point url defined earlier.
# 
#         Author_id: provides the id of the __user__ who posted
#         id: provides the __tweet id__
#         text: provides the __text__ of the tweet
#         public_metrics: provides the __retweets, likes_count, reply_count,__ and __quote_count__.
#         created_at: proved the __date__ on which the post was made
#         
# I added __entities__ as well, which contains __hashtags__. This field will be useful when answering questions on how an artist is using twitter. For example, I could use this information to check if posts with the #digitalart got more reactions then #traditionalart.

# In[7]:


tweet_fields = 'author_id,id,text,public_metrics,created_at,entities'


# I added the expansion "author_id" and added it to my query as _expansions_ containing "username".

# In[8]:


expansions = 'author_id'


# In[43]:


url = endpoint_url + '?query={}&tweet.fields={}&expansions={}&user.fields={}&max_results=100'.format(query,tweet_fields,expansions,"username")


# ## Creating Dataframes

# Using __resquest__ from the _requests_ library i requested the data from the url I defined with headers and assigned that data to a variable.
#     I then used __loads__ from the _json_ library to create a ___dictionary___ out of the text file.

# In[11]:


response_1 = requests.request("GET", url, headers=header)


# In[12]:


response_1_dict = json.loads(response_1.text)


# I created a __three dataframes__, one that held the original data, one that held the user data, and one that held the public metrics data

# In[13]:


df = pd.DataFrame(response_1_dict['data'])


# In[14]:


user1 = pd.DataFrame(response_1_dict['includes']['users'])


# In[15]:


metrics = pd.DataFrame(list(df['public_metrics']))


# I then added the elements I wanted from each dictionary onto my primary dictionary. I did this with each of the separate "pages" of data.

# In[16]:


df['name'] = user1['name']
df['username'] = user1['username']
df['likes'] = metrics['like_count']
df['retweets'] = metrics['retweet_count']
df['replys'] = metrics['reply_count']


# Because Each dataset maxed out at 100, I had to access the next set or "page" of data. this is done with the _next_token_
#     in order to access this I identified the keys of the dictionary and used the 'next_token' key from the 'meta' key. 

# In[17]:


response_1_dict.keys()


# In[ ]:


response_1_dict['meta']['next_token']


# To access the more data:
# 
#     - I added the next token to my url and assigned it to a variable 
#     - I then repeated the process above to create a new dictionary of data
#     - I repeated this process 2 more times to create 4 different dictionaries
#     

# In[19]:


page2 = url +'&next_token={}'.format(response_1_dict['meta']['next_token'])


# In[20]:


response_2 = requests.request("GET",url = page2, headers=header)


# In[21]:


response_2_dict = json.loads(response_2.text)


# In[22]:


df2 = pd.DataFrame(response_2_dict['data'])
user2 = pd.DataFrame(response_2_dict['includes']['users'])
metrics2 = pd.DataFrame(list(df2['public_metrics']))
ht2 = pd.DataFrame(list(df2['entities']))


# In[23]:


df2['name'] = user2['name']
df2['username'] = user2['username']
df2['likes'] = metrics2['like_count']
df2['retweets'] = metrics2['retweet_count']
df2['replys'] = metrics2['reply_count']


# In[24]:


page3 = url +'&next_token={}'.format(response_2_dict['meta']['next_token'])


# In[25]:


response_3 = requests.request("GET",url = page3, headers=header)


# In[26]:


response_3_dict = json.loads(response_3.text)


# In[27]:


df3 = pd.DataFrame(response_3_dict['data'])
user3 = pd.DataFrame(response_3_dict['includes']['users'])
metrics3 = pd.DataFrame(list(df3['public_metrics']))


# In[28]:


df3['name'] = user3['name']
df3['username'] = user3['username']
df3['likes'] = metrics3['like_count']
df3['retweets'] = metrics3['retweet_count']
df3['replys'] = metrics3['reply_count']


# In[29]:


page4 = url +'&next_token={}'.format(response_3_dict['meta']['next_token'])


# In[30]:


response_4 = requests.request("GET",url = page4, headers=header)


# In[31]:


response_4_dict = json.loads(response_4.text)


# In[32]:


df4 = pd.DataFrame(response_4_dict['data'])
user4 = pd.DataFrame(response_4_dict['includes']['users'])
metrics4 = pd.DataFrame(list(df4['public_metrics']))
ht4 = pd.DataFrame(list(df4['entities']))


# In[33]:


df4['name'] = user4['name']
df4['username'] = user4['username']
df4['likes'] = metrics4['like_count']
df4['retweets'] = metrics4['retweet_count']
df4['replys'] = metrics4['reply_count']


# 10. I __combined__ the four dictionaries together to create a _400 row_ dataframe by using the __DataFrame__ function from the _pandas library_

# ## Combining Data Frames

# In[34]:


tweets = pd.concat([df, df2, df3, df4])


# I delete the 'public_metrics' column from my master Data Frame to avoid duplication. 

# In[35]:


del tweets['public_metrics']


# In[36]:


len(tweets.index) 


# I used the __concat__ function from the _pandas_ library to combine all my previous Data Frames and make one master data frame I called "tweets". "tweets" was 400 rows long.
# 
# Then I used the __head__ and __tail__ functions to display the first and last 10 rows in my master dataframe.

# In[37]:


tweets.head(10)


# In[38]:


tweets.tail(10)


# 11. I was satisfied with this data so I __exported__ my full data frame as a csv using the __to_csv__ function in python. 
# 
# I saved my data into the same folder as my jupyternotebook so that I may refer to it later when answering hypothesis.

# In[39]:


tweets.to_csv(r'C:\Users\glori\Data in EMAT\tweets.csv')


# ## Potential weaknesses:
# - This is only 400 tweets, in the grand scheme of things that is not much data. However it is enouph to give me some evidence to answer the questions I have. There are some issues with the data where it stands right now. For example, from _entities_ I only want _hashtag_ so I need to find a way to isolate that aspect and change the header to read __hashtags__. However the issue is that 'entities' is set as a string not a list, and I dont have the knowledge yet to parse it into a list. 
# 
# - It should also be noted that the like_count appears to be 0 for all the columns. This is most likely inacurate. For example a tweet with over 2000 retweets, such as the one on line 98, would most likely NOT hav 0 likes.
# 
# - there is a lot of duplicate code. It would be beneficial  to create a function that created each of the individual data frames so that I could simply add in a couple variables and cut down on the lines of code.
# 
# ## Next Steps
# 
# In order to have the best results for my hypothesis I would need to:
# 1. Retrieve the 'tag' value from the _entities_ column
# 2. find a way to retrieve accurate "like" counts
# 3. Understand why some of the values are listed as NaN
# 4. create a function to combine and create the different "pages" of data.
