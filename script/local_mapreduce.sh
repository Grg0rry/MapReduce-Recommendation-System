#!/bin/bash

# Input
# input_data="netflix_data/cleaned_moviesTitles.csv" # 2GB
input_data="netflix_data/sample" # 500MB
output_data="results/local_mapreduce/output"

# Check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi
hadoop fs -rm -r results/local_mapreduce

# Check directory
directory="/home/hadoop/recommendation-system/src/py_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd $directory
    echo "Switch directory to $directory"
fi

# Store output
rm -r results
mkdir results
echo "Created directory results to temporary store output"
hadoop fs -get "$input_data" "results/$(basename "$input_data")"
tmp_input="results/$(basename "$input_data")"
hadoop fs -mkdir results/local_mapreduce

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
ls results/job1
if [[ $? -ne 0 ]]; then
    time cat $tmp_input | python3 DataDividedByMovie_Mapper.py | sort | tee results/job1 >/dev/null
    echo "task 1/4 done..."
fi

# Job2: UserList
ls results/job2
if [[ $? -ne 0 ]]; then
    time cat $tmp_input | python3 UserList_Mapper.py | sort | python3 UserList_Reducer.py | tee results/job2 >/dev/null
    echo "task 2/4 done..."
fi

# Job3: MoviesVector
ls results/job3
if [[ $? -ne 0 ]]; then
    time cat results/job1 results/job2 | python3 MoviesVector_Mapper.py | sort | python3 MoviesVector_Reducer.py | tee results/job3 >/dev/null
    echo "task 3/4 done..."
fi

# Job4: CosineSimilarity
ls results/job4
if [[ $? -ne 0 ]]; then
    time cat results/job3 | python3 CosineSimilarity_Mapper.py | sort | python3 CosineSimilarity_Reducer.py | tee results/job4 >/dev/null
    echo "task 4/4 done..."
fi

# Upload Job
hadoop fs -put results/job1 results/local_mapreduce/job1
hadoop fs -put results/job2 results/local_mapreduce/job2
hadoop fs -put results/job3 results/local_mapreduce/job3
hadoop fs -put results/job4 $output_data
rm -r results

# Calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results in hdfs -> $output_data"
