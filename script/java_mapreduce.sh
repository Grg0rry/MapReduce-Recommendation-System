#!/bin/bash

# Input -- input_data="netflix_data/cleaned_moviesTitles.csv"
input_data="netflix_data/sample"
output_data="results/java_mapreduce/output"

# Check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi
hadoop fs -rm -r results/java_mapreduce

# Check directory
directory="/home/hadoop/recommendation-system/src/java_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd $directory
    echo "Switch directory to $directory"
fi

# Compile to Jar
javac -classpath `hadoop classpath` solution/*.java
jar cvf javamr.jar solution/*.class

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
hadoop fs -ls results/java_mapreduce/job1
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.DataDividedByMovie \
    $input_data \
    results/java_mapreduce/job1
    echo "task 1/4 done..."
fi

# Job2: UserList
hadoop fs -ls results/java_mapreduce/job2
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.UserList \
    $input_data \
    results/java_mapreduce/job2
    echo "task 2/4 done..."
fi

# Job3: MoviesVector
hadoop fs -ls results/java_mapreduce/job3
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.MoviesVector \
    results/java_mapreduce/job2/part-r-00000 results/java_mapreduce/job1/part-r-00000 \
    results/java_mapreduce/job3
    echo "task 3/4 done..."
fi

# Job4: CosineSimilarity
hadoop fs -ls results/java_mapreduce/job4
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.CosineSimilarity \
    results/java_mapreduce/job3/part-r-00000 \
    $output_data
    echo "task 4/4 done..." 
fi

# Calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results in hdfs -> $output_data"
