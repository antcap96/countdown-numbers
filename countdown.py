from itertools import combinations, product, permutations
import operator
import numpy as np
from copy import copy

numbers = [75, 25, 5, 9 ,8, 10]

def get_solutions(numbers, target, operation=None):
    if len(numbers) == 1 and numbers[0] == target:
        return [[]]
    elif len(numbers) == 1:
        return None

    result = []

    if operation == None:
        for op in [operator.add, operator.sub, operator.mul, operator.floordiv]:
            a = get_solutions(numbers, operation=op, target=target)
            if a != None:
                for b in a:
                   b.append(op)
                result = result + a
    
    elif operation == operator.add or operation == operator.mul:
        for pair in combinations(range(len(numbers)), 2):
            numbers_c = copy(numbers)
            numbers_c[min(pair)] = operation(numbers[pair[0]], numbers[pair[1]])
            del numbers_c[max(pair)]

            a = get_solutions(numbers_c, operation=None, target=target)
            if a != None:
                for b in a:
                   b.append(pair)
                result = result + a
    
    # if subtract use permutations instead of combinations (order matters)
    elif operation == operator.sub:
        for pair in permutations(range(len(numbers)), 2):
            numbers_c = copy(numbers)
            numbers_c[min(pair)] = operation(numbers[pair[0]], numbers[pair[1]])
            del numbers_c[max(pair)]
            
            a = get_solutions(numbers_c, operation=None, target=target)
            if a != None:
                for b in a:
                   b.append(pair)
                result = result + a
    
    # if divide make sure number is divisible first
    else:
        for pair in permutations(range(len(numbers)), 2):
            if numbers[pair[1]] == 0 or numbers[pair[0]] % numbers[pair[1]] != 0:
                continue
            numbers_c = copy(numbers)
            numbers_c[min(pair)] = operation(numbers[pair[0]], numbers[pair[1]])
            del numbers_c[max(pair)]
            
            a = get_solutions(numbers_c, operation=None, target=target)
            if a != None:
                for b in a:
                   b.append(pair)
                result = result + a

    return result if result != [] else None

operation = {operator.add      : '+',
             operator.mul      : '*',
             operator.sub      : '-',
             operator.floordiv : '/'}

def parse(solution, numbers):
    result = '_0_'

    for i, pair, op in zip(range(len(solution)), solution[0::2], solution[1::2]):
        for j in range(i+1,max(pair)-1,-1):
            result = result.replace('_' + str(j) + '_', '_' + str(j+1) + '_')
        result = result.replace('_'+str(min(pair))+'_', '(_{}_{}_{}_)'.format(pair[0], operation[op], pair[1]))

    for i in range(len(numbers)):
        result = result.replace('_'+str(i)+'_', str(numbers[i]))

    return result

class node:
    def __init__(self, left=None, right=None, string=None):
        self.left = left
        self.right = right
        self.string = string

def dismantle(s):
    if s[0] == '(' and s[-1] == ')':
        s = s[1:-1]
    stack = []
    op_idx = None
    for i,c in enumerate(s):
        if c == '(':
            stack.append('(')
        if c == ')':
            stack.pop()
        
        if len(stack) == 0 and i != len(s)-1:
            op_idx = i

    if op_idx != None:
        root = node(left=dismantle(s[:op_idx]), right=dismantle(s[op_idx+1:]), string=s[op_idx])
    else:
        root = node(string=s)
    
    return root
    
priority = {'+': 0, 
            '-': 0, 
            '*': 1, 
            '/': 1}

def build(node, prev=0):
    
    if node.left == node.right == None:
        return node.string
    # priorities
    p = priority[node.string]

    s = build(node.left, p) + node.string + build(node.right, p)
    if p >= prev:
        return s
    else:
        return '(' + s + ')'


def solve(numbers, target):
    results = []
    solutions = get_solutions(numbers, target)
    if solutions != None:    
        for solution in solutions:
            results.append(build(dismantle(parse(solution, numbers))))

    return results