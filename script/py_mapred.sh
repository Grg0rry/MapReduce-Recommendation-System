#!/bin/bash
set -e

# check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi


# remove output if already exist
hadoop fs -rm -r results/py_mapred/job1 || true
hadoop fs -rm -r results/py_mapred/job2 || true
hadoop fs -rm -r results/py_mapred/job3 || true
hadoop fs -rm -r results/py_mapred/job4 || true


# continue
start=$(date +%s)

#-input netflix_data/sample_movies \
mapred streaming \
-files ./src/py_mapred/DataDividedByMovie_Mapper.py,./src/py_mapred/DataDividedByMovie_Reducer.py \
-input netflix_data/sample_movies.csv \
-output results/py_mapred/job1 \
-mapper "python3 ./src/py_mapred/DataDividedByMovie_Mapper.py" \
-reducer "python3 ./src/py_mapred/DataDividedByMovie_Reducer.py"

-input netflix_data/cleaned_moviesTitles.csv \

mapred streaming \
-files ./src/py_mapred/UserList_Mapper.py \
-input netflix_data/cleaned_moviesTitles.csv \
-output results/py_mapred/job2 \
-mapper "python3 ./src/py_mapred/UserList_Mapper.py"

mapred streaming \
-files ./src/py_mapred/MoviesVector_Reducer.py \
-input hdfs:///user/hadoop/results/py_mapred/job1/part*,hdfs:///user/hadoop/results/py_mapred/job2/part* \
-output results/py_mapred/job3 \
-reducer "python3 ./src/py_mapred/MoviesVector_Reducer.py"

mapred streaming \
-files ./src/py_mapred/CosineSimilarity_Reducer.py \
-input hdfs:///user/hadoop/results/py_mapred/job3/part* \
-output results/py_mapred/job4 \
-reducer "python3 ./src/py_mapred/CosineSimilarity_Reducer.py"

end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds" 