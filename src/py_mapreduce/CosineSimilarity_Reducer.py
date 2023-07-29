#!/usr/bin/env python3

import sys
# from itertools import combinations
# import numpy as np

Movie_Vector = {}
Magnitude = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = [int(item.strip()) for item in line[1].strip('[]').split(',')]
    # Vector = np.array([int(item.strip()) for item in line[1].strip('[]').split(',')])
    # Magnitude[MovieTitle] = np.linalg.norm(Vector)

    Movie_Vector[MovieTitle] = Vector
    Magnitude[MovieTitle] = sum(val * val for val in Vector)
    
    print('%s\t%s' % (MovieTitle, Magnitude[MovieTitle]))


# for i, (MovieTitle_1, Vector_1) in enumerate(Movie_Vector.items()):
#     for MovieTitle_2, Vector_2 in list(Movie_Vector.items())[i + 1:]:
#         dot_product = sum(v1 * v2 for v1, v2 in zip(Vector_1, Vector_2))
#         similarity = dot_product / (Magnitude[MovieTitle_1] * Magnitude[MovieTitle_2])
#         print('%s\t%s' % ((MovieTitle_1, MovieTitle_2), similarity))


# for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
#     dot_product = np.dot(Vector, Next_Vector)
#     similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])
#     print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))
