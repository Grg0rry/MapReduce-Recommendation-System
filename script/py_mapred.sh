#!/bin/bash
set -e

# check hdfs connection
hadoop fs -ls /
if [[ $? -ne 0 ]]; then
    echo "HDFS connection failed. Exiting..."
fi


# remove output if already exist
hadoop fs -rm -r results/py_mapred/job || true


# continue
start=$(date +%s)

# -input netflix_data/cleaned_moviesTitles.csv \
mapred streaming \
-files ./src/py_mapred/DataDividedByMovie_Mapper.py,./src/py_mapred/UserList_Mapper.py,./src/py_mapred/MoviesVector_Reducer.py \
-input sample_movies.csv \
-output results/py_mapred/job \
-mapper "python3 ./src/py_mapred/DataDividedByMovie_Mapper.py" \
-mapper "python3 ./src/py_mapred/UserList_Mapper.py" \
-reducer "python3 ./src/py_mapred/MoviesVector_Reducer.py"

end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"