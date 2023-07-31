#!/usr/bin/env python3

from pyspark.sql import SparkSession

def initialize_session(appName):
    spark = SparkSession.builder.master("local[*]").appName(appName).getOrCreate()
    global sc=spark.sparkContext

shakespeare_rdd = sc.textFile("/shakespeare/comedies/")

if __name__ == '__main__':



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
    initialize_session("UserList")
