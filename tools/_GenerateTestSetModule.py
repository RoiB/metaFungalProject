from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def makeTestSet(shortName, intergenic_length, sourceGtf, sourceFasta, targetGtf, targetFasta):
    '''
    execute
    '''
    #gene_locations = get_gene_locationV1(sourceGtf)
    gene_locations = get_gene_locationV1Choice2(sourceGtf)
    cutFasta(shortName,intergenic_length, gene_locations, sourceFasta, targetFasta)
    updateGtf(shortName,intergenic_length, gene_locations, sourceGtf, targetGtf)

def cutFasta(shortName,intergenic_length, gene_locations, sourceFasta, targetFasta):
    SeqRecords = list(SeqIO.parse(sourceFasta, 'fasta'))
    SeqRecordsPairs = {SeqRecord.id:SeqRecord for SeqRecord in SeqRecords}


    genes = (map(lambda ((contig,_),(a,b)): ('{}__{}__{}__{}'.format(shortName,contig,a,b), 
                                         cut_geneV1(SeqRecordsPairs[contig], a, b, intergenic_length))
                 ,gene_locations))

    genes = map(lambda (key,val): SeqRecord(val.seq, id=key, description=''), genes)
    
#     genes = (sc.parallelize(gene_locations)
#              .map(lambda ((contig,_),(a,b)): 
#                   ('{}__{}__{}__{}'.format(shortName,contig,a,b),
#                    cut_geneV1(SeqRecordsPairs[contig], a, b, intergenic_length)))
#              .map(lambda (key,val): SeqRecord(val.seq, id=key, description=''))
#              .collect())

    SeqIO.write(genes, targetFasta, "fasta")
    print 'multi-fasta file is saved at:',targetFasta

def updateGtf(shortName, intergenic_length, gene_locations, sourceGtf, targetGtf):
    shifts = calculate_shift(gene_locations,intergenic_length)
    gene_locations = {gene:(c,d)for ((a,gene),(c,d)) in gene_locations}
    with open(sourceGtf) as f:
        with open(targetGtf,'w') as f1:
            for line in f:
                alist1 = line.split()
                gene = alist1[9]
                alist2 = line.split('\t')
                alist2[0] = '{}__{}__{}__{}'.format(shortName,alist2[0],gene_locations[gene][0],gene_locations[gene][1])
                start = shifts[gene]+int(alist1[3]); stop = shifts[gene]+int(alist1[4])
                if start < 0:                         ## need to talk with Alex, some CDS with no start or stop
                    print shifts[gene]
                    print line 
                    print '\t'.join(alist2)
                    continue
                alist2[3] = str(start); alist2[4] = str(stop)
                
                f1.write('\t'.join(alist2))
            print 'updated annotation is saved at:',targetGtf

def calculate_shift(gene_locs, intergenic_length):
    '''
    helper function for 'updateGtf'
    shift value is negative if goes to the left
    '''
    shift = {}
    for ((_,gene),(a,b)) in gene_locs:
        shift[gene] = intergenic_length-int(a)+1
    return shift

# def updateGtf():

def get_gene_locationV1(inputFile):
    '''
    updated: include contig name in V1
    original helper function for 'update_annotation'
    input: annotation file
    output: tuple, (genename, range)
    '''
    pairs = {} # put start, stop location to a list associated with 
    with open(inputFile) as f:
        for line in f:
            if 'start_codon' in line or 'stop_codon' in line:
                alist = line.split()
                a,b = map(int,[alist[3], alist[4]])
                key = (alist[0],alist[9])
                if key not in pairs:
                    pairs[key] = [a,b]
                else:
                    pairs[key].append(a); pairs[key].append(b)
                    
    for key in pairs:
        pairs[key] = sorted(pairs[key])
            
    gene_locs = map(lambda (key, alist): (key, (min(alist), max(alist))), pairs.items())
#     print gene_locs
    return sorted(gene_locs, key = lambda x: x[1])
        
def get_gene_locationV1Choice2(inputFile):
    '''
    choice2: include gene with CDS out of boundary
    updated: include contig name in V1
    original helper function for 'update_annotation'
    input: annotation file
    output: tuple, (genename, range)
    '''
    pairs = {} # put start, stop location to a list associated with 
    with open(inputFile) as f:
        for line in f:
            alist = line.split()
            a,b = map(int,[alist[3], alist[4]])
            key = (alist[0],alist[9])
            if key not in pairs:
                pairs[key] = [a,b]
            else:
                pairs[key].append(a); pairs[key].append(b)
                    
    for key in pairs:
        pairs[key] = sorted(pairs[key])
        
    gene_locs = map(lambda (key, alist): (key, (min(alist), max(alist))), pairs.items())
#     print gene_locs
    return sorted(gene_locs, key = lambda x: x[1])

def cut_geneV1(seq_record, a, b, intergenic_length):
    '''
    updated: add down stream
    helper function
    input: SeqRecord; start and stop location (a,b) on annotation(index starts from 1)
    output: SeqRecord with the desired region and an intergenic region at front
    '''
    gene = seq_record[a-1:b]
    
    if a-1-intergenic_length > 0:
        intergenic_region_front = seq_record[a-1-intergenic_length:a-1]
    else:
        intergenic_region_front = seq_record[b:b+intergenic_length]
        
    if b+intergenic_length > len(seq_record):
        intergenic_region_back = seq_record[a-1-intergenic_length:a-1]
    else:
        intergenic_region_back = seq_record[b:b+intergenic_length]
        
    return intergenic_region_front+gene+intergenic_region_back