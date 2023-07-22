#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip().split(",", 2)

    if len(line) < 3:
        continue

    UserID = int(line[1])
    MovieTitle = line[0]
    Rating = int(line[2])
    
    print('%s\t%s' % (MovieTitle, f'{UserID}:{Rating}'))
