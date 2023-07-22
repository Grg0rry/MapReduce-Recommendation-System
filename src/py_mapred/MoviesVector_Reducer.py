#!/usr/bin/env python3

import sys
from collections import defaultdict

temp_UserList = []
MovieRating = defaultdict(list)

# process both mappers
for line in sys.stdin:
    line = line.strip().split('\t', 1)
    
    if len(line) < 2:
        continue

    if line[0].startswith("$User_List"):
        temp_UserList.append(line[1])
    else:
        UserID, Rating = line[1].split(':')
        MovieTitle = line[0]
        # UserRating = MovieRating.get(MovieTitle, [])
        # UserRating.append((UserID, Rating))
        MovieRating[MovieTitle].append((UserID, Rating))

# compiles to a vector
UserList = list(sorted(set(temp_UserList)))
for MovieTitle, UserRating in MovieRating.items():
    Vector = [0] * len(UserList)
    for UserID, Rating in UserRating:
        if UserID in UserList:
            Vector[UserList.index(UserID)] = Rating
    print('%s\t%s' % (MovieTitle, Vector))
