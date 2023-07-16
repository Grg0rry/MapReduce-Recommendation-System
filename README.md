# recommendation-system
A recommendation system built on top of Hadoop Distributed File System and MapReduce

## Background
The whole system will be running on AWS EC2 instance with the SunU-Hadoop-Image v1.3 AMI. In addition, the system has been configured with 1 master node and 3 slave nodes, all of which uses the t2.large instance type. 

**Note:** 
Because of the file structure and format of the combined_data_*.txt file, preprocessing the data couldn't be done using the MapReduce method. Therefore the bash script `preprocessing.sh` had to be performed locally on one of the instances (t2.xlarge) with the EBS volume size set to at least (20 GiB). The output of the script is the `cleaned_moviesTitles.csv` file which can be used for MapReduce processing.

## File Structure
Below is the structure used in organising files in both the HDFS and Local Linux Directory.

Directory Structure (Local):
```
home/hadoop/workspace
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
|   `-- cleaned_moviesTitles.csv
`-- results
    |-- local_mapreduce
    |-- py_mapred
    |-- py_mrjob
    `-- java_mapreduce
```

## Data
Data Repository [[Download](https://netflix-big-data-assignment.s3.amazonaws.com/Datafiles.zip)],
Netflix Kaggle Competition Page [[Click Here](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data)]
```
|-- data
|   |-- combined_data_1.txt
|   |-- combined_data_2.txt
|   |-- combined_data_3.txt
|   |-- combined_data_4.txt
|   |-- movies_titles.csv
|   |-- cleaned_movies.csv
|   |-- cleaned_titles.csv
|   `-- cleaned_moviesTitles.csv
```

Info on `cleaned_moviesTitles.csv` and the number of missing values in each column. 
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100480507 entries, 0 to 100480506
Data columns (total 6 columns):
 #   Column       Dtype  
---  ------       -----  
 0   UserID       int64  
 1   Rating       int64  
 2   RatingDate   object 
 3   MovieID      int64  
 4   ReleaseYear  float64
 5   MovieTitle   object 
dtypes: float64(1), int64(3), object(2)
memory usage: 4.5+ GB
```
```
>>> df.isnull().sum()
UserID           0
Rating           0
RatingDate       0
MovieID          0
ReleaseYear    965
MovieTitle       0
dtype: int64
```

A simple descriptive analysis on `cleaned_moviesTitles.csv`
```
# The number of Users
>>> df['UserID'].nunique()
480189

# The number of Movies
>>> df['MovieID'].nunique()
17770

# The number of Ratings
>>> df['UserID'].count()
100480507

# The distribution of Ratings
>>> df['Rating'].value_counts()
Rating
4    33750958
3    28811247
5    23168232
2    10132080
1     4617990
Name: count, dtype: int64
```

