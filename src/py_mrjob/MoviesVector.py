#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class MovieVector(MRJob):
    
    def configure_args(self):
        """
        Takes in the additional input of UserList
        """
        super(MovieVector, self).configure_args()
        self.add_file_arg('--file1', required=True, type=str)

    def userlist(self):
        """
        Lists the Unique UserID
        """
        self.UserList = []

        with open(self.options.file1, 'r') as file1:
            for line in file1:
                line = line.strip().replace('"','').split('\t',1)
                self.UserList.append(int(line[1]))

    def mapper(self, _, line):
        """
        Performs mapper to create MovieTitle with a list of UserRating
        """
        line = line.strip().replace('"','').split('\t', 1)

        MovieTitle = str(line[0])
        UserRating = []
        for pair in line[1].strip('[]').split(','):
            UserID, Rating = pair.split(':')
            UserRating.append((int(UserID), int(Rating)))
        yield MovieTitle, UserRating

    def reducer(self, MovieTitle, UserRatings):
        """
        Using UserList and Mapper to create the vector of ratings for each MovieTitle
        """
        UserRatingsByOrder = {Order_UserID: 0 for Order_UserID in self.UserList}

        for UserRating in UserRatings:
            for UserID, Rating in UserRating:
                if UserID in UserRatingsByOrder:
                    UserRatingsByOrder[UserID] = int(Rating)

        Vector = list(UserRatingsByOrder.values())
        yield (MovieTitle, Vector)

    def steps(self):
        """
        Combines and chains the functions together
        """
        return [
            MRStep(mapper=self.mapper,
                   reducer_init=self.userlist,
                   reducer=self.reducer)
        ]
    
if __name__ == '__main__':
    MovieVector.run()


