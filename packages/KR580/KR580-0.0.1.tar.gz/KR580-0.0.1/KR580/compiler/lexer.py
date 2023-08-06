import ply.lex as lex

from .symbols import cmds, rg_names, tokens

def t_DECLARATION(t):
    r'[A-Za-z]+[0-9]*\:'
    cnt = t.lexer.counter
    if cnt - t.lexer.last_declaration == 1:
        cnt -= 1
    label = t.value[:-1]
    t.lexer.symtable[label] = cnt
    t.lexer.last_declaration = cnt

def t_CMD(t):
    r'([A-Z]|[a-z])+'
    if t.value.upper() in cmds:
        t.type = 'CMD'
        t.lexer.counter += 1
    elif t.value in rg_names:
        t.type = 'RG_NAME'
    else:
        return
    return t

def t_WORD(t):
    r'[A-Fa-f0-9]{2}'
    t.value = int(t.value, 16)
    t.lexer.counter += 1
    return t

def t_ID(t):
    r'[A-Za-z]*[0-9]+'
    t.value = (t.lexer.counter, t.value)
    t.lexer.to_inline.append(t.value)
    t.lexer.counter += 2
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r';.*'
    pass

t_ignore  = '\t, '

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
lexer.symtable = {}
lexer.to_inline = []
lexer.last_declaration = -2
lexer.counter = 0
