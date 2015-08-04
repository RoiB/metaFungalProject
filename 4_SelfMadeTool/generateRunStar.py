'''
The file is used to generate run_star file to facilitate automated run seq process
It basically parse splitted sra file names and generate bash command according to these filenames
'''
import os
filenames = os.listdir("../arx")
base = 'p="../arx"\n'
base += 'nohup /home/tool/STAR/source/STAR --genomeDir ../data/starg  --runThreadN 8   --readFilesIn '

mateFiles = [name for name in filenames if 'fastq' in name and '_' in name]
if len(mateFiles) is 2:
    for name in filenames:
        base += '$p/'+name+" "
elif len(mateFiles) is 0:
    base +=




base += '> loginfo &\n'
with open("run_star.sh",'w') as f:f.write(base)
