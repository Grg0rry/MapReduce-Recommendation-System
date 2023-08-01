#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        line = line.strip().split(",", 2)

        # check if it contains at least 3 elements
        if len(line) < 3:
            return

        UserID = int(line[1])
        MovieTitle = line[0]
        Rating = int(line[2])

        yield(str(MovieTitle), f'{int(UserID)}:{int(Rating)}')

    def reducer(self, key, values):
        yield(key, list(values))

if __name__ == '__main__':
    DataDividedByMovie.run()
