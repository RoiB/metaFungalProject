import sys

def filter_annotation(annotationFile,outputFile,keyword):
    with open(annotationFile) as f:
        with open(outputFile,'w') as f1:
            for line in f:
                if keyword in line:
                    f1.write(line)
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "please provide both input and output file"
    else:
        print 'input:', sys.argv[1]
        print 'output:', sys.argv[2]
        print 'keyword', sys.argv[3]
        filter_annotation(sys.argv[1], sys.argv[2],sys.argv[3])
