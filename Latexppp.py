from mimetypes import init
from operator import truediv
from re import T
import re
from xmlrpc.client import Boolean
import ply.lex as lex


error = False

tokens = ["TITLE","BOLD","ITALIC","WORD"]

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_TITLE(t):
    r'\#[\w\s]*\#'
    t.value = re.sub(r'(?:\#)([\w\s]*)(?:\#)',r'\\title{\1}',t.value)
    return t

def t_BOLD(t):
    r'\$\$[\w\s]*\$\$'
    t.value = re.sub(r'(?:\$\$)([\w\s]*)(?:\$\$)',r'\\textbf{\1}',t.value)
    return t

def t_ITALIC(t):
    r'\%\%[\w\s]*\%\%'
    t.value = re.sub(r'(?:\%\%)([\w\s]*)(?:\%\%)',r'\\textit{\1}',t.value)
    return t

#t_ignore = '\n\t '

def t_error(t):
    error = True
    #print(f"ERROR: Illegal character '{t.value[0]}' at position ({t.lineno},{t.lexpos})")
    print(t.value,end="")
    t.lexer.skip(len(t.value)) 

t_WORD = r'[\w\s]+'

# Analisador léxico
lexer = lex.lex()

import sys

for line in sys.stdin:
    lexer.input(line)
    for tok in lexer:	
        if(error == False):
    	    print(tok.value,end="")
        else: error = False
    



