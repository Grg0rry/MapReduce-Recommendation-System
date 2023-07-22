#!/usr/bin/env python3

import sys

MovieRating = {}
MovieVector = {}
UserList = []
SearchList = []
num_recommendation = 10


for line in sys.stdin:
    
    line = line.strip().split('\t', 1)
    if line[0].startswith("$User_List"):
        UserList.append(line[1])
    elif line[0].startswith("$Search_Key"):
        SearchList.append(line[1])
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

    MovieVector[MovieTitle] = Vector
    # print('%s\t%s' % (MovieTitle, Vector))


for MovieTitle in SearchList:
    MovieSimilarity = []

    for Next_MovieTitle in MovieVector:
        if MovieTitle != Next_MovieTitle:
            Vector = MovieVector[MovieTitle]
            Next_Vector = MovieVector[Next_MovieTitle]
            
            dot_product = sum(x * y for x, y in zip(Vector, Next_Vector))
            magnitude = (sum(x ** 2 for x in Vector) ** 0.5) * (sum(x ** 2 for x in Next_Vector) ** 0.5)
            MovieSimilarity.append((Next_MovieTitle, dot_product/magnitude))

    MovieSimilarity.sort(key=lambda x: x[1], reverse=True)

    print(f'Top {num_recommendation} similar movies to {MovieTitle}')
    for movie, similarity in MovieSimilarity[:num_recommendation]:
        print('%s\t%s' % (movie, similarity))


