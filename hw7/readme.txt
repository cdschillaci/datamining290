As currently set up, k_means.py tries to find the global best k clustering by 

1. Randomly choosing k different data points as initial centroids
2. Iteratively searching using the k-means algorithm for the best centroids, stopping when no centroid moves by more than min_error.
3. Repeat 1 and 2 using different initial centroids n_iterations times
4. Select the centroids which minimize the within-cluster error

It prints the centroids and the cluster contents for each cluster, and plots the resulting clustering as an eps figure.

The code as submitted uses
  k=2
  n_iterations=50
  min_error=0.01

I am using the Euclidean (l2) distance. 