There are two codes here. I worked with Ana Rufino Ferreira so there may be many similarities in our codes.

stats.py < INPUT_PATH
This will give statistics calculated from all of the transactions. The statistics are also given in min-max normalized form.

candidateStats.py < INPUT_PATH
This creates a CSV files called "byCandidate.csv" listing all candidates and their statistics, including a z-normalized total contribution. The first row describes the columns. Data for a sample candidate is also printed. The transactions with no candidate ID are left out of the calculations.