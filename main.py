import re

class Token:
    """Token class, containing data about the token
    """
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

def load_file(filename):
    """Loads a file content

    Args:
        filename (str): File name

    Returns:
        str: File content
    """
    with open(filename, 'r') as file: content = file.read()
    return content

def getrules():
    """Gets the compiler token classes

    Returns:
        list[]: List of token classes
    """
    return [
        ('INT', r'int'),            # int
        ('FLOAT', r'float'),        # float
        ('IF', r'if'),              # if
        ('ELSE', r'else'),          # else
        ('WHILE', r'while'),        # while
        ('FOR', r'for'),            # for
        ('LBRACKET', r'\('),        # (
        ('RBRACKET', r'\)'),        # )
        ('LBRACE', r'\{'),          # {
        ('RBRACE', r'\}'),          # }
        ('COMMA', r','),            # ,
        ('PCOMMA', r';'),           # ;
        ('EQ', r'=='),              # ==
        ('NE', r'!='),              # !=
        ('LE', r'<='),              # <=
        ('GE', r'>='),              # >=
        ('OR', r'\|\|'),            # ||
        ('AND', r'&&'),             # &&
        ('ATTR', r'\='),            # =
        ('LT', r'<'),               # <
        ('GT', r'>'),               # >
        ('PLUS', r'\+'),            # +
        ('MINUS', r'-'),            # -
        ('MULT', r'\*'),            # *
        ('DIV', r'\/'),             # /
        ('ID', r'[a-zA-Z]\w*'),     # IDENTIFIERS
        ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),   # FLOAT
        ('INTEGER_CONST', r'\d(\d)*'),          # INT
        ('NEWLINE', r'\n'),         # NEW LINE
        ('SKIP', r'[ \t\r]+'),        # SPACE and TABS
        ('ERRONEOUS', r'.'),         # ANOTHER CHARACTER
    ]

def checkinside(l, x):
    """Checks if the token x is inside the dict l

    Args:
        l (dict): Dict containing data
        x (Token Class): Value to be checked

    Returns:
        bool: True if x is found in l
    """
    for y in l:
        if y.lexeme == x.lexeme: return True
    return False

def tokenize(code):
    """Gets tokens from a file

    Args:
        code (str): File content

    Raises:
        RuntimeError: Lexical error found

    Returns:
        list, list, list: Returns the symbol table, keyword table and the whole table of tokens
    """
    lin_num = 1
    rules = getrules()
    tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
    symboltable = {}
    keywordtable = {}
    fulltable = {}
    breaklines = []
    i1 = 0
    i2 = 0
    i3 = 0
    count = 0
    keywordlist = ['int', 'float', 'if', 'else', 'for', 'while', '=', '+', '-', '*', '/', '>', '<', '>=', '<=', '==', '(', ')', '{', '}']
    for m in re.finditer(tokens_join, code):
        token_type = m.lastgroup
        token_lexeme = m.group(token_type)
        if token_type == 'NEWLINE': 
            lin_num += 1
            breaklines.append(count)
        elif token_type == 'SKIP': continue
        elif token_type == 'ERRONEOUS': raise RuntimeError('ERRONEOUS: %r inesperado na linha %d' % (token_lexeme, lin_num))
        else:
            count = count + 1
            t = Token(token_type, token_lexeme)
            fulltable[i3] = t
            i3 = i3 + 1
            if token_type == 'ID':
                if(checkinside(symboltable.values(), t)): continue
                symboltable[i1] = t
                i1 = i1 + 1
            if t.lexeme in keywordlist:
                if(checkinside(keywordtable.values(), t)): continue
                keywordtable[i2] = t
                i2 = i2 + 1
    return symboltable, keywordtable, fulltable, breaklines

def getline(i, breaklines):
    """Gets error line

    Args:
        i (int): Token index
        breaklines (int[]): List of breaklines relative to token count

    Returns:
        int: Error line
    """
    for index,x in enumerate(breaklines):
        if i < x - 1: return index + 1

def checkerrors(fulltable, breaklines):
    """Gets lexical erros on the code

    Args:
        fulltable (dict): Dict of tokens
        breaklines (int[]): List of breaklines relative to token count

    Raises:
        RuntimeError: Lexical error found

    Returns:
        bool: Returns False if no lexical error is found
    """
    for index,x in enumerate(fulltable):
        if fulltable[x].token == 'FLOAT' or fulltable[x].token == 'INT':
            next = fulltable[index + 1].token
            nextlex = fulltable[index + 1].lexeme
            if next != 'ID':
                line = getline(index + 1, breaklines)
                raise RuntimeError('Erro léxico: %r inesperado na linha %d' % (nextlex, line))
    return False

def showMenu():
    """Shows the application menu

    Returns:
        int: Choosen option
    """
    print('\n\n[Lexical Analyzer]')
    print('\t1)Show symbol table')
    print('\t2)Show keyword table')
    print('\t3)Show full table')
    return int(input('Option: '))

def printdata(symboltable, keywordtable, fulltable, answer):
    """Show data to the user

    Args:
        symboltable (dict): Symbol table
        keywordtable (dict): Keyword table
        fulltable (dict): Full table
        answer (int): Choosen option
    """
    if answer == 1:
        for x in symboltable: print(symboltable[x].lexeme, end=" ")
    if answer == 2:
        for x in keywordtable: print(keywordtable[x].lexeme, end=" ")
    if answer == 3:
        for x in fulltable: print(fulltable[x].token, end=" ")
        
def main():
    """Main function
    """
    content = load_file(input('Source file name: '))
    symboltable, keywordtable, fulltable, breaklines = tokenize(content)
    if checkerrors(fulltable, breaklines): return
    answer = showMenu()
    while answer != 4:
        printdata(symboltable, keywordtable, fulltable, answer)
        answer = showMenu()
        
if __name__ == '__main__': main()
