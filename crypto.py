from string import ascii_uppercase as pomlist
from json import dumps as json_dumps

class Enigma:
    mapping = {c: ord(c) - 65 for c in pomlist}

    def __init__(self, rotors: dict=None, reflector=None, plugboard=None):
        self.rotors = rotors  # create a new copy of rotors dict
        self.reflector = reflector
        self.plugboard = plugboard
        # self.mapping = dict((c, ord(c) - 65) for c in pomlist)

    def __str__(self):
        rotors = ''
        for i, rotor in self.rotors.items():
            rotors += '%d. %s\n' % (i, rotor)
        sep = '#' * 85
        return '%s\nEnigma:\n%s\n%s\n\n%s\n%s' % (sep, rotors, self.reflector, self.plugboard, sep)

    def setRotors (self, rotors: dict):
        self.rotors = dict(rotors)

    def setReflector (self, reflector):
        self.reflector = reflector

    def setPlugboard (self, plugboard):
        self.plugboard = plugboard
            
    def EDcrypt(self, text):
        r1pos = self.rotors[1].grund
        r2pos = self.rotors[2].grund
        r3pos = self.rotors[3].grund
        scrambled = ""
        
        for letter in text:
            onecipher = ""
            enc = 0
            r3pos += 1

            stepagain1 = False # 2 notches on VI VII VIII --- moving slowest rotor
            stepagain2 = False # 2 notches on VI VII VIII --- moving middle rotor
            
            # doublestepagain2 = False # magic

            if self.rotors[3].step == 13 and r3pos == 26: 
                stepagain2 = True

            if self.rotors[2].step == 13 and r2pos + 1 == 26: 
                stepagain1 = True 
            
            if r3pos == self.rotors[3].step or stepagain2 == True or r2pos + 1 == self.rotors[2].step or stepagain1 == True: # or (double stepping of middle rotor)
                r2pos += 1
                #print("stepping middle")

                if (self.rotors[2].step == 13 and r2pos == 26):
                  stepagain1 = True

                if (r2pos == self.rotors[2].step or stepagain1 == True):
                    #print("stepping slow")
                    r1pos += 1
                    stepagain1 = False
         
            if r3pos > 25:
                r3pos = 0
            
            if r2pos > 25:
                r2pos = 0
                
            if r1pos > 25:
                r1pos = 0
    
            onecipher = letter
            
            if onecipher in self.plugboard.wiring:
                onecipher = self.plugboard.wiring.get(onecipher)

            onecipher = self.rotors[3].wiring[((pomlist.index(onecipher) + r3pos) % 26)]
            onecipher = pomlist[pomlist.index(onecipher)] #out - rotor3.ring  offset ringstellung
            onecipher = self.rotors[2].wiring[((self.mapping.get(onecipher)-r3pos + r2pos) % 26)]
            onecipher = self.rotors[1].wiring[((self.mapping.get(onecipher)-r2pos + r1pos) % 26)]
            onecipher = self.reflector.setting[((self.mapping.get(onecipher)-r1pos) % 26)]
            onecipher = pomlist[((pomlist.index(onecipher) + r1pos) % 26)]
            onecipher = pomlist[((self.rotors[1].wiring.index(onecipher)) % 26)]
            onecipher = pomlist[((pomlist.index(onecipher) + r2pos-r1pos) % 26)]
            onecipher = pomlist[((self.rotors[2].wiring.index(onecipher)) % 26)]             
            onecipher = pomlist[((pomlist.index(onecipher) + r3pos-r2pos) % 26)]
            onecipher = pomlist[pomlist.index(onecipher)] 
            onecipher = pomlist[self.rotors[3].wiring.index(onecipher)]
            onecipher = pomlist[((pomlist.index(onecipher)-r3pos) % 26)]


            if onecipher in self.plugboard.wiring:
                onecipher = self.plugboard.wiring.get(onecipher)
            scrambled += onecipher

        return scrambled
