'''
The file is used to generate run_star file to facilitate automated run seq process
It basically parse splitted sra file names and generate bash command according to these filenames
'''
import os
filenames = os.listdir("../arx")
base = 'p="../arx"\n'
base += 'nohup /home/tool/STAR/source/STAR --genomeDir ../data/starg  --runThreadN 8   --readFilesIn '

mateFiles = [name for name in filenames if 'fastq' in name and '_' in name]
singleFile = [name for name in filenames if 'fastq' in name and '_' not in name]

if len(mateFiles) is 2:
    for name in mateFiles:
        base += '$p/'+name+" "
    base += '> loginfo &\n'
elif len(singleFile) is 1:
    base += '$p/' + singleFile[0]+" "
    base += '> loginfo &\n'
else:
    print "##problem with script"
    print filenames

print "mateFiles: ", mateFiles
print "singleFile", singleFile
with open("run_star.sh",'w') as f:f.write(base)
