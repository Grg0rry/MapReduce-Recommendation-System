from mrjob.job import MRJob


class DataDividedByMovie(MRJob):      

    def mapper(self, _, line):
        User_Movie_Rating = line.split(",")

        UserID = int(User_Movie_Rating[0])
        MovieID = User_Movie_Rating[1]
        Rating = int(User_Movie_Rating[2])
        yield(MovieID, f'{UserID}:{Rating}')

    def reducer(self, MovieID, UserRating):
        yield(MovieID, list(UserRating))

if __name__ == '__main__':
    DataDividedByMovie.run()