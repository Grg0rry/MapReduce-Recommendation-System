#!/usr/bin/env python3

import sys

MovieRating = {}
UserList = []

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    if line[0].startswith("$User_List"):
        UserList.append(int(line[1]))
    else:
        UserID, Rating = line[1].split(':')
        MovieTitle = line[0]

        if MovieTitle in MovieRating:
            MovieRating[MovieTitle].append((int(UserID), int(Rating)))
        else:
            MovieRating[MovieTitle] = [(int(UserID), int(Rating))]


for MovieTitle, UserRating in MovieRating.items():
    UserRatingsByOrder = {UserID: 0 for UserID in UserList}

    for UserID, Rating in UserRating:
        UserRatingsByOrder[UserID] = Rating
    
    Vector = list(UserRatingsByOrder.values())
    print('%s\t%s' % (MovieTitle, Vector))


# UserRating = MovieRating.get(MovieTitle, [])
# UserRating.append((int(UserID), int(Rating)))
# MovieRating[MovieTitle] = UserRating

