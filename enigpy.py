#!/usr/bin/env python3

#local
import cracker

#global
import itertools
import multiprocessing
from datetime import datetime

def listener(q):
    '''listens for messages on the q, writes to file. '''

    f = open("all.txt", 'a') # all that pass the limit set during exhaustion, currently at 0.04
    #b40 = open("best0040.txt", 'a') # IC > 0.04
    b45 = open("best0045.txt", 'a') # IC > 0.045
    b50 = open("best0050.txt", 'a') # IC > 0.05
    start=datetime.now()
    f.write("START: "+format(start, '%H:%M:%S')+"\n\n")
    f.flush()
    while 1:
        m = q.get()
        if m == 'kill':
            f.write("STOP: "+format(datetime.now(), '%H:%M:%S')+"\nRUN TIME: "+str(datetime.now()-start)+"\nEND\n\n\n")
            print ("STOP: "+format(datetime.now(), '%H:%M:%S')+"\nRUN TIME: "+str(datetime.now()-start))
            f.flush()
            break
        mscore = float(m.split(';')[0])
        f.write(str(m) + '\n')
        if (mscore > 0.045):
            if (mscore > 0.05):
                b50.write(str(m) + '\n')
                b50.flush()
                print ("50 EEEY")
            else:        
                b45.write(str(m) + '\n')
                b45.flush()
                print ("45 EY")
    f.close()
    #b40.close()
    b45.close()
    b50.close()


if __name__ == "__main__":

    '''
    cracker.simpleTest("WTGPLT","MUUQJZVQLORVMCOLYKXEPMCDCWGHNTQVMEHGECOEULBULBOCZPGBIXIFWCYXZKZKLYAEVCJDGXJZQKQGVXSORRQNZMATPZDOEXITXFIUVJFIZUAYLIJWVVGFYXGRDQKAGUUWBNUUOUXQQUCXKUXPTYUIIXPAYXRLTZPZQRNLOPAODDUSVFWMILZEOBVOPIPWHXVYADCORXPIIEUZVTXBRJRECTGLCPKQAJDAMI")
    cracker.hillTest("WTGPLT","MUUQJZVQLORVMCOLYKXEPMCDCWGHNTQVMEHGECOEULBULBOCZPGBIXIFWCYXZKZKLYAEVCJDGXJZQKQGVXSORRQNZMATPZDOEXITXFIUVJFIZUAYLIJWVVGFYXGRDQKAGUUWBNUUOUXQQUCXKUXPTYUIIXPAYXRLTZPZQRNLOPAODDUSVFWMILZEOBVOPIPWHXVYADCORXPIIEUZVTXBRJRECTGLCPKQAJDAMI")
    '''

    '''
    print ("test")
    scrambled="KYYUGIWKSEYPQDFYPIJNTGNDIAHNBROXDIKEKPTMOUHBEJRRJPVBAOCUZRDFSAZDCNUNNMRPCCMCHJBWSTIKZIREBBVJQAXZARIYVANIJVOLDNBUMXXFNZVRQEGOYXEVVNMPWEBSKEUTJJOKPBKLHIYWGNFFPXKIEWSNTLMDKYIDMOFPTDFJAZOHVVQETNIPVZGTUMYJCMSEAKTYELPZUNHEYFCLAADYPEEXMHQMVAVZZDOIMGLERBBLATHQJIYCBSUPVVTRADCRDDSTYIXYFEAFZYLNZZDPNNXXZJNRCWEXMTYRJOIAOEKNRXGXPNMTDGKFZDSYHMUJAPOBGANCRCZTMEPXESDZTTJZGNGQRMKNCZNAFMDAXXTJSRTAZTZKRTOXHAHTNPEVNAAVUZMHLPXLMSTWELSOBCTMBKGCJKMDPDQQGCZHMIOCGRPDJEZTYVDQGNPUKCGKFFWMNKWPSCLENWHUEYCLYVHZNKNVSCZXUXDPZBDPSYODLQRLCGHARLFMMTPOCUMOQLGJJAVXHZZVBFLXHNNEJXS" 
    scorer_tri=ngram_score('grams/german_trigrams1941.txt')
    crackerTest=cracker(scrambled,scorer_tri)
    crackerTest.testHillClimb()
    '''

    
    print("Entering the castle of Aaaaaaaaaaaaaaaaaargh")
    walzennumbers = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]  
    #jobs = []
    print ("Logical cores available %d" % multiprocessing.cpu_count())
    noteating=4
    print ("Cores NOT being eaten omnomnom %d" % noteating)
    
    manager = multiprocessing.Manager()
    q = manager.Queue()
    pool = multiprocessing.Pool(multiprocessing.cpu_count()-noteating) #use logical cores
    
    watcher = pool.apply_async(listener, (q,))

    jobs = []

    for subset in itertools.permutations(walzennumbers, 3):
        job = pool.apply_async(cracker.initial_exhaustion, (subset,q))
            #p=multiprocessing.Process(target=multi7, args=(subset,))
            #jobs.append(p)
            #p.start()
        jobs.append(job)
  
    for job in jobs: 
        job.get()
    
    q.put('kill')
    pool.close()
    pool.join()
