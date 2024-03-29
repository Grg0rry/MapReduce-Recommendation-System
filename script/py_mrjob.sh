#!/bin/bash

# Input
# input_data="hdfs:///user/hadoop/netflix_data/cleaned_moviesTitles.csv" # 2GB
input_data="hdfs:///user/hadoop/netflix_data/sample" # 500MB
output_data="hdfs:///user/hadoop/results/py_mrjob/output"

# Check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
    exit
fi
hadoop fs -rm -r results/py_mrjob

# Check and Change directory
directory="./src/py_mrjob"
if [[ $(pwd) != directory ]]; then
    cd $directory  
    echo "Switch directory to $directory"
fi

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
hadoop fs -ls results/py_mrjob/job1
if [[ $? -ne 0 ]]; then
    time python3 DataDividedByMovie.py \
    -r hadoop $input_data \
    --output hdfs:///user/hadoop/results/py_mrjob/job1
    echo "task 1/4 done..."
fi

# Job2: UserList
hadoop fs -ls results/py_mrjob/job2
if [[ $? -ne 0 ]]; then
    time python3 UserList.py \
    -r hadoop $input_data \
    --output hdfs:///user/hadoop/results/py_mrjob/job2
    echo "task 2/4 done..."
fi

# Job3: MoviesVector
hadoop fs -ls results/py_mrjob/job3
if [[ $? -ne 0 ]]; then
    hadoop fs -get results/py_mrjob/job2/part-00000 temp

    time python3 MoviesVector.py \
    -r hadoop \
    hdfs:///user/hadoop/results/py_mrjob/job1/part-00000 \
    --file1 temp \
    --output hdfs:///user/hadoop/results/py_mrjob/job3
    echo "task 3/4 done..."

    rm temp
fi

# Job4: CosineSimilarity
hadoop fs -ls results/py_mrjob/output
if [[ $? -ne 0 ]]; then
    time python3 CosineSimilarity.py \
    -r hadoop hdfs:///user/hadoop/results/py_mrjob/job3/part-00000 \
    --output $output_data
    echo "task 4/4 done..."
fi

# Calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results in hdfs -> $output_data"