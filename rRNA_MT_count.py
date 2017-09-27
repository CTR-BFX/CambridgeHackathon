#!/usr/bin/python

# Malwina Prater, mn367@cam.ac.uk,  2017, Copyright
# Centre for Trophoblast Research, University of Cambridge
#
# Script version: v01.
#
# Script to calculate the percent of transcripts mapping to rRNA
#
#  INPUTS :
# 1. HTseq_counts file
# 2. Original reference transcriptome alignned to
#
#  USAGE :    
#  For producing table(s) with rRNA and MT counts for each sample use commands like that:
#
#    ./rRNA_MT_count.py --gtf /Users/malwina/Documents/CTR-Data/genomes/Mus_musculus/mm10/Mus_musculus.GRCm38.84.gtf --htseq C17_3_S20_Aligned.out.srt.bam_htseq_combined_counts.txt
#


# import modules: 
import os,sys
from optparse import OptionParser
import re

# parse in the user options:

parser = OptionParser(usage="%prog [-x Excel [-i imagefile] [-s squares]",
                      version="%prog 0.1")

parser.add_option("--htseq", dest="FileName", type="string", action="store")
parser.add_option("--gtf", dest="GTF", type="string", action="store")

(options, args) = parser.parse_args()


#files = sys.argv[]
HTSEQ_COUNTS = options.FileName
GTF = options.GTF


# check if files supplied exist:
try:
    handle = open(GTF, "rU")
    handle.close()
except:
    print "\nError->\tGTF File: %s does not exist\n" % GTF
    sys.exit()

try:
    handle = open(HTSEQ_COUNTS, "rU")
    handle.close()
except:
    print "\nError->\tFile: %s does not exist\n" % HTSEQ_COUNTS
    sys.exit()


#
# First job is to extract all the identifiers of genes/transcripts mapping to the rRNA and MT genes and store in 2 arrays
#

rRNA_identifiers = {}
MT_identifiers = {}


with open(GTF, "rU") as handle:
    #line = handle.readline()
    for line in handle:
    	line.rstrip('\n')
    	if 'gene_biotype "rRNA"' in line:
            identifier = line
            identifier = re.sub('.*gene_id "', '', identifier)
            identifier = re.sub('"; gene_version.*\n', '', identifier)
            rRNA_identifiers[identifier] = 1
        if 'MT' in line:
            identifier = line
            identifier = re.sub('.*gene_id "', '', identifier)
            identifier = re.sub('"; gene_version.*\n', '', identifier)
            MT_identifiers[identifier] = 1    
handle.close()    

#print("rRNA:")
#print(rRNA_identifiers.keys())
#print("MT:")
#print(MT_identifiers.keys())


#
# Second job is to go through the HTSEQ-couts and count reads matching the rRNA identifiers
#
Cummulative_rRNA_Count = 0
rRNA_genes = 0
ReadCount = 0
line_number = 0
MT_genes = 0;
Cummulative_MT_Count = 0;

with open(HTSEQ_COUNTS, "rU") as handle:
    for line in handle:
    	line.rstrip('\n')            

        split_line = line.split("\t")
        if line_number > 0:
       	    if split_line[0] in rRNA_identifiers.keys():  # if rRNA_identifiers[gene_id]
                rRNA_genes += 1
                Cummulative_rRNA_Count += int(split_line[1])
            if split_line[0] in MT_identifiers.keys():
                MT_genes += 1
                Cummulative_MT_Count += int(split_line[1])
            ReadCount += int(split_line[1])
        line_number += 1
handle.close()    
#print(Cummulative_MT_Count)
#print(Cummulative_rRNA_Count)


#
# wiritng the output files:
#              
out = HTSEQ_COUNTS + '_rRNAmtRNACounts.txt'; 
out = re.sub('.txt_', '_', out)

print "Summary output file:		", out, "\n"

OUT = open(out, "w")
OUT.write('HT-SEQ file name: \t' + HTSEQ_COUNTS + '\n\n')
OUT.write('GTF file name: \t\t' + GTF + '\n\n\n')
OUT.write('---------------------------------------------------------------------------------' + '\n')
OUT.write('  rRNA and MT identifiers\n')
OUT.write('---------------------------------------------------------------------------------' + '\n')
OUT.write('No. of rRNA identifiers: ' + str(len(rRNA_identifiers.keys())) + '\n') # PRINT size of this hash
OUT.write('No. of MT identifiers: ' + str(len(MT_identifiers.keys())) + '\n') # PRINT size of this hash
OUT.write('\n\n')
OUT.write('---------------------------------------------------------------------------------' + '\n')
OUT.write('  HTSEQ mapping summary\n')
OUT.write('---------------------------------------------------------------------------------' + '\n')
OUT.write('ReadCount: ' + str(ReadCount) + '\n\n')
#OUT.write('  Number of rRNA genes: ' + str(rRNA_genes) + '\n')
OUT.write('Total no. of rRNA transcripts: ' + str(Cummulative_rRNA_Count) + '\n')
perc_rRNA = 100*float(Cummulative_rRNA_Count)/float(ReadCount)
perc_rRNA = str(round(perc_rRNA, 3))
OUT.write('Percent rRNA mapped reads: ' + str(Cummulative_rRNA_Count) + ' / ' + str(ReadCount) + ' * 100 = ' + perc_rRNA + '%\n\n')
#OUT.write('\n  Number of MT genes: ' + str(MT_genes) + '\n')
OUT.write('Total no. of MT transcripts: ' + str(Cummulative_MT_Count) + '\n')
perc_MT = 100*float(Cummulative_MT_Count)/float(ReadCount)
perc_MT = str(round(perc_MT, 3))
OUT.write('Percent MT mapped reads: ' + str(Cummulative_MT_Count) + ' / ' + str(ReadCount) + ' * 100 = ' + perc_MT + '%\n\n')
OUT.close()


