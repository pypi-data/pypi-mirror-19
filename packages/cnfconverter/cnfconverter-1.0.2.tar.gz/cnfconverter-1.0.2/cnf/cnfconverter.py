#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: cnf.py
# Author: Jinbo Pan
# Mail: pan.jinbo@outlook.com
# Created Time:  2017-01-06
#############################################
import ply.lex as lex
import re
import copy

tokens = (
    'Predicate',
    'And',
    'Or',
    'Not',
    'Inference',
    'Left',
    'Right',
    )

t_And = r'&'
t_Or = r'\|'
t_Not = r'~'
t_Inference = r'=>'
t_Left = r'\('
t_Right = r'\)'
t_ignore = ' '

def t_Predicate(t):
    r'[A-Z][a-zA-Z]*\(.+?\)'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
data = 'D(x,y)'

precedence = (
    ('left','Inference'),
    ('left','Or'),
    ('left','And'),
    ('right','Not'),
    )


def p_expression_group(t):
    'expression : Left expression Right'
    t[0] =  t[2] 

def p_expression_predicate(t):
    '''expression : Predicate'''
    t[0] = { 'value': t[1] }

def p_expression_binop(t):
    ''' expression : expression And expression
                    | expression Or expression
                    | expression Inference expression'''
    if t[2] == '&' : 
        t[0] = { 'left': t[1], 'right': t[3], 'op':'&'}
    elif t[2] == '|' :
        t[0] = { 'left': t[1], 'right': t[3], 'op':'|'}
    elif t[2] == '=>':
        temp = { 'child':t[1],'op':'~'}
        t[0] = { 'left': temp, 'right': t[3], 'op':'|'}



def p_expression_negative(t):
    'expression : Not expression'
    t[0] = { 'child': t[2], 'op': '~'}

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    
import ply.yacc as yacc
parser = yacc.yacc()




def checkNot(node):
    if 'op' in node and node['op'] == '~':
        return True
    return False

def checkValue(node):
    if 'value' in node:
        return True
    return False

def checkAnd(node):
    if 'op' in node and node['op'] == '&':
        return True
    return False

def isValue(node):
    return checkValue(node) or checkNot(node)

def value(node):
    if checkValue(node):
        return node['value']
    elif checkNot(node):
        return '~'+node['child']['value']


def Neg(node):
    neg1 = {'child':node['child']['left'],'op':'~' }
    neg2 = {'child':node['child']['right'],'op':'~'}
    node['child']['left'] = neg1
    node['child']['right'] = neg2
    if  node['child']['op'] == '&':
        node['child']['op'] = '|'
    elif  node['child']['op'] == '|':
        node['child']['op'] = '&'
    return node['child']

def NegNeg(node):
    node = node['child']['child']
    return node
#print(Neg(ast))

def NegTree(ast):
    if ast == None:
        return 
    if 'value' in ast:
        return ast
    if ast['op'] == '~' and 'op' in ast['child'] and ( ast['child']['op'] == '&' or ast['child']['op'] == '|' ) :
        ast = Neg(ast)
        ast['left'] = NegTree(ast['left'])
        ast['right'] = NegTree(ast['right'])
    elif ast['op'] == '~' and 'op' in ast['child'] and ast['child']['op'] == '~':
        ast = NegNeg(ast)
    elif ast['op'] == '~':
        ast['child'] = NegTree(ast['child'])
    else:
        ast['left'] = NegTree(ast['left'])
        ast['right'] = NegTree(ast['right'])
    return ast


def CheckDis(node):
    if isValue(node):
        return False
    if  node['op'] == '&':
        return False
    if node['op'] == '|':
        left = node['left']
        right = node['right']
        if isValue(left) and isValue(right):
            return False
        if 'op' in left and left['op']=='&':
            return True
        if 'op' in right and right['op'] =='&':
            return True
        return CheckDis(left) | CheckDis(right)

def Dis(node):
    if 'op' in node['left'] and node['left']['op'] == '&':
        A = node['left']['left']
        B = node['left']['right']
        C = node['right']
        node['op']='&'
        left = { 'left':A,'right':C, 'op':'|'}
        right = { 'left':B,'right':C, 'op':'|'}
        node['left'] = left
        node['right'] = right
        return node
    if 'op' in node['right'] and node['right']['op'] == '&':
        A = node['left']
        B = node['right']['left']
        C = node['right']['right']
        node['op'] = '&'
        left = {'left':A,'right':B,'op':'|'}
        right = {'left':A,'right':C,'op':'|'}
        node['left'] = left
        node['right'] = right
        return node

def DisTree(ast):
    if isValue(ast):
        return ast
    if ast['op'] == '|' and 'op' in ast['left'] and ast['left']['op'] == '|' and CheckDis(ast['left']):
        ast['left'] = DisTree(ast['left'])

    if ast['op'] == '|' and 'op' in ast['right'] and ast['right']['op'] == '|' and CheckDis(ast['right']):
        ast['right'] = DisTree(ast['right'])
        

    if CheckDis(ast):
        ast = Dis(ast)
        #print(ast)
        ast['left'] = DisTree(ast['left'])
        #print(ast)
        ast['right'] = DisTree(ast['right'])
    else:
        ast['left'] = DisTree(ast['left'])
        ast['right'] = DisTree(ast['right'])
    return ast


def to_cnf(ast):
    if isValue(ast):
        return [value(ast)]
    if ast['op'] == '&':
        
        res = []
        left = to_cnf(ast['left'])
        right = to_cnf(ast['right'])
        if isinstance(left[0],str):
            res.append(left)
        else:
            for i in left:
                res.append(i)
        if isinstance(right[0],str):
            res.append(right)
        else:
            for i in right:
                res.append(i)
        return res
    if ast['op'] == '|':
        res = to_cnf(ast['left'])+to_cnf(ast['right'])
        return res

def to_CNF(data):
    ast = parser.parse(data)
    ast = NegTree(ast)
    ast = DisTree(ast)
    ast = to_cnf(ast)
    if isinstance(ast[0],str):
        return [ast]
    return ast



