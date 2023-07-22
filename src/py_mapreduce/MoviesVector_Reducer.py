#!/usr/bin/env python3

import sys

MovieRating = {}
MovieVector = {}
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


UserIndexMap = {user: index for index, user in enumerate(UserList)}

for MovieTitle, UserRating in MovieRating.items():
    Vector = [0] * len(UserList)
    for UserID, Rating in UserRating:
        if UserID in UserList:
            Vector[UserIndexMap[UserID]] = Rating
    MovieVector[MovieTitle] = Vector
    # print('%s\t%s' % (MovieTitle, Vector))


movie_pairs = [(MovieTitle, Next_MovieTitle) for MovieTitle in MovieVector for Next_MovieTitle in MovieVector if MovieTitle != Next_MovieTitle]

for MovieTitle, Next_MovieTitle in movie_pairs:
    Vector = MovieVector[MovieTitle]
    Next_Vector = MovieVector[Next_MovieTitle]

    dot_product = sum(x * y for x, y in zip(Vector, Next_Vector))
    magnitude = (sum(x ** 2 for x in Vector) ** 0.5) * (sum(x ** 2 for x in Next_Vector) ** 0.5)
    
    print('%s\t%s' % ((MovieTitle, Next_MovieTitle), dot_product/magnitude))
