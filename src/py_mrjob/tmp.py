#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        line = line.strip().split("\t", 1)

        MovieTitle = str(line[0])
        UserID, Rating = str(line[1]).strip().split()

        yield UserID, int(Rating)

if __name__ == '__main__':
    DataDividedByMovie.run()
