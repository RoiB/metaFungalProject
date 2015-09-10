class ESModel():
    """Take in 4th run of model file as text and extract info"""
    def __init__(self, filename):
        self.f = open(filename)
    
    def maxSpacerPosition(self):
        '''
        return the position with the highest probability
        '''
        spacerData = []
        switch = False
        for line in self.f:
            if switch:
                spacerData.append(line)
            if "$BP_ACC_DISTR" in line:
                switch = True
            if "40\t" in line:
                switch = False
                break

        spacerData = map(lambda line: line.rstrip().split("\t"), spacerData)
        spacerDistr = map(lambda (a,b): float(b), spacerData)
        positionProb = np.array(spacerDistr)
        # print positionProb
        return range(2,41)[positionProb.argmax()]
    
    def maxSingleExonPosition(self, length = 9999):
        '''
        return the position with the highest probability
        location range from 300 to 9999
        '''
        exonData = []
        switch = False
        for line in self.f:
            if switch:
                exonData.append(line)
            if "$SINGLE_DISTR" in line:
                switch = True
            if switch and "{}\t".format(length) in line:
                switch = False
                break
        exonData = map(lambda line: line.rstrip().split("\t"), exonData)
        exonDistr = map(lambda (a,b): float(b), exonData)
        positionProb = np.array(exonDistr)
        # print positionProb
        try:
            return range(300,10000)[positionProb.argmax()]
        except:
            return 'NA'        

    def maxInitialExonPosition(self, length = 10000):
        '''
        return the position with the highest probability
        range from 3 to 10000
        '''
        exonData = []
        switch = False
        for line in self.f:
            if switch:
                exonData.append(line)
            if "$INITIAL_DISTR" in line:
                switch = True
            if switch and "{}\t".format(length) in line:
                switch = False
                break
        exonData = map(lambda line: line.rstrip().split("\t"), exonData)
        exonDistr = map(lambda (a,b): float(b), exonData)
        positionProb = np.array(exonDistr)
        # print positionProb
        try:
            return range(3,10001)[positionProb.argmax()]
        except:
            return 'NA'     
        
    def maxExonPosition(self, length = 10000):
        '''
        return the position with the highest probability
        '''
        exonData = []
        switch = False
        for line in self.f:
            if switch:
                exonData.append(line)
            if "$EXON_DISTR" in line:
                switch = True
            if switch and "{}\t".format(length) in line:
                switch = False
                break
        exonData = map(lambda line: line.rstrip().split("\t"), exonData)
        exonDistr = map(lambda (a,b): float(b), exonData)
        positionProb = np.array(exonDistr)
        # print positionProb
        try:
            return range(3,10001)[positionProb.argmax()]
        except:
            return 'NA'    
        
    def maxTerminalExonPosition(self, length = 10000):
        '''
        return the position with the highest probability
        '''
        exonData = []
        switch = False
        for line in self.f:
            if switch:
                exonData.append(line)
            if "$TERMINAL_DISTR" in line:
                switch = True
            if switch and "{}\t".format(length) in line:
                switch = False
                break
        exonData = map(lambda line: line.rstrip().split("\t"), exonData)
        exonDistr = map(lambda (a,b): float(b), exonData)
        positionProb = np.array(exonDistr)
        # print positionProb
        try:
            return range(3,10001)[positionProb.argmax()]
        except:
            return 'NA'             

    def maxIntronPosition(self, length = 3000):
            '''
            return the position with the highest probability
            '''
            intronData = []
            switch = False
            for line in self.f:
                if switch:
                    intronData.append(line)
                if "$INTRON_DISTR" in line:
                    switch = True
                if switch and "{}\t".format(length) in line:
                    switch = False
                    break

            intronData = map(lambda line: line.rstrip().split("\t"), intronData)
            intronDistr = map(lambda (a,b): float(b), intronData)
            positionProb = np.array(intronDistr)
            # print positionProb
            try:
                return range(20,3001)[positionProb.argmax()]
            except:
                return 'NA'

    def maxDonorToBpIntronPosition(self, length = 3000):
            '''
            return the position with the highest probability
            '''
            intronData = []
            switch = False
            for line in self.f:
                if switch:
                    intronData.append(line)
                if "$DON_BP_DISTR" in line:
                    switch = True
                if switch and "{}\t".format(length) in line:
                    switch = False
                    break

            intronData = map(lambda line: line.rstrip().split("\t"), intronData)
            intronDistr = map(lambda (a,b): float(b), intronData)
            positionProb = np.array(intronDistr)
            # print positionProb
            try:
                return range(5,3001)[positionProb.argmax()]
            except:
                return 'NA'
    def close(self):
        self.f.close()