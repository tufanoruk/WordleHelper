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

from email.quoprimime import quote
import encodings
from nis import match
import os
from sre_parse import State
import sys
import io
import argparse
from tracemalloc import start

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

TRLETTERS=['A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 
           'L', 'M', 'N', 'O', 'Ö', 'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z']

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

def print_usage():
    print('''Usage: wordlehelp.py <word list file> <first guess>''')

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
        
        self.words=[wrdhupper(w).rsplit()[0] for w in self.words]
        
        self.words.sort();
        
    def removeWords(self, nonexistingletters, existingletters, onspotletters):
        pass
    
    def has(self, word):
        return word in self.words
        
    def isEmpty(self):
           return len(self.words) == 0
        
    def dump(self):
        for w in self.words:
            print(w) # print adds \n to the end 

class Node():
    '''state is a State object, parent is a Node object, 
    actipn is the guesses word which takes us here'''
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
        
class Frontier():
    '''Possible sollutions for the problem'''
    def __init__(self, solution_set):
        self.solutionSet=solution_set
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)
        
    def removeNode(self):
        '''removing node shortens the solution set to make us closer to the solution'''
        if self.isEmpty(): 
            raise Exception("Empty frontier")
        else:
            node = self.nodes[-1]
            self.solutionSet.removeWords(nonexistingletters=node.state.notexist,
                                     existingletters=node.state.exist,
                                     onspotletters=node.state.match)

            return node

    def isEmpty(self):
        return len(self.nodes) == 0
        #return self.solutionSet.isEmpty()    



class State():
    '''state is the feedback provided by the wordle game given guessed word
    we take this feedback from the user here and form the state'''
    def __init__(self, guess):
        self.notexist = []
        self.exist = []
        self.match =['?','?','?','?','?']
        self.__getInput(guess)

    def __getInput(self, guess):    
        guess = wrdhupper(guess)
        print("For guessed word '"+guess+"' enter the feedback provided by the game")
        
        match = input("Letters in correct place: ")
        match = wrdhupper(match)
        if not all(letter in list(guess) for letter in list(match)):
            raise Exception("There is a wrong letter in the entry ", match)
        
        self.exist = input("Letters in wrong place  : ")
        self.exist = wrdhupper(self.exist)
        if not all(letter in list(guess) for letter in list(self.exist)):
            raise Exception("There is a wrong letter in the entry ", self.exist)

        i=0
        for letter in list(guess):
            if i<len(match) and list(match)[i] == letter:
                self.match[i] = letter 
            i = i+1
            if letter not in match + self.exist:
                self.notexist.append(letter)
        
        print("Letters not exist : ", ''.join(self.notexist))
        
    def print(self):
        print(''.join(self.match))
        
    def isGoal(self):
        return len(self.exist) == 5 and len(self.notexist) == 0 and all (letter != '?' for letter in self.match)

class  Wordle():
    def __init__(self, wordsfile, firstguess):
        solution_set = SolutionSet(wordsfile)
        self.frontier = Frontier(solution_set)
        
        guess = wrdhupper(firstguess)        
        if len(guess) != 5:
            raise Exception("Guess word must have 5 letters")
        elif not solution_set.has(guess): 
            raise Exception("Guess word does not exist in the provided word list!")
        
        self.state = State(guess)        
        
    def solve(self):
        start = Node(state=self.state, parent=None, action=None)        
        self.frontier.addNode(start)
        
        start.state.print()
        
        while True:
            if self.frontier.isEmpty():
                raise Exception("There is no solution!")
            
            node = self.frontier.removeNode()
            
            if node.state.isGoal():
                print("Solution is ", node.state.print())
                return
            
            guess = input("Guess a new word : ")
            state = State (guess)
            child = Node(state=state, parent=node, action=guess)
            self.frontier.addNode(child)

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
