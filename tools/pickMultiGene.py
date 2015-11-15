## version 1 add modified key ##
import sys
import re
def filter_out_single_gene(inputFile,outputFile):
    '''
    Filter out single gene and keep multi-fasta gene from gtf annotation
    '''
    gene_counter = {}
    annotation_container = {}
    with open(inputFile) as f:
        for line in f:
            elems = line.split()
            key = re.sub('\;','',elems[9])
            gene_counter[key] = [0,0] #[exon number, CDS number]
            annotation_container[key] = []
            
    with open(inputFile) as f:
        for line in f:
            elems = line.split()
            key = re.sub('\;','',elems[9])
            annotation_container[key].append(line)
            if 'exon' in elems[2]:
                gene_counter[key][0] += 1
            if 'CDS' in elems[2]:
                gene_counter[key][1] += 1

    with open(outputFile,'w') as f1:
        for key in gene_counter:
            if gene_counter[key][0] > 1 or gene_counter[key][1] > 1:
                for line in annotation_container[key]:
                    f1.write(line)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "please provide both input and output file"
    else:
        filter_out_single_gene(sys.argv[1], sys.argv[2])