#!/usr/bin/env python3

import sys
import tqdm

for line in tqdm.tqdm(sys.stdin):
    line = line.strip().split(",", 5)

    UserID = int(line[0])
    MovieTitle = line[5]
    Rating = int(line[1])
    
    print('%s\t%s' % (MovieTitle, f'{UserID}:{Rating}'))
