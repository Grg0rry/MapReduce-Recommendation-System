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


for MovieTitle, UserRating in MovieRating.items():
    
    Vector = []
    found = False

    if len(UserRating) < 1000:
        continue

    for Order_UserID in UserList:
        for UserID, Rating in UserRating:
            if Order_UserID == UserID:
                Vector.append(Rating)
                found = True
                break

        if not found:
            Vector.append(0)

    print('%s\t%s' % (MovieTitle, Vector))


