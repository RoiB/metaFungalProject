import sys
'''
updated to change contig name
'''
## need to articulate the code
seqname = "chromosome_1"
source = "GeneMark"
score ='.'

def get_pos(pos, shift): return str(int(pos)+shift)

def change_plus_single(temp,result, strand):

    number = temp[0]
    start = temp[4]; 
    stop = temp[5]
#     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    
    ## add start
    start1 = "\t".join([seqname, source, "start_codon", start, get_pos(start, 2), ".", strand, frame])
    result += start1+"\t"+part2+"\n"
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", start, get_pos(stop,-3), ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    ## add stop region
    stop1 = "\t".join([seqname, source, "stop_codon", get_pos(stop,-2), stop, ".", strand, frame])
    result+= stop1+"\t"+part2+"\n"
#     print result
    return result

def change_minus_single(temp,result, strand):

    number = temp[0]
    stop = temp[4]; 
    start = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    
    ## add start
    start1 = "\t".join([seqname, source, "start_codon", get_pos(start, -2), start, ".", strand, frame])
    result += start1+"\t"+part2+"\n"
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", get_pos(stop,3), start, ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    ## add stop region
    stop1 = "\t".join([seqname, source, "stop_codon", stop,get_pos(stop,+2),  ".", strand, frame])
    result+= stop1+"\t"+part2+"\n"
#     print result
    return result

def change_plus_terminal(temp,result, strand):
    number = temp[0]
    start = temp[4]; 
    stop = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", start, get_pos(stop,-3), ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    ## add stop region
    stop1 = "\t".join([seqname, source, "stop_codon", get_pos(stop,-2), stop, ".", strand, frame])
    result+= stop1+"\t"+part2+"\n"
    return result

def change_minus_terminal(temp,result, strand):
    number = temp[0]
    stop = temp[4]; 
    start = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", get_pos(stop,3),start, ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    ## add stop region
    stop1 = "\t".join([seqname, source, "stop_codon", stop, get_pos(stop,2), ".", strand, frame])
    result+= stop1+"\t"+part2+"\n"
    return result

def change_plus_initial(temp,result, strand):
    number = temp[0]
    start = temp[4]; 
    stop = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    
    ## add start
    start1 = "\t".join([seqname, source, "start_codon", start, get_pos(start, 2), ".", strand, frame])
    result += start1+"\t"+part2+"\n"
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", start, stop, ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    return result

def change_minus_initial(temp,result, strand):
    number = temp[0]
    stop = temp[4]; 
    start = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    
    ## add start
    start1 = "\t".join([seqname, source, "start_codon", get_pos(start, -2), start, ".", strand, frame])
    result += start1+"\t"+part2+"\n"
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", stop, start, ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    return result

def add_plus_internal(temp,result, strand):

    number = temp[0]
    start = temp[4]; 
    stop = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", start, stop, ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    
    return result

def add_minus_internal(temp,result, strand):

    number = temp[0]
    start = temp[4]; 
    stop = temp[5]
    #     frame = str(int(temp[7])-1)
    frame = '.'
    
    part2 = 'gene_id "{}"; transcript_id "{}";'.format("x"+number,"x"+number+".a")
    ## add CDS region
    part1 = "\t".join([seqname, source, "CDS", start, stop, ".", strand, frame])
    result+= part1+"\t"+part2+"\n"
    
    return result


import sys

def convert(filename1, output_path1):
    source = "GeneMark"
    score ='.'

    inside = False
    result1 = ""
    with open(filename1) as handle:
        container = []
        for line in handle:
            temp = line.split()

            if len(temp)==11:

                strand = temp[2]
                

                if strand == '+':
                    if temp[3] == "Single":
                        result1 = change_plus_single(temp,result1, strand)

                    elif temp[3] == "Internal":
                        result1 = add_plus_internal(temp,result1, strand)

                    elif temp[3] == "Initial":
                        result1 = change_plus_initial(temp,result1, strand)

                    elif temp[3] == "Terminal":
                        result1 = change_plus_terminal(temp,result1, strand)

                else: # strand is negative
                    container.append(temp)
        strand = "-"
        while len(container)!=0:
            temp = container.pop()
            if temp[3] == "Single":
                result1 = change_minus_single(temp,result1, strand)
            elif temp[3] == "Internal":
                result1 = add_minus_internal(temp,result1, strand)
            elif temp[3] == "Initial":
                result1 = change_minus_initial(temp,result1, strand)
            elif temp[3] == "Terminal":
                result1 = change_minus_terminal(temp,result1, strand)


    with open(output_path1,'w') as handle: handle.write(result1)
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "please provide both gmhmme3 prediction file, output file"
    else:
        with open(sys.argv[1]) as f:
            for line in f:
                if 'FASTA defline' in line:
                    seqname = line.split('>')[-1].rstrip()
                    break
        convert(sys.argv[1], sys.argv[2])