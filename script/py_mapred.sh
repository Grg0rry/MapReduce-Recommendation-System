#!/bin/bash
set -e

# SEARCH (EDIT HERE)
movie_file="/home/hadoop/recommendation-system/Movie_Search.txt"
input_data="netflix_data/cleaned_moviesTitles.csv"


# check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi

# check if in directory
directory="/home/hadoop/recommendation-system/src/py_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd "/home/hadoop/recommendation-system/src/py_mapreduce" 
    echo "Switch directory to $directory"
fi

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
hadoop fs -ls results/py_mapred_streaming/job1
if [[ $? -ne 0 ]]; then
    mapred streaming \
    -files DataDividedByMovie_Mapper.py,DataDividedByMovie_Reducer.py \
    -input $input_data \
    -output results/py_mapred_streaming/job1 \
    -mapper "python3 DataDividedByMovie_Mapper.py" \
    -reducer "python3 DataDividedByMovie_Reducer.py"
fi

# Job2: UserList
hadoop fs -ls results/py_mapred_streaming/job2
if [[ $? -ne 0 ]]; then
    mapred streaming \
    -files UserList_Mapper.py,UserList_Reducer.py \
    -input $input_data \
    -output results/py_mapred_streaming/job2 \
    -mapper "python3 UserList_Mapper.py" \
    -reducer "python3 UserList_Reducer.py"
fi

# Job3: MoviesVector
hadoop fs -ls results/py_mapred_streaming/job3
if [[ $? -ne 0 ]]; then
    mapred streaming \
    -files MoviesVector_Mapper.py,MoviesVector_Reducer.py \
    -input results/py_mapred_streaming/job1/part-00000,results/py_mapred_streaming/job2/part-00000 \
    -output results/py_mapred_streaming/job3 \
    -mapper "python3 MoviesVector_Mapper.py" \
    -reducer "python3 MoviesVector_Reducer.py"
fi

# Job4: CosineSimilarity
hadoop fs -ls results/py_mapred_streaming/job4
if [[ $? -ne 0 ]]; then
    mapred streaming \
    -files CosineSimilarity_Mapper.py,CosineSimilarity_Reducer.py \
    -input results/py_mapred_streaming/job3/part-00000 \
    -output results/py_mapred_streaming/job4 \
    -mapper "python3 CosineSimilarity_Mapper.py" \
    -reducer "python3 CosineSimilarity_Reducer.py"
fi

# Job5: SearchRecommendation
hadoop fs -ls results/py_mapred_streaming/job5
if [[ $? -ne 0 ]]; then
    mapred streaming \
    -files QueryRecommendation_Mapper.py,QueryRecommendation_Reducer.py \
    -input results/py_mapred_streaming/job4/part-00000,$movie_file \
    -output results/py_mapred_streaming/job5 \
    -mapper "python3 QueryRecommendation_Mapper.py" \
    -reducer "python3 QueryRecommendation_Reducer.py"
fi

# calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results can be found in hdfs -> results/py_mapred/job5"


# -D mapred.reduce.tasks=4 
# -file ~/mayo/smplMapper.py -mapper smplMapper.py 
# -file ~/mayo/smplReducer.py -reducer smplReducer.py 
# -input customers.dat -input countries.dat -output mayo -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -jobconf stream.map.output.field.separator=^ -jobconf stream.num.map.output.key.fields=4 -jobconf map.output.key.field.separator=^ -jobconf num.key.fields.for.partition=1
