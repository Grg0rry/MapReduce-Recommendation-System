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
    if len(UserRating) < 1000:
        continue
    
    UserRatingsByOrder = {Order_UserID: 0 for Order_UserID in UserList}

    for UserID, Rating in UserRating:
        if UserID in UserRatingsByOrder:
            UserRatingsByOrder[UserID] = Rating
    
    Vector = list(UserRatingsByOrder.values())
    print('%s\t%s' % (MovieTitle, Vector))


