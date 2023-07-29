#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep
# import numpy as np
# from itertools import combinations

class CosineSimilarity(MRJob):

    def reducer_init(self):
        self.Movie_Vector = {}
        self.Magnitude = {}

    def mapper(self, _, line):
        line = line.strip().replace('"','').split('\t', 1)
        
        MovieTitle = str(line[0])
        Vector = []
        for Rating in line[1].strip('[]').split(','):
            Vector.append(int(Rating))

        yield(MovieTitle, Vector)

    def reducer(self, MovieTitle, Vectors):
        for Vector in Vectors:
            self.Movie_Vector[MovieTitle] = Vector

            magnitude = 0
            for val in Vector:
                magnitude += val * val
            self.Magnitude[MovieTitle] = magnitude

            # self.Movie_Vector[MovieTitle] = np.array(Vector)
            # self.Magnitude[MovieTitle] = np.linalg.norm(Vector)
    
    def reducer_final(self):
        for MovieTitle_1, Vector_1 in self.Movie_Vector.items():
            for MovieTitle_2, Vector_2 in self.Movie_Vector.items():
                if MovieTitle_1 != MovieTitle_2:

                    dot_product = 0
                    for i in range(len(Vector_1)):
                        dot_product += Vector_1[i] * Vector_2[i]
                    
                    similarity = dot_product / (self.Magnitude[MovieTitle_1] * self.Magnitude[MovieTitle_2])
                    yield ((MovieTitle_1, MovieTitle_2), similarity)

        # for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(self.Movie_Vector.items(), 2):
        #     dot_product = np.dot(Vector, Next_Vector)
        #     similarity = dot_product / (self.Magnitude[MovieTitle] * self.Magnitude[Next_MovieTitle])
        #     yield ((MovieTitle, Next_MovieTitle), similarity)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer_init=self.reducer_init,
                   reducer=self.reducer,
                   reducer_final=self.reducer_final)
        ]

if __name__ == '__main__':
    CosineSimilarity.run()
