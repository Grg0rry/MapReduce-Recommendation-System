#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class MovieVector(MRJob):
    
    def configure_args(self):
        super(MovieVector, self).configure_args()
        self.add_file_arg('--job1')
        self.add_file_arg('--job2')

    def mapper_init(self):
        self.UserList = []
        self.MovieRating = {}

        with open(self.options.job2, 'r') as job2:
            for line in job2:
                line = line.strip().split('\t',1)
                self.UserList.append(line[0])

        with open(self.options.job1, 'r') as job1:
            for line in job1:
                line = line.strip().split('\t',1)

                UserID, Rating = line[1].split(':')
                MovieTitle = line[0]
                UserRating = self.MovieRating.get(MovieTitle, [])
                UserRating.append((int(UserID), int(Rating)))
                self.MovieRating[MovieTitle] = UserRating

    def mapper(self, _, line):
        for MovieTitle, UserRating in self.MovieRating.items():
            for UserID, Rating in UserRating:
                yield (MovieTitle, (UserID, Rating))

    def reducer(self, MovieTitle, values):        
        UserRating = list(values)

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


