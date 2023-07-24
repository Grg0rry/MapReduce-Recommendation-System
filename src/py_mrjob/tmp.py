#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        line = line.strip().split("\t", 2)

        yield line[0], line[1]

    def reducer(self, movie, values):
        yield movie, list(values)

    # def reducer(self, key, values):
    #     yield(key, list(values))

if __name__ == '__main__':
    DataDividedByMovie.run()
