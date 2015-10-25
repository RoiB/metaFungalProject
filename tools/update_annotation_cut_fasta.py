import sys

from Bio import SeqIO
from operator import add

def cut_gene(seq_record, a, b, intergenic_length):
    '''
    helper function
    input: SeqRecord; start and stop location (a,b) on annotation(index starts from 1)
    output: SeqRecord with the desired region and an intergenic region at front
    '''
    gene = seq_record[a-1:b]
    
    if a-1-intergenic_length > 0:
        intergenic_region_front = seq_record[a-1-intergenic_length:a-1]
    else:
        intergenic_region_front = seq_record[b:b+intergenic_length]
        
    return intergenic_region_front+gene

def cut_genes(seq_record, gene_location, intergenic_length):
    '''
    seq_record should be a single genome
    batch cut
    '''
    gene_location = [atuple for (key, atuple) in gene_location]
    genes = map(lambda (a,b): cut_gene(seq_record, a, b, intergenic_length), gene_location)
    return reduce(add, genes)+genes[0][:intergenic_length]

def cut_single_fasta(fastaFile, fastaFileCut, gene_location, intergenic_length):
    fasta = SeqIO.parse(fastaFile,'fasta')
    seq_record = list(fasta)[0]
    
    seq_record_cut = cut_genes(seq_record, gene_location, intergenic_length)
    SeqIO.write(seq_record_cut, fastaFileCut, 'fasta')
    print 'The cut fasta file is saved at', fastaFileCut


def get_gene_location(inputFile):
    '''
    helper function for 'update_annotation'
    input: annotation file
    output: tuple, (genename, range)
    '''
    pairs = {} # put start, stop location to a list associated with 
    with open(inputFile) as f:
        for line in f:
            if 'start_codon' in line or 'stop_codon' in line:
                alist = line.split()
                a,b = map(int,[alist[3], alist[4]])
                key = alist[9]
                if key not in pairs:
                    pairs[key] = [a,b]
                else:
                    pairs[key].append(a); pairs[key].append(b)
                    
    for key in pairs:
        pairs[key] = sorted(pairs[key])
        
    gene_locs = map(lambda (key, alist): (key, (min(alist), max(alist))), pairs.items())
    return sorted(gene_locs, key = lambda x: x[1])

def rearrange_location(gene_locs, intergenic_length):
    '''
    helper function for 'update_annotation'
    '''
    acc = 0
    shift = {}
    for pairs in gene_locs:
        acc += intergenic_length
        key,[a,b] = pairs
        shift[key] = acc-a+1
        gene_length = b-a+1
        acc+=gene_length
    return shift


def update_annotation(inputFile, outputFile, gene_locs, intergenic_length):
    shift = rearrange_location(gene_locs, intergenic_length)
    
    with open(inputFile) as f:
        with open(outputFile,'w') as f1:
            for line in f:
                alist1 = line.split()
                key = alist1[9]
                alist2 = line.split('\t')
                start = shift[key]+int(alist1[3]); stop = shift[key]+int(alist1[4])
                if start < 0: continue
                alist2[3] = str(start); alist2[4] = str(stop)
                f1.write('\t'.join(alist2))
    print 'The updated annotation file is saved at:',outputFile
    
    
def update_annotation_cut_fasta(intergenic_length, inputFile, outputFile, fastaFile, fastaFileCut):
    gene_locs = get_gene_location(inputFile)
    
    update_annotation(inputFile, outputFile, gene_locs, intergenic_length)
    
    cut_single_fasta(fastaFile, fastaFileCut, gene_locs, intergenic_length)
    
    
if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "please provide intergenic_length, inputFile, outputFile, fastaFile, fastaFileCut"
    else:
        update_annotation_cut_fasta(int(sys.argv[1]), sys.argv[2],sys.argv[3], sys.argv[4], sys.argv[5])