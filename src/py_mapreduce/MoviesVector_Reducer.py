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

        if MovieTitle in MovieRating:
            UserRating.append((int(UserID), int(Rating)))
        else:
            UserRating = [(int(UserID), int(Rating))]
        MovieRating[MovieTitle] = UserRating

        print('%s\t%s' % (MovieTitle, MovieRating[MovieTitle]))

# for MovieTitle, UserRating in MovieRating.items():  
#     UserRatingsByOrder = {Order_UserID: 0 for Order_UserID in UserList}

#     for UserID, Rating in UserRating:
#         if UserID in UserRatingsByOrder:
#             UserRatingsByOrder[UserID] = Rating
    
#     Vector = list(UserRatingsByOrder.values())
#     print('%s\t%s' % (MovieTitle, Vector))


# UserRating = MovieRating.get(MovieTitle, [])
# UserRating.append((int(UserID), int(Rating)))
# MovieRating[MovieTitle] = UserRating

