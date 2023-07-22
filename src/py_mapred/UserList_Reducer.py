#!/usr/bin/env python3

import sys

last_UserID = ""

for line in sys.stdin:
    line = line.strip().split("\t", 1)
    
    UserID = int(line[0])

    if last_UserID != UserID:
        print('%s\t%s' % ("_$UserList", last_UserID))

    last_UserID = UserID