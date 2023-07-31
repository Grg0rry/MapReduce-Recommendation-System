#!/usr/bin/env python3

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("UserList").getOrCreate()
sc=spark.sparkContext 


class UserList(MRJob):

    def mapper(self, _, line):
        line = line.strip().split(",", 2)

        if len(line) < 3:
            return
        UserID = int(line[1])
        
        yield(UserID, "")

    def reducer(self, key, values):
        yield(str("$User_List"), int(key))

if __name__ == '__main__':
    UserList.run()
