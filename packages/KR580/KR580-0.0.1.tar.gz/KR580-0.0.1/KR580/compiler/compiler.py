import ply.yacc as yacc

from .compiler_utils import construct_list, resolve_name
from .lexer import lexer, tokens

deffered = []

def p_exp_list(p):
    """exp_list : exp_list term
                | term
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = construct_list(p[1], p[2])

def p_ID(p):
    'term : ID'
    p[0] = [-1, -1]

def p_two_rg_names(p):
    'term : CMD RG_NAME RG_NAME'
    opcode = resolve_name(p)
    p[0] = opcode

def p_two_words(p):
    'term : CMD WORD WORD'
    opcode = resolve_name(p[:2])
    p[0] = [opcode, p[3], p[2]]

def p_rg_name_cmd(p):
    'term : CMD RG_NAME'
    opcode = resolve_name(p)
    p[0] = opcode

def p_one_word(p):
    'term : CMD WORD'
    opcode = resolve_name(p[:2])
    p[0] = [opcode, p[2]]

def p_nular(p):
    'term : CMD'
    opcode = resolve_name(p)
    p[0] = opcode

def p_word(p):
    'term : WORD'
    p[0] = p[1]

parser = yacc.yacc()

def inline_links(parsed):
    deffered = lexer.to_inline
    if len(deffered) == 0:
        return parsed
    while True:
        try:
            pos, name = deffered.pop()
            addr = lexer.symtable[name]
            parsed[pos], parsed[pos+1] = addr & 0xFF, addr >> 8
        except IndexError:
            break
    return parsed

def compile_(src):
    parsed = parser.parse(src)
    parsed = inline_links(parsed)
    lexer.counter = 0
    lexer.symtable = {}
    return parsed
