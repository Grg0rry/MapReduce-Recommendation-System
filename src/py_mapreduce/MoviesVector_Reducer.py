#!/usr/bin/env python3

import sys
from collections import defaultdict
import ast

MovieRating = defaultdict(list)
UserList = []

for line in sys.stdin:
    line = line.strip().split('\t', 1)
    
    if len(line) < 2:
        continue

    if line[0].startswith("$User_List"):
        UserList.append(line[1])
    else:
        MovieRating[line[0]] = [item for item in ast.literal_eval(line[1])]

# compiles to a vector
for MovieTitle, UserRating in MovieRating.items():
    Vector = [0] * len(UserList)
    for UserID, Rating in UserRating:
        if UserID in UserList:
            Vector[UserList.index(UserID)] = Rating
    print('%s\t%s' % (MovieTitle, Vector))
