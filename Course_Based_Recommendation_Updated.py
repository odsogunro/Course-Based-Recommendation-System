# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 17:06:49 2016

@author: keyur
"""

# import os
# os.getcwd()
# os.chdir('Path')

from math import sqrt
#from xlrd import open_workbook
#book = open_workbook('FE550 Project Plan & Data.xlsx')
#
#xl_sheet = book.sheet_by_index(2)
#print ('Sheet name: %s' % xl_sheet.name)


# In[]:
from pandas import *
import pandas as pd
import numpy as np
xls = ExcelFile('FE550 Project Plan & Data_Updated.xlsx')
df = xls.parse(xls.sheet_names[4])
print df.to_dict()


data_frame = df[['Student Name','Course Name','Course Rating']]

#data_frame.groupby(data_frame['Student Name'])

# In[]:
#data_frame.set_index('Student Name').T.to_dict()
#temp = data_frame[1:2]
#temp1 = data_frame[48:50]


# In[]:

# Changing unicode string to normal string

types = data_frame.apply(lambda x: pd.lib.infer_dtype(x.values))
     
for col in types[types=='unicode'].index:
    data_frame[col] = data_frame[col].astype(str)

data_frame.apply(lambda x: pd.lib.infer_dtype(x.values))

# In[]:

# Function to convert pandas dataframe into dictionary
def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.ix[:,1:]) for k,g in grouped}
    return d
    
 # In[]:

# Creating nested dictionary    
course_reviews = recur_dictify(data_frame)


# In[]:

# Removing White spaces from dictionary
#def removew(d):
#    return   {k.strip():removew(v)
#             if isinstance(v, dict)
#             else v
#             for k, v in d.iteritems()}
#
#removew(course_reviews)
##removew(course_reviews['Keyur Doshi'])
#
#
## In[]:
#
##for sub in course_reviews['Addie Gin']:
##    for key in sub:
##        sub[key] = float(sub[key])
#
#dict_with_ints = dict((k.strip(),v) for k,v in course_reviews.iteritems())

# In[]:
# Get Slice of dictionary
from itertools import islice
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

take(7,course_reviews.iteritems())

# In[1]:
# Returns a distance-based similarity score for student1 and student2
def sim_distance(prefs,student1,student2):
  # Get the list of shared_items
  si={}
  for item in prefs[student1]:
    if item in prefs[student2]:
       si[item]=1
    
  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[student1][item]-prefs[student2][item],2)
                      for item in si])

  # Above function calculates the distance which will be smaller for people who are more similar.
  # However, you need a function that gives higher values for people who are similar. 
  # This can be done by adding 1 to the function (so you don’t get a division-by-zero error) and inverting it:
  return 1/(1+sqrt(sum_of_squares))
  
# sqrt(pow(3.5-4,2))  
# sim_distance(course_reviews,'Yu Strobl','Yun Chen')

# In[2]:
# Returns the Pearson correlation coefficient for student1 and student2
#def sim_pearson(prefs,student1,student2):
#  # Get the list of mutually rated items
#  si={}
#  for item in prefs[student1]:
#    if item in prefs[student2]: si[item]=1
#
#  # Find the number of elements
#  n=len(si)
#
#  # if they have no ratings in common, return 0
#  if n==0: return 0
#
#  # Add up all the preferences
#  sum1=sum([prefs[student1][it] for it in si])
#  sum2=sum([prefs[student2][it] for it in si])
#
#  # Sum up the squares
#  sum1Sq=sum([pow(prefs[student1][it],2) for it in si])
#  sum2Sq=sum([pow(prefs[student2][it],2) for it in si])
#
#  # Sum up the products
#  pSum=sum([prefs[student1][it]*prefs[student2][it] for it in si])
#
#  # Calculate Pearson score
#  num=pSum-(sum1*sum2/n)
#  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
#  if den==0: return 0
#  r=num/den
#
#  return r
  
# sim_pearson(course_reviews,'Yu Strobl','Yun Chen')
# Similarity scores ranges from -1 to 1, 1 means two people has exactly same rating for each item
  
# In[3]:
# Returns the best matches for student from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,student,n=5,similarity=sim_distance): #sim_pearson can be used
  scores=[(similarity(prefs,student,other),other)
                  for other in prefs if (other!=student)]

  # Sort the list so the highest scores appear at the top
  scores.sort(  )
  scores.reverse(  )
  return scores[0:n]

#topMatches(dict_with_ints,'Addie Gin')

# In[]:

# In[4]:
# Gets recommendations for a student by using a weighted average
# of every other student's rankings
def getRecommendations(prefs,student,similarity=sim_distance): #sim_pearson can be used
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==student: continue
    sim=similarity(prefs,student,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:

      # only score course I haven't taken yet
      if item not in prefs[student] or prefs[student][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items(  )]

  # Return the sorted list
  rankings.sort(  )
  rankings.reverse(  )
  return rankings

# Which course should I take next
# getRecommendations(course_reviews,'Pricing and Hedging')
# In[5]:
# Transform preference
def transformPrefs(prefs):
  result={}
  for student in prefs:
    for item in prefs[student]:
      result.setdefault(item,{})

      # Flip item and person
      result[item][student]=prefs[student][item]
  return result
  
  # rev_reviews=transformPrefs(course_reviews)
  # topMatches(rev_reviews,'Web Analytics')
  # getRecommendations(rev_reviews,'Web Analytics')
  
# In[6]:
# Calculate similar items
def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}

  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

itemsim=calculateSimilarItems(course_reviews)

# Courses similar to each course
# itemsimim

# In[7]:
def getRecommendedItems(prefs,itemMatch,student):
  userRatings=prefs[student]
  scores={}
  totalSim={}

  # Loop over items rated by this user
  for (item,rating) in userRatings.items(  ):

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue

      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating

      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items(  )]

  # Return the rankings from highest to lowest
  rankings.sort(  )
  rankings.reverse(  )
  return rankings

# getRecommendedItems(course_reviews,itemsim,'Gary')


# In[]: Compute the like minded person for a given person -- topMatches(course_reviews,'Gary')

# Get recommendation to the poeple who have not taken this course so far:
 # rev_reviews=transformPrefs(course_reviews)
 # topMatches(rev_reviews,'Web Analytics')
 # getRecommendations(rev_reviews,'Web Analytics') 

# Get the list of course recommendation of the person:
# getRecommendedItems(course_reviews,itemsim,'Gary')
