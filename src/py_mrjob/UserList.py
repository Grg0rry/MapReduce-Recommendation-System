#!/usr/bin/python
# -*-coding:utf-8 -*

from mrjob.job import MRJob

class UserList(MRJob):

    def mapper(self, _, line):
        MovieRating = line.split(",", 5)

        UserID = int(MovieRating[0])
        yield("", UserID)


    def reducer(self, _, UserID):
        UserList = []
        last_UserID = ""

        if UserID != last_UserID:
            UserList.append(UserID)
        last_UserID = UserID
        
        yield(None, UserList)


if __name__ == '__main__':
    UserList.run()