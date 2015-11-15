import re
def get_intron_density(gtfFile):
    '''
    output: intron density, multi-exon included only
    '''
    gene_class = {}
    with open(gtfFile) as f:
        for line in f:
            items = line.split()
            key = re.sub('\;','',items[9])
            if key not in gene_class:
                gene_class[key] = {'exon': 0, 'CDS':0}
    
    with open(gtfFile) as f:
        for line in f: 
            items = line.split()
            key = re.sub('\;','',items[9])
            if 'exon' in items[2]:
                gene_class[key]['exon']+=1
            if 'CDS' in items[2]:
                gene_class[key]['CDS']+=1
    
    exon_number = sum([gene_class[key]['exon'] for key in gene_class])
    CDS_number = sum([gene_class[key]['CDS'] for key in gene_class])
    multi_exon_gene = [key for key in gene_class if gene_class[key]['exon']>1 or gene_class[key]['CDS']>1]
    return 1.*(exon_number - len(gene_class)) / len(multi_exon_gene)