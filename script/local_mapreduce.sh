#!/bin/bash

# Input -- input_data="/home/hadoop/recommendation-system/data/cleaned_moviesTitles.csv"
input_data="/home/hadoop/recommendation-system/data/500MB/sample"
output_data="/home/hadoop/recommendation-system/src/py_mapreduce/results/output"

# Check directory
directory="/home/hadoop/recommendation-system/src/py_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd "/home/hadoop/recommendation-system/src/py_mapreduce"    
    echo "Switch directory to $directory"
fi

# Store output
rm -r results
mkdir results
echo "Created directory results to store output"

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
ls results/job1
if [[ $? -ne 0 ]]; then
    time cat $input_data | python3 DataDividedByMovie_Mapper.py | sort | tee results/job1 >/dev/null
    echo "task 1/4 done..."
fi

# Job2: UserList
ls results/job2
if [[ $? -ne 0 ]]; then
    time cat $input_data | python3 UserList_Mapper.py | sort | python3 UserList_Reducer.py | tee results/job2 >/dev/null
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
    time cat results/job3 | python3 CosineSimilarity_Mapper.py | sort | python3 CosineSimilarity_Reducer.py | tee $output_data >/dev/null
    echo "task 4/4 done..."
fi

# Calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results can be found in local -> $output_data"
