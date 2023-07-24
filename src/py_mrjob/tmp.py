#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        line = line.strip().split("\t", 2)

        MovieTitle = str(line[0])
        UserID, Rating = line[1].split(':')

        yield UserID, int(Rating)

if __name__ == '__main__':
    DataDividedByMovie.run()
