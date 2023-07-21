#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        MovieRating = line.split("\t", 5)
        # MovieRating = line.split(",", 5)

        UserID = int(MovieRating[0])
        MovieTitle = MovieRating[5]
        Rating = int(MovieRating[1])
        yield(MovieTitle, f'{UserID}:{Rating}')

    def reducer(self, MovieTitle, UserRating):
        yield(MovieTitle, list(UserRating))

if __name__ == '__main__':
    DataDividedByMovie.run()