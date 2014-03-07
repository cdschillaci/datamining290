###
# Implement simple k-means clustering using 1 dimensional data
#
##/

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

dataset = [
    -13.65089255716321, -0.5409562932238607, -88.4726466247223,
    39.30158828358612, 4.066458182574449, 64.64143300482378,
    38.68269424751338, 33.42013676314311, 31.18603331719732,
    -0.2027616409406292, 45.13590038987272, 30.791899783552395,
    61.1727490302448, 18.167220741624856, 88.88077709786394,
    -1.3808002119514704, 50.14991362212521, 55.92029956281276,
    -6.759813255299466, 34.28290084421072
]

k = 2  # number of clusters
n_iterations=50 # Use the minimum error clustering from this number of initial seeds
min_error=0.01 # This is the stopping criterion for the k means search, stop when no 
                # mean changes by more than ths value


def pick_centroids(xs, num):
    """Return list of num centroids given a list of numbers in xs"""
    # Centroids are initialized randomly by shuffling then returning the first num datapoints 
    return np.random.choice(xs,num)



def distance(a, b):
    """Return the Euclidean distance of numbers a and b"""
    return np.abs(a-b)


def centroid(xs):
    """Return the centroid number given a list of numbers, xs"""
    return np.mean(xs)


def cluster(xs, centroids):
    """Return a list of clusters centered around the given centroids.  Clusters
    are lists of numbers."""

    clusters = [[] for c in centroids]

    for x in xs:
        # find the closest cluster to x
        dist, cluster_id = min(
            (distance(x, c), cluster_id) for cluster_id, c in enumerate(centroids)
        )
        # place x in cluster
        clusters[cluster_id].append(x)

    return clusters


def iterate_centroids(xs, centroids):
    """Return stable centroids given a dataset and initial centroids"""

    err = min_error  # minimum amount of allowed centroid movement
    observed_error = 1  # Initialize: maxiumum amount of centroid movement
    new_clusters = [[] for c in centroids]  # Initialize: clusters

    while observed_error > err:
        new_clusters = cluster(xs, centroids)
        new_centroids = map(centroid, new_clusters)

        observed_error = max(abs(new - old) for new, old in zip(new_centroids, centroids))
        centroids = new_centroids

    
    return (centroids, new_clusters, error)

def error_centroids(xs, centroids, clusters):
    """ Return the within-cluster variation error"""
    error=0
    for centroid, cluster in zip(centroids,clusters):
        for point in cluster:
            error+=distance(point, centroid)**2
            
    return error
###
# Main part of program:
# Pick initial centroids
# Iterative to find final centroids
# Iterate this over n_iterations initial seeds to find best
# Print results
# Plot clusters
##/

error=0 #This will be overwritten on he first loop
for it in range(n_iterations):
    initial_centroids = pick_centroids(dataset, k)
    
    new_final_centroids, new_final_clusters, new_error = iterate_centroids(dataset, initial_centroids)
    
    if it==0 or new_error<error:
        final_centroids=new_final_centroids
        final_clusters=new_final_clusters
        error=new_error
    

for centroid, cluster in zip(final_centroids, final_clusters):
    print "Centroid: %s" % centroid
    print "Cluster contents: %r" % cluster

# Initialize figure and plot
fig,ax=plt.subplots()

colors=cm.rainbow(np.linspace(0, 1, k))

# This will be used ot make the legend, false black scatter points
ax.scatter(np.zeros([1,1]),np.zeros([1,1]),s=.001,color='k',label='Data')
ax.scatter(np.zeros([1,1]),np.zeros([1,1]),s=.0075,color='k',marker='x',label='Centroid')

for cluster,centroid,c in zip(final_clusters,final_centroids,colors):
    ax.scatter(cluster,np.zeros_like(cluster),color=c,label='Data')
    ax.scatter(centroid,0,color=c,marker='x',s=150,label='Centroid')
    
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[0:2], labels[0:2],scatterpoints=1,markerscale=130)


ax.set_title("Plot of best k-means clustering with k="+str(k)+"\n from "+str(n_iterations)+" random starting centroids")
ax.get_yaxis().set_visible(False)

fig.savefig('kmeans_plot_k'+str(k)+'_n'+str(n_iterations)+'.eps',format='eps')
plt.close(fig)