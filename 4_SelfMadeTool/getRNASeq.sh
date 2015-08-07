cd /storage3/w/richard/meta2015/logFile/
#python ~richard/research/4_SelfMadeTool/makeGetRNASeq.py "$1"
python ~richard/research/4_SelfMadeTool/makeGetRNASeqV2.py "$1"
nohup bash getRNASeqData_"$1".sh > getRNASeqData_"$1".out &

