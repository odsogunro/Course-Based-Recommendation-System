# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 19:40:03 2016

@author: keyur
"""
# Anticipated issue:
# Sparse Matrix Challenges (https://en.wikipedia.org/wiki/Collaborative_filtering)
# Cold Start issue (https://en.wikipedia.org/wiki/Cold_start)

from math import sqrt


# In[2]:
# A dictionary of course_reviews and their ratings of a small set of courses
# Entire List of course:
#    Web Analytics
#    Data Mining & Knowledge Discovery
#    Statistical Learning
#    Data Visualization
#    Social Network Analysis
#    Data Mining - II

course_reviews={'Alex': {'Web Analytics': 2.5, 'Data Mining & Knowledge Discovery': 3.5,
 'Statistical Learning': 3.0, 'Data Visualization': 3.5, 'Social Network Analysis': 2.5,
 'Data Mining - II': 3.0},
 
'Bob': {'Web Analytics': 3.0, 'Data Mining & Knowledge Discovery': 3.5,
 'Statistical Learning': 1.5, 'Data Visualization': 5.0, 'Social Network Analysis': 3.5},

'Charlie': {'Web Analytics': 2.5, 'Data Mining & Knowledge Discovery': 3.0,
 'Data Visualization': 3.5, 'Data Mining - II': 4.0},

'Doug': {'Data Mining & Knowledge Discovery': 3.5, 'Statistical Learning': 3.0,
 'Data Mining - II': 4.5, 'Data Visualization': 4.0,
 'Social Network Analysis': 2.5},

'Emily': {'Web Analytics': 3.0, 'Data Mining & Knowledge Discovery': 4.0,
 'Statistical Learning': 2.0, 'Data Visualization': 3.0, 'Data Mining - II': 3.0,
 'Social Network Analysis': 2.0},

'Frank': {'Web Analytics': 3.0, 'Data Mining & Knowledge Discovery': 4.0,
 'Data Mining - II': 3.0, 'Data Visualization': 5.0, 'Social Network Analysis': 3.5},

'Gary': {'Data Mining & Knowledge Discovery':4.5,'Social Network Analysis':1.0,'Data Visualization':4.0}}

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
# sim_distance(course_reviews,'Alex','Gary')

# In[2]:
# Returns the Pearson correlation coefficient for student1 and student2
def sim_pearson(prefs,student1,student2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[student1]:
    if item in prefs[student2]: si[item]=1

  # Find the number of elements
  n=len(si)

  # if they have no ratings in common, return 0
  if n==0: return 0

  # Add up all the preferences
  sum1=sum([prefs[student1][it] for it in si])
  sum2=sum([prefs[student2][it] for it in si])

  # Sum up the squares
  sum1Sq=sum([pow(prefs[student1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[student2][it],2) for it in si])

  # Sum up the products
  pSum=sum([prefs[student1][it]*prefs[student2][it] for it in si])

  # Calculate Pearson score
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0
  r=num/den

  return r
  
# sim_pearson(course_reviews,'Alex','Gary')
# Similarity scores ranges from -1 to 1, 1 means two people has exactly same rating for each item
  
# In[3]:
# Returns the best matches for student from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,student,n=5,similarity=sim_distance): #sim_pearson can be used
  scores=[(similarity(prefs,student,other),other)
                  for other in prefs if other!=student]

  # Sort the list so the highest scores appear at the top
  scores.sort(  )
  scores.reverse(  )
  return scores[0:n]

# topMatches(course_reviews,'Gary')

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
# getRecommendations(course_reviews,'Web Analytics')
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