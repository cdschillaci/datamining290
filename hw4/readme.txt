The review with the most unique words in the entire data set is in German, with review_ID='IrPktNaTJMm3-OrJ0T0A5g'

I really wanted to find the review in English with the most unique words, so I did some crude language discrimination. The python script language_count.py is an mrjob which counts the number of reviews in English, German, Spanish, and French. Short reviews are hard to discriminate, and some others combine multiple languages. These are assigned to the language "Unknown"

The English review with the most unique words has review ID 'RBRY-Pxk0iIramUbqFVMVw', and is a bunch of egg puns.

