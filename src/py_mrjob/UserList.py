#!/usr/bin/env python3

from mrjob.job import MRJob

class UserList(MRJob):

    def mapper(self, _, line):
        MovieRating = line.split("\t", 5)
        # MovieRating = line.split(",", 5)

        UserID = int(MovieRating[0])
        yield(1, UserID)


    def reducer(self, key, UserID):        
        yield(None, list(set(UserID)))


if __name__ == '__main__':
    UserList.run()