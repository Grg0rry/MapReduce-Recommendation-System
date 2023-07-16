#!/bin/bash

# check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
    return 
fi

# continue
start=$(date +%s)

python3 ./src/py_mrjob/DataDividedByMovie.py \
-r hadoop hdfs:///user/hadoop/netflix_data/cleaned_movies.csv \
--output hdfs:///user/hadoop/results/py_mrjob/job1

python3 ./src/py_mrjob/UserList.py \
-r hadoop hdfs:///user/hadoop/netflix_data/cleaned_movies.csv \
--output hdfs:///user/hadoop/results/py_mrjob/job2

python3 ./src/py_mrjob/.py \
-r hadoop hdfs:///user/hadoop/results/py_mrjob/job1 \
--addition_input hdfs:///user/hadoop/results/py_mrjob/job2 \
--output hdfs:///user/hadoop/results/py_mrjob/job3

end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"