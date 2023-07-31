#!/bin/bash

codePath=./src/main.py
num_to_recommend=10
movie1="Batman Beyond: The Movie"
movie2="The Addams Family"
movie3="The Avengers"

rm -r temp
mkdir temp
py_mapred_streaming="/home/hadoop/recommendation-system/temp/py_mapred_streaming"
local_mapreduce="/home/hadoop/recommendation-system/temp/local_mapreduce"
py_mrjob="/home/hadoop/recommendation-system/temp/py_mrjob"
java_mapreduce="/home/hadoop/recommendation-system/temp/java_mapreduce"

hadoop fs -get "results/py_mapred_streaming/output/part-00000" "$py_mapred_streaming"
hadoop fs -get "results/local_mapreduce/output" "$local_mapreduce"
hadoop fs -get "results/py_mrjob/output/part-00000" "$py_mrjob"
hadoop fs -get "results/java_mapreduce/output/part-r-00000" "$java_mapreduce"

echo "py_mapred_streaming"
echo "-------------------"
python3 "$codePath" \
-CosineSim_Reducer "$py_mapred_streaming" \
-Search_Movie "$movie1" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$py_mapred_streaming" \
-Search_Movie "$movie2" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$py_mapred_streaming" \
-Search_Movie "$movie3" \
-Num_Recommend $num_to_recommend


echo "local_mapreduce"
echo "-------------------"
python3 "$codePath" \
-CosineSim_Reducer "$local_mapreduce" \
-Search_Movie "$movie1" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$local_mapreduce" \
-Search_Movie "$movie2" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$local_mapreduce" \
-Search_Movie "$movie3" \
-Num_Recommend $num_to_recommend


echo "py_mrjob"
echo "-------------------"
python3 "$codePath" \
-CosineSim_Reducer "$py_mrjob" \
-Search_Movie "$movie1" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$py_mrjob" \
-Search_Movie "$movie2" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$py_mrjob" \
-Search_Movie "$movie3" \
-Num_Recommend $num_to_recommend


echo "java_mapreduce"
echo "-------------------"
python3 "$codePath" \
-CosineSim_Reducer "$java_mapreduce" \
-Search_Movie "$movie1" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$java_mapreduce" \
-Search_Movie "$movie2" \
-Num_Recommend $num_to_recommend

python3 "$codePath" \
-CosineSim_Reducer "$java_mapreduce" \
-Search_Movie "$movie3" \
-Num_Recommend $num_to_recommend

rm -r temp