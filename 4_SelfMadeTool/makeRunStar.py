'''
prep work
1. Download *.sra file to '/storage3/w/richard/meta2015/dataForRNASeq/'
2. update
'''
import pandas as pd
import sys

def main():
    fullTable = pd.read_csv("/home/richard/research/1_DataSmall/fullTableInfoGff3GffRNA.csv")
    fullTable.index = fullTable['shortName']
    RNASeqFileInfo = pd.read_csv("/home/richard/research/1_DataSmall/rnaSeqFileList.csv")
    dataForRNASeq = '/storage3/w/richard/meta2015/dataForRNASeq/'
    placeForRNASeq = '/storage3/w/richard/meta2015/placeForRNASeq/'
    dataPath = '/storage3/w/richard/meta2015/fasta_gff_gtf_07302015/'
    tempPath = '/storage3/w/richard/tempFile/'
    logPath = '/storage3/w/richard/meta2015/logFile/'

    shortName = sys.argv[1]


    fastaName = fullTable.loc[shortName]['fastaName']

    idx = (RNASeqFileInfo['shortName'] == shortName); 
    rnaSeqFileNames = RNASeqFileInfo['fileName'].loc[idx]
    rnaSeqFileURLs = RNASeqFileInfo['URL'].loc[idx]

    # make script for the whole process of rna seq, prep -> ran-seq
    # create directory
    script = 'cd {}\n'.format(placeForRNASeq)
    script += 'mkdir {0}\ncd {0}\n'.format(shortName)

    # prep folders
    script += 'mkdir arx data data/starg star\n'

    # copy genome file and unzip it
    script += 'cp {}{}/{} ./data\n'.format(dataPath, shortName, fastaName)
    script += 'gunzip ./data/{}\n'.format(fastaName)

    # get RNA-seq 
    script += 'cd arx\n'
    for fileName in rnaSeqFileNames:
        script += 'cp {}{} .\n'.format(dataForRNASeq,fileName)
        script += '/home/tool/sratoolkit/bin/fastq-dump --split-3 {}\n'.format(fileName)

    # prepare genome for star
    script += 'cd ../data/starg\n'
    script += '/home/tool/STAR/source/STAR --runMode genomeGenerate --genomeDir . --genomeFastaFiles ../{} --runThreadN 8\n'.format(fastaName[:-3])

    ## run rna-seq
    # generate run_star.sh
    script += "cd ../../star\n"

    ################################################################################
    ################################################################################
    #######################  generate seperate file ################################
    runStar = "nohup /home/tool/STAR/source/STAR --genomeDir ../data/starg --runThreadN 8 --readFilesIn "
    group1, group2 = [], []
    for fileName in rnaSeqFileNames:
        group1.append('../arx/'+fileName[:-4]+'_1.fastq')
        group2.append('../arx/'+fileName[:-4]+'_2.fastq')
    runStar += ','.join(group1) + ' '
    runStar += ','.join(group2) + ' > loginfo &\n'
    with open(tempPath+'run_star_'+shortName+'.sh', 'w') as f: f.write(runStar)
    print "prepare script for run_star...Done!"
    ################################################################################
    ################################################################################

    # copy and execute run_star.sh
    script += 'cp {}run_star_{}.sh .\n'.format(tempPath,shortName)
    script += 'bash run_star_{}.sh &\n'.format(shortName)

    with open("{}rnaSeq_{}.sh".format(logPath,shortName), 'w') as f: f.write(script)
    print "please run rnaSeq_{}.sh in the star folder".format(shortName)
    
if __name__ == '__main__':
    main()