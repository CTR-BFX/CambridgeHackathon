#!/usr/bin/python

#--------------------------------------------------------------------------------------------------
# fastq_check
# Performs basic checks on the intergrity of the fastq file
# 1. Searches for duplicate read names
# 2. Checks the sequence and quality string are the same length
#
# Malwina Prater (mn367@cam.ac.uk) and Russell S. Hamilton (rsh46@cam.ac.uk)
# Copyright 2017
# License GPLv3
#--------------------------------------------------------------------------------------------------

# Python version used: Python 2.7.12 :: Anaconda 4.2.0 (x86_64)


#  Subsample fastq files:
#
# ~/Documents/CTR-Repositories/Hackathon2017/CambridgeHackathon/seqtk sample -s100 read1.fq 10000 > sub1.fq
# seqtk sample -s100 read2.fq 10000 > sub2.fq
#
# seqtk sample -s100 SRR392418.fastq 10000 > sub.fq


#import Biopython as Bio
import os,sys
import numpy as np
from Bio import SeqIO
import pandas as pd 
import matplotlib.pyplot as plt
from beeswarm import *


# define variables:
DupCount = 0
Progress = 0
BailOnFirstError = 1
FileName = "small.fastq"
record_id_count = {}  # create empty dict
AllRecords_List = []  # create empty list
ii_list = []

try:
    with open(FileName, "rU") as handle:
        for record in SeqIO.parse(handle, "fastq-illumina"):
            AllRecords_List.append(record.id)
        #print(record.id)
            # Initialize an empty dictionary: record_id_count
            if record.id in record_id_count.keys():
                record_id_count[record.id] += 1
            else:
                record_id_count[record.id] = 1

    #print(record_id_count)
    #print(AllRecords_List)

# Make a dictionary of all entries with a duplicate:
        DupCount = {k:v for (k,v) in record_id_count.items() if v > 1}
        #print("\nDuplicated records:")
        #print(DupCount)

# Get indexes of entries with duplicates:
        y = DupCount.keys()
    
        values = np.array(AllRecords_List)
        searchvalues = y

        for searchval in searchvalues:
            ii = np.where(values == searchval)[0]
            ii_list.append(ii)
    #print("\nIndexes for each dup record (ii_list):")
    #print(ii_list)
        id_list = map(str, ii_list)

        Flat_list = [item for sublist in ii_list for item in sublist]
        Matching_records = [AllRecords_List[i] for i in Flat_list]

        df = pd.DataFrame({'Index' : Flat_list, 'Record_id' : Matching_records }, columns=['Index','Record_id']) 

        df_sorted = df.sort_values(by='Index')
    #print("\nTable with duplicated records:")
    #print(df_sorted)
 
        df_sorted.to_csv("Duplicated_records.csv", index = False, header = True)


#   https://matplotlib.org/users/pyplot_tutorial.html
#   https://github.com/mgymrek/pybeeswarm

    #print(list(df_sorted.columns.values))

# Plot duplicated records
 
        named_ii_list = dict(zip(DupCount, ii_list))
        #print(ii_list)
 
        bs, ax = beeswarm(ii_list, method="swarm", labels=DupCount)
        #plt.show(bs)
        plt.savefig("Beeswarm_plot_duplicates.png")
  


except:
    print "\nError->\tFile: %s does not exist\n" % FileName
    sys.exit()



#close(handle)
handle.close()





