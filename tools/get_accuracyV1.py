import pandas as pd
import sys
import os

'''
updated with table sorted by short name
'''
def accuracy_vec(filename):
    '''
    input: filename with file path
    output: accuracy vector (internal exon Sn, internal exon Sp, nucleotide Sn, nucleotide Sp)
    '''
    counter = 0
    flag = False
    with open(filename) as f:
        for line in f:
            if 'Nucleotide Sensitivity' in line:
                nuc_sn = float(line.split('Nucleotide Sensitivity')[1].split('%')[0])
            if 'Nucleotide Specificity' in line:
                nuc_sp = float(line.split('Nucleotide Specificity')[1].split('%')[0])

            if 'Internal' in line:
                counter += 1
                if counter == 3:
                    flag = True
                    counter = 100 #to ignore comming 'Internals'
            if flag:
                if 'Correct Specificity' in line:
                    internal_exon_sp = float(line.split('Correct Specificity')[1].split('%')[0])

                if 'Correct Sensitivity' in line:
                    internal_exon_sn = float(line.split('Correct Sensitivity')[1].split('%')[0])
                    flag = False
        return (internal_exon_sn, internal_exon_sp, nuc_sn, nuc_sp)
    
def get_accuracy(source):
    filenames = os.listdir(source)
    df = (pd.DataFrame(map(lambda x: accuracy_vec(source+"/"+x), filenames), 
                   index= map(lambda x: x.split('.eval')[0],filenames), 
                   columns=['Internal_Exon_Sn','Internal_Exon_Sp','Nucleotide_Sn', 'Nucleotide_Sp']))
    return df

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "please provide source folder adn output file"
    else:
        table = get_accuracy(sys.argv[1])
        order = sorted(list(table.index))
        table.ix[order].to_csv(sys.argv[2])
        print 'table file is saved at {}'.format(sys.argv[2])