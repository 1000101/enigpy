from collections import Counter

class ic_score(object):

    def __init__(self):
        pass

    def score(self,text,messagelenght):
        icscore=0

        temp=Counter(text)
        
        for key,value in temp.items():
            icscore+=value*(value-1)
  
        icscore=icscore/(messagelenght*(messagelenght-1))

        return icscore
