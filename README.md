# recommendation-system
A recommendation system built on top of Hadoop Distributed File System and MapReduce

## Background
The whole system will be running on AWS EC2 instance with the SunU-Hadoop-Image v1.3 AMI. In addition, the system has been configured with 1 master node and 3 slave nodes, all of which uses the t2.large instance type. 

Note:
Because of the file structure and format of the combined_data_*.txt file, preprocessing the data couldn't be done using the MapReduce method. Therefore the bash script `preprocessing.sh` had to be performed locally on one of the instances (t2.xlarge) with the EBS volume size set to at least (20 GiB). The output of the script is the `cleaned_moviesTitles.csv` file which can be used for MapReduce processing.

## File Structure
Below is the structure used in organising files in both the HDFS and Local Linux Directory.

Directory Structure (Local):
```
home/hadoop/workspace
|-- data
|   |-- combined_data_1.txt
|   |-- combined_data_2.txt
|   |-- combined_data_3.txt
|   |-- combined_data_4.txt
|   `-- movies_titles.csv
|-- src
|   |-- local_mapreduce
|   |   |-- main.py
|   |   |-- UserList
|   |   |   |-- mapper.py
|   |   |   `-- reducer.py
|   |   |-- UtilityMatrix
|   |   |   |-- mapper.py
|   |   |   `-- reducer.py
|   |   `-- ConsineSimilarity
|   |       |-- mapper.py
|   |       `-- reducer.py
|   |-- py_mapred
|   |   |-- main.py
|   |   |-- UserList
|   |   |   |-- mapper.py
|   |   |   `-- reducer.py
|   |   |-- UtilityMatrix
|   |   |   |-- mapper.py
|   |   |   `-- reducer.py
|   |   |-- ConsineSimilarity
|   |       |-- mapper.py
|   |       `-- reducer.py
|   |-- py_mrjob
|   |   |-- main.py
|   |   |-- UserList.py
|   |   |-- UtilityMatrix.py
|   |   `-- ConsineSimilarity.py
|   `-- java_mapreduce
|       |-- UserList
|       |   |-- mapper.java
|       |   |-- reducer.java
|       |   `-- driver.java
|       |-- UtilityMatrix
|       |   |-- mapper.java
|       |   |-- reducer.java
|       |   `-- driver.java
|       `-- ConsineSimilarity
|           |-- mapper.java
|           |-- reducer.java
|           `-- driver.java
|-- preprocessing
|   |-- ratingsPreprocessing.py
|   |-- titlesPreprocessing.py
|   `-- combineMovieTitles.py
`-- script
    |-- preprocessing.sh
    |-- local_mapreduce.sh
    |-- py_mapred.sh
    |-- py_mrjob.sh
    `-- java_mapreduce.sh
```

Directory Structure (HDFS)
```
user/hadoop
|-- netflix_data
|   |-- combined_data_1.txt
|   |-- combined_data_2.txt
|   |-- combined_data_3.txt
|   |-- combined_data_4.txt
|   `-- movies_titles.csv
`-- results
    |-- local_mapreduce
    |-- py_mapred
    |-- py_mrjob
    `-- java_mapreduce
```

## Data
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1426551 entries, 0 to 1426550
Data columns (total 4 columns):
 #   Column   Non-Null Count    Dtype 
---  ------   --------------    ----- 
 0   CustId   1426551 non-null  int64 
 1   Rating   1426551 non-null  int64 
 2   Date     1426550 non-null  object
 3   MovieId  1426551 non-null  int64 
dtypes: int64(3), object(1)
memory usage: 43.5+ MB
```
