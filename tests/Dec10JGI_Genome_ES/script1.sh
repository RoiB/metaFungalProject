nohup ssh node001 "cd /storage3/w/richard/meta2016/JGI38/Picst3; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node002 "cd /storage3/w/richard/meta2016/JGI38/Canta1; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node003 "cd /storage3/w/richard/meta2016/JGI38/Debha1; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node004 "cd /storage3/w/richard/meta2016/JGI38/Hypbu1; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node005 "cd /storage3/w/richard/meta2016/JGI38/Cante1; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node006 "cd /storage3/w/richard/meta2016/JGI38/Metbi1; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node008 "cd /storage3/w/richard/meta2016/JGI38/Canar1; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
nohup ssh node009 "cd /storage3/w/richard/meta2016/JGI38/Hanpo2; /home/tool/gmes/gmes_petap.pl --ES --fungus  --min_contig 10000 --cores 8 --v  --seq genome.fasta" &
