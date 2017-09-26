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
import numpy #as na
from Bio import SeqIO


# define variables:
DupCount = 0
Progress = 0
BailOnFirstError = 1
FileName = "small.fastq"
record_id_count = {}


#try:
with open(FileName, "rU") as handle:
    for record in SeqIO.parse(handle, "fastq-illumina"):
        #print(record.id)
            # Initialize an empty dictionary: record_id_count
        if record.id in record_id_count.keys():
                record_id_count[record.id] += 1
        else:
                record_id_count[record.id] = 1

    #print(record_id_count)

        # Make a dictionary of all entries with a duplicate
    DupCount = {k:v for (k,v) in record_id_count.items() if v > 1}
    print(DupCount)
    #for key, value in record_id_count.items():
    #    if 1 < value:
    #        print key

    y = DupCount.keys()
    print(y)
    x = record_id_count.keys()
    print(x)
    
    print(x.index(y))
    

#except:
#    print "\nError->\tFile: %s does not exist\n" % FileName
#    sys.exit()



#close(handle)
handle.close()





