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

# This class describes a candidate
class Candidate:
    'This class stores a candidates records and some statistical info about them'
    nCandidates=0
    
    def _init_(self, candidateID):
        self.ID=candidateID
        Candidate.nCandidates+=1
        self.transactionAmounts=[]
        self.nTransactions=0
        
    def addTransaction(self, transactionAmount):
        self.transactionAmounts.append(transactionAmount)
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
        print "Total contributions: %.2f" % self.total
        print "Minimum: %.2f" % self.minTransaction
        print "Maximum: %.2f" % self.maxTransaction
        print "Mean: %.2f" % self.meanTransaction
        print "Median: %.2f" % self.medianTransaction
        print "Standard Deviation: %.2f" % self.transactionVariance**0.5

# This is the code which does the work        
candidateDict={}
candidateList=[]
for row in csv.reader(fileinput.input(), delimiter='|'):

    tempID = row[candidateID_col]
    tempTransAmount = row[transactionAmount_col]
    
    if tempID not in candidateDict:
        candidateDict[tempID]=Candidate.nCandidates
        candidateList.append(Candidate(tempID))
    else:
        candidateList[candidateDict[tempID]].addTransaction(tempTransAmount)
        
