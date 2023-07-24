#!/usr/bin/env python3

from mrjob.job import MRJob
import numpy as np
from itertools import combinations

class CosineSimilarity(MRJob):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Movie_Vector = {}
        self.Magnitude = {}

    def mapper(self, _, line):
        line = line.strip().split('\t', 1)

        yield(line[0], line[1])

    def reducer(self, key, values):
        MovieTitle = key
        Vector = np.array([int(item.strip()) for item in values.strip('[]').split(',')])

        self.Movie_Vector[MovieTitle] = Vector
        self.Magnitude[MovieTitle] = np.linalg.norm(Vector)
    
    def reducer_final(self):
        for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(self.Movie_Vector.items(), 2):
            dot_product = np.dot(Vector, Next_Vector)
            similarity = dot_product / (self.Magnitude[MovieTitle] * self.Magnitude[Next_MovieTitle])
            yield ((MovieTitle, Next_MovieTitle), similarity)

if __name__ == '__main__':
    CosineSimilarity.run()