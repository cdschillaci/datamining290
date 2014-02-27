#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
import collections as coll
import numpy as np

jump=15


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

transactions=[] # Pairs [transaction_amt, candidate_name]
trans_amts=[] # List of transaction amounts


############### Read through files
for row in csv.reader(fileinput.input('itpas2.txt'), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    
    transactions.append([float(row[TRANSACTION_AMT]),candidate_name])
    trans_amts.append(float(row[TRANSACTION_AMT]))
  
#Total number of transactions
total=float(len(trans_amts))

# Sort and unique trans_amts
trans_amts=list(set(trans_amts))
trans_amts.sort()

best_split=[trans_amts[0]-1,trans_amts[0]-1,1]

# Search over the possible transaction amounts, in intervals of jump values
for split1 in trans_amts[::jump]:
    print "Currently working on split1= "+str(split1)
    for split2 in trans_amts[::jump]:
        if split2<=split1:
            continue
        # 
        dict_set=[coll.defaultdict(int),coll.defaultdict(int),coll.defaultdict(int)]
        for transaction in transactions:
            if transaction[0]<=split1:
                dict_set[0][transaction[1]]+=1
            elif transaction[0]<=split2:
                dict_set[1][transaction[1]]+=1
            else:
                dict_set[2][transaction[1]]+=1
                
        split_gini=sum( (1-sum((temp[cand]/float(sum(temp.values())))**2 for cand in temp))*sum(temp.values())/total for temp in dict_set)  # weighted average of the Gini Indexes using candidate names, split up by zip code
        if split_gini<best_split[2]:
            best_split=[split1,split2,split_gini]
            print best_split
            
            
# Now search over all values near the coarse-grained best
split1Index=trans_amts.index(best_split[0])      
split2Index=trans_amts.index(best_split[0])            
            
for split1 in trans_amts[split1Index-jump:split1Index+jump]:
    print "Currently working on split1= "+str(split1)
    for split2 in trans_amts:
        if split2<=split1:
            continue
        dict_set=[coll.defaultdict(int),coll.defaultdict(int),coll.defaultdict(int)]
        for transaction in transactions:
            if transaction[0]<=split1:
                dict_set[0][transaction[1]]+=1
            elif transaction[0]<=split2:
                dict_set[1][transaction[1]]+=1
            else:
                dict_set[2][transaction[1]]+=1
                
        split_gini=sum( (1-sum((temp[cand]/float(sum(temp.values())))**2 for cand in temp))*sum(temp.values())/total for temp in dict_set)  # weighted average of the Gini Indexes using candidate names, split up by zip code
        if split_gini<best_split[2]:
            best_split=[split1,split2,split_gini]
            print best_split
            
print best_split
