import pydoop.hdfs as hdfs

with hdfs.open('/user/hadoop/results/py_mrjob/job2/part-00000', 'r') as f:
    cnt = 1
    for line in f:
        if cnt > 10:
            break
        line = line.strip().split('\t',1)
        print(line[0])