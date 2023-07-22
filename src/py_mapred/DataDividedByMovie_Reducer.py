#!/usr/bin/env python3

import sys
from collections import defaultdict

MovieRating = defaultdict(list)

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    UserID, Rating = line[1].split(':')
    MovieTitle = line[0]
    MovieRating[MovieTitle].append((UserID, Rating))

for MovieTitle, UserRating in MovieRating.items():
    if len(UserRating) > 100:
        print('%s\t%s' % (MovieTitle, UserRating))
