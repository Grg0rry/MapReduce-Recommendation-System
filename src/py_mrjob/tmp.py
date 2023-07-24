import subprocess
cat = subprocess.Popen(["hadoop", "fs", "-cat", "/user/hadoop/results/py_mapred_streaming/job2/part-00000"], stdout=subprocess.PIPE)
cnt = 1
for line in cat.stdout:
    
    if cnt > 10:
        break
        
    line = line.strip().split('\t',1)
    print(line[0])