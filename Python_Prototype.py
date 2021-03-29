# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 22:35:41 2021

@author: Clark Xu
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

class DimensionError(Exception):
    """
    Exception for errors in array dimension
    """
    def __init__(self,dimension,message="Error with dimensions"):
        self.dimension = dimension
        self.message = message
        super().__init__(self.message+" "+str(self.dimension))

def generateData(filename,n,ids,ages):
    """
    Input: filename (str), Number of users - n (int), ID range - ids ([int,int]), Age range - ages ([int,int])
    Output: Create comma-delimited file withs lines: user ID (int), user age (int) 
    """
    
    #Generate Data
    
    ##User IDs of size n drawn uniquely from idRange 
    idRange = np.arange(start=ids[0],stop=ids[1])
    userIDs = np.random.choice(a=idRange,size=(n,1),replace=False)
    
    ##User Ages of size n drawn with replacement from ageRange
    ageRange = np.arange(start=ages[0],stop=ages[1])
    userAges = np.random.choice(a=ageRange,size=(n,1),replace=True)
    
    ##Combine User IDs and User Ages
    data = np.concatenate((userIDs,userAges),axis=1)
    
    ##Note Output is of shape n,2
    outputCheck = (n,2)
    if not(np.shape(data) == outputCheck):
        raise DimensionError(np.shape(data))
    
    #Save Data (decimal, comma-delimited, one user per line, with headers)
    np.savetxt(filename,data,fmt='%d',delimiter=',',newline='\n',header='userID,userAge',comments='')
    
    #Check for File
    fileCheck = os.path.isfile(filename)
    
    #Indicate Whether Data Generation Successful
    return print("Data Generated: "+str(fileCheck))

def countData(filename,resultfile):
    """
    Input: filename (str), resultfile (str)
    Output: Create comma-delimited file withs lines: user age (int), count of age (int) 
    """
    
    #Load Data (integer, comma-delimited, one user per line, with headers)
    data = np.loadtxt(filename,dtype=int,delimiter=',',skiprows=1)
    
    #Count Age (age in second column)
    countAge = np.unique(data[:,1],return_counts=True)
    
    #Format Age Data (as numpy array, transposed)
    ageData = np.array(countAge).T
    
    #Save Data (decimal, comma-delimited, one user per line, with headers)
    np.savetxt(resultfile,ageData,fmt='%d',delimiter=',',newline='\n',header='age,ageCount',comments='')
    
    #Check for File
    fileCheck = os.path.isfile(resultfile)
    
    #Indicate Whether Data Generation Successful
    return print("Data Counted: "+str(fileCheck))   

def graphData(filename,resultfile):
    """
    Input: filename (str), resultfile (str)
    Output: Create data visualization
    """

    #Load Data (integer, comma-delimited, one user per line, with headers)
    data = pd.read_csv(filename,sep=",")
    
    #Plot Data
    graph = seaborn.distplot(data['age'],kde=False,color='blue',bins=10)
    
    #Label Plot
    plt.title('Patient Age Distribution',fontsize=14)
    plt.xlabel('Age (years)',fontsize=12)
    plt.ylabel('Age Count (frequency)',fontsize=12)
    
    #Save Plot
    graph.figure.savefig(resultfile)
    
    #Check for File
    fileCheck = os.path.isfile(resultfile)
    
    #Indicate Whether Data Generation Successful
    return print("Data Graphed: "+str(fileCheck))

def main():
    """
    Input: File which contains an arbitrary number of lines.
    Each line contains an integer user ID and an integer user age, delimited by a comma.
    
    Output: List of tuples.
    Each tuple contains a distinct age and the count of users with that age, delimited by a comma.
    """
    #Create 750 patients, with ages between 1 and 89, and MRNs between 100000 and 999999
    generateData(filename='Test Data',n=750,ids=[100000,999999],ages=[1,89])
    
    #Return ages and counts of users with age
    countData(filename='Test Data',resultfile='Output')
    
    #Visualize data
    graphData(filename='Output',resultfile='Output Visualization.png')

if __name__ == "__main__":
    main()
