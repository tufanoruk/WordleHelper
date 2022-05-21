#!/usr/bin/env python3
'''work to remove words from bir word list'''

import sys
import re
import termcolor

ANYLETTER='.'

TRUPPERMAP={
    ord(u'ı'): u'I',
    ord(u'i'): u'İ',            
}

def wrdhupper(str):
    return str.translate(TRUPPERMAP).upper()

def main():
    file="a.txt"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    words=[]    
    with open(file=file, mode='r', encoding='utf8') as fd:
        words = fd.readlines()
        
    words=[wrdhupper(w).rsplit()[0] for w in words]
    words.sort();
    words[:] = list(set(words))
 
    onspot      = input("Onspot letters (place . for others)..... : ")
    misaligned  = input("Misalligned letters (place . for others) : ")
    nonexisting = input("Non existing letters: ")

    nonexisting = wrdhupper(nonexisting)
    misaligned = wrdhupper(misaligned)
    onspot = wrdhupper(onspot)
    
    text = "Number of words "+str(len(words))
    termcolor.cprint(text, 'red')
    
    exp=''
    if len(nonexisting) > 0:
        exp = ''.join(nonexisting)
        p = re.compile('['+exp+']')
        words[:] = [w for w in words if not p.search(w)]            
    print("Number of words after removal of words containing '"+exp+"' is ", len(words))
    print(words)
    
    if any(letter != ANYLETTER for letter in list(misaligned)):
        '''word must include misaligned letters'''
        words[:] = [w for w in words if has_all(w,misaligned)]
        '''but NOT in given places'''
        exp='^'
        for c in misaligned:
            if c == ANYLETTER:
                exp+=ANYLETTER
            else:
                exp+=not_letter(c)
        exp+='$'                
        print (f"RegEx '{exp}'")
        p = re.compile(''.join(exp))
        words[:] = [w for w in words if p.match(w)]
    print("Number of words after removing misaligned letters '"+misaligned+"' is ", len(words))
        
 
    exp = ''.join(onspot)
    p = re.compile(exp)
    words[:] = [w for w in words if p.search(w)]            
    print("Number of words after selecting of words w/ matching '"+exp+"' is ", len(words))
    print(words)
    
 
def not_letter(c):
    return f"[^{c}]"


def has_all (word, letters):
    return all (c==ANYLETTER or c in word for c in letters)

 
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        instance = sys.exc_info()
        print("ERROR. Terminating!" + str(instance))
