#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
for file in os.listdir("./"):
    
    filename=str(file)
    print(filename)
    name = filename.split('_')
    print(name)
    if file.endswith("Throughput.csv"):
        df=pd.read_csv(file,header=None)
        df = df.transpose()
        plt.plot(df)
        plt.title("Throughput")
        plt.xlabel('Batches Completed')
        plt.ylabel('Time Taken')
        plt.savefig(name[0]+'_'+name[2]+'_throughput.png')
        plt.show()  
    if file.endswith("Time.csv"):
        df=pd.read_csv(file,header=None)
        df = df.transpose()
        plt.title("Time")
        plt.xlabel('Batches Completed')
        plt.ylabel('Time Taken')
        x=plt.plot(df)
        plt.savefig(name[0]+'_'+name[2]+'_time.png')
        plt.show()
    
        


# In[ ]:




