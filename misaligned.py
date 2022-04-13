#!/usr/bin/env python3
'''expand search to a list of strings w/ one letter each'''

from math import exp
import sys
import re

TRUPPERMAP={
    ord(u'ı'): u'I',
    ord(u'i'): u'İ',            
}

ANYLETTER='.'

def wrdhupper(str):
    return str.translate(TRUPPERMAP).upper()


def notLetter(c):
    return f"[^{c}]"

def hasAll (word, letters):
        return all (c==ANYLETTER or c in word for c in letters)

def main():
    file="a.txt"
    misaligned = "..a.n"

    if len(sys.argv) > 1:
        file=sys.argv[1]
    if len(sys.argv) > 2:
        misaligned = sys.argv[2]

    misaligned=wrdhupper(misaligned)

    words=[]    
    with open(file=file, mode='r', encoding='utf8') as fd:
        words = fd.readlines()
        
    words=[wrdhupper(w).rsplit()[0] for w in words]
    words.sort();
    words[:] = list(set(words))    

    exp='^'
    for c in misaligned:
        if c == ANYLETTER:
            exp+=ANYLETTER
        else:
            exp+=notLetter(c)
    exp+='$'  
    if any(c != ANYLETTER for c in exp):
        words[:] = [w for w in words if hasAll(w,misaligned)]
        print(words)
        print (f"RegEx '{exp}'")
        p = re.compile(''.join(exp))
        words[:] = [w for w in words if p.match(w)]
        
    
    print(words)
    print(len(words))

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        instance = sys.exc_info()
        print("ERROR. Terminating!" + str(instance))
