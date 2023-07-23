#!/usr/bin/env python3

import sys
from itertools import combinations
import numpy as np
from collections import defaultdict
import heapq

Movie_Vector = {}
Magnitude = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = np.array([int(item.strip()) for item in line[1].strip('[]').split(',')])

    Movie_Vector[MovieTitle] = Vector
    Magnitude[MovieTitle] = np.linalg.norm(Vector)

movie_vectors = np.array(list(Movie_Vector.values()))
magnitudes = np.linalg.norm(movie_vectors, axis=1)
dot_products = np.dot(movie_vectors, movie_vectors.T)
similarities = dot_products / np.outer(magnitudes, magnitudes)

for i, (MovieTitle, Next_MovieTitle) in enumerate(list(combinations(Movie_Vector.keys(), 2))):
    similarity = similarities[i]
    print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))


# Similarities = {}

# for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
#     dot_product = np.dot(Vector, Next_Vector)
#     similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])   

#     if MovieTitle in Similarities:
#         Similarities[MovieTitle].append((Next_MovieTitle, similarity))
#     else:
#         Similarities[MovieTitle] = [(Next_MovieTitle, similarity)]

# for movie in Similarities:
#     top_movies = heapq.nlargest(10, Similarities[movie], key=lambda x: x[1])
#     for similar_movie, similarity in top_movies:
#         print('%s\t%s' % (movie, (similar_movie, similarity)))
