from components import Plugboard, Reflector, Rotor
from crypto import Enigma
from scorer_ngrams import scorer_ngrams
from scorer_ic import scorer_ic
from datetime import datetime
from string import ascii_uppercase as pomlist
from time import time
from decimal import Decimal
import collections
#import pymongo

class cracker():
    
    def __init__(self, grundStellung, textToCrack, scorer_IC, scorer_bi, scorer_tri):
        self.grundStellung = grundStellung
        self.ttc = textToCrack
        self.scorer_IC = scorer_IC
        self.scorer_bi = scorer_bi
        self.scorer_tri = scorer_tri

    def decodeGrundStellung(self):
        #find out the starting grund stellung if we know the other parts
        enigmai = Enigma(
            rotors = {
                1: Rotor("VIII",19-1, pomlist.index(self.grundStellung[0])),  #slowest, left-most
                2: Rotor("II",7-1, pomlist.index(self.grundStellung[1])),  #middle
                3: Rotor("IV",12-1, pomlist.index(self.grundStellung[2])),  #fastest, right-most
            },
            reflector = Reflector("B"),
            plugboard = Plugboard({"B":"D","C":"O","E":"I","G":"L","J":"S","K":"T","N":"V","P":"M","Q":"R","W":"Z"})
        )
        text = enigmai.EDcrypt(self.grundStellung[3:])

        return text

    def test(self):
        #print (self.grundStellung)
        grunds = self.decodeGrundStellung()
        enigmai = Enigma(
            rotors = {
                1: Rotor("VIII",19-1, pomlist.index(grunds[0])), #slowest, left-most
                2: Rotor("II",7-1, pomlist.index(grunds[1])),    #middle
                3: Rotor("IV",12-1, pomlist.index(grunds[2])),   #fastest, right-most
            },
            reflector = Reflector("B"),
            plugboard = Plugboard({"B":"D","C":"O","E":"I","G":"L","J":"S","K":"T","N":"V","P":"M","Q":"R","W":"Z"})
        )    
        text = enigmai.EDcrypt(self.ttc)
        print ("DECRYPTED TEXT: "+text)
        print ("STECKERS: %s" % enigmai.plugboard.wiring)


    # Well, hill-climb is not easy... todo:
    # 1st run - try letter combinations of letter with highest frequency!
    # 
    # Some more thoughts:
    # Wermacht decided to use 10 out of 13 (2x13=26) possible plugs. 
    # This means that an empty plugboard already holds 6 correct letters
    # 

    def testHillClimb(self):
        #print ("testHillClimb")
        bestoftherun = -10000
        bestoftherunIC = -10000
        bestoftherunGRAM = -10000
        myscore = -10000

        steckerscoreIC = -10000
        steckerscoreGRAM = -10000
        steckerscoreAIC = -10000

        steckerinfo = []
        
        plugsIC = 4 #how many plugs we'd like to try to find in 1st run IC
        plugsGRAM = 6 #how many plugs we'd like to try to find in 2nd run trigram
        plugs3 = 0 #how many plugs we'd like to try to find in 3rd run trigram

        f = open("testHillClimb.txt", 'a')
        start = datetime.now()
        f.write("\n\nSTART: "+format(start, '%H:%M:%S')+"\n\n")
        f.flush()

        grunds = self.decodeGrundStellung()
        plugboardi = Plugboard()
        reflectori = Reflector("B")
        rotors = {
            1: Rotor("VIII",19-1, pomlist.index(grunds[0])),  #slowest, left-most
            2: Rotor("II",7-1, pomlist.index(grunds[1])),  #middle
            3: Rotor("IV",12-1, pomlist.index(grunds[2])),  #fastest, right-most
        }
        enigmai = Enigma(rotors, reflectori, plugboardi)    
        print(enigmai)
        text = enigmai.EDcrypt(self.ttc)

        myic = self.scorer_IC.score(text)
        print ("Original IC / plain text (before heuristics): "+str(myic))
        startTime = time()     
        steckerscoreIC, steckerscoreGRAM, steckerscoreAIC, steckerinfo = self.steckerHillClimbTest(rotors, reflectori, myic, plugsIC, plugsGRAM)
        print ("Execution time is: %.3fs" % (time()-startTime))
        print ("\nScores\n"+"Original IC:"+str(myic)+"\nAfterwards IC:"+str(steckerscoreAIC)+"\nTrigram:"+str(steckerscoreGRAM))
        print ("End of heuristics\n\n")

        print ("Heuristics results:")
        if ((steckerscoreIC > bestoftherunIC and steckerscoreAIC > 0.05) or (steckerscoreGRAM > bestoftherunGRAM and steckerscoreAIC > 0.06)):
                                                #print ("CHECKTHISOUT: " +text+"\n")
            bestoftherunIC = steckerscoreIC
            bestoftherunGRAM = steckerscoreGRAM
            #print ("\nScores\n"+"Original IC:"+str(steckerscoreIC)+"\nAfterwards IC:"+str(steckerscoreAIC)+"\nTrigram:"+str(steckerscoreGRAM))
            #print (str(steckerinfo))
            #print ("TEXT: " +text+"\n")

            if steckerscoreAIC > 0.065:                                         
                print ("BINGO IC!!! "+str(steckerscoreAIC))
                print ("BEST DESCRYPTED TEXT (IC METHOD): " +text+"\n")    
                print ("STECKERS:"+str(steckerinfo))

            if steckerscoreGRAM > -1500:
                print ("BINGO GRAM!!! GRAM: "+str(steckerscoreGRAM)) # Trigram score
                print ("BINGO GRAM!!! ORIC: "+str(myic))   # original IC score
                print ("BINGO GRAM!!! BEIC: "+str(steckerscoreIC))   # IC score after first 4 plugs
                print ("BINGO GRAM!!! AFIC: "+str(steckerscoreAIC)+"\n")   # IC sore after Trigrams applied
                print ("BEST DESCRYPTED TEXT (GRAM METHOD): " +text)  
                print ("STECKERS:"+str(steckerinfo))                
             
        #print (text)

    def steckerHillClimbTest(self, rotors, reflectori, score, plugsIC, plugsGRAM):
        plugboardi = Plugboard()
        
        
        # we'll try to hill-climb the first 3 most frequent letters using IC
        # mostusedletters = ["E","N","X","R"] # we will use 4 most used letters for the 1st run using IC
        frequencyAnalysis=collections.Counter(self.ttc)
        print (frequencyAnalysis)
        print (frequencyAnalysis.most_common(3))
        mostCommon3=frequencyAnalysis.most_common(3)
        input("Press Enter to continue...")


        #mostusedletters = ["E","N","X","R"] # we will use 4 most used letters for the 1st run using IC
        #mostusedletters2ndrun = list("STAHDULCGMOBWFKZVPJYQ") #2nd run for trigrams
        letters = list(pomlist)
        bestpairscoreGRAM = -10000
        topscore = score
        bestpairscoreIC = score

        best = ["",""]
        best[0] = ""
        best[1] = ""

        print('Looking up best pair out of most used letters...')
        start = time()
        #print ("Top score: "+str(topscore))
        for i in range(plugsIC):  #find the first best pair out of most used letters
            #print (i)
            for firstletter,value in mostCommon3:
                for secondletter in letters: #check every combination of the most used letters one by one
                    if secondletter != firstletter:
                        plugboardtestpairs = {firstletter:secondletter}
                        print (firstletter)
                        plugboardtestdict = dict(plugboardtestpairs, **plugboardi.wiring)
                        plugboardtest = Plugboard(plugboardtestdict)
                        #print (plugboardtest.wiring)
                        enigmai = Enigma(rotors, reflectori, plugboardtest)    
                        text = enigmai.EDcrypt(self.ttc)
                        myscore = self.scorer_IC.score(text)
                        #print (myscore)
                        if myscore > bestpairscoreIC:
                            bestpairscoreIC = myscore
                            best = [firstletter, secondletter]
                            #print ("Best one: "+str(bestpairscore)+" "+firstletter+secondletter)
            #print ("letas:"+str(letters))
            #print ("most:"+str(mostusedletters))
            #print (best[0])
            #print (best[1])
            if best[0] in letters:
                letters.remove(best[0])

            if best[1] in letters:
                letters.remove(best[1])

            if best[0] in mostCommon3:
                mostCommon3.remove(best[0])
           
            plugboardi.wiring[best[0]] = best[1]
            
            best[0] = ""
            best[1] = ""
            
            #print ((plugboardi.wiring))

        print('Finished in %.2f seconds.' % (time() - start))

        if not plugboardi:
                return bestpairscoreIC, bestpairscoreGRAM, dict(plugboardi.wiring)

        if bestpairscoreIC > score:
            # if we found something, we continue to hill-climb

            print('Continuing to hillclimb...')
            start = time()

            enigmai = Enigma(rotors, reflectori, plugboardi)  # initial trigram score
            text = enigmai.EDcrypt(self.ttc)
            bestpairscoreGRAM = Decimal(self.scorer_bi.score(text))

            for i in range(plugsGRAM):
                for firstletter in letters:
                    for secondletter in letters: #check every combination of the most used letters one by one
                        if secondletter != firstletter:
                            plugboardtestpairs = {firstletter:secondletter}
                            plugboardtestdict = dict(plugboardtestpairs, **plugboardi.wiring)
                            plugboardtest = Plugboard(plugboardtestdict)
                            #print (plugboardtest.wiring)
                            enigmai = Enigma(rotors, reflectori, plugboardtest)    
                            text = enigmai.EDcrypt(self.ttc)
                            myscore = Decimal(self.scorer_bi.score(text))
                            if myscore > bestpairscoreGRAM:
                                bestpairscoreGRAM = myscore
                                best = [firstletter, secondletter]

            if best[0] in letters:
                letters.remove(best[0])

            if best[1] in letters:
                letters.remove(best[1])

            #if best[0] in mostusedletters2ndrun:
            #    mostusedletters2ndrun.remove(best[0])
           
            plugboardi.wiring[best[0]] = best[1]
            
            best[0] = ""
            best[1] = ""

        #print ((plugboardi.wiring))

        # IC calculation after the 2nd step of hill climb
        enigmai = Enigma(rotors, reflectori, plugboardi)    
        text = enigmai.EDcrypt(self.ttc)
        afterwardsIC = self.scorer_IC.score(text)

        return bestpairscoreIC, bestpairscoreGRAM, afterwardsIC, dict(plugboardi.wiring)


#cracker suitable for parallel computation
class crackerParallel():

    #there are two possible methods to do brute force + hill-climbing. Each comprises of several steps

    # Method #1:
    # 1st step: brute force all combinations: reflectors (2) + walzen order (60 [5] or 336 [8]) + ring positions (26^3) + fastest grund (26) using Index of Coincidence (IC). 
    # Combinations: 54 837 120 (5 rotors) or 307 087 872 (8 rotors)
    # Save the data for later hill-climb
    # Optional 2nd step: brute force fastest (3rd) and middle (2nd) ring settings (26^2) using best IC.
    # Combinations: 676
    # 3rd step: Hill-climb first 3 steckers using IC,
    # Combinations: 150 738 274 937 250 [26!/(6!*10!*2^10)] = not feasible to brute force.
    # 4th step: Hill-climb next steckers using bigrams and then trigrams (possibly quadgrams).
    # Combinations: 150 738 274 937 250 [26!/(6!*10!*2^10)] = not feasible to brute force.
    #
    # Steckers (when X steckers are connected):
    # Plain = % of Plaintext 
    # Mono  = % of Monoalphabetic substition
    # Mist  = % of Mist/Garble
    #
    # X     Plain   Mono    Mist
    # 0  :  10.1    18.5    71.4 <--- 71.4% is mist, can't use trigrams. Use IC on Mono part
    # 1  :  13.3    22.4    64.3
    # 2  :  17.8    25.0    57.2
    # 3  :  23.6    26.4    50.0
    # 4  :  30.6    26.5    42.9 <--- mist clears up significantly, can now use trigrams
    # 5  :  39.0    25.3    35.7
    # 6  :  48.6    22.8    28.6
    # 7  :  59.6    19.0    21.4
    # 8  :  71.7    14.0    14.3
    # 9  :  85.2     7.7     7.1
    # 10 : 100.0     0.0     0.0
    #
    #
    # Method #2 (much slower due to 1st step):
    # 1st step: brute force reflectors (2) + walzen order (60) + positions (26^3) + fastest (3rd) ring (26) using IC.
    # Combinations: 54 837 120
    # 2nd step: Hill-climb first few (~3-4) steckers using monograms. 
    # Combinations: 3 453 450 - 164 038 875
    # 3rd step: Hill-climb next few (~3-4) steckers using bigrams. 
    # Combinations: 3 453 450 - 164 038 875
    # 4th step: Hill-climb last few (~2-3) steckers using trigrams. 
    # Combinations: 44 850 -  3 453 450
    #
    # Method #3 
    # 1st step: precompute all possible combinations 27 418 560 (54 837 120 with 2 types of reflector)
    # 2nd step: Hill-climb using same technique as in method #1
    #
    # Index of Coincidence (IC):
    # Random text, that is where all letters are present with nearly the same frequency, will have an IC 
    # ‘score’ of 1/26 or 0.03846. If we measure the IC score of plain Enigma text it can be up to around 
    # 0.05 to 0.07, depending on the actual frequencies of the letters in the plain message.
    # German IC = 0.0762 German WWII IC = 0.061
    #

        
    def __init__(self, textToCrack, subset, q):
        self.ttc = textToCrack
        self.subset = subset
        self.q = q

    def steckerHillClimbTest(self, rotors, reflectori, score, plugsIC, plugsGRAM):
        plugboardi = Plugboard({})

        # we'll try to hill-climb just the most used pairs
        mostusedletters = ["E","N","X","R"] # we will use 4 most used letters for the 1st run using IC
        mostusedletters2ndrun = list("STAHDULCGMOBWFKZVPJYQ") #2nd run for trigrams
        letters = list(pomlist)
        bestpairscoreGRAM = -10000
        topscore = score
        bestpairscoreIC = score

        best = ["",""]
        best[0] = ""
        best[1] = ""

        #print ("Top score: "+str(topscore))
        for i in range(plugsIC):  #find the first best pair out of most used letters
            #print (i)
            for firstletter in mostusedletters:
                for secondletter in letters: #check every combination of the most used letters one by one
                    if secondletter != firstletter:
                        #plugboardtest = dict(plugboardi.wiring)
                        plugboardtestpairs = {firstletter:secondletter}
                        plugboardtestdict = dict(plugboardtestpairs, **plugboardi.wiring)
                        plugboardtest = Plugboard(plugboardtestdict)
                        #print (plugboardtest.wiring)
                        enigmai = Enigma(rotors, reflectori, plugboardtest)    
                        text = enigmai.EDcrypt(self.ttc)
                        myscore = self.scorer.icscore(text)
                        #print (myscore)
                        if myscore > bestpairscoreIC:
                            bestpairscoreIC = myscore
                            best = [firstletter, secondletter]
                            #print ("Best one: "+str(bestpairscore)+" "+firstletter+secondletter)
            #print ("letas:"+str(letters))
            #print ("most:"+str(mostusedletters))
            #print (best[0])
            #print (best[1])
            if best[0] in letters:
                letters.remove(best[0])

            if best[1] in letters:
                letters.remove(best[1])

            if best[0] in mostusedletters:
                mostusedletters.remove(best[0])
           
            plugboardi.wiring[best[0]] = best[1]
            
            best[0] = ""
            best[1] = ""
            
            #print ((plugboardi.wiring))

        if not plugboardi:
                return bestpairscoreIC, bestpairscoreGRAM, dict(plugboardi.wiring)

        if plugsGRAM > 0:
            # if we found something, we continue to hill-climb

            enigmai = Enigma(rotors, reflectori, plugboardi)  # initial trigram score
            text = enigmai.EDcrypt(self.ttc)
            bestpairscoreGRAM = self.scorer.score(text)
            #print (bestpairscoreGRAM)

            for i in range(plugsGRAM):
                for firstletter in mostusedletters2ndrun:
                    for secondletter in letters: #check every combination of the most used letters one by one
                        if secondletter != firstletter:
                            plugboardtestpairs = {firstletter:secondletter}
                            plugboardtestdict = dict(plugboardtestpairs, **plugboardi.wiring)
                            plugboardtest = Plugboard(plugboardtestdict)
                            #print (plugboardtest.wiring)
                            enigmai = Enigma(rotors, reflectori, plugboardtest)    
                            text = enigmai.EDcrypt(self.ttc)
                            myscore = self.scorer.score(text)
                            #print (myscore)
                            if myscore > bestpairscoreGRAM:
                                bestpairscoreGRAM = myscore
                                best = [firstletter, secondletter]

            if best[0] in letters:
                letters.remove(best[0])

            if best[1] in letters:
                letters.remove(best[1])

            if best[0] in mostusedletters2ndrun:
                mostusedletters2ndrun.remove(best[0])
           
            plugboardi.wiring[best[0]] = best[1]
            
            best[0] = ""
            best[1] = ""

        #print ((plugboardi.wiring))

        # IC calculation after the 2nd step of hill climb
        enigmai = Enigma(rotors, reflectori, plugboardi)    
        text = enigmai.EDcrypt(self.ttc)
        afterwardsIC = self.scorer.icscore(text)

        return bestpairscoreIC, bestpairscoreGRAM, afterwardsIC, dict(plugboardi.wiring)

    def ultimate_MP_method_1_INITIAL_EXHAUSTION_FAST(self): 
        #1st step is to find out the plausible walzen and ring settings candidates for next steps using IC

        scorer = scorer_ic()

        #strtowrite = "!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ self.subset[0]+"-"+self.subset[1]+"-"+ self.subset[2]
        #self.q.put(strtowrite)
        print ("!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ self.subset[0]+"-"+self.subset[1]+"-"+ self.subset[2])
        messagelenght = len(self.ttc)

        bestoftherunIC = -10000
        bestoftherunGRAM = -10000
        myscore = -10000
        botrstring = ""
        myic=0
        topIC=0

        # initliaze empty enigma for further re-use
        enigmai = Enigma()

        cunt=0
        olmajtytajm=0

        for r in range(2):
            #reflectors B and C
            enigmai.reflector = Reflector("B" if r == 0 else "C")

            for i in range(26):
                for j in range(26):
                    for k in range(26):
                        firstIC=0
                        #start = time()
                        rotors = {
                            # i,j,k = rings
                            # l = fastest grund / offset
                            1: Rotor(self.subset[0], i, 0),  #slowest, left-most
                            2: Rotor(self.subset[1], j, 0),  #middle
                            3: Rotor(self.subset[2], k, 0),  #fastest, right-most
                        }
                        enigmai.rotors = rotors
                        text = enigmai.EDcrypt(self.ttc)
                        firstIC=scorer.score(text,messagelenght)
                        
                        topIC=firstIC
                        #test Grunds for fast and middle wheels
                        for l in range(26):
                            rotors = {
                                # i,j,k = rings
                                # l = fastest grund / offset
                                1: Rotor(self.subset[0], i, 0),  #slowest, left-most
                                2: Rotor(self.subset[1], j, 0),  #middle
                                3: Rotor(self.subset[2], k, l),  #fastest, right-most
                            }
                            enigmai.rotors = rotors
                            #print(enigmai)

                            text = enigmai.EDcrypt(self.ttc)
                            secondIC = scorer.score(text,messagelenght)
                            if secondIC>topIC:
                                topIC=secondIC
                                topGrundFast=l


                        if (topIC>firstIC):
                            strtowrite = str(topIC)+";"+rotors[1].number+";"+rotors[2].number+";"+rotors[3].number+";"+str(r)+";"+str(i)+";"+str(j)+";"+str(k)+";"+str(topGrundFast)
                            self.q.put(strtowrite)
                        else:
                            strtowrite = str(firstIC)+";"+rotors[1].number+";"+rotors[2].number+";"+rotors[3].number+";"+str(r)+";"+str(i)+";"+str(j)+";"+str(k)+";0"
                            self.q.put(strtowrite)
                                    

    def ultimate_MP_method_1_INITIAL_EXHAUSTION_EXTENDED_SLOOOW(self): 
            #1st step is to find out the plausible walzen and ring settings candidates for next steps using IC

            scorer = scorer_ic()

            #strtowrite = "!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ self.subset[0]+"-"+self.subset[1]+"-"+ self.subset[2]
            #self.q.put(strtowrite)
            print ("!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ self.subset[0]+"-"+self.subset[1]+"-"+ self.subset[2])
            messagelenght = len(self.ttc)

            bestoftherunIC = -10000
            bestoftherunGRAM = -10000
            myscore = -10000
            botrstring = ""
            myic=0
            topIC=0

            # initliaze empty enigma for further re-use
            enigmai = Enigma()

            cunt=0
            olmajtytajm=0

            for r in range(2):
                #reflectors B and C
                enigmai.reflector = Reflector("B" if r == 0 else "C")

                for i in range(26):
                    for j in range(26):
                        for k in range(26):
                            firstIC=0
                            #start = time()
                            rotors = {
                                # i,j,k = rings
                                # l = fastest grund / offset
                                1: Rotor(self.subset[0], i, 0),  #slowest, left-most
                                2: Rotor(self.subset[1], j, 0),  #middle
                                3: Rotor(self.subset[2], k, 0),  #fastest, right-most
                            }
                            enigmai.rotors = rotors
                            text = enigmai.EDcrypt(self.ttc)
                            firstIC=scorer.score(text,messagelenght)
                            
                            topIC=firstIC
                            #test Grunds for fast and middle wheels
                            for l in range(26):
                                for m in range(26):
                                    rotors = {
                                        # i,j,k = rings
                                        # l = fastest grund / offset
                                        1: Rotor(self.subset[0], i, 0),  #slowest, left-most
                                        2: Rotor(self.subset[1], j, l),  #middle
                                        3: Rotor(self.subset[2], k, m),  #fastest, right-most
                                    }
                                    enigmai.rotors = rotors
                                    #print(enigmai)

                                    text = enigmai.EDcrypt(self.ttc)
                                    secondIC = scorer.score(text,messagelenght)
                                    if secondIC>topIC:
                                        topIC=secondIC
                                        topGrundFast=m
                                        topGrundMiddle=l


                            if (topIC>firstIC):
                                strtowrite = str(topIC)+";"+rotors[1].number+";"+rotors[2].number+";"+rotors[3].number+";"+str(r)+";"+str(i)+";"+str(j)+";"+str(k)+";"+str(topGrundMiddle)+";"+str(topGrundFast)
                                self.q.put(strtowrite)
                            else:
                                strtowrite = str(firstIC)+";"+rotors[1].number+";"+rotors[2].number+";"+rotors[3].number+";"+str(r)+";"+str(i)+";"+str(j)+";"+str(k)+";0"
                                self.q.put(strtowrite)
                                        
                            '''
                            olmajtytajm+=time() - start
                            cunt+=1
                            print ("Finished in average of %.4f seconds." % (olmajtytajm/cunt))
                            '''


    def ultimate_MP_method_1_GRUND_EXHAUSTION(self): 
            # 2nd step is to find out the plausible grund settings as candidates for Hill Climbing

            scorer = scorer_ic()
            
            candidate = self.subset.split(';')
            #print (candidate[0])
            
            #strtowrite = "!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ self.subset[0]+"-"+self.subset[1]+"-"+ self.subset[2]
            #self.q.put(strtowrite)
            print ("!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ candidate[0]+"-"+candidate[1]+"-"+ candidate[2]+"-"+candidate[3])
            messagelenght = len(self.ttc)

            myIC=0
            topIC=float(candidate[0])

            # initliaze empty enigma for further re-use
            enigmai = Enigma()

            enigmai.reflector = Reflector("B" if int(candidate[4]) == 0 else "C")

            for i in range(26):
                for j in range(26):
                    for k in range(26):
                        #start = time()
                        rotors = {
                            # i,j,k = rings
                            # l = fastest grund / offset
                            1: Rotor(candidate[1], int(candidate[5]), i),  #slowest, left-most
                            2: Rotor(candidate[2], int(candidate[6]), j),  #middle
                            3: Rotor(candidate[3], int(candidate[7]), k),  #fastest, right-most
                        }
                        enigmai.rotors = rotors
                        text = enigmai.EDcrypt(self.ttc)
                        myIC=scorer.score(text,messagelenght)
                        #print (myIC)
                        if myIC>topIC:
                            topIC=myIC
                            topGrundSlow=i
                            topGrundMiddle=j
                            topGrundFast=k
                            topText=text
                            print (topText)


            if (myIC>topIC):
                strtowrite = str(candidate[0])+";"+str(topIC)+";"+rotors[1].number+";"+rotors[2].number+";"+rotors[3].number+";"+str(topGrundSlow)+";"+str(topGrundMiddle)+";"+str(topGrundFast)+"\n"+text+"\n"
                self.q.put(strtowrite)
            else:
                strtowrite = str(candidate[0])+" FOUND NUTHIN'!"
                self.q.put(strtowrite)

    def ultimate_MP_method_1_HILLCLIMB(self): 
        #1st step is to find out the plausible walzen and ring settings candidates for next steps using IC
        strtowrite = "!!! Starting at " +format(datetime.now(), '%H:%M:%S')+ " with: "+ self.subset[0]+"-"+self.subset[1]+"-"+ self.subset[2]     
        self.q.put(strtowrite)
        messagelenght = len(self.ttc)
        ic = 0 #threshold, everything less than this won't be even evaluated further
        topic = ic

        scorer_bi = scorer_ngrams('grams/german_bigrams1941.txt')
        scorer_tri = scorer_ngrams('grams/german_trigrams1941.txt')
        scorer_quad = scorer_ngrams('grams/german_trigrams1941.txt')

        plugs1run = 4               #number of plugs to be indentified by IC
        plugs2run = 10-plugs1run    #rest of the plugs, identified by trigram score

        plugboardi = Plugboard()
        bestoftherunIC = -10000
        bestoftherunGRAM = -10000
        myscore = -10000
        botrstring = ""

        #-1725 bi1941 #-2900 tri #-4300 quad
        steckertop = -2900

        for r in range(2):
            reflectori = Reflector("B" if r == 0 else "C")
            for i in range(26):
                for j in range(26):
                    for k in range(26):
                        rotors = {
                            1: Rotor(self.subset[0], 0,i),  #slowest, left-most
                            2: Rotor(self.subset[1], 0,j),  #middle
                            3: Rotor(self.subset[2], 0,k),  #fastest, right-most
                        }
                        enigmai = Enigma(rotors, reflectori, plugboardi)    
                        text = enigmai.EDcrypt(self.ttc)
                        myic = self.scorer.icscore(text)
                        #myscore = self.scorer_mono.score(text) #in case we'd need monograms (but we don't at this moment)
                        
                        if myic > ic:
                            topic = myic
                            '''
                            strtowrite = ""+format(datetime.now(), '%H:%M:%S')\
                            +"\n 1st step Score\n"+str(myic)+"\nGuess: "+text\
                            +"\nGrunds original: "+str(i)+":"+str(j)+":"+str(k)\
                            +" Ring3: "+str("0")+" Wheels: "\
                            +rotor1.number+":"+rotor2.number+":"+rotor3.number\
                            +" Ref:"+str(reflectori.typ)+"\n"
                            self.q.put(strtowrite)
                            '''
                            
                            #2nd step is to test right-most and middle rotor combinations for the best scored ones
                            for x in range(26):
                                for y in range(26):
                                        #r3shift = 0+y
                                        #r2shift = 0
                                        #if rotor2.step>=r3shift:
                                        #    r2shift = 1

                                        #rotor1 = rotor(self.subset[0], 0,i)
                                        #rotor2 = rotor(self.subset[1], x,(abs(j-r2shift-x)%26))
                                        #rotor3 = rotor(self.subset[2], y,((k+r3shift)%26))
                                        rotors = {
                                            1: Rotor(self.subset[0], 0,i),
                                            2: Rotor(self.subset[1], x,j),
                                            3: Rotor(self.subset[2], y,k),
                                        }
                                        enigmai = Enigma(rotors, reflectori, plugboardi)
                                        text = enigmai.EDcrypt(self.ttc)

                                        myic = self.scorer.icscore(text)

                                        #3rd step is Hill-climbing steckers using trigrams
                                        if myic > topic and myic > 0.040:
                                            topic = myic

                                            '''
                                            strtowrite = ""+format(datetime.now(), '%H:%M:%S')\
                                            +"\n2nd step Score\n"+str(myic)+"\nGuess: "+text\
                                            +"\nGrunds original: "+str(i)+":"+str(j)+":"+str(k)\
                                            +" Ring2: "+str(x)+ " Ring3: "+str(y)+" Wheels: "\
                                            +rotor1.number+":"+rotor2.number+":"+rotor3.number\
                                            +" Ref:"+str(reflectori.typ)+"\n"
                                            self.q.put(strtowrite)
                                            '''
                                            #bestoftherunIC = topscore #nope
                                            #stecker
                                           
                                            '''strtowrite = ""+format(datetime.now(), '%H:%M:%S')
                                            +"\nORIGINAL Score\n"+str(myscore)+"\nGuess: "
                                            +text+"\nGrunds original: "+str(i)+":"+str(j)+":"+str(k)
                                            +" Grunds new: "+str(i)+":"
                                            +str(abs(j-r2shift)%26)+":"+str((k+r3shift)%26)
                                            +" Ring3: "+str(o)
                                            +" Wheels: "+rotor1.number+":"+rotor2.number+":"+rotor3.number
                                            +" Ref:"+str(reflectori.typ)+"\n"
                                            #self.q.put(strtowrite)
                                            '''
                                            #myscore = self.scorer.score(text)
                                            steckerscoreIC, steckerscoreGRAM, steckerscoreAIC, steckerinfo = self.steckerHillClimbTest(rotor1,
                                                                                           rotor2,
                                                                                           rotor3,
                                                                                           reflectori,
                                                                                           myic, plugs1run, plugs2run)

                                            #strtowrite = "STECKER: "+str(steckerinfo)+"\n\n"
                                            #self.q.put(strtowrite)
                                            if ((steckerscoreIC > bestoftherunIC and steckerscoreAIC > 0.055) or (steckerscoreGRAM > bestoftherunGRAM and steckerscoreAIC > 0.055)):
                                                #print ("CHECKTHISOUT: " +text+"\n")
                                                bestoftherunIC = steckerscoreIC
                                                bestoftherunGRAM = steckerscoreGRAM
                                                strtowrite = "Time "\
                                                +format(datetime.now(), '%H:%M:%S')\
                                                +"\nORIGINAL Score\n"+str(myic)\
                                                +"\nScores\n"+"Original IC:"+str(steckerscoreIC)+"\nAfterwards IC:"+str(steckerscoreAIC)+"\nTrigram:"+str(steckerscoreGRAM)\
                                                +"\nGuess: "+text+"\nGrunds original: "\
                                                +str(i)+":"+str(j)+":"+str(k)+" Grunds new: "\
                                                +"Ring2: "+str(x)+" Ring3: "+str(y)\
                                                +" Wheels: "+rotor1.number+":"+rotor2.number+":"+rotor3.number\
                                                +" Ref:"+str(reflectori.typ)+"\n"\
                                                +"STECKER: "+str(steckerinfo)+"\n\n"
                                                self.q.put(strtowrite)

                                            if steckerscoreAIC > 0.06:                                         
                                                print ("BINGO IC!!! "+str(steckerscoreAIC))
                                                print ("CHECKTHISOUT: " +text+"\n")

                                            if steckerscoreGRAM > -2900:
                                                print ("CHECKTHISOUT: " +text+"\n")
                                                print ("BINGO GRAM!!! GRAM:"+str(steckerscoreGRAM)) # Trigram score
                                                print ("BINGO GRAM!!! ORIC:"+str(myic))   # original IC score
                                                print ("BINGO GRAM!!! BEIC:"+str(steckerscoreIC))   # IC score after first 3 plugs

                                                print ("BINGO GRAM!!! AFIC:"+str(steckerscoreAIC)+"\n\n")   # IC sore after Trigrams applied
                                            #stecker

        if bestoftherunIC > -10000:
            strtowrite = "BOTR: "+str(bestoftherunIC)+"\n"+str(botrstring)
        strtowrite = ""
        self.q.put(strtowrite)

def initial_exhaustion(subset, q):
    scrambled = "KYYUGIWKSEYPQDFYPIJNTGNDIAHNBROXDIKEKPTMOUHBEJRRJPVBAOCUZRDFSAZDCNUNNMRPCCMCHJBWSTIKZIREBBVJQAXZARIYVANIJVOLDNBUMXXFNZVRQEGOYXEVVNMPWEBSKEUTJJOKPBKLHIYWGNFFPXKIEWSNTLMDKYIDMOFPTDFJAZOHVVQETNIPVZGTUMYJCMSEAKTYELPZUNHEYFCLAADYPEEXMHQMVAVZZDOIMGLERBBLATHQJIYCBSUPVVTRADCRDDSTYIXYFEAFZYLNZZDPNNXXZJNRCWEXMTYRJOIAOEKNRXGXPNMTDGKFZDSYHMUJAPOBGANCRCZTMEPXESDZTTJZGNGQRMKNCZNAFMDAXXTJSRTAZTZKRTOXHAHTNPEVNAAVUZMHLPXLMSTWELSOBCTMBKGCJKMDPDQQGCZHMIOCGRPDJEZTYVDQGNPUKCGKFFWMNKWPSCLENWHUEYCLYVHZNKNVSCZXUXDPZBDPSYODLQRLCGHARLFMMTPOCUMOQLGJJAVXHZZVBFLXHNNEJXS" 
    crackerF = crackerParallel(scrambled, subset, q)
    crackerF.ultimate_MP_method_1_INITIAL_EXHAUSTION_FAST()

def initial_exhaustion_grunds(subset, q):
    scrambled = "KYYUGIWKSEYPQDFYPIJNTGNDIAHNBROXDIKEKPTMOUHBEJRRJPVBAOCUZRDFSAZDCNUNNMRPCCMCHJBWSTIKZIREBBVJQAXZARIYVANIJVOLDNBUMXXFNZVRQEGOYXEVVNMPWEBSKEUTJJOKPBKLHIYWGNFFPXKIEWSNTLMDKYIDMOFPTDFJAZOHVVQETNIPVZGTUMYJCMSEAKTYELPZUNHEYFCLAADYPEEXMHQMVAVZZDOIMGLERBBLATHQJIYCBSUPVVTRADCRDDSTYIXYFEAFZYLNZZDPNNXXZJNRCWEXMTYRJOIAOEKNRXGXPNMTDGKFZDSYHMUJAPOBGANCRCZTMEPXESDZTTJZGNGQRMKNCZNAFMDAXXTJSRTAZTZKRTOXHAHTNPEVNAAVUZMHLPXLMSTWELSOBCTMBKGCJKMDPDQQGCZHMIOCGRPDJEZTYVDQGNPUKCGKFFWMNKWPSCLENWHUEYCLYVHZNKNVSCZXUXDPZBDPSYODLQRLCGHARLFMMTPOCUMOQLGJJAVXHZZVBFLXHNNEJXS" 
    crackerF = crackerParallel(scrambled, subset, q)
    crackerF.ultimate_MP_method_1_GRUND_EXHAUSTION()

def final(subset, q):
    #insert the scrambled text 547 char long
    scrambled = "KYYUGIWKSEYPQDFYPIJNTGNDIAHNBROXDIKEKPTMOUHBEJRRJPVBAOCUZRDFSAZDCNUNNMRPCCMCHJBWSTIKZIREBBVJQAXZARIYVANIJVOLDNBUMXXFNZVRQEGOYXEVVNMPWEBSKEUTJJOKPBKLHIYWGNFFPXKIEWSNTLMDKYIDMOFPTDFJAZOHVVQETNIPVZGTUMYJCMSEAKTYELPZUNHEYFCLAADYPEEXMHQMVAVZZDOIMGLERBBLATHQJIYCBSUPVVTRADCRDDSTYIXYFEAFZYLNZZDPNNXXZJNRCWEXMTYRJOIAOEKNRXGXPNMTDGKFZDSYHMUJAPOBGANCRCZTMEPXESDZTTJZGNGQRMKNCZNAFMDAXXTJSRTAZTZKRTOXHAHTNPEVNAAVUZMHLPXLMSTWELSOBCTMBKGCJKMDPDQQGCZHMIOCGRPDJEZTYVDQGNPUKCGKFFWMNKWPSCLENWHUEYCLYVHZNKNVSCZXUXDPZBDPSYODLQRLCGHARLFMMTPOCUMOQLGJJAVXHZZVBFLXHNNEJXS" 
    #scorer_mono = scorer_ngrams('grams/german_monograms.txt')

    #scorer_quad = scorer_ngrams('grams/german_quadgrams.txt')
    scorer = scorer_tri

    crackerF = crackerParallel(scrambled, subset, q)
    crackerF.ultimate_MP_method_1_HILLCLIMB()

def simpleTest(grundstellung, scrambledtext):
   
    print ("---------- simple test - Right decryption: ----------------")

    scorer_IC = scorer_ic()
    scorer_bi = scorer_ngrams('grams/german_bigrams1941.txt')
    scorer_tri = scorer_ngrams('grams/german_trigrams1941.txt')
    crackerTest = cracker(grundstellung, scrambledtext, scorer_IC, scorer_bi, scorer_tri)
    crackerTest.test()
    print ("-----------------------------------------------------------")
    print ("")

def hillTest(grundstellung, scrambledtext):
    print ("-------- hill test - work in progress heuristics: ---------")
    #scrambled = "KYYUGIWKSEYPQDFYPIJNTGNDIAHNBROXDIKEKPTMOUHBEJRRJPVBAOCUZRDFSAZDCNUNNMRPCCMCHJBWSTIKZIREBBVJQAXZARIYVANIJVOLDNBUMXXFNZVRQEGOYXEVVNMPWEBSKEUTJJOKPBKLHIYWGNFFPXKIEWSNTLMDKYIDMOFPTDFJAZOHVVQETNIPVZGTUMYJCMSEAKTYELPZUNHEYFCLAADYPEEXMHQMVAVZZDOIMGLERBBLATHQJIYCBSUPVVTRADCRDDSTYIXYFEAFZYLNZZDPNNXXZJNRCWEXMTYRJOIAOEKNRXGXPNMTDGKFZDSYHMUJAPOBGANCRCZTMEPXESDZTTJZGNGQRMKNCZNAFMDAXXTJSRTAZTZKRTOXHAHTNPEVNAAVUZMHLPXLMSTWELSOBCTMBKGCJKMDPDQQGCZHMIOCGRPDJEZTYVDQGNPUKCGKFFWMNKWPSCLENWHUEYCLYVHZNKNVSCZXUXDPZBDPSYODLQRLCGHARLFMMTPOCUMOQLGJJAVXHZZVBFLXHNNEJXS" 
    scorer_IC = scorer_ic()
    scorer_bi = scorer_ngrams('grams/german_bigrams1941.txt')
    scorer_tri = scorer_ngrams('grams/german_trigrams1941.txt')
    crackerTest = cracker(grundstellung, scrambledtext, scorer_IC, scorer_bi, scorer_tri)
    crackerTest.testHillClimb()
    print ("-----------------------------------------------------------")

