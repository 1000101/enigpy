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

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("VI",0, 12),
            2: components.Rotor("VII",0, 0),
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

def test_enigmaCase5():
    print('\nRunning test case 5')

    # Reflector B
    # Plugboard Empty
    # Slowest rotor grund forced to pass Z
    # Rotors with double step and single step mixed

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("VI",0, 16),
            2: components.Rotor("VII",0, 0),
            3: components.Rotor("VIII",0, 0),
        },
        reflector = components.Reflector("B"),
        plugboard = components.Plugboard({})
    )

    test_input = open('tests/testCases5.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, output_line = line.split('\n')
        assert testNigma.EDcrypt(input_line) == output_line
    
    print('Done!')

def test_enigmaCase6():
    print('\nRunning test case 6')

    # Reflector B
    # Plugboard Empty

    testNigma = crypto.Enigma(
        rotors = {
            1: components.Rotor("VI",12, 16),
            2: components.Rotor("VI",12, 16),
            3: components.Rotor("II",12, 16),
        },
        reflector = components.Reflector("B"),
        plugboard = components.Plugboard({})
    )

    test_input = open('tests/testCases6.txt', 'r').read().split('\n\n')
    
    for line in test_input:
        input_line, output_line = line.split('\n')
        assert testNigma.EDcrypt(input_line) == output_line
    
    print('Done!')