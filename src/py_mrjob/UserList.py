#!/usr/bin/env python3

from mrjob.job import MRJob

class UserList(MRJob):

    def mapper(self, _, line):
        line = line.strip().split(",", 2)

        # check if it contains at least 3 elements
        if len(line) < 3:
            return
        
        UserID = int(line[1])
        yield(UserID, "")

    def reducer(self, key, values):
        yield(str("$User_List"), int(key))

if __name__ == '__main__':
    UserList.run()
