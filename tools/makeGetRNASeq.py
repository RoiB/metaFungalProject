import pandas as pd
import sys
def main():
    logPath = '/storage3/w/richard/meta2015/logFile/'
    RNASeqFileInfo = pd.read_csv("/home/richard/research/1_DataSmall/rnaSeqFileList.csv")
    dataForRNASeq = '/storage3/w/richard/meta2015/dataForRNASeq/'

    shortName = sys.argv[1]
    # make script to download rna seq
    script_rna = 'cd {}\n'.format(dataForRNASeq)
    idx = RNASeqFileInfo['shortName'] == shortName;
    for URL in RNASeqFileInfo.loc[idx]['URL']:
        script_rna+="wget {}\n".format(URL)
    #print script_rna
    with open("{}getRNASeqData_{}.sh".format(logPath, shortName), 'w') as f: f.write(script_rna)
    print "please run bash {}getRNASeqData_{}.sh to download rna seq file and wait util it's done".format(logPath,shortName)
    

if __name__ == '__main__':
    main()