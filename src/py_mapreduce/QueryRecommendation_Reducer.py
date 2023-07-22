#!/usr/bin/env python3

import sys
from collections import defaultdict
import ast

MovieRating = defaultdict(list)


    print('%s\t%s' % ("$Search_Movie", line[0].lower()))
    print('%s\t%s' % ((MovieTitle, Next_MovieTitle), dot_product/magnitude))

MovieSearch = []
MovieSimilarity = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    if line[0].startswith("$Search_Movie"):
        MovieSearch.append(line[1])
    else:
        MovieTitle_1, MovieTitle_2 = ast.literal_eval(line[0])
        MovieSimilarity[MovieTitle_1] = (MovieTitle_2, float(line[1]))

for Search in MovieSearch:
    MovieSimilarity[Search]


# compiles to a vector
for MovieTitle, UserRating in MovieRating.items():
    Vector = [0] * len(UserList)
    for UserID, Rating in UserRating:
        if UserID in UserList:
            Vector[UserList.index(UserID)] = Rating
    print('%s\t%s' % (MovieTitle, Vector))
