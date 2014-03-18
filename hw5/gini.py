#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
import collections as coll


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

# For calculating the Gini index over the two Candidates
candidate_count=coll.defaultdict(int)

# We will store a defaultdict(int) of candidates for each zip-code
zip_dicts={}

############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    
    candidate_count[candidate_id]+=1    
    
    # Get only the first 5 digits of zip code
    zip_code = row[ZIP_CODE][0:5]
    
    # Discard if blank
    if len(zip_code)==0:
        continue
        
    # If the zip_code has not been seen yet, add a new dict
    if zip_code not in zip_dicts:
        zip_dicts[zip_code]=coll.defaultdict(int)
        
    # Increment the candidate's dictionary entry in the correct zip code
    zip_dicts[zip_code][candidate_id]+=1
    

candidate_counter=coll.Counter()
candidate_counter.update(candidate_count)

# Total number of records
total=float(sum(candidate_counter.values()))

gini = 1-sum((float(candidate_counter[cand])/total)**2 for cand in candidate_counter)  # current Gini Index using candidate name as the class

# Total number of records with a non-blank zip code
total=float(0)
for code in zip_dicts:
    total+=sum(zip_dicts[code].values())

# Use an unreadabe nested for/sum statement to calculate split gini
split_gini = sum( (1-sum((zip_dicts[code][cand]/float(sum(zip_dicts[code].values())))**2 for cand in zip_dicts[code]))*sum(zip_dicts[code].values())/total for code in zip_dicts)  # weighted average of the Gini Indexes using candidate names, split up by zip code


print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
