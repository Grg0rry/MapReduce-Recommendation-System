#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        line = line.strip().split(",", 2)

        if len(line) < 3:
            return

        UserID = int(line[1])
        MovieTitle = line[0]
        Rating = int(line[2])

        yield(MovieTitle, f'{UserID}:{Rating}')

    def reducer(self, key, value):
        yield(key, list(value))

if __name__ == '__main__':
    DataDividedByMovie.run()
