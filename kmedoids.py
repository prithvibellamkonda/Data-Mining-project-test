#!/bin/python3
import argparse
import sys
import random
import math
import matplotlib.pyplot as plt

def read_data(filename):
    points = []
    with open(filename, "r") as f:
        for line in f:
            x,y = line.split(',')
            points.append([float(x), float(y)])
    return points

def print_points(points):
    for p in points:
        print("x=%.2f, y=%.2f" % (p[0], p[1]))

def print_medoids(medoids):
    print("Medoids:", end=" ")
    for medo in medoids:
        print("[%.2f, %.2f]" % (medo[0], medo[1]), end="")
    print("")

#Find Euclidean distance between two points
def distance(p, q):
    #(y1 - x1)^2 + (y2 - x2)^2
    d = math.pow(abs(q[0]-p[0]), 2) + math.pow(abs(q[1]-p[1]), 2);
    return math.sqrt(d)

#Calculate average intra-cluster distance
# We sum distance from centroid to each point, and divide vy number of points
def distance_intra(idx, cluster_idx, centr, points):
    d = 0.0
    dn = 0
    n = len(points)
    for i in range(n):
        if cluster_idx[i] == idx:
            d += distance(centr, points[i])
            dn += 1
    return d / dn

#Calculate average intra-square cluster distance
# We sum squared distance from centroid to each point, and divide by number of points
def distance_intra_sq(idx, cluster_idx, centr, points):
    sqd = 0.0
    dn = 0
    n = len(points)
    for i in range(n):
        if cluster_idx[i] == idx:
            d = distance(centr, points[i])
            sqd += math.pow(d, 2)
            dn += 1
    return sqd / dn

#Classify each point into a cluster
def classify(k, means, p):
    index = 0
    dmin = distance(p, means[0])

    #for aech cluster
    for i in range(1, k):
        #find distance between point and mean
        d = distance(p, means[i])
        if d < dmin:
            dmin = d
            index = i

    return index

# Calculate the cluster medoid
def cluster_medoid(idx, cluster_idx, points, medo):
    #medoid point
    medoid = medo
    #sum to squared distance to all other points
    medoid_sqd = distance_intra_sq(idx, cluster_idx, medo, points)

    #for each point
    for i in range(len(points)):
        #calculate squared distance to all other points
        sqd = distance_intra_sq(idx, cluster_idx, points[i], points)
        if sqd < medoid_sqd:
            medoid = points[i]
            medoid_sqd = sqd

    return medoid

def show_stats_header(k):
    print("%s" % "Iteration#", end="")
    for i in range(k):
        print("%25s\t" % ("Cluster#"+str(i)), end="")
    print("%25s\t" % "TSSE", end="")
    print("%25s\t" % "TSE", end="")
    print("")

    print("%10s" % " ", end="")
    for i in range(k):
        print("%14s %s\t" % ("intra-sq-dist", "intra-dist"), end="")
    print("")

def show_stats(iter, cluster_idx, means, points):
    print("%10s" % str(iter), end="")
    td = 0.0
    tsqd = 0.0
    for i in range(len(means)):
        d   = distance_intra(i, cluster_idx, means[i], points)
        sqd = distance_intra_sq(i, cluster_idx, means[i], points)
        print("%14s %10s\t" % (str("%.2f" % sqd), str("%.2f" % d)), end="")
        td += d
        tsqd += sqd
    print("%25s\t" % (str("%.2f" % td)), end="")
    print("%25s\t" % (str("%.2f" % tsqd)), end="")
    print("")

def plot_iter(iter, means, points, cluster_idx):
    color = ['red', 'green', 'blue', 'yellow', 'purple', 'pink', 'black', 'grey', 'brown', 'orange']
    marker  = ['x', 's', 'v', '^', '<', '>', '+', '-', '*', '.']

    plt.axis([1, 100, 1, 100])

    for i in range(len(means)):
        xs = []
        ys = []
        for j in range(len(points)):
            if cluster_idx[j] == i:
                xs.append(points[j][0])
                ys.append(points[j][1])

        plt.plot([means[i][0]], [means[i][1]], 'o', color=color[i])
        plt.plot(xs, ys, marker[i], color=color[i])

    #plt.show()
    plt.savefig("plot"+str(iter)+".png")
    plt.clf()

def rand_medoids(k, points):
    #generate k unique indexes for points[]
    indices = []
    while len(indices) != k:
        idx = random.randint(1, len(points))
        if idx not in indices:
            indices.append(idx)


    medoids = [ points[indices[i]] for i in range(k) ]
    return medoids

def kmedoids(k, points, iters):


    #create medoid for each cluster
    medoids = rand_medoids(k, points)
    print_medoids(medoids)

    #print table headings
    show_stats_header(k)

    #shows to which cluster the point belongs
    cluster_idx  = [0 for i in range(len(points))]

    for iter in range(1, iters + 1):

        #shows if points moved between clusters
        no_change = True

        for i in range(len(points)):
            idx = classify(k, medoids, points[i])

            #if point was classified in another cluster
            if idx != cluster_idx[i]:
                no_change = False

                #point belongs to cluster[index]
                cluster_idx[i] = idx

        #if no points moved between clusters
        if no_change:
            break

        #plot before updating means[]
        plot_iter(iter, medoids, points, cluster_idx)

        #The centroid of each of the k clusters becomes the new mean
        for idx in range(k):
            medoids[idx] = cluster_medoid(idx, cluster_idx, points, medoids[idx])
        #print_medoids(medoids)

        #show iteration statistics
        show_stats(iter, cluster_idx, medoids, points)

random.seed(1234567)

#parse the program options
parser = argparse.ArgumentParser()
#parser.add_argument("-k", type=int, help="k parameter", default=2)
parser.add_argument("datafile", help="Data file with points")
args = parser.parse_args()

#load data
points = read_data(args.datafile)
#print_points(points)

kmedoids(4, points, 100)
