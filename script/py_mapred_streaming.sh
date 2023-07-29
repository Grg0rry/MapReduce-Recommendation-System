#!/bin/bash

# Input -- input_data="netflix_data/cleaned_moviesTitles.csv"
input_data="netflix_data/sample"
output_data="results/py_mapred_streaming/output"

# Check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi
hadoop fs -rm -r results/py_mapred_streaming

# Check directory
directory="/home/hadoop/recommendation-system/src/py_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd $directory
    echo "Switch directory to $directory"
fi

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
hadoop fs -ls results/py_mapred_streaming/job1
if [[ $? -ne 0 ]]; then
    time mapred streaming \
    -files DataDividedByMovie_Mapper.py \
    -input $input_data \
    -output results/py_mapred_streaming/job1 \
    -mapper "python3 DataDividedByMovie_Mapper.py"
    echo "task 1/4 done..."
fi

# Job2: UserList
hadoop fs -ls results/py_mapred_streaming/job2
if [[ $? -ne 0 ]]; then
    time mapred streaming \
    -files UserList_Mapper.py,UserList_Reducer.py \
    -input $input_data \
    -output results/py_mapred_streaming/job2 \
    -mapper "python3 UserList_Mapper.py" \
    -reducer "python3 UserList_Reducer.py"
    echo "task 2/4 done..."
fi

# Job3: MoviesVector
hadoop fs -ls results/py_mapred_streaming/job3
if [[ $? -ne 0 ]]; then
    time mapred streaming \
    -files MoviesVector_Mapper.py,MoviesVector_Reducer.py \
    -input results/py_mapred_streaming/job1/part-00000,results/py_mapred_streaming/job2/part-00000 \
    -output results/py_mapred_streaming/job3 \
    -mapper "python3 MoviesVector_Mapper.py" \
    -reducer "python3 MoviesVector_Reducer.py"
    echo "task 3/4 done..."
fi

# Job4: CosineSimilarity
hadoop fs -ls $output_data
if [[ $? -ne 0 ]]; then
    time mapred streaming \
    -files CosineSimilarity_Mapper.py,CosineSimilarity_Reducer.py \
    -input results/py_mapred_streaming/job3/part-00000 \
    -output $output_data \
    -mapper "python3 CosineSimilarity_Mapper.py" \
    -reducer "python3 CosineSimilarity_Reducer.py"
    echo "task 4/4 done..." 
fi

# Calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results in hdfs -> $output_data"
