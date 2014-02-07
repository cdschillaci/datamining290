#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

# Column numbers in data file for various info. Subtract one to convert to python indexing
transactionAmount_col = 14 #15-1
candidateID_col = 16 #17-1

# This class describes a candidate, computes the statistics for that candidate
# and provides some interfaces to return this info in various ways
class Candidate:
    'This class stores a candidates records and some statistical info about them'
    nCandidates=0
    csvHeader=['Candidate ID']+['Total Contributions']+['Z Value of Total']+['Minimum Contribution']\
        +['Maximum Contribution']+['Median Contribution']+['Mean Contribution']+['Stdev of Contributions']
    
    def __init__(self, candidateID):
        self.ID=candidateID
        Candidate.nCandidates+=1
        self.transactionAmounts=[]
        self.nTransactions=0
        
    def addTransaction(self, transactionAmount):
        self.transactionAmounts.append(float(transactionAmount))
        self.nTransactions+=1

    def calcStats(self):
        self.transactionAmounts.sort() #for median
        self.total = sum(self.transactionAmounts)
        self.maxTransaction = max(self.transactionAmounts)
        self.minTransaction = min(self.transactionAmounts)
        self.meanTransaction = self.total / self.nTransactions
        self.medianTransaction = self.transactionAmounts[int(self.nTransactions//2)]

        # Calculate the variance
        self.transactionVariance = 0
        for value in self.transactionAmounts:
            self.transactionVariance += (value-self.meanTransaction)**2
        self.transactionVariance /= self.nTransactions
        
    def printStats(self):
        print "For candidate "+self.ID+":"
        print "Total contributions: %.2f" % self.total
        print "Minimum: %.2f" % self.minTransaction
        print "Maximum: %.2f" % self.maxTransaction
        print "Mean: %.2f" % self.meanTransaction
        print "Median: %.2f" % self.medianTransaction
        print "Standard Deviation: %.2f\n" % self.transactionVariance**0.5
        
    # This function prints the z-normalized transaction total to the terminal
    # mean and variance are of the transaction totals. These must be derived from the
    # set of all candidates    
    def printTotal_Znorm(self,mean,variance):
        self.zTotal=(self.total-mean)/(variance**0.5)
        print "For candidate "+self.ID+":"
        print "The z-score of the candidate's total contributions is %.3f\n" % self.zTotal
        
    # This function returns a list of data formatted for writing to a csv file
    # mean and variance are of the transaction totals. These must be derived from the
    # set of all candidates    
    def csvRow(self,mean,variance):
        self.zTotal=(self.total-mean)/(variance**0.5)
        return [self.ID,"%.2f"%self.total,"%.4f"%self.zTotal,"%.2f"%self.minTransaction,"%.2f"%self.maxTransaction,"%.2f"%self.medianTransaction,"%.2f"%self.meanTransaction,"%.2f"%(self.transactionVariance**0.5)]
        

# This is the code which does the work        
candidateDict={}
candidateList=[]
for row in csv.reader(fileinput.input(), delimiter='|'):

    tempID = row[candidateID_col]
    tempTransAmount = row[transactionAmount_col]
    
    if tempID not in candidateDict:
        candidateDict[tempID]=Candidate.nCandidates
        candidateList.append(Candidate(tempID))
        
    candidateList[candidateDict[tempID]].addTransaction(tempTransAmount)

print "There are a total of %d candidates.\n" %Candidate.nCandidates        
        
      
        
# This loops over all candidates and computes statistics for each, as well as the mean of the 
# total transactions for the candidates
mean=0
for i in range (0,Candidate.nCandidates):
    candidateList[i].calcStats()
    mean+=candidateList[i].total
    
mean/=Candidate.nCandidates
 
# Compute variance of the candidates' total contributions   
variance=0
for i in range (0,Candidate.nCandidates):
    variance+=(candidateList[i].total-mean)**2
variance/=Candidate.nCandidates

#These lines can be used to print info for one candidate to the terminal
candidateList[1].printStats()
candidateList[1].printTotal_Znorm(mean,variance)

# Write the statistics by candidate to a new csv file with | as delimiters
# Note that any old file with the same name is erased
with open('byCandidate.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter='|',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    #Write the column headers in the first row
    writer.writerow(Candidate.csvHeader)
   
    #Write data for each candidate
    for i in range (0,Candidate.nCandidates):  
        writer.writerow(candidateList[i].csvRow(mean,variance))
      