#!/usr/bin/env python3

from mrjob.job import MRJob

class UserList(MRJob):

    def mapper(self, _, line):
        line = line.strip().split(",", 2)

        if len(line) < 3:
            return
        
        UserID = int(line[1])
        
        yield(UserID, "")

    def reducer(self, key, values):
        UserID = int(key)

        yield("$User_List", UserID)

if __name__ == '__main__':
    UserList.run()
