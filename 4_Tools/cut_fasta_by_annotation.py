from Bio import SeqIO

def filter_fasta(fastaFile, annotationFile, fastaFileFiltered, annotationFileUpdated):
    '''Wrapper function to filter multifasta file according to annotation'''
    seqRecords = read_fasta(fastaFile)
    annotation_boudary, annotation_items = read_annotation_location(annotationFile)
    # deal with fasta
    SeqRecords_filtered = filter(lambda x: x!=None, map(lambda x: cut_fasta_by_annotation(x,annotation_boudary),seqRecords))
    SeqIO.write(SeqRecords_filtered, fastaFileFiltered, "fasta")
    # deal with annotation
    items_updated = calculate_location_shift(annotation_items)
    update_annotation(items_updated,annotationFile,annotationFileUpdated)
    print "The filtered fasta file is stored at location:", fastaFileFiltered




def read_annotation_location(annotationFile):
    '''Version 0.1, cut start and stop region'''
    gene_info = {}
    with open(annotationFile) as f:
        for line in f:
            if "start_codon" in line or "stop_codon" in line:
                info = line.split()
                fasta_id = info[0]
                gene_id = info[9]
                key = (fasta_id,gene_id)
                if key not in gene_info:
                    gene_info[key] = []                
                
                gene_info[key].append(int(info[3]))
                gene_info[key].append(int(info[4]))
    for key in gene_info:
        locs = sorted(gene_info[key])
        try:
            gene_info[key] = (locs[0],locs[3])
        except:
            print 'there is a problem with: ', key
    items = gene_info.items()
    result = map(lambda x: (x[0][0],x[1]),items)
    return sorted(result), sorted(items)

def calculate_location_shift(annotation_items):
    '''
    input tuple: (key, (start,end))
    return left_shift_lengths    
    '''
    #add length need to shift left and gene length for counter prep
    items = map(lambda x: (x[0], x[1],x[1][0]-1,x[1][1]-x[1][0]+1), annotation_items)
    # calculate shift for each gene
    counter = {fasta:0 for fasta in set(map(lambda x: x[0][0],items))}

    items_updated = []
    for item in items:
        key = item[0]
        first_left_shift = item[2]
        gene_length = item[3]
        
        left_shift = first_left_shift-counter[key[0]]
        counter[key[0]] += gene_length
        items_updated.append((key,left_shift,(item[1][0]-left_shift, item[1][1]-left_shift))) #verification purpose
    return items_updated

def update_annotation(items_updated,annotationFile,annotationFileUpdated):
    '''
    take in tuple of (key, left_shift)
    output update annotationFile
    '''
    #transform tuples into dictionary
    lookup_table = {key:val for key,val,_ in items_updated}
    with open(annotationFile) as f:
        with open(annotationFileUpdated,'w') as f1:
            for line in f:
                info = line.split()
                data = line.split('\t')
                key = (info[0],info[9])
                shift_val = lookup_table[key]
                data[3] = str(int(data[3])- shift_val)
                data[4] = str(int(data[4])- shift_val)
                f1.write('\t'.join(data))

def cut_fasta_by_annotation(seqRecord, filteredAnnotation):
    '''
    20151003
    The function take in one fasta file(seq record) and all the filtered annotation
    The (multi)fasta file is cut by the CDS location of the annotation
    return seq record cut by location
    '''
    idx = seqRecord.id
    locations = filter(lambda x: x[0] == idx,filteredAnnotation)
#     print sum(map(lambda (_,(a,b)): b-a+1,locations)) #check cut accuracy; checked correct
    if len(locations) == 0:
        return None
    pieces = map(lambda (_,(start,end)): seqRecord[start-1:end],locations)
    return reduce(lambda a,b: a+b, pieces)

def read_fasta(fastaFile): return list(SeqIO.parse(fastaFile,'fasta'))

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "please provide fastaFile, annotationFile, fastaFileFiltered, annotationFileUpdated"
    else:
        filter_fasta(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4])
        