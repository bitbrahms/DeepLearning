# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 07:44:27 2017

@author: manny
"""

def checkio(text):
    text = list(text.lower())
    text_list = []
    [text_list.append(i) for i in text if i>='a' and i<='z']
    #[text.remove(i) for i in text if i in ',!.?"']
    text_dict = {}
    for i in text_list:
        if i not in text_dict:
            text_dict[i] = 1
        else:
            text_dict[i] += 1
    text_list = sorted(text_dict.keys())
    print(text_list)
    num = 0
    for i in text_list:
        if text_dict[i] > num:
            num = text_dict[i]
            letter = i
    return letter

if __name__ == '__main__':
    text = input()
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio("Hello World!") == "l", "Hello test"
    assert checkio("How do you do?") == "o", "O is most wanted"
    assert checkio("One") == "e", "All letter only once."
    assert checkio("Oops!") == "o", "Don't forget about lower case."
    assert checkio("AAaooo!!!!") == "a", "Only letters."
    assert checkio("abe") == "a", "The First."
    print("Start the long test")
    assert checkio("a" * 9000 + "b" * 1000) == "a", "Long."
    print("The local tests are done.")
    print(checkio(text))