## convert JGI gff annotation to gtf format
import re
import sys
def JGIgff_to_gtf(target, output):
    '''
    format prokaryote gmhmm output to gtf that could be recognized by eval
    example line: 
    scaffold_1	JGI	exon	6287	6313	.	-	.	name "estExt_fgenesh1_pg.C_1_t10002"; transcriptId 519841
    '''
    
    converted_text = ''
    with open(target) as f:
        for line in f:
            ## need to add up with the location
            ## format need to be consistant, fasta name to help locate gene
                elems = line.split()
                converted_text+='\t'.join(elems[:8])
                converted_text+= format_gene_id_JGI_gff(elems[8:])
    with open(output,'w') as f: f.write(converted_text)
        
def format_gene_id_JGI_gff(last_col):
    '''helper function for gff to gtf'''
    name = last_col[1].split(';')[0]
    gene_id = re.sub('\#','x',name)
    return '\tgene_id {0}; transcript_id {0};\n'.format(gene_id)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "please provide both input and output file"
    else:
        JGIgff_to_gtf(sys.argv[1], sys.argv[2])