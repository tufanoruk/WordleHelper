#!/usr/bin/env python3
''' wordlehlep.py:  Helps to solve Wordle puzzle'''

__author__ = "Tufan Oruk"
__copyright__ = "Creative Commons"
__license__ = "Creative Commons Attribution 4.0 International"
__credits__ = ["Brin Yu", "Can Nuhlar"]
__email__ = "tufan.oruk@gmail.com"

'''To discover solution frontier a file containing list of 5 letter words needs to be provided. 
You provide your initial guess as the initial state to the program and enter the feedback provided by the game.  
"state" is letters not-exist, exist and fully matched.

Say the word selected by the game is "TUFAN"
Your first guess is "BRAIN" thus game provied 
    B,R,I letters are not exist, 
    A exist but not in corrrect place
    N is a match  
    
You provide this result as follows

% python3 wordlehelp.py <five letter word list file> BRAIN
Letters in correct place: N
Letters in wrong place  : A
(
    program figures out B,R and I do not exist in the word.
    and provides a list of 5 letter words to select from,
    and asks for your next guess
) 
Letters not exist       : BRI  
Possible words;
..........
Enter your next guess   : WOMAN
Letters in correct place: AN
Letters in wrong place  : 
(
    program figures out W,O and M do not exist in the word.
    and provides a list of 5 letter words to select from
    and asks for your next guess
) 
Letters not exist       : WOM  
Possible words;
..........
Enter your next guess   :...
...
'''

import encodings
import os
from sre_parse import State
import sys
import io
import argparse

''' Here I used an (AI) search algorithm
    Start w/ a frontier that contains initial state
    Start w/ an empty explored set
    Repeat:
        - frontier empty => no solution
        - remove a node from frontier
        - node has "goal state" => solution (~done)
        - add the node to the explored set
        - expand node, add adjacent  nodes to frontier if they aren't already in the frontier OR the explored set
        
    Thanks to 
    Brin Yu (edX CS50AI) for algorithm template and 
    Can Nuhlar for Turkish words (https://github.com/CanNuhlar/Turkce-Kelime-Listesi)  
'''


''' To pass "the Turkey Test" İIiı upper lower conversions must be provided
'''
TRLOWERMAP={
    ord(u'I'): u'ı',
    ord(u'İ'): u'i',
}

TRUPPERMAP={
    ord(u'ı'): u'I',
    ord(u'i'): u'İ',            
}

def wrdhupper(str):
    return str.translate(TRUPPERMAP).upper()

def wrdhlower(str):
    return str.translate(TRLOWERMAP).lower()


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        

class Frontier():
    def __init__(self):
        self.frontier=[]

    def addNode(self, node):
        self.frontier.append(node)
        
    def removeNode(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def isEmpty(self):
        return len(self.frontier) == 0    

    def containsState(self, state):
        return any(node.state == state for node in self.frontier)


class SolutionSet():
    '''5 letter words'''
    def __init__(self, wordsfile):

        self.trlowermap={
            ord(u'I'): u'ı',
            ord(u'İ'): u'i',
        }
        self.truppermap={
            ord(u'ı'): u'I',
            ord(u'i'): u'İ',            
        }

        self.words=[]
        with open(file=wordsfile, mode='r', encoding='utf8') as fd:
            self.words = fd.readlines()
            
        #self.words=[w.translate(self.truppermap).rsplit()[0].upper() for w in self.words]
        
        self.words=[wrdhupper(w).rsplit()[0] for w in self.words]
        
        self.words.sort();
        
    def removeWords(self, nonexistingletters, existingletters, onspotletters):
        pass
    
    def has(self, word):
        return word in self.words
        
    def dump(self):
        for w in self.words:
            print(w) # print adds \n to the end 

class  Wordle():
    def __init__(self, wordlsfile, firstguess):
        
        self.solutionSet = SolutionSet(wordlsfile)        
        guess = wrdhupper(firstguess)        
        if len(guess) != 5:
            raise Exception("Guess word must have 5 letters")
        elif not self.solutionSet.has(guess): 
            raise Exception("Guess word does not exist in the provided word list!")
        
        self.node = Node(state=guess, parent=None, action=None)

    def solve(self):
        pass

def print_usage():
    print('''Usage: wordlehelp.py <word list file> <first guess>''')

def main():
    if len(sys.argv) != 3:
        print_usage();
        exit();
        
    wrdl = Wordle(sys.argv[1], sys.argv[2])
    
    wrdl.solve()
    
        
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        instance = sys.exc_info()
        print("ERROR. Terminating!" + str(instance))
