#!/usr/bin/env python3
''' wordlehlep.py:  Helps to solve Wordle puzzle'''

__author__ = "Tufan Oruk"
__copyright__ = "Creative Commons"
__license__ = "Creative Commons Attribution 4.0 International"
__credits__ = ["Brin Yu", "Can Nuhlar"]
__email__ = "tufan.oruk@gmail.com"

''' Thanks to 
    Brin Yu (edX CS50AI) for algorithm template and 
    Can Nuhlar for Turkish words (https://github.com/CanNuhlar/Turkce-Kelime-Listesi)  
'''

''' To get the initial state you need to provide 
    - a file containing list of 5 letter words and 
    - your initial guess.  
    "state" is build from the feedback game provides about the guess.
    A letter in the guess is etiher 
    - not-exist, 
    - exist but misaligned or 
    - on spot

Say the word selected by the game is "TUFAN"
Your first guess is "BRAIN" thus game provies following information about the letters 
    B,R,I letters are not exist, 
    "A" exist but not in corrrect place
    "N" esixts and on the spot  
    
A sample flow is below;

% python3 ./wordlehelp.py <five letter word list file> BRAIN
Letters in correct place: ....N
Letters in wrong place  : ..A..
(
    program figures out B,R and I are not exist in the word.
    and provides a list of 5 letter words to select from,
    and asks for your next guess.
) 
Letters not exist       : BRI  
Possible words;
..........
Enter your next guess   : WOMAN
Letters in correct place: ...AN
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

ANYLETTER='.'

''' To pass "the Turkey Test" İIiı upper lower conversions must be provided
'''

TRUPPERMAP={
    ord(u'ı'): u'I',
    ord(u'i'): u'İ',            
}

def wrdhupper(str):
    return str.translate(TRUPPERMAP).upper()

def print_usage():
    print('''Usage: wordlehelp.py <word list file> <first guess>''')

class SolutionSet():
    '''given 5 letter words make up the solution set'''
    def __init__(self, wordsfile):
        self.words=[]
        with open(file=wordsfile, mode='r', encoding='utf8') as fd:
            self.words = fd.readlines()
        
        self.words=[wrdhupper(w).rsplit()[0] for w in self.words]
        self.words.sort();
        self.words=list(set(self.words))


    def __notLetter(self, c):
        return f"[^{c}]"
        
    def __hasAll (self, word, letters):
        return all (c==ANYLETTER or c in word for c in letters)
    
    def removeWords(self, nonexisting, misaligned, onspot):
        '''reduce the solution set from the provided information
        - remove words that contains nonexisting letters
        - select words contaninig misaligned letters and remove theones ont he wrong spot
        - select the words whith letters on the spot.
        '''
        print("Number of words ",len(self.words))
    
        exp=''
        if len(nonexisting) > 0:
            exp = ''.join(nonexisting)
            p = re.compile('['+exp+']')
            self.words[:] = [w for w in self.words if not p.search(w)]            
        print("Number of words after removal of letters containing '"+exp+"' is ", len(self.words))

        if any(letter != ANYLETTER for letter in list(misaligned)):
            '''word must include misaligned letters'''
            self.words[:] = [w for w in self.words if self.__hasAll(w,misaligned)]
            '''but not in given places'''
            exp='^'
            for c in misaligned:
                if c == ANYLETTER:
                    exp+=ANYLETTER
                else:
                    exp+=self.__notLetter(c)
            exp+='$'                
            print (f"RegEx '{exp}'")
            p = re.compile(''.join(exp))
            self.words[:] = [w for w in self.words if p.match(w)]
        print("Number of words after removing misaligned letters '"+misaligned+"' is ", len(self.words))
        
        if any(letter != ANYLETTER for letter in list(onspot)):        
            exp=''.join(onspot)
            p=re.compile(exp)
            self.words[:]=[w for w in self.words if p.match(w)]            
        print("Number of words after selecting of words w/ matching '"+onspot+"' is ", len(self.words))
            
        self.words.sort() # this is the remaning word list

        
    def has(self, word):
        return word in self.words
        
    def isEmpty(self):
           return len(self.words) == 0
        
    def dump(self):
        for w in self.words:
            print(w, end=",") # print adds \n to the end 
            
   
class Node():
    '''state is a State object, parent is a Node object, 
    action is the guesses word which takes us here'''
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
    def print(self):
        self.state.print()
        print(",",end="")
        print(self.action,end=",")
        if self.parent is not None:
            self.parent.print()
        print()
        
class Frontier():
    '''Possible sollutions for the problem'''
    def __init__(self, solution_set):
        self.solutionSet=solution_set
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)
        
    def removeNode(self):
        '''removing node reduces the solution set to make us closer to the solution'''
        if self.isEmpty(): 
            raise Exception("Empty frontier")
        else:
            node = self.nodes[-1]
            self.solutionSet.removeWords(nonexisting=node.state.notexist,
                                     misaligned=node.state.misaligned,
                                     onspot=node.state.onspot)

            return node

    def isEmpty(self):
        return len(self.nodes) == 0


class State():
    '''state is the feedback provided by the wordle game given guessed word
    we take this feedback from the user here and form the state'''
    def __init__(self, guess):
        self.notexist = []
        self.misaligned = [ANYLETTER, ANYLETTER, ANYLETTER, ANYLETTER, ANYLETTER]
        self.onspot =[ANYLETTER, ANYLETTER, ANYLETTER, ANYLETTER, ANYLETTER]
        self.__getInput(guess)

    def __check(self, guess, entry):
        if len(entry.strip()) == 0:
            '''empty line is '.....' '''
            entry=5*ANYLETTER
        else:        
            entry = wrdhupper(entry)
            if not all(letter==ANYLETTER or letter in list(guess) for letter in list(entry)):
                raise Exception("There is a wrong letter in the entry ", entry)
            if len(entry) != 5:
                raise Exception("Did you forget to put . for other letters? ", entry)
        return entry
    
    def __getInput(self, guess):    
        guess = wrdhupper(guess)
        print("For guessed word '"+guess+"' enter the feedback provided by the game")
        
        self.onspot = input("Letters in correct place (place . for others) : ")
        self.onspot = self.__check(guess, self.onspot)
        
        self.misaligned = input("Letters in wrong place (place . for others).. : ")
        self.misaligned = self.__check(guess, self.misaligned)

        for letter in list(guess):
            if letter not in self.onspot + self.misaligned:
                self.notexist.append(letter)
        
        print("Letters not exist : ", ''.join(self.notexist))
        
    def print(self):
        print(''.join(self.onspot), end="")
        
    def isGoal(self):
        '''there souldn't be any misaligned and nonexisting letters and have a full match'''
        return all (letter != ANYLETTER for letter in self.onspot)
        #len(self.misaligned) == 0 and len(self.notexist) == 0 and 

class  Wordle():
    '''helps solving the puzzle '''
    
    def __init__(self, wordsfile, firstguess):
        '''initilize the state and the frontier'''
        solution_set = SolutionSet(wordsfile)
        self.frontier = Frontier(solution_set)
        
        guess = wrdhupper(firstguess)        
        if len(guess) != 5:
            raise Exception("Guess word must have 5 letters")
        elif not solution_set.has(guess): 
            raise Exception("Guess word does not exist in the provided word list!")
        
        self.state = State(guess)        
        
    def solve(self):
        ''' Here I used an (AI) search algorithm
        Start w/ a frontier that contains initial state
        Start w/ an empty explored set - not needed in this problem
        Repeat:
            - frontier empty => no solution
            - remove a node from frontier
            - node has "goal state" => solution (~done)
            - add the node to the explored set
            - expand node, add adjacent  nodes to frontier if they aren't already in the frontier OR the explored set
        '''
        start = Node(state=self.state, parent=None, action=None)        
        self.frontier.addNode(start)
        
        while True:
            if self.frontier.isEmpty():
                raise Exception("There is no solution!")
            
            node = self.frontier.removeNode()
            
            if node.state.isGoal():
                print("Solution is ", end="")
                node.state.print()
                '''print how we get here'''
                node.print()
                return

            '''action to get to the next state'''
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
