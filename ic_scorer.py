from collections import Counter

class ic_score(object):

    def __init__(self):
        pass

    def score(self,text):
        icscore=0

        temp=Counter(text)
        
        for key,value in temp.items():
            icscore+=value*(value-1)
  
        icscore=icscore/((len(text))*(len(text)-1))

        return icscore
