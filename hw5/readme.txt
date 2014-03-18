The python code 'gini.py' takes the names dataset and outputs the Gini index for the two candidates, as well as the weighted Gini index after partitioning by zip code. 
-Records with no zip code are discarded. 
-When zip+4 is given, the last four digits are ignored so partitioning is strictly by 5 digit zip code.

Gini Index: 0.487709185938
Gini Index after split: 0.413638827259

--------------------------------------------------------------------------
Extra Credit

'continuous_gini.py' finds the two split points which minimize the weighted Gini index of first partitioning the transaction_amts into three categories:

1: transaction_amt <= split1
2: split1 < transaction_amt <= split2
3: split2 < transaction_amt 

The optimal splits are
[split1, split2, split_gini] = [42.0, 731.0, 0.4774443523689614]

I did this more or less by brute force, I'm sure there are more elegant search solutions. It takes a while.

