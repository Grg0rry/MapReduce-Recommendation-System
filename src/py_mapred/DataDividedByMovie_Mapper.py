#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip().split(",")

    UserID = int(line[0])
    MovieTitle = line[5]
    Rating = int(line[1])
    
    print('%s\t%s' % (MovieTitle, f'{UserID}:{Rating}'))
