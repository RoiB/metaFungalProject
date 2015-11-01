from Bio import SeqIO
import sys
def pickFastaByNumber(fastaFile, gtfFile, targetFasta, targetGtf, number):
    SeqRecords = list(SeqIO.parse(fastaFile,'fasta'))[:number]
    SeqIO.write(SeqRecords, targetFasta, 'fasta')

    contigs = set(map(lambda x: x.id, SeqRecords[:number]))
    with open(targetGtf,'w') as f:
        with open(gtfFile) as f0:
            for line in f0:
                contig = line.split()[0]
                if contig in contigs:
                    f.write(line) 
if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "please provide fastaFile, gtfFile, targetFasta, targetGtf, filterLength"
    else:
        pickFastaByNumber(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]))