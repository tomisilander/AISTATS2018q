#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['text.usetex'] = True
import seaborn as sns

def subplots(folder = "results/real_dag_shd/", save = False):
    
    names = ["Survey", "Earthquake", "Sachs","Cancer","Asia"]
    
    filee = open(folder + names[0].lower() + ".txt", mode = 'r')
    line1 = filee.readline()
    filee.close()
    
    line1 = line1.rstrip("\n")
    header = line1.split(" ")
    
    methods = header.copy()
    methods.pop(0)    

    methods = ["BIC", "BDeu", "fNML", "qNML"] 
    
    fig,axs = plt.subplots(nrows = 3, ncols = 2,sharex = True, figsize = (10,11) )
    
    axs = axs.flatten()
    linestyles = ['--', ':', '-.', '-']

    jj = 0
    
    for dag_name in names: 
    
        x = np.loadtxt(folder + dag_name.lower() + ".txt", skiprows = 1)
        
        ns = x[:,0]
        shds = x[:,1::]


        sns.set_style("ticks")
        sns.set_palette("colorblind")
                
        ax = axs[jj]

        ax.set(xscale = "log")

        for ii in range(0,len(methods)):
            ax.plot(ns,shds[:,ii],linestyles[ii],label = methods[ii])

        jj += 1
        
        ax.set_title(dag_name)
        sns.set_context("poster", font_scale = 2, rc={"lines.linewidth": 7})
        sns.despine()
        
        
    ax = axs[len(names)]
   
    for i in range(0,len(methods)):
        lab = methods[i]
        ax.plot([],[],linestyles[i],label = lab)
        
    ax.legend(loc="center")
    
    ax.set_axis_off() 
    
    
    for jj in range(0,len(names)):
        ax = axs[jj]
    
        
    
    #plt.tight_layout()
    plt.show()
    
    
    # tweak the y labels
    for jj in range(0,len(names)):
        ax = axs[jj]
    
        labels = ax.get_yticklabels()
        
        #print(labels[2])
        for kkk in range(0,len(labels)):
            if kkk % 2 == 1:
                labels[kkk].set_text("")
                
        ax.set_yticklabels(labels)
    
    
        
    if save:
        fig.savefig(folder + "shd_all.pdf")
    

    
def rank_shd(folder = "results/real_dag_shd/", save = False):
    
    names = ["survey", "earthquake", "sachs","cancer","asia"]
    
    filee = open(folder + names[0] + ".txt", mode = 'r')
    line1 = filee.readline()
    filee.close()
    
    line1 = line1.rstrip("\n")
    header = line1.split(" ")
    
    methods = header.copy()
    methods.pop(0)    

    createArray = True
    
    for dag_name in names:
        
        x = np.loadtxt(folder + dag_name + ".txt", skiprows = 1)     
        ns = x[:,0]
        shds = x[:,1::]
 
        if createArray:
            n,d = shds.shape
            avg_ranks = np.zeros((n,d))
            createArray = False


        ranks = score_to_rank(shds)
        avg_ranks += ranks
        
    
    avg_ranks = avg_ranks/len(names)    

    
    fig = plt.figure()
      
    sns.set_style("ticks")
    sns.set_palette("colorblind")
        
    linestyles = ['--', ':', '-.', '-']
  
    ax = plt.subplot(111)
    
    ax.set(xscale = "log")
    
    for ii in range(0,len(methods)):
        ax.plot(ns,avg_ranks[:,ii],linestyles[ii],label = methods[ii], linewidth = 6)
            
      
    ax.set_ylabel("Avgerage rank")
    ax.set_xlabel("Sample size")    
    
    plt.legend(loc = "best")
         
    sns.despine()
    sns.set_context("poster")
    plt.show()

    if save:
        fig.savefig(folder + "shd_rank.pdf")
    
   
def rank_shd_from_single_tests(folder = "results/real_dag_shd/", save = False):
    
    names = ["Survey", "Earthquake", "Sachs","Cancer","Asia"]
    NTESTS = 1000    

    filee = open(folder + names[0].lower() + "_all.txt", mode = 'r')
    line1 = filee.readline()
    filee.close()
    
    line1 = line1.rstrip("\n")
    header = line1.split(" ")
    
    methods = header.copy()
    methods.pop(0)    
    methods = ["BIC", "BDeu", "fNML", "qNML"] 
    createArray = True
    
    
    # sum ranks over different dags
    for dag_name in names:
        
        x = np.loadtxt(folder + dag_name.lower() + "_all.txt", skiprows = 1)
        ns_all = x[:,0]
        shds_all = x[:,1::]
        
        if createArray:
            n,d = shds_all.shape
            ranks_all = np.zeros((n,d))
            createArray = False


        ranks = score_to_rank(shds_all)
        ranks_all += ranks
        
    
    n_samplesizes = int(n/NTESTS)
    
    ns = np.zeros(n_samplesizes,dtype = np.int)
    avg_ranks = np.zeros((len(ns),4))  
    
    # sum over 1000 tests for each sample size
    for tt in range(0,n_samplesizes):
        start_inx = tt*NTESTS
        end_inx = (tt+1)*NTESTS
           
        ns[tt] = np.unique(ns_all[start_inx:end_inx])
        avg_ranks[tt,:] = np.sum(ranks_all[start_inx:end_inx,:],axis = 0)
    
              
    avg_ranks = avg_ranks/(len(names)*NTESTS)    

    fig = plt.figure()
    
   
    sns.set_style("ticks")
    sns.set_palette("colorblind")
        
    linestyles = ['--', ':', '-.', '-']
  
    ax = plt.subplot(111)
    
    ax.set(xscale = "log")
    
    for ii in range(0,len(methods)):
        ax.plot(ns,avg_ranks[:,ii],linestyles[ii],label = methods[ii], linewidth = 6)
            
      
    ax.set_ylabel("Average rank")
    ax.set_xlabel("Sample size")    
    
    plt.legend(loc = "best")
         
    plt.gcf().subplots_adjust(bottom=0.15)
    sns.despine()
    sns.set_context("poster", font_scale = 2, rc={"lines.linewidth": 6})
    plt.show()
    
    
    if save:
        fig.savefig(folder + "shd_rank_all.pdf")
    
#    return(ns,avg_ranks,header) 
        
def score_to_rank(x):
        
    n,d = x.shape
    ranks = np.zeros((n,d),dtype = np.int)
        
    for ii in range(0,n):      
        sortted = np.unique(x[ii,:],return_inverse = True)[1]
      
        for jj in range(0,d):
            ranks[ii,jj] = sortted[jj] + 1
        
    return(ranks)
    
if __name__ == "__main__":
    save = True
    folder = "results/real_dag_shd/"
    subplots(folder = folder, save = save)
    #rank_shd(folder = folder, save = save)
    rank_shd_from_single_tests(folder = folder, save = save)
    
    
