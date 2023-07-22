#!/usr/bin/env python3

import sys

MovieRating = {}
UserList = []

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    if line[0].startswith("$User_List"):
        UserList.append(line[1])
    else:
        UserID, Rating = line[1].split(':')
        MovieTitle = line[0]
        UserRating = MovieRating.get(MovieTitle, [])
        MovieRating[MovieTitle].append((UserID, int(Rating)))

# compiles to a vector
for MovieTitle, UserRating in MovieRating.items():
    Vector = [0] * len(UserList)
    for UserID, Rating in UserRating:
        if UserID in UserList:
            Vector[UserList.index(UserID)] = Rating
    print('%s\t%s' % (MovieTitle, Vector))
