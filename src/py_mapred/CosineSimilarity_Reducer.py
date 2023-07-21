#!/usr/bin/python3

import sys
import ast

last_Tuple = None

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    vectors = [int(item) for item in ast.literal_eval(line[1])]

    if last_Tuple != None:
        last_Movie, last_Vector = last_Tuple

        dot_product = sum(x * y for x, y in zip(vectors, last_Vector))
        magnitude = (sum(x ** 2 for x in vectors) ** 0.5) * (sum(x ** 2 for x in last_Vector) ** 0.5)

        print('%s\t%s' % ((MovieTitle, last_Movie), dot_product/magnitude))

    last_Tuple = (MovieTitle, vectors)