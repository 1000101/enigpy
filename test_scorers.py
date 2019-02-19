#!/usr/bin/env python3

import scorer_ic
import scorer_ngrams

def test_Case_IC():
    print('\nRunning IC test')
    

    # IC

    icscorer = scorer_ic.scorer_ic()
    test_input = open('tests/test_Case_IC.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, score_line = line.split('\n')
        print (icscorer.score(input_line,len(input_line)))
        assert round(icscorer.score(input_line,len(input_line)),5) == float(score_line)
    
    print('Done!')
    
'''
    def test_Case_IC():
    print('\nRunning bigram test')
    

    # IC

    icscorer = scorer_ic.scorer_ic()
    test_input = open('tests/test_Case_BI.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, score_line = line.split('\n')
        print (icscorer.score(input_line,len(input_line)))
        assert round(icscorer.score(input_line,len(input_line)),5) == float(score_line)
    
    print('Done!')
'''