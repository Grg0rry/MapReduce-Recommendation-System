# MapReduce Recommendation System
Recommendation engine using the item-based collaborative filtering technique built on top of Hadoop Distributed File System and MapReduce to recommend movies with a repository of Netflix movie rating data.

## Background
The whole system runs on a cluster of AWS EC2 instances with the `SunU-Hadoop-Image v1.3 AMI`, where it is configured with 1 master node and 5 slave nodes, all of which uses the `t2.large` instance type.

### MapReduce Flow
The flow of task orchestrating follows the flow below:
```mermaid
stateDiagram
    Netflix_Dataset(Input) --> UserList
    Netflix_Dataset(Input) --> DataDividedByMovie
    DataDividedByMovie --> MovieVector
    UserList --> MovieVector
    MovieVector --> CosineSimilarity
    CosineSimilarity --> Similarity_Table(Output)
```

**UserList** \
Key: "$User_List" \
Pair: UserID \
_Eg. "$User_List" = 1025579_

**DataDividedByMovie** \
Key: MovieTitle \
Pair: (UserID, Rating) \
_Eg. Character = (1025579, 4)_

**MovieVector** \
Key: MovieTitle \
Pair: VectorSpace \
_Eg. Character = [4, 0, 5, 0, 0, ...]_

**CosineSimilarity** \
Key: (MovieTitle, MovieTitle) \
Pair: SimilarityScore \
_Eg. (Character, Captain Blood) = 0.2121_

## How to run?
1. Ensure you have configured EC2 clusters accordingly with MapReduce and HDFS.
```
# check if its empty
hadoop fs -ls /

# create the directories
hadoop fs -mkdir /user
hadoop fs -mkdir /user/hadoop
hadoop fs -mkdir /user/hadoop/netflix_data
hadoop fs -mkdir /user/hadoop/results
```
2. Clone the repository in the master node
```
git clone "https://github.com/Grg0rry/MapReduce-Recommendation-System"
```
3. Download the dataset [[follow here](#data)]
4. Upload the data to HDFS
```
hadoop fs -put data/cleaned_moviesTitles.csv netflix_data/
hadoop fs -put data/sample netflix_data/
```
**IMPORTANT** Double check if it follow the file structure [[follow here](#file-structure)] \
(_Proceed only if the file structure matches_)

1. run chmod to make the scripts executable
```
chmod +x script/*
```
2. execute the script
```
script/<script-file.sh>
```

---
### Data 
The original dataset comes from Netflix Kaggle Competition Page [[Click Here](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data)]
```
|-- data
|   |-- combined_data_1.txt
|   |-- combined_data_2.txt
|   |-- combined_data_3.txt
|   |-- combined_data_4.txt
|   |-- movies_titles.csv
|   |-- ...
```

Data Cleaning was done using the `script/processing.sh` script to merge and aggregate the data to form the structure below.
```
|-- data
|   |-- ...
|   |-- cleaned_ratings.csv
|   |-- cleaned_titles.csv
|   |-- cleaned_moviesTitles.csv
|   |-- sample
|   |-- ...
```
_For the sample, it is obtained by running _
```bash
split -b 500M data/cleaned_moviesTitles.csv sample
```

To directly access the cleaned dataset
1. Download the zip file:
[[Download](https://public-netflix-data-store.s3.amazonaws.com/datafiles.zip)]
2. Access through AWS-CLI
```
aws s3 ls s3://public-netflix-data-store/data

aws s3 sync s3://public-netflix-data-store/data/* <local-folder>
```

**Note:** \
The data cleaning can only be done on a local instance without MapReduce due to the format and structure of `combined_data_*.txt` file. 
Preferably perform it with `instances type of (t2.xlarge)` with the EBS volume size set to at least `(20 GiB)`.

---
### File Structure
Below is the structure used in organising files in both the HDFS and Local Linux Directory.

Directory Structure (Local):
```
/home/hadoop/recommendation-system
|-- src
|   |-- java_mapreduce
|   |   |-- javamr.jar
|   |   `-- solution
|   |       |-- UserList.java
|   |       |-- DataDividedByMovie.java
|   |       |-- MoviesVector.java
|   |       `-- CosineSimilarity.java
|   |-- py_mapreduce
|   |   |-- UserList_Mapper.py
|   |   |-- UserList_Reducer.py
|   |   |-- DataDividedByMovie_Mapper.py
|   |   |-- DataDividedByMovie_Reducer.py
|   |   |-- MoviesVector_Mapper.py
|   |   |-- MoviesVector_Reducer.py
|   |   |-- CosineSimilarity_Mapper.py
|   |   `-- CosineSimilarity_Reducer.py
|   |-- py_mrjob
|   |   |-- UserList.py
|   |   |-- DataDividedByMovie.py
|   |   |-- MoviesVector.py
|   |   `-- CosineSimilarity.py
|   `-- main.py
|-- preprocessing
|   |-- RatingsPreprocessing.py
|   |-- TitlesPreprocessing.py
|   `-- CombineMovieTitles.py
|-- script
|   |-- preprocessing.sh
|   |-- local_mapreduce.sh
|   |-- py_mapred_streaming.sh
|   |-- py_mrjob.sh
|   |-- java_mapreduce.sh
|   |-- java_py_mapreduce.sh
|   `-- recommendMovie.sh
|...
```

Directory Structure (HDFS):
```
/user/hadoop
|-- netflix_data
|   |-- sample
|   `-- cleaned_moviesTitles.csv
`-- results
    |-- local_mapreduce
    |-- py_mapred
    |-- py_mrjob
    |-- java_mapreduce
    `-- java_py_mapreduce
```
