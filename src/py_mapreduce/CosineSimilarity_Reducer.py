#!/usr/bin/env python3

import sys
import math

Movie_Vector = {}
Magnitude = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = [int(item.strip()) for item in line[1].split(',')]
    Movie_Vector[MovieTitle] = Vector
    Magnitude[MovieTitle] = math.sqrt(sum(x ** 2 for x in Vector))

for MovieTitle, Vector in Movie_Vector.items():
    for Next_MovieTitle, Next_Vector in Movie_Vector.items():
        if MovieTitle != Next_MovieTitle:
            dot_product = sum(x * y for x, y in zip(Vector, Next_Vector))
            similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])

            print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))