#!/usr/bin/env python3

import sys
from itertools import combinations
import numpy as np

# Movie_Vector = {}
# Magnitude = {}

# for line in sys.stdin:
#     line = line.strip().split('\t', 1)

#     MovieTitle = line[0]
#     Vector = [int(item.strip()) for item in line[1].strip('[]').split(',')]
    
#     Vector = np.array([int(item.strip()) for item in line[1].strip('[]').split(',')])
#     Magnitude[MovieTitle] = np.linalg.norm(Vector)
#     Movie_Vector[MovieTitle] = Vector


# for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
#     dot_product = np.dot(Vector, Next_Vector)
#     similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])
#     print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))
#     print('%s\t%s' % ((Next_MovieTitle, MovieTitle), similarity))


movie_vector_map = {}
magnitude_map = {}
combinations_set = set()

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = np.array([int(item.strip()) for item in line[1].strip('[]').split(',')])
    magnitude_map[MovieTitle] = np.linalg.norm(Vector)
    movie_vector_map[MovieTitle] = Vector


similarity_map = {}
for movie_title1, vector1 in movie_vector_map.items():
    for movie_title2, vector2 in movie_vector_map.items():
        if movie_title1 != movie_title2 and (movie_title1 + "," + movie_title2) not in combinations_set:
            dot_product = np.dot(vector1, vector2)
            
            similarity = dot_product / (magnitude_map[movie_title1] * magnitude_map[movie_title2])
            print('%s\t%s' % ((movie_title1, movie_title2), similarity))
            
            combinations_set.add(movie_title1 + "," + movie_title2)
            combinations_set.add(movie_title2 + "," + movie_title1)