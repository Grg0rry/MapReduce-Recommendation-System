#!/usr/bin/env python3

import sys

temp_UserList = []
MovieRating = {}

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
        UserRating = MovieRating.get(MovieTitle, [])
        UserRating.append((UserID, Rating))
        MovieRating[MovieTitle] = UserRating

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
