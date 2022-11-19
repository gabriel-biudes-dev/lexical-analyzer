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
        x (_type_): Value to be checked

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
    i1 = 0
    i2 = 0
    i3 = 0
    keywordlist = ['int', 'float', 'if', 'else', 'for', 'while', '=', '+', '-', '*', '/', '>', '<', '>=', '<=', '==', '(', ')', '{', '}']
    for m in re.finditer(tokens_join, code):
        token_type = m.lastgroup
        token_lexeme = m.group(token_type)
        if token_type == 'NEWLINE': lin_num += 1
        elif token_type == 'SKIP': continue
        elif token_type == 'ERRONEOUS': raise RuntimeError('ERRONEOUS: %r inesperado na linha %d' % (token_lexeme, lin_num))
        else: 
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
    return symboltable, keywordtable, fulltable

def main():
    """Main function
    """
    content = load_file(input('Source file name: '))
    symboltable, keywordtable, fulltable = tokenize(content)
    for x in symboltable: print(symboltable[x].lexeme)
    #for x in fulltable: print(fulltable[x].lexeme)
    #for x in keywordtable: print(keywordtable[x].lexeme)

if __name__ == '__main__': main()

