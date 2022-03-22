# Preprocessador de latex
# 03/2022

import re
from xml.etree.ElementInclude import include
import ply.lex as lex
import sys

# Estados possíveis
states = (
	('title','inclusive'),
	('bold','inclusive'),
	('italic','inclusive'),
	('list','inclusive'),
	('figure','inclusive'),
	('caption','inclusive'),
	('numberedlist','inclusive'),
)

# Token
tokens = ["OPENFIGURE",
		  "CLOSEFIGURE",
		  "OPENCAPTION",
		  "CLOSECAPTION",
		  "OPENTITLE",
		  "CLOSETITLE",
		  "OPENBOLD",
		  "CLOSEBOLD",
		  "OPENITALIC",
		  "CLOSEITALIC",
		  "OPENLIST",
		  "CLOSELIST",
		  "OPENNUMBEREDLIST",
		  "CLOSENUMBEREDLIST",
		  "SPECIALCHAR",
		  "WORDS"]

# Define carater especial (barra \ seguida de um caracter -> print desse mesmo caracter sem aplicar regras)
def t_SPECIALCHAR(t):
	r'\\.'
	return t

t_WORDS = r'([\w\s])+'

# Define o caracter de abertura de título
def t_OPENTITLE(t):
	r'\#+'
	titlestr = "\\"
	for i in range(1,len(t.value)):
		titlestr += 'sub'
	titlestr += 'section{'
	t.value = titlestr
	t.lexer.states.append('title')
	t.lexer.begin('title')
	return t

# Define o caracter de fecho de título
def t_CLOSETITLE(t):
	r'\/\#'
	t.value = '}'
	t.lexer.begin('INITIAL')
	t.lexer.states = t.lexer.states[:-1]
	return t
	
# Regra interior do título
def t_title_rule1(t):
	r'[\w\s]+'
	print(t.value,end = '')


# Define o caracter de abertura de bold
def t_OPENBOLD(t):
	r'\$'
	t.lexer.states.append('bold')
	t.lexer.begin('bold')
	t.value = '\\textbf{'
	return t


# Define o caracter de fecho de bold
def t_CLOSEBOLD(t):
	r'\/\$'
	t.value = '}'
	t.lexer.states = t.lexer.states[:-1]
	return t

# Regra interior bold
def t_bold_rule1(t):
	r'[\w\s]+'
	print(t.value,end = '')

# Define o caracter de abertura de italico
def t_OPENITALIC(t):
	r'\%'
	t.lexer.states.append('italic')
	t.lexer.begin('italic')
	t.value = '\\textit{'
	return t

# Define o caracter de fecho de italico
def t_CLOSEITALIC(t):
	r'\/\%'
	t.value = '}'
	t.lexer.states = t.lexer.states[:-1]
	return t

# Regra interior italico
def t_italic_rule1(t):
	r'[\w\s]+'
	print(t.value,end = '')

# Define o caracter de abertura de lista numerada
def t_OPENNUMBEREDLIST(t):
	r'\[N'
	t.lexer.states.append('numberedlist')
	t.lexer.begin('numberedlist')
	t.value = '\\begin{enumerate}\n'
	return t

# Define o caracter de fecho da lista numerada
def t_CLOSENUMBEREDLIST(t):
	r'\/\]'
	t.value = '\end{enumerate}'
	t.lexer.states = t.lexer.states[:-1]
	return t

# Define o interior da lista numerada
def t_numberedlist_rule1(t):
	r'\-[\w\s]+'
	print('\n\t\item ' + t.value[1:])


# Define o caracter de abertura de lista
def t_OPENLIST(t):
	r'\['
	t.lexer.states.append('list')
	t.lexer.begin('list')
	t.value = '\\begin{itemize}\n'
	return t

# Define o caracter de fecho da lista
def t_CLOSELIST(t):
	r'\/\]'
	t.value = '\end{itemize}'
	t.lexer.states = t.lexer.states[:-1]
	return t

# Define o interior da lista
def t_list_rule1(t):
	r'\-[\w\s]+'
	print('\n\t\item ' + t.value[1:],end="")



# Define o caracter de abertura de imagem
def t_OPENCAPTION(t):
	r'='
	t.lexer.begin('caption')
	t.lexer.states.append('caption')
	t.value = '\\caption{'
	return t

# Define o interior da imagem
def t_caption_rule1(t):
	r'\s*[\w\.]+\s*'
	print(t.value,end="")
	#print(t.value,end="")

# Define o interior da imagem
def t_CLOSECAPTION(t):
	r'\/='
	t.value = '}'
	t.lexer.states = t.lexer.states[:-1]
	return t

# Define o caracter de abertura de imagem
def t_OPENFIGURE(t):
	r'«'
	t.lexer.begin('figure')
	t.lexer.states.append('figure')
	t.value = '\\begin{figure}[h]\n\includegraphics[width=400px]{'
	return t

# Define o interior da imagem
def t_figure_rule1(t):
	r'\s*[\w\.]+\s*'
	print(t.value + '}\n',end="")
	#print(t.value,end="")

# Define o interior da imagem
def t_figure_rule2(t):
	r'\|'
	print(t.lexer.states)

	print('\caption{',end="")
	t.lexer.states.append('caption')
	t.lexer.begin('caption')


# Define o interior da imagem
def t_CLOSEFIGURE(t):
	r'»'
	t.value = '\n\end{figure}\n'
	t.lexer.states = t.lexer.states[:-1]
	return t

# Comportamento de erro
def t_error(t):
	#print(f"\nERROR: Illegal character '{t.value[0]}' at position ({t.lineno},{t.lexpos})")
	print(t.value[0],end ='')
	t.lexer.skip(1)

# Analisador léxico
lexer = lex.lex()
lexer.states = ['INITIAL']

# Ler do STDIN e escrever para o STDOUT

print("\\documentclass{article}")
print("\\usepackage[utf8]{inputenc}")
print("\\usepackage{graphicx}")
print("\\begin{document}")
for line in sys.stdin:
	lexer.input(line)
	for tok in lexer:
		print(tok.value,end="")
print("\\end{document}")


