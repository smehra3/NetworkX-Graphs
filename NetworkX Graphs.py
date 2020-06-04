
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 1 - Creating and Manipulating Graphs
# 
# Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file `Employee_Movie_Choices.txt`.
# 
# A second file, `Employee_Relationships.txt`, has data on the relationships between different coworkers. 
# 
# The relationship score has value of `-100` (Enemies) to `+100` (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.
# 
# Both files are tab delimited.

# In[2]:


import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite


# This is the set of employees
employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])


# you can use the following function to plot graphs
# make sure to comment it out before submitting to the autograder
def plot_graph(G, weight_name=None):
    '''
    G: a networkx G
    weight_name: name of the attribute for plotting edge weights (if G is weighted)
    '''
    get_ipython().magic('matplotlib notebook')
    import matplotlib.pyplot as plt
    
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None
    
    if weight_name:
        weights = [int(G[u][v][weight_name]) for u,v in edges]
        labels = nx.get_edge_attributes(G,weight_name)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights);
    else:
        nx.draw_networkx(G, pos, edges=edges);


# ### Question 1
# 
# Using NetworkX, load in the bipartite graph from `Employee_Movie_Choices.txt` and return that graph.
# 
# *This function should return a networkx graph with 19 nodes and 24 edges*

# In[11]:


def answer_one():
        
    # Your Code Here
    movie_choices_df = pd.read_csv('Employee_Movie_Choices.txt', sep='\t',
                       header=None, skiprows = 1, names=['Employees', 'Movies'])
    return nx.from_pandas_dataframe(movie_choices_df, 'Employees', 'Movies')


# ### Question 2
# 
# Using the graph from the previous question, add nodes attributes named `'type'` where movies have the value `'movie'` and employees have the value `'employee'` and return that graph.
# 
# *This function should return a networkx graph with node attributes `{'type': 'movie'}` or `{'type': 'employee'}`*

# In[14]:


def answer_two():
    
    # Your Code Here
    graph = answer_one()
    graph.add_nodes_from(employees, bipartite=0, type='employee')
    graph.add_nodes_from(movies, bipartite=1, type='movie')
    return graph# Your Answer Here


# ### Question 3
# 
# Find a weighted projection of the graph from `answer_two` which tells us how many movies different pairs of employees have in common.
# 
# *This function should return a weighted projected graph.*

# In[15]:


def answer_three():
        
    # Your Code Here
    
    return bipartite.weighted_projected_graph(answer_two(),employees)# Your Answer Here


# In[16]:


answer_three().edges(data=True)


# ### Question 4
# 
# Suppose you'd like to find out if people that have a high relationship score also like the same types of movies.
# 
# Find the Pearson correlation ( using `DataFrame.corr()` ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in common it should be treated as a 0, not a missing value, and should be included in the correlation calculation.
# 
# *This function should return a float.*

# In[19]:


def answer_four():
        
    # Your Code Here
    er_df = pd.read_csv('Employee_Relationships.txt', sep='\t', header = None, names = ['emp1','emp2','relationship'])
    #print(er_df['relationship'])
    #er_df[1]['relationship']=er_df[1]['relationship'].map(lambda z: z['relationship'])
    #er = nx.read_edgelist('Employee_Relationships.txt', data=[('relationship', int)])
    #er_df = pd.DataFrame(er.edges(data=True), columns=['emp1', 'emp2', 'relationship'])
    
    common_movies_df = pd.DataFrame(answer_three().edges(data=True), columns=['emp1','emp2','no_of_common_movies'])
    common_movies_df['no_of_common_movies']=common_movies_df['no_of_common_movies'].map(lambda x: x['weight'])
    
    common_movies_df_flipped = common_movies_df.copy()
    common_movies_df_flipped.rename(columns={'emp1':'emp2', 'emp2':'emp1'}, inplace=True)
    #common_movies_df_flipped.rename(columns={'emp1_':'emp2'}, inplace=True)
    #common_movies_df_flipped.rename(columns={'emp1':'emp2', 'emp2':'emp1'}, inplace=True)
    
    common_movies_all_df = pd.concat([common_movies_df, common_movies_df_flipped], ignore_index=True)
    
    merged = pd.merge(common_movies_all_df, er_df, on = ['emp1', 'emp2'], how='right')
    #merged['no_of_common_movies'] = merged['no_of_common_movies'].map(lambda x: x['weight'] if type(x)==dict else None)
    #merged['relationship'] = merged['relationship'].map(lambda x: x['relationship'])
    merged['no_of_common_movies'].fillna(value=0, inplace=True)
    #print(merged)
    #merged = merged.fillna(0)
    #return merged['no_of_common_movies'].corr(merged['relationship'])
    return merged.corr(method ='pearson')['no_of_common_movies']['relationship']# Your Answer Here

