from mrjob.job import MRJob, MRStep


class VectorMovie(MRJob):

    def configure_args(self):
        super(VectorMovie, self).configure_args()
        self.add_file_arg('--addition_input', help='Path of the UserList Job')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_MovieID = None
        self.UserList = []

    def mapper_init(self):
        with open(self.options.addition_input, 'r') as f:
            self.UserList = list(eval(f.read))

    def mapper(self, _, line):
        Vector = []

        MovieID, UserRating_list = line.split(",", 1)
        UserRating_list = eval(UserRating_list)
        
        for Search_UserID in self.UserList:
            found_match = False

            for UserRating in UserRating_list:
                UserID, Rating = UserRating.split(":", 1)

                if UserID == Search_UserID:
                    Vector.append(Rating)
                    found_match = True
                    break
                
            if not found_match:
                Vector.append(0)

        yield(MovieID, Vector)


    def reducer(self, MovieID, Vector):
        if self.last_MovieID is not None:
            last_MovieID, last_Vector = self.last_MovieID

            dot_product = sum(x * y for x, y in zip(Vector, last_Vector))
            magnitude = (sum(x ** 2 for x in Vector) ** 0.5) * (sum(x ** 2 for x in last_Vector) ** 0.5)

            yield((MovieID, last_MovieID), dot_product/magnitude)

        self.last_MovieID = (MovieID, Vector)

    
    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init, mapper=self.mapper, reducer=self.reducer)
        ]


if __name__ == '__main__':
    VectorMovie.run()
