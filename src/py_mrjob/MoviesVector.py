#!/usr/bin/env python3

from mrjob.job import MRJob

class MovieVector(MRJob):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserList = []

    def mapper(self, _, line):
        line = line.strip().split('\t', 1)

        if line[0].startswith("$User_List"):
            self.UserList.append(line[1])
        else:
            yield (line[0], line[1])

    def reducer(self, key, values):

        MovieTitle = key
        UserRating = list((value.strip("[]").split(':') for value in values))

        if len(UserRating) < 1000:
            return
        
        UserRatingsByOrder = {Order_UserID: 0 for Order_UserID in self.UserList}

        for UserID, Rating in UserRating:
            if UserID in UserRatingsByOrder:
                UserRatingsByOrder[UserID] = int(Rating)

        Vector = list(UserRatingsByOrder.values())
        yield (MovieTitle, Vector)

if __name__ == '__main__':
    MovieVector.run()
