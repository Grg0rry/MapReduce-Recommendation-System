#!/usr/bin/env python3

import sys
import tqdm

for line in tqdm.tqdm(sys.stdin):
    line = line.strip().split("\t", 5)

    UserID = int(line[0])

    print('%s\t%s' % ("_$UserList", UserID))