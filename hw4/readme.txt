The review with the most unique words in the entire data set is in German, with review_ID='IrPktNaTJMm3-OrJ0T0A5g'

I really wanted to find the review in English with the most unique words, so I did some crude language discrimination. The python script language_count.py is an mrjob which counts the number of reviews in English, German, Spanish, and French. Short reviews are hard to discriminate, and some others combine multiple languages. These are assigned to the language "Unknown". NOTE: this code won't run unless the paths to the language dictionary .txt files are correct. 

The English review with the most unique words has review ID 'RBRY-Pxk0iIramUbqFVMVw', and is a bunch of egg puns.

To find the user similarity, I restricted the search to those users who have at least two reviews. The Jaccard similarity of .5 when one user has only reviewed one business is not terribly interesting, since this gives all the other users who have reviewed the business but not more than one other business. It also saves a lot of time, since computing the pairwise similarity is of O(n^2) in the number of users. The output, saved in 'similar_users.txt', is a list of user ids pairs as keys and their Jaccard similarity as the value, e.g. 
 
 User ID                    User ID 2                   Jaccard Similarity
["6PFbHhq7aQQkTy40a2K36w", "rSV_rjo1uzgvKPsJxL_QaA"]	1.0