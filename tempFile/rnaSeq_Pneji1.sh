cd /storage3/w/richard/meta2015/rnaSeqPlace
mkdir Pneji1
cd Pneji1
mkdir arx data data/starg star
cp /home/richard/1_DataLarge/fasta_gff_gtf_07302015/Pneji1/Pneji1_AssemblyScaffolds.fasta.gz ./data
gunzip ./data/Pneji1_AssemblyScaffolds.fasta.gz
cd arx
cp /storage3/w/richard/meta2015/rnaSeqData/ERR135878.sra .
/home/tool/sratoolkit/bin/fastq-dump --split-3 ERR135878.sra
cd ../data/starg
/home/tool/STAR/source/STAR --runMode genomeGenerate --genomeDir . --genomeFastaFiles ../Pneji1_AssemblyScaffolds.fasta --runThreadN 8
cd ../../star
python /home/richard/research/4_SelfMadeTool/generateRunStar.py .
bash run_star.sh &
