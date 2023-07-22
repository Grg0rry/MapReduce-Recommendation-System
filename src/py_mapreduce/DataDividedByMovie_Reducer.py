#!/usr/bin/env python3

import sys

MovieRating = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    UserID, Rating = line[1].split(':')
    MovieTitle = line[0]
    UserRating = MovieRating.get(MovieTitle, [])
    MovieRating[MovieTitle].append((UserID, int(Rating)))

for MovieTitle, UserRating in MovieRating.items():
    print('%s\t%s' % (MovieTitle, UserRating))
