#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

# Columns corresponding to desired data, subtract 1 to get to python indexing
transactionAmount_col = 14 #15-1
candidateID_col = 16 #17-1

# These will store the info from the file
colvalues_array = []
candidateID_array = []

for row in csv.reader(fileinput.input(), delimiter='|'):
    #if not fileinput.isfirstline():
    #in this case first line is also data (not all the fieldnames)

    #For median, need to store all elements of array
    #but in that case, just calculate statistics after this for loop
    #using built-in functions of the list
    colvalues_array.append(float(row[transactionAmount_col]))    
    if row[candidateID_col] not in candidateID_array:
        candidateID_array.append(row[candidateID_col]) #candidateID can be str


colvalues_array.sort() #for median
total = sum(colvalues_array)
maxvalue = max(colvalues_array)
minvalue = min(colvalues_array)
count = len(colvalues_array)
mean = total / count
median = colvalues_array[int(count//2)]

variance = 0
for value in colvalues_array:
    variance += (value-mean)**2
variance /= count

##### Print out the stats
print "Statistics for all transactions:"
print "Total: %.2f" % total
print "Minimum: %.2f" % minvalue
print "Maximum: %.2f" % maxvalue
print "Mean: %.2f" % mean
print "Median: %.2f" % median
print "Standard Deviation: %.2f" % variance**0.5

##### Comma separated list of unique candidate ID numbers
print "Candidates:%.0f" % (len(candidateID_array)-1)
print "There are also transactions with no candidate ID.\n"
#print "%s" % (",".join(candidateID_array))


def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    norm = (value - minvalue)/(maxvalue - minvalue)
    return norm

##### Min-max normalize the statistics
print "Min-max normalized stats:"
print "Total contributions: %.2f" % minmax_normalize(total)
print "Minimum: %.2f" % minmax_normalize(minvalue)
print "Maximum: %.2f" % minmax_normalize(maxvalue)
print "Mean: %.2e" % minmax_normalize(mean)
print "Median: %.2e" % minmax_normalize(median)
print "Standard Deviation: %.2e" % minmax_normalize(variance**0.5)




#class Candidate:
#    ID
#    MEAN