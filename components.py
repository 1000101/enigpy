from json import dumps as json_dumps

class Rotor:
    options = {
                     #ABCDEFGHIJKLMNOPQRSTUVWXYZ
            "I"    : "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
            "II"   : "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "III"  : "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "IV"   : "ESOVPZJAYQUIRHXLNFTGKDCMWB",
            "V"    : "VZBRGITYUPSDNHLXAWMJQOFECK",
            "VI"   : "JPGVOUMFYQBENHZRDKASXLICTW",
            "VII"  : "NZJHGRCXMYSWBOUFAIVLPEKQDT",
            "VIII" : "FKQHTLXOCBJSPDZRAMEWNIUYGV"
            }
    
    stepoptions = {
                     #12345678901234567890123456
                     #ABCDEFGHIJKLMNOPQRSTUVWXYZ
            "I"    : 17, #Q
            "II"   : 5, #E
            "III"  : 22, #V
            "IV"   : 10, #J
            "V"    : 26, #Z
            "VI"   : 13, #Z+M 13+26
            "VII"  : 13, #Z+M 13+26
            "VIII" : 13  #Z+M 13+26
            }

    def __init__(self, walzen, ringstellung, grundstellung):
        self.number = walzen
        self.ring = ringstellung
        self.grund = grundstellung 
        self.step = self.stepoptions.get(walzen,"")
        self.wiring = self.options.get(walzen,"")
        self.wiring = self.setWiring()
        
    def setWiring(self):
        if self.ring > 0:
            pomlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            pom = ""
            index = 0
            #put wires in the right spot
            pom += self.wiring[-self.ring:]
            pom += self.wiring[:26-self.ring]
            self.wiring = pom
            pom = ""
            #adjust the letter + self.ring
            for letter in self.wiring:         
                
                pom += pomlist[(pomlist.index(letter)+self.ring)%26]

                index += 1
                
            #print ("new wiring %s" % pom)
        else:
            pom = self.wiring
            #print ("old wiring %s" % pom)
        return pom

    def __repr__(self):
        return 'Rotor %s, ring: %s, grund: %s, step: %s, wiring: %s' % (self.number, self.ring, self.grund, self.step, json_dumps(self.wiring, indent=4, sort_keys=True))
        
class Reflector:
    options = {
                  #ABCDEFGHIJKLMNOPQRSTUVWXYZ
            "B" : "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            "Bt": "ENKQAUYWJICOPBLMDXZVFTHRGS",
            "C" : "FVPJIAOYEDRZXWGCTKUQSBNMHL",
            "Ct": "RDOBJNTKVEHMLFCWZAXGYIPSUQ"
            }

    def __init__(self, umkehrwalze):
        if umkehrwalze not in self.options:
            raise ValueError('"%s" is not a valid reflector type! Possible options are: [%s]' % (umkehrwalze, ', '.join(self.options)))
        self.typ = umkehrwalze
        self.setting = self.options[umkehrwalze]

    def __repr__(self):
        return 'Reflector %s: %s' % (self.typ, self.setting)
        
class Plugboard:
    def __init__(self, steckerbrett: dict = None):
        if not steckerbrett:
            steckerbrett = {}
        self.wiring = self.setWiring(steckerbrett)
    
    def setWiring(self, steckerbrett: dict):
        wiring = {}
        for key,value in steckerbrett.items():
            wiring[key]=value
            wiring[value]=key
        return wiring

    def __repr__(self):
        return 'Plugboard: %s' % json_dumps(self.wiring, indent=4, sort_keys=True)

