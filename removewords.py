'''work to remove words from bir word list'''

import sys
import re

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
 
    nonexistingletters = input("Non existing letters: ")
    misallignedletters = input("Misalligned letters : ")
    onspotletters = input("Onspot letters (place .) : ")
 
    nonexistingletters = wrdhupper(nonexistingletters)
    misallignedletters = wrdhupper(misallignedletters)
    onspotletters = wrdhupper(onspotletters)
    
    print("Number of words ",len(words))
    
    exp = ''.join(onspotletters)
    p = re.compile(exp)
    words[:] = [w for w in words if p.search(w)]            
    print("Number of words after selecting of words w/ matching '"+exp+"' is ", len(words))
    print(words)
    
    exp=''
    if len(nonexistingletters) > 0:
        exp = ''.join(nonexistingletters)
        p = re.compile('['+exp+']')
        words[:] = [w for w in words if not p.search(w)]            
    print("Number of words after removal of words containing '"+exp+"' is ", len(words))
    print(words)
    
    exp=''
    if len(misallignedletters) > 0:
        # exp = ''.join(misallignedletters)
        # p = re.compile(exp)
        # words[:] = [w for w in words if p.search(w)]            
        words[:] = [w for w in words if hasAll(w, misallignedletters)]            
    print("Number of words after selecting of words containing '"+misallignedletters+"' is ", len(words))
    print(words)
 
    words[:] = [w for w in words if hasAll(w, misallignedletters)]            
     
def hasAll (word, letters):
    return all (c in word for c in letters)
 
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        instance = sys.exc_info()
        print("ERROR. Terminating!" + str(instance))
