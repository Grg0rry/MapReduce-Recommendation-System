#!/bin/bash
set -e

# check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi

# check if in directory
directory="/home/hadoop/recommendation-system/src/py_mapred"
if [[ $(pwd) != directory ]]; then
    cd "/home/hadoop/recommendation-system/src/py_mapred"    
    echo "Switch directory to $directory"
fi

# remove output if already exist
hadoop fs -rm -r results/py_mapred/job1 || true
hadoop fs -rm -r results/py_mapred/job2 || true
hadoop fs -rm -r results/py_mapred/job3 || true
hadoop fs -rm -r results/py_mapred/job4 || true
hadoop fs -rm -r results/py_mapred/job5 || true

# start timer
start=$(date +%s)

# execute mapreduce -- sample_movies.csv
mapred streaming \
-files DataDividedByMovie_Mapper.py \
-input netflix_data/cleaned_moviesTitles.csv \
-output results/py_mapred/job1 \
-mapper "python3 DataDividedByMovie_Mapper.py"

mapred streaming \
-files UserList_Mapper.py,UserList_Reducer.py \
-input netflix_data/cleaned_moviesTitles.csv \
-output results/py_mapred/job2 \
-mapper "python3 UserList_Mapper.py" \
-reducer "python3 UserList_Reducer.py"

hadoop fs -rm -r results/py_mapred/job3 || true

mapred streaming \
-files MoviesVector_Mapper.py,MoviesVector_Reducer.py \
-input results/py_mapred/job1/part-00000,results/py_mapred/job2/part-00000 \
-output results/py_mapred/job3 \
-mapper "python3 MoviesVector_Mapper.py" \
-reducer "python3 MoviesVector_Reducer.py"

-inputformat org.apache.hadoop.mapred.TextInputFormat

hadoop fs -cat -quiet results/py_mapred/job1/part-00000 results/py_mapred/job2/part-00000 -put results/py_mapred/job3

cat hdfs:///user/hadoop/results/py_mapred/job1/part-m-00000 hdfs:///user/hadoop/results/py_mapred/job2/part-m-00000 > hdfs:///user/hadoop/results/py_mapred/job3/part-m-00000 2>&1 > /dev/null








hadoop jar ../contrib/streaming/hadoop-0.20.1+169.89-streaming.jar 
-D mapred.reduce.tasks=4 
-file ~/mayo/smplMapper.py -mapper smplMapper.py 
-file ~/mayo/smplReducer.py -reducer smplReducer.py 
-input customers.dat -input countries.dat -output mayo -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -jobconf stream.map.output.field.separator=^ -jobconf stream.num.map.output.key.fields=4 -jobconf map.output.key.field.separator=^ -jobconf num.key.fields.for.partition=1


mapred streaming \
-files CosineSimilarity_Reducer.py \
-input hdfs:///user/hadoop/results/py_mapred/job3/part-00000 \
-output results/py_mapred/job4 \
-reducer "python3 CosineSimilarity_Reducer.py"

# calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds" 