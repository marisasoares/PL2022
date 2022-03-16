# Preprocessador de latex
# 03/2022

import re
import ply.lex as lex
import sys

# Estados possíveis
states = (
	('title','inclusive'),
	('bold','inclusive'),
	('italic','inclusive'),
	('list','inclusive'),
)

# Token
tokens = ["OPENTITLE",
		  "CLOSETITLE",
		  "OPENBOLD",
		  "CLOSEBOLD",
		  "OPENITALIC",
		  "CLOSEITALIC",	
		  "OPENLIST",
		  "CLOSELIST",
		  "WORDS"]

t_WORDS = r'[\w\s]+'

# Define o caracter de abertura de título
def t_OPENTITLE(t):
	r'\#'
	t.lexer.begin('title')
	t.value = '\\title{'
	return t

# Define o caracter de fecho de título
def t_CLOSETITLE(t):
	r'\/\#'
	t.value = '}'
	t.lexer.begin('INITIAL')
	return t
	
# Regra interior do título
def t_title_rule1(t):
	r'[\w\s]+'
	print(t.value,end = '')


# Define o caracter de abertura de bold
def t_OPENBOLD(t):
	r'\$'
	t.lexer.begin('bold')
	t.value = '\\textbf{'
	return t


# Define o caracter de fecho de bold
def t_CLOSEBOLD(t):
	r'\/\$'
	t.value = '}'
	t.lexer.begin('INITIAL')
	return t

	
# Regra interior bold
def t_bold_rule1(t):
	r'[\w\s]+'
	print(t.value,end = '')

# Define o caracter de abertura de italico
def t_OPENITALIC(t):
	r'\%'
	t.lexer.begin('italic')
	t.value = '\\textit{'
	return t

# Define o caracter de fecho de italico
def t_CLOSEITALIC(t):
	r'\/\%'
	t.value = '}'
	t.lexer.begin('INITIAL')
	return t
	
# Regra interior italico
def t_italic_rule1(t):
	r'[\w\s]+'
	print(t.value,end = '')

# Define o caracter de abertura de lista
def t_OPENLIST(t):
	r'\['
	t.lexer.begin('list')
	t.value = '\\begin{itemize}\n'
	return t

# Define o caracter de fecho da lista
def t_CLOSELIST(t):
	r'\/\]'
	t.value = '\end{itemize}'
	t.lexer.begin('INITIAL')
	return t

# Define o interior da lista
def t_list_rule1(t):
	r'\-[\w\s]+'
	print('\n\t\item ' + t.value,end="")

# Comportamento de erro
def t_error(t):
	#print(f"\nERROR: Illegal character '{t.value[0]}' at position ({t.lineno},{t.lexpos})")
	print(t.value[0],end ='')
	t.lexer.skip(1) 

# Analisador léxico
lexer = lex.lex()

# Ler do STDIN e escrever para o STDOUT
for line in sys.stdin:
	lexer.input(line)
	for tok in lexer:	
		print(tok.value,end="")
	



