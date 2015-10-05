import pandas as pd
import sys
import datetime

def fill(num):
        if len(num) == 1:
            return "0"+num
        else:
            return num

def addTimeStamp():
    obj = datetime.datetime.now()
    timeStamp = "".join(map(fill,map(str,[obj.year, obj.month, obj.day, obj.hour, obj.minute])))
    return timeStamp


logPath = '/storage3/w/richard/meta2015/logFile/'
RNASeqFileInfo = pd.read_csv("/home/richard/research/1_DataSmall/rnaSeqFileList.csv")
RNASeqFileInfo.to_csv("/home/richard/research/1_DataSmall/rnaSeqFileInfoBackup/rnaSeqFileList{}.csv".format(addTimeStamp()), index = None)
dataForRNASeq = '/storage3/w/richard/meta2015/dataForRNASeq/'

shortName = sys.argv[1]

def main():
    # make script to download rna seq
    script_rna = 'cd {}\n'.format(dataForRNASeq)
    idx = RNASeqFileInfo['shortName'] == shortName;

    for filename in RNASeqFileInfo.loc[idx]['fileName']:
        if filename[-3:] == "sra":
            runName = filename[:-4]
        else:
            runName = filename
        runNameURL = "{}/{}/{}/{}.sra".format(runName[:3],runName[:6],runName,runName)
        #print runNameURL
        base = "ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/"
        URL = base + runNameURL
        script_rna+="wget {}\n".format(URL)

        RNASeqFileInfo.loc[idx,'fileName'] = runName+".sra"
        RNASeqFileInfo.loc[idx,'URL'] = URL

    #print script_rna

    RNASeqFileInfo.to_csv("/home/richard/research/1_DataSmall/rnaSeqFileList.csv", index = None)
    with open("{}getRNASeqData_{}.sh".format(logPath, shortName), 'w') as f: f.write(script_rna)
    print "Please wait until the download is done to run alignment with command: bash runAlignment.sh {}".format(shortName)
    # RNASeqFileInfo



if __name__ == '__main__':
    main()
