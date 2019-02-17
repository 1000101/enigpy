#!/usr/bin/env python3

import crypto
import components

def test_enigmaCase1():
    print('\nRunning test case 1')

    # Reflector B
    # Plugboard Empty

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("I",0, 0),
            2: components.Rotor("II",0, 0),
            3: components.Rotor("III",0, 0),
        },
        reflector = components.Reflector("B"),
        plugboard = components.Plugboard({})
    )

    test_input = open('tests/testCases1.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, output_line = line.split('\n')
        assert testNigma.EDcrypt(input_line) == output_line
    
    print('Done!')

def test_enigmaCase2():
    print('\nRunning test case 2')

    # Reflector B
    # Plugboard Empty
    # Slowest rotor grund forced to pass Z

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("I",0, 12),
            2: components.Rotor("II",0, 0),
            3: components.Rotor("III",0, 0),
        },
        reflector = components.Reflector("B"),
        plugboard = components.Plugboard({})
    )

    test_input = open('tests/testCases2.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, output_line = line.split('\n')
        assert testNigma.EDcrypt(input_line) == output_line
    
    print('Done!')

def test_enigmaCase3():
    print('\nRunning test case 3')

    # Reflector B
    # Plugboard Empty
    # Slowest rotor grund forced to pass Z
    # Rotors with double step

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("VI",0, 0),
            2: components.Rotor("VII",0, 0),
            3: components.Rotor("VIII",0, 0),
        },
        reflector = components.Reflector("B"),
        plugboard = components.Plugboard({})
    )

    test_input = open('tests/testCases3.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, output_line = line.split('\n')
        assert testNigma.EDcrypt(input_line) == output_line
    
    print('Done!')

def test_enigmaCase4():
    print('\nRunning test case 4')

    # Reflector B
    # Plugboard Empty
    # Slowest rotor grund forced to pass Z
    # Rotors with double step and single step mixed

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("VI",0, 12),
            2: components.Rotor("II",0, 0),
            3: components.Rotor("VIII",0, 0),
        },
        reflector = components.Reflector("B"),
        plugboard = components.Plugboard({})
    )

    test_input = open('tests/testCases4.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, output_line = line.split('\n')
        assert testNigma.EDcrypt(input_line) == output_line
    
    print('Done!')

'''
def test_enigmaCase3(self):
    testNigma = Enigma(
        rotors = {
            1: Rotor("VIII",19-1, 0),
            2: Rotor("II",7-1, 0),
            3: Rotor("IV",12-1, 0),
        },
        reflector = Reflector("B"),
        plugboard = Plugboard({"B":"D","C":"O","E":"I","G":"L","J":"S","K":"T","N":"V","P":"M","Q":"R","W":"Z"})
    )
    self.assertEqual(testNigma.EDcrypt(""), "")

def test_enigmaCase4(self):
    testNigma = Enigma(
        rotors = {
            1: Rotor("VIII",19-1, 0),
            2: Rotor("II",7-1, 0),
            3: Rotor("IV",12-1, 0),
        },
        reflector = Reflector("B"),
        plugboard = Plugboard({"B":"D","C":"O","E":"I","G":"L","J":"S","K":"T","N":"V","P":"M","Q":"R","W":"Z"})
    )
    self.assertEqual(testNigma.EDcrypt(""), "")
'''

'''
import unittest

class Test_TestEnigma(unittest.TestCase):
    def test_enigmaCase1(self):
        testNigma = Enigma(
            rotors = {
                1: Rotor("VIII",19-1, 0),
                2: Rotor("II",7-1, 0),
                3: Rotor("IV",12-1, 0),
            },
            reflector = Reflector("B"),
            plugboard = Plugboard({"B":"D","C":"O","E":"I","G":"L","J":"S","K":"T","N":"V","P":"M","Q":"R","W":"Z"})
        )
        self.assertEqual(testNigma.EDcrypt(""), "")

    def test_enigmaCase2(self):
        self.assertEqual(inc_dec.increment(3), "")

if __name__ == '__main__':
    unittest.main()
'''
