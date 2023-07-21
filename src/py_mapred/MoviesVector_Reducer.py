#!/usr/bin/python3

from operator import itemgetter
import sys

temp_UserList = []
MovieRating = {}

# process both mappers
for line in sys.stdin:
    line = line.strip().split('\t', 1)

    if line[0].startswith("_$UserList"):
        temp_UserList.append(line[1])
    else:
        UserID, Rating = line[1].split(':')
        MovieTitle, UserRating = MovieRating.get(MovieTitle, ([],))
        MovieRating[MovieTitle].append((UserID, Rating))

# compiles to a vector
UserList = list(sorted(set(temp_UserList)))
for MovieTitle, UserRating in MovieRating.items():
    Vector = []
    
    for Search_UserID in UserList:
        found_match = False

        for UserID, Rating in UserRating:
            if UserID == Search_UserID:
                Vector.append(Rating)           
                found_match = True
                break
        
        if not found_match:
            Vector.append(0)
    
    print('%s\t%s' % (MovieTitle, Vector))
