#!/bin/bash
set -e

num_to_recommend=10
movie1="Batman Beyond: The Movie"
movie2="The Addams Family"
movie3="The Avengers"

py_mapred_streaming="results/py_mapred_streaming/output/part-00000"
local_mapreduce="results/local_mapreduce/output"
py_mrjob="results/py_mrjob/output/part-00000"
java_mapreduce="results/java_mapreduce/output/part-r-00000"


echo "py_mapred_streaming"
echo $movie1
python3 ./main.py \
-CosineSim_Reducer $py_mapred_streaming \
-Search_Movie $movie1 \
-Num_Recommend $num_to_recommend

echo "py_mapred_streaming"
echo $movie2
python3 ./main.py \
-CosineSim_Reducer $py_mapred_streaming  \
-Search_Movie $movie2 \
-Num_Recommend $num_to_recommend

echo "py_mapred_streaming"
echo $movie3
python3 ./main.py \
-CosineSim_Reducer $py_mapred_streaming  \
-Search_Movie $movie3 \
-Num_Recommend $num_to_recommend

echo "local_mapreduce"
echo $movie1
python3 ./main.py \
-CosineSim_Reducer $local_mapreduce \
-Search_Movie $movie1 \
-Num_Recommend $num_to_recommend

echo "local_mapreduce"
echo $movie2
python3 ./main.py \
-CosineSim_Reducer $local_mapreduce \
-Search_Movie $movie2 \
-Num_Recommend $num_to_recommend

echo "local_mapreduce"
echo $movie3
python3 ./main.py \
-CosineSim_Reducer $local_mapreduce \
-Search_Movie $movie3 \
-Num_Recommend $num_to_recommend

echo "py_mrjob"
echo $movie1
python3 ./main.py \
-CosineSim_Reducer $py_mrjob \
-Search_Movie $movie1 \
-Num_Recommend $num_to_recommend

echo "py_mrjob"
echo $movie2
python3 ./main.py \
-CosineSim_Reducer $py_mrjob \
-Search_Movie $movie2 \
-Num_Recommend $num_to_recommend

echo "py_mrjob"
echo $movie3
python3 ./main.py \
-CosineSim_Reducer $py_mrjob \
-Search_Movie $movie3 \
-Num_Recommend $num_to_recommend

echo "java_mapreduce"
echo $movie1
python3 ./main.py \
-CosineSim_Reducer $java_mapreduce \
-Search_Movie $movie1 \
-Num_Recommend $num_to_recommend

echo "java_mapreduce"
echo $movie2
python3 ./main.py \
-CosineSim_Reducer $java_mapreduce \
-Search_Movie $movie2 \
-Num_Recommend $num_to_recommend

echo "java_mapreduce"
echo $movie3
python3 ./main.py \
-CosineSim_Reducer $java_mapreduce \
-Search_Movie $movie3 \
-Num_Recommend $num_to_recommend
