#!/bin/python3
import random
import sys

if len(sys.argv) != 2:
    print("Usage: ./points.py {seed}")
    sys.exit(1)

#seed the generator with our input
random.seed(int(sys.argv[1]))

# Generate 2D points in range [1.0; 100.0]
with open("data" + sys.argv[1] + ".txt", "w") as f:
    for i in range(0, 50):
        x = random.uniform(1.0, 100.0)
        y = random.uniform(1.0, 100.0)

        f.write(str("%.2f" % x) + ',' + str("%.2f" % y) + "\n")
