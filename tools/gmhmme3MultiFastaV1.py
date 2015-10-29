from Bio import SeqIO
import subprocess
import sys

def gmhmmMultiFasta(modelFile, multiFastaFile, shortName):
    '''
    assume short name has Assembly inside
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
    for SeqRecord in SeqRecords:
        filename = '{}{}.fasta'.format(fastaPieceLocation,SeqRecord.id)
        SeqIO.write(SeqRecord, filename,'fasta')
        fastaPieceFiles.append('{}.fasta'.format(SeqRecord.id))

    
    ## perform gmhmm on each piece
    script = ''
    base_command1 = '/home/tool/gmes/gmhmme3 -m {}'.format(modelFile)
    base_command2 = 'python /home/richard/research/tools/gmhmme3_to_gtfV4.py'

    counter = 0
    for fastaPiece in fastaPieceFiles:
        counter += 1
        #gmhmm prediction
        tempName = fastaPiece[:-5]+'tmp'
        command0 = '{} {}{} -o {}{}\n'.format(base_command1, fastaPieceLocation,fastaPiece,predictionLocation,tempName)
        subprocess.check_call(command0,shell = True)
        #convert prediciton
        outputName = tempName[:-3]+'prediction.gtf'
    #     print outputName
        predictionFiles.append(outputName)

        command1 = '{} {}{} {}{}\n'.format(base_command2, predictionLocation, tempName, predictionLocation, outputName)
        subprocess.check_call(command1,shell = True)
        command2 = 'rm {}{}\n'.format(predictionLocation, tempName)
        subprocess.check_call(command2,shell = True)
        command3 = 'echo "#{} prediction of {} is done!"\n'.format(counter, fastaPiece)
        subprocess.check_call(command3,shell = True)
    
    ## consolidate predicitons
    with open(consolidatedPrediction, 'w') as f:
        for predictionFile in predictionFiles:
            with open(predictionLocation+predictionFile) as f0:
                for line in f0:
                    f.write(line)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "please provide model file, multi-fasta file and shortName"
    else:
        gmhmmMultiFasta(sys.argv[1], sys.argv[2],sys.argv[3])