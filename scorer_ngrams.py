from collections import Counter
from math import log10

class scorer_ngrams(object):

    ngrams = {}
    L=0
    floor=0
    # careful you dumbass! it won't work with different ngram files, just one!

    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities and keep them in memory '''
        if not scorer_ngrams.ngrams:
            with open(ngramfile) as file:
                for line in file:
                    key,count = line.split(sep) 
                    scorer_ngrams.ngrams[key] = int(count)

            scorer_ngrams.L = len(key)
            self.N = sum(scorer_ngrams.ngrams.values())

            #calculate log probabilities
            for key in scorer_ngrams.ngrams.keys():
                scorer_ngrams.ngrams[key] = log10(float(scorer_ngrams.ngrams[key])/self.N)
            scorer_ngrams.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text (n-gram) '''
        score = 0
        ngrams = self.ngrams.__getitem__

        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor
        return score