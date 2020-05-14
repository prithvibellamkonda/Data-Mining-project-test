1. Data
To generate 10 different input data files do
  $ for i in $(seq 0, 10); do python ./points.py $RANDOM; done

2. Plots
Program generates plots for each iteration.
Ceontroids of each cluster are represened with a circle.
Each cluster has its own corlor.

3. Execution
  $ python ./kmeans.py -k4 data4931.txt
Means: [25.00, 25.00] [50.00, 50.00] [75.00, 75.00] [100.00, 100.00]
Iteration#                Cluster#0                     Cluster#1                       Cluster#2                       Cluster#3                            TSSE                             TSE
           intra-sq-dist intra-dist      intra-sq-dist intra-dist        intra-sq-dist intra-dist        intra-sq-dist intra-dist
         1        411.26      18.63            1420.89      33.51               451.50      18.61                 5.14       2.27                           73.02                         2288.79
         2        450.28      19.29             512.92      20.09               561.48      20.77                94.24       8.98                           69.13                         1618.92
         3        354.67      17.68             365.53      17.84               466.69      20.78               308.25      16.46                           72.76                         1495.15
