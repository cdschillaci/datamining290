#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
import collections as coll
import numpy as np


(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

list_thing=[]
list_thing2=[]


############### Read through files
for row in csv.reader(fileinput.input('itpas2.txt'), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    
    list_thing.append([float(row[TRANSACTION_AMT]),candidate_name])
    list_thing2.append(float(row[TRANSACTION_AMT]))
  
temp=list_thing2
#list_thing.sort()
total=float(len(list_thing2))

list_thing2=list(set(list_thing2))
list_thing2.sort()

best_split=[list_thing2[0]-1,1]


for split in [np.median(temp)]:# list_thing2:
    dict_pair=[coll.defaultdict(int),coll.defaultdict(int)]
    for transaction in list_thing:
        if transaction[0]<=split:
            dict_pair[0][transaction[1]]+=1
        else:
            dict_pair[1][transaction[1]]+=1
            
    split_gini=sum( (1-sum((temp[cand]/float(sum(temp.values())))**2 for cand in temp))*sum(temp.values())/total for temp in dict_pair)  # weighted average of the Gini Indexes using candidate names, split up by zip code
    if split_gini<best_split[1]:
        best_split=[split,split_gini]
        print best_split
        
print best_split
