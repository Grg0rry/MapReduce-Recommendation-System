#!/bin/bash

# Input
# input_data="netflix_data/cleaned_moviesTitles.csv" # 2GB
input_data="netflix_data/sample" # 500MB
output_data="results/java_py_mapreduce/output"

# Check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi
hadoop fs -rm -r results/java_py_mapreduce

# Check directory -> Java src
directory="./src/java_mapreduce"
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
hadoop fs -ls results/java_py_mapreduce/job1
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.DataDividedByMovie \
    $input_data \
    results/java_py_mapreduce/job1
    echo "task 1/4 done..."
fi

# Job2: UserList
hadoop fs -ls results/java_py_mapreduce/job2
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.UserList \
    $input_data \
    results/java_py_mapreduce/job2
    echo "task 2/4 done..."
fi

# Job3: MoviesVector
hadoop fs -ls results/java_py_mapreduce/job3
if [[ $? -ne 0 ]]; then
    time hadoop jar javamr.jar solution.MoviesVector \
    results/java_py_mapreduce/job2/part-r-00000 results/java_py_mapreduce/job1/part-r-00000 \
    results/java_py_mapreduce/job3
    echo "task 3/4 done..."
fi

# Check directory -> Python src
directory="./src/py_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd $directory
    echo "Switch directory to $directory"
fi

# Job4: CosineSimilarity
hadoop fs -ls $output_data
if [[ $? -ne 0 ]]; then
    time mapred streaming \
    -files CosineSimilarity_Mapper.py,CosineSimilarity_Reducer.py \
    -input results/java_py_mapreduce/job3/part-r-00000 \
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
