#!/usr/bin/python3

import sys, math

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    vectors = []

    for v in line[1][1:-1].split(','):
        vectors.append(int(v))

    length = math.sqrt(sum(v**2 for v in vectors))
    normalized_vector = [v / length for v in vectors]

    print('%s\t%s' % (MovieTitle, normalized_vector))
