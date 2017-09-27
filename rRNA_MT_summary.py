#!/usr/bin/env python

# Malwina Prater, mn367@cam.ac.uk,  2017, Copyright
# Centre for Trophoblast Research, University of Cambridge
#
# Script version: v01.
#
# Script to calculate the percent of transcripts mapping to rRNA
#
#  INPUTS :
# Outputs of rRNA_MT_count.py program that used HTseq_counts and GTF files.
# Outputs can be recognised by pattern: *_htseq_combined_counts.txt
#
#
#  USAGE :    
# Use command for summary:
#
# ./rRNA_MT_summary.py --start C --end _rRNAmtRNACounts.txt --pattern _Aligned.out.srt.bam_htseq_combined_counts
# python rRNA_MT_summary.py --pattern _Aligned.out.srt.bam_htseq_combined_counts _rRNAmtRNACounts.txt


# import modules: 

#import os.path
import os,sys
from optparse import OptionParser
import re
import numpy as np
import pandas as pd 



parser = OptionParser(usage="%prog [-x Excel [-i imagefile] [-s squares]",
                      version="%prog 0.1")

#parser.add_option("--start", dest="start", type="string", action="store")
#parser.add_option("--end", dest="end", type="string", action="store")
#parser.add_option("--pattern", dest="pattern", type="string", action="store")
parser.add_option("--pattern", dest="pattern", type="string", action="store")

(options, args) = parser.parse_args()

#files = sys.argv[]
#start = options.start
#end = options.end
pattern = options.pattern
print pattern



files = []
#   http://pythoncentral.io/series/python-recursive-file-and-directory-manipulation/
topdir = '.'
# The arg argument for walk, and subsequently ext for step
exten = '_rRNAmtRNACounts.txt'
def step(ext, dirname, names):
    ext = ext.lower()
    for name in names:
        if name.lower().endswith(ext):
            #print(os.path.join(dirname, name))
            files.append(os.path.join(dirname, name))

# Start the walk
os.path.walk(topdir, step, exten) 


#logname = 'HTSEQ_rRNA_MT_count_files_list.log' 
#def step((ext, logpath), dirname, names):
#    ext = ext.lower()
#    for name in names:
#        if name.lower().endswith(ext):
#            # Instead of printing, open up the log file for appending
#            with open(logpath, 'a') as logfile:
#                logfile.write('%s\n' % os.path.join(dirname, name))
#     Change the arg to a tuple containing the file
#     extension and the log file name. Start the walk.
#os.path.walk(topdir, step, (exten, logname))

rRNA_reads = []
MT_reads = []
sample = []

for file in files:
    print "File processed: ", file,  "\n";
    try:
        handle = open(file, "rU")
        handle.close()
    except:
        print "\nError->\t File: %s does not exist\n" % file
        sys.exit()


for file in files:
    with open(file, "rU") as handle:
        for line in handle:
            line.rstrip()
            if 'HT-SEQ file name: ' in line:
                values = line.split(" ")
                name = values[3]
                name = re.sub(pattern, '', name) 
                name = re.sub(".txt", '', name) 
                sample.append(name)
                #print(name)
            if 'No. of rRNA identifiers' in line:
                values = line.split(" ")
                #print(values[4])
                rRNA_reads.append(values[4])
            if 'No. of MT identifiers' in line:
                values = line.split(" ")
                #print(values[4])
                MT_reads.append(values[4])                
        
handle.close()  

print(rRNA_reads, MT_reads)



df = pd.DataFrame({'Sample' : sample, 'MT' : MT_reads, 'rRNA' : rRNA_reads }, columns=['Sample','MT', 'rRNA']) 


file = "rRNA_mtRNA.summary.txt"









