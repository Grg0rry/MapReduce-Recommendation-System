#!/usr/bin/env python3

import sys, math
import ast

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    vectors = [int(item) for item in ast.literal_eval(line[1])]

    length = math.sqrt(sum(v**2 for v in vectors))
    normalized_vector = [v / length for v in vectors]

    print('%s\t%s' % (MovieTitle, normalized_vector))
