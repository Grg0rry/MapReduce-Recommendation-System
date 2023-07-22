#!/usr/bin/env python3

from mrjob.job import MRJob

class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        line = line.strip().split(",", 2)

        UserID = int(MovieRating[0])
        MovieTitle = MovieRating[5]
        Rating = int(MovieRating[1])
        yield(MovieTitle, f'{UserID}:{Rating}')

    def reducer(self, MovieTitle, UserRating):
        yield(MovieTitle, list(UserRating))

if __name__ == '__main__':
    DataDividedByMovie.run()


for line in sys.stdin:
    line = line.strip().split(",", 2)

    if len(line) < 3:
        continue

    UserID = int(line[1])
    MovieTitle = line[0]
    Rating = int(line[2])
    
    print('%s\t%s' % (MovieTitle, f'{UserID}:{Rating}'))
