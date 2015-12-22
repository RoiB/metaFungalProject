## instead of using single GC model file across all sequences, we use heuristic model with sequence gc

from Bio import SeqIO
from Bio.SeqUtils import GC
import subprocess
import sys

def gmhmmMultiFasta(modelFilePath, multiFastaFile, shortName):
    '''
    assume short name has Assembly inside
    model files must follow format: MetaFungal_model_30_mid.txt
    '''
    subprocess.check_call('mkdir {}'.format(shortName), shell = True)
    subprocess.check_call('mkdir {}/{}'.format(shortName,'fastaPieces'), shell = True)
    subprocess.check_call('mkdir {}/{}'.format(shortName,'predictions'), shell = True)
    fastaPieceLocation = '{}/{}/'.format(shortName,'fastaPieces')
    predictionLocation = '{}/{}/'.format(shortName,'predictions')
    fastaPieceFiles = []
    predictionFiles = []
    consolidatedPrediction = '{}/{}_fullPrediction.gtf'.format(shortName,shortName)
    
    ## split fasta file
    SeqRecords = SeqIO.parse(multiFastaFile,'fasta')
    id_gc_pair = {}
    for SeqRecord in SeqRecords:
        ## add info to id_gc_pair
        gc = max(30, int(round(GC(SeqRecord.seq))))
        gc = min(gc, 60)
        id_gc_pair[SeqRecord.id] = gc
        ## process fasta file
        filename = '{}{}.fasta'.format(fastaPieceLocation,SeqRecord.id)
        SeqIO.write(SeqRecord, filename,'fasta')
        fastaPieceFiles.append('{}.fasta'.format(SeqRecord.id))

    
    ## perform gmhmm on each piece
    script = ''
    base_command1 = '/home/tool/gmes/gmhmme3 -m {}/{}'#.format(modelFile)
    base_command2 = 'python /home/richard/research/tools/gmhmme3_to_gtfV4.py'

    counter = 0
    for fastaPiece in fastaPieceFiles:
        counter += 1
        #gmhmm prediction
        tempName = fastaPiece[:-5]+'tmp'
        ## add model file name
        fastaName = fastaPiece[:-6]
        command0 = ('{} {}{} -o {}{}\n'
                    .format(base_command1.format(modelFilePath,'MetaFungal_model_'+str(id_gc_pair[fastaName])+'_*'), 
                            fastaPieceLocation,fastaPiece,predictionLocation,tempName))
        subprocess.check_call(command0,shell = True)
        #convert prediciton
        outputName = tempName[:-3]+'prediction.gtf'
    #     print outputName
        predictionFiles.append(outputName)

        command1 = '{} {}{} {}{}\n'.format(base_command2, predictionLocation, tempName, predictionLocation, outputName)
        subprocess.check_call(command1,shell = True)
        command2 = 'rm {}{}\n'.format(predictionLocation, tempName)
        subprocess.check_call(command2,shell = True)
        command3 = 'echo "#{} prediction of {} is done! ---- Model used: GC {}"\n'.format(counter, fastaPiece, id_gc_pair[fastaName])
        subprocess.check_call(command3,shell = True)
    
    ## consolidate predicitons
    with open(consolidatedPrediction, 'w') as f:
        for predictionFile in predictionFiles:
            with open(predictionLocation+predictionFile) as f0:
                for line in f0:
                    f.write(line)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "please provide model file path, multi-fasta file and shortName"
    else:
        gmhmmMultiFasta(sys.argv[1], sys.argv[2],sys.argv[3])