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
        UserRating.append((UserID, int(Rating)))
        MovieRating[MovieTitle] = UserRating

# compiles to a vector
UserIndexMap = {user: index for index, user in enumerate(UserList)}

for MovieTitle, UserRating in MovieRating.items():
    Vector = [0] * len(UserList)
    for UserID, Rating in UserRating:
        if UserID in UserList:
            Vector[UserIndexMap[UserID]] = Rating
    print('%s\t%s' % (MovieTitle, Vector))
