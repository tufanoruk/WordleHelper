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

import re
import sys

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

ANYLETTER='.'

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
        self.words=[]
        with open(file=wordsfile, mode='r', encoding='utf8') as fd:
            self.words = fd.readlines()
        
        self.words=[wrdhupper(w).rsplit()[0] for w in self.words]
        self.words.sort();
        self.words = list(set(self.words))
        
    def removeWords(self, nonexistingletters, existingletters, onspotletters):
        '''remove words that contains nonexistinfletters and existing letters fron solution set'''
        print("Number of words ",len(self.words))
    
        exp = ''.join(onspotletters)
        p = re.compile(exp)
        self.words[:] = [w for w in self.words if p.search(w)]            
        print("Number of words after selecting of words w/ matching' "+exp+"' is ", len(self.words))
        #print(self.words)
        
        exp=''
        if len(nonexistingletters) > 0:
            exp = ''.join(nonexistingletters)
            p = re.compile('['+exp+']')
            self.words[:] = [w for w in self.words if not p.search(w)]            
        print("Number of words after removal of words containing' "+exp+"' is ", len(self.words))
        #print(self.words)
        
        exp=''
        if len(existingletters) > 0:
            exp = ''.join(existingletters)
            p = re.compile('['+exp+']')
            self.words[:] = [w for w in self.words if p.search(w)]            
        print("Number of words after selecting of words containing' "+exp+"' is ", len(self.words))
        #print(self.words)
        self.words.sort()
        
        
    def has(self, word):
        return word in self.words
        
    def isEmpty(self):
           return len(self.words) == 0
        
    def dump(self):
        for w in self.words:
            print(w, end=",") # print adds \n to the end 

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
                                     existingletters=node.state.misalligned,
                                     onspotletters=node.state.onspot)

            return node

    def isEmpty(self):
        return len(self.nodes) == 0


class State():
    '''state is the feedback provided by the wordle game given guessed word
    we take this feedback from the user here and form the state'''
    def __init__(self, guess):
        self.notexist = []
        self.misalligned = []
        self.onspot =[ANYLETTER, ANYLETTER, ANYLETTER, ANYLETTER, ANYLETTER]
        self.__getInput(guess)

    def __getInput(self, guess):    
        guess = wrdhupper(guess)
        print("For guessed word '"+guess+"' enter the feedback provided by the game")
        
        match = input("Letters in correct place: ")
        match = wrdhupper(match)
        if not all(letter in list(guess) for letter in list(match)):
            raise Exception("There is a wrong letter in the entry ", match)
        
        self.misalligned = input("Letters in wrong place  : ")
        self.misalligned = wrdhupper(self.misalligned)
        if not all(letter in list(guess) for letter in list(self.misalligned)):
            raise Exception("There is a wrong letter in the entry ", self.misalligned)

        for matchedletter in list(match):
            i=0
            for letter in list(guess):
                if matchedletter==letter:
                    self.onspot[i] = letter 
                    break
                i=i+1                    

        for letter in list(guess):
            if letter not in match + self.misalligned:
                self.notexist.append(letter)
        
        print("Letters not exist : ", ''.join(self.notexist))
        
    def print(self):
        print(''.join(self.onspot))
        
    def isGoal(self):
        '''there souldn't be any misalligned and nonexisting letters and have a full match'''
        return len(self.misalligned) == 0 and len(self.notexist) == 0 and all (letter != 'ANYLETTER' for letter in self.onspot)

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
                print("Solution is ", end="")
                node.state.print()
                return

            self.frontier.solutionSet.dump()
            print("")
            while True:        
                guess = input("Guess a new word : ")
                if (not self.frontier.solutionSet.has(wrdhupper(guess))):
                    print("This guess is not in the solution set!")
                else:
                    break
            
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
