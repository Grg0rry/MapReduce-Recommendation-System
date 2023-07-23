#!/usr/bin/env python3

import sys
from itertools import combinations
import numpy as np
from collections import defaultdict
import heapq

Movie_Vector = {}
Magnitude = {}
# Similarities = defaultdict(list)

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = [int(item.strip()) for item in line[1].strip('[]').split(',')]

    Movie_Vector[MovieTitle] = Vector
    Magnitude[MovieTitle] = np.linalg.norm(np.array(Vector))

for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
    dot_product = np.dot(np.array(Vector), np.array(Next_Vector))
    similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])

    print('%s\t%s' % ((MovieTitle, MovieTitle), similarity))

#     Similarities[MovieTitle].append((Next_MovieTitle, similarity))
#     Similarities[Next_MovieTitle].append((MovieTitle, similarity))

# for movie in Similarities:
#     top_similar_movies = heapq.nlargest(10, Similarities[movie], key=lambda x: x[1])
#     for similar_movie, similarity in top_similar_movies:
#         print('%s\t%s' % ((movie, similar_movie), similarity))