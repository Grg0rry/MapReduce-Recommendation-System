#!/usr/bin/env python3

import sys
import ast

Movie_Vector = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    vectors = [int(item) for item in ast.literal_eval(line[1])]

    Movie_Vector[MovieTitle] = vectors


for MovieTitle, Vector in Movie_Vector.items():
    for Next_MovieTitle, Next_Vector in Movie_Vector.items():
        dot_product = sum(x * y for x, y in zip(Vector, Next_Vector))
        magnitude = (sum(x ** 2 for x in Vector) ** 0.5) * (sum(x ** 2 for x in Next_Vector) ** 0.5)
        print('%s\t%s' % ((MovieTitle, Next_MovieTitle), dot_product/magnitude))