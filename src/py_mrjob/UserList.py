from mrjob.job import MRJob


class UserList(MRJob):

    def mapper(self, _, line):
        MovieRating = line.split(",", 5)

        UserID = int(MovieRating[0])
        yield(UserID, "")


    def reducer(self, UserID, _):
        user_list = []
        user_list.append(UserID)
        yield(None, user_list)

if __name__ == '__main__':
    UserList.run()