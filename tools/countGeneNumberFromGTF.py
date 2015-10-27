import sys
def countGeneNumber(inputFile):
    'count number of genes from annotation'
    result = set()
    with open(inputFile) as f:
        for line in f:
            elems = line.split()
            result.add(elems[9])
    print 'gene number:',len(result)
    return len(result)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "please provide inputFile"
    else:
        countGeneNumber(sys.argv[1])