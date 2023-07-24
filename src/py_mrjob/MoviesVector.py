#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class MovieVector(MRJob):
    
    def configure_args(self):
        super(MovieVector, self).configure_args()
        self.add_file_arg('--file1')

    def mapper_init(self):
        self.UserList = []
        self.MovieRating = {}

        with open(self.options.file1, 'r') as file1:
            for line in file1:
                line = line.strip().split('\t',1)
                self.UserList.append(line[1])

    def mapper(self, _, line):
        line = line.strip().split('\t', 1)
        
        UserID, Rating = line[1].split(':')
        MovieTitle = line[0]
        UserRating = self.MovieRating.get(MovieTitle, [])
        UserRating.append((int(UserID), int(Rating)))
        self.MovieRating[MovieTitle] = UserRating

        yield (MovieTitle, "")


    def reducer(self, MovieTitle, _):        
        UserRating = self.MovieRating[MovieTitle]

        if len(UserRating) < 1000:
            return
        
        UserRatingsByOrder = {Order_UserID: 0 for Order_UserID in self.UserList}

        for UserID, Rating in UserRating:
            if UserID in UserRatingsByOrder:
                UserRatingsByOrder[UserID] = int(Rating)

        Vector = list(UserRatingsByOrder.values())
        yield (MovieTitle, Vector)

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init, 
                   mapper=self.mapper,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':
    MovieVector.run()


