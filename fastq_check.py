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



#  Subsample fastq files:
#
# ~/Documents/CTR-Repositories/Hackathon2017/CambridgeHackathon/seqtk sample -s100 read1.fq 10000 > sub1.fq
# seqtk sample -s100 read2.fq 10000 > sub2.fq
#
# seqtk sample -s100 SRR392418.fastq 10000 > sub.fq


#import Biopython as Bio
import os,sys
import numpy #as na

# define variables:
DupCount = 0
Progress = 0
BailOnFirstError = 1
FileName = "small.fastq"
record_id_count = {}

from Bio import SeqIO

try:
    with open(FileName, "rU") as handle:
        for record in SeqIO.parse(handle, "fastq-illumina"):
            print(record.id)
            #print(record)
            # Initialize an empty dictionary: record_id_count
            if record.id in record_id_count.keys():
                record_id_count += 1
            else:
                record_id_count[record.id] = 1
            print(record_id_count)

        print(record_id_count)

        # Make a dictionary of all entries with a duplicate
        print "Hello"

        DupCount = { key:value for key, value in record_id_count() if value > 1 }
        print(DupCount)


except:
    print "\nError->\tFile: %s does not exist\n" % FileName
    sys.exit()



#close(handle)
handle.close()





