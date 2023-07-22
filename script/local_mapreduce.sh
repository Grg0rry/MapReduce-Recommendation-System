#!/bin/bash
set -e

# SEARCH (EDIT HERE)
movie_file="/home/hadoop/recommendation-system/Movie_Search.txt"
# input_data="/home/hadoop/recommendation-system/data/cleaned_moviesTitles.csv"
input_data="/home/hadoop/recommendation-system/data/chunksaa"


# check if in directory
directory="/home/hadoop/recommendation-system/src/py_mapreduce"
if [[ $(pwd) != directory ]]; then
    cd "/home/hadoop/recommendation-system/src/py_mapreduce"    
    echo "Switch directory to $directory"
fi

# store output
ls results
if [[ $? -ne 0 ]]; then
    mkdir results
    echo "Created directory results to store output"
fi

# Execute each job
start=$(date +%s)

# Job1: DataDividedByMovie
ls results/job1 || true
if [[ $? -ne 0 ]]; then
    cat $input_data | python3 DataDividedByMovie_Mapper.py | sort | python3 DataDividedByMovie_Reducer.py | tee results/job1 >/dev/null
fi

# Job2: UserList
ls results/job2 || true
if [[ $? -ne 0 ]]; then
    cat $input_data | python3 UserList_Mapper.py | sort | python3 UserList_Reducer.py | tee results/job2 >/dev/null
fi

# Job3: MoviesVector
ls results/job3 || true
if [[ $? -ne 0 ]]; then
    cat results/job1 results/job2 | python3 MoviesVector_Mapper.py | sort | python3 MoviesVector_Reducer.py | tee results/job3 >/dev/null
fi

# Job4: CosineSimilarity
ls results/job4 || true
if [[ $? -ne 0 ]]; then
    cat results/job3 | python3 CosineSimilarity_Mapper.py | sort | python3 CosineSimilarity_Reducer.py | tee results/job4 >/dev/null
fi

# Job5: QueryRecommendation
ls results/job5 || true
if [[ $? -ne 0 ]]; then
    cat results/job4 $movie_file | python3 QueryRecommendation_Mapper.py | sort | python3 QueryRecommendation_Reducer.py | tee results/job5 >/dev/null
fi

# calculate time
end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"
echo "-- Results can be found in local -> results/job5"


# -D mapred.reduce.tasks=4 
# -file ~/mayo/smplMapper.py -mapper smplMapper.py 
# -file ~/mayo/smplReducer.py -reducer smplReducer.py 
# -input customers.dat -input countries.dat -output mayo -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -jobconf stream.map.output.field.separator=^ -jobconf stream.num.map.output.key.fields=4 -jobconf map.output.key.field.separator=^ -jobconf num.key.fields.for.partition=1
