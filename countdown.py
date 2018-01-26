from itertools import combinations, product, permutations
import operator
from copy import copy

#numbers = [75, 25, 5, 9 ,8, 10]

def get_solutions(numbers, target, operation=None):
    """find the solutions. Output is kinda of unreadable
    
    Arguments:
        numbers {list of (int)} -- list of the numbers used to get target
        target {int} -- target number
    
    Keyword Arguments:
        operation  -- used internally (default: {None})
    
    Returns:
        list of (list) -- list of possible solutions (to be parsed)
    """
    if len(numbers) == 1 and numbers[0] == target:
        return [[]]
    elif len(numbers) == 1:
        return None

    result = []

    if operation is None:
        for op in [operator.add, operator.sub, operator.mul, operator.floordiv]:
            a = get_solutions(numbers, operation=op, target=target)
            if a is not None:
                for b in a:
                   b.append(op)
                result = result + a
    
    elif operation == operator.add or operation == operator.mul:
        for pair in combinations(range(len(numbers)), 2):
            numbers_c = copy(numbers)
            numbers_c[min(pair)] = operation(numbers[pair[0]], numbers[pair[1]])
            del numbers_c[max(pair)]

            a = get_solutions(numbers_c, operation=None, target=target)
            if a is not None:
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
            if a is not None:
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
            if a is not None:
                for b in a:
                   b.append(pair)
                result = result + a

    return result if result != [] else None

operation = {operator.add      : '+',
             operator.mul      : '*',
             operator.sub      : '-',
             operator.floordiv : '/'}

def parse(solution, numbers):
    """parse the output of get_solutions
    
    Arguments:
        solution {list} -- an element of the output of get_solutions
        numbers {list of (int)} -- numbers given to get_solutions
    
    Returns:
        str -- solution without operator priority
    """
    result = '_0_'

    for i, pair, op in zip(range(len(solution)), solution[0::2], solution[1::2]):
        for j in range(i+1,max(pair)-1,-1):
            result = result.replace('_' + str(j) + '_',
                                    '_' + str(j+1) + '_')
        result = result.replace('_' + str(min(pair)) + '_',
                                '(_{}_{}_{}_)'.format(pair[0], operation[op], pair[1]))

    for i in range(len(numbers)):
        result = result.replace('_'+str(i)+'_', str(numbers[i]))

    return result

class Node:
    """Simple node class to create a tree
    If string is an operation, left and right should be arguments to the operation
    Otherwise string should be a number (and left, right = None, None)
    """

    def __init__(self, left=None, right=None, string=None):
        """Constructor
        
        Keyword Arguments:
            left {Node} -- left side (default: {None})
            right {Node} -- right side (default: {None})
            string {str} -- operator or number (default: {None})
        """
        self.left = left
        self.right = right
        self.string = string

def dismantle(s):
    """Break a string of operations with parenticies into a tree
    
    Arguments:
        s {str} -- string of operations
    
    Returns:
        Node -- tree of the operations
    """
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

    if op_idx is not None:
        root = Node(left=dismantle(s[:op_idx]), right=dismantle(s[op_idx+1:]), string=s[op_idx])
    else:
        root = Node(string=s)
    
    return root
    
priority = {'+': 0, 
            '-': 0, 
            '*': 1, 
            '/': 1}

def build(node, prev=0):
    """take a tree of operations and turn it into a string
    with only the necessary parentices
    
    Arguments:
        node {Node} -- tree of operations
    
    Keyword Arguments:
        prev {int} -- priority of the operation above (default: {0})
    
    Returns:
        str -- string of the operations
    """
    if node.left is node.right is None:
        return node.string
    # priorities
    p = priority[node.string]

    s = build(node.left, p) + node.string + build(node.right, p)
    if p >= prev:
        return s
    else:
        return '(' + s + ')'


def solve(numbers, target):
    """find operations using numbers to get target
    
    Arguments:
        numbers {list of (int)} -- numbers to use
        target {int} -- target number
    
    Returns:
        list of (str) -- list of strings with the results
    """
    results = []
    solutions = get_solutions(numbers, target)
    if solutions is not None:    
        for solution in solutions:
            results.append(build(dismantle(parse(solution, numbers))))

    return results