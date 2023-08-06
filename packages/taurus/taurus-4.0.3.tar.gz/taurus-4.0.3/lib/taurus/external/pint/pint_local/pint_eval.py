'''
Created on Mar 4, 2015

@author: aaron
'''

from decimal import Decimal
import math
import operator

import token as tokenlib

#for controlling order of operations
_OP_PRIORITY = {
    '**' : 3,
    '^' : 3,
    'unary' : 2,
    '*' : 1,
    '' : 1, #operator for implicit ops
    '/' : 1,
    '+' : 0,
    '-' : 0
}

_BINARY_OPERATOR_MAP = {
    '**': operator.pow,
    '*': operator.mul,
    '': operator.mul, #operator for implicit ops
    '/': operator.truediv,
    '+': operator.add,
    '-': operator.sub
}

_UNARY_OPERATOR_MAP = {
    '+': lambda x : x,
    '-': lambda x : x * -1
}


class EvalTreeNode(object):
    
    def __init__(self, left, operator=None, right=None):
        '''
        left + operator + right --> binary op
        left + operator --> unary op
        left + right --> implicit op
        left --> single value
        '''
        self.left = left
        self.operator = operator
        self.right = right
        
    def to_string(self):
        #for debugging purposes
        if self.right:
            comps = [self.left.to_string()]
            if self.operator:
                comps.append(self.operator[1])
            comps.append(self.right.to_string())
        elif self.operator:
            comps = [self.operator[1], self.left.to_string()]
        else:
            return self.left[1]
        return '(%s)' % ' '.join(comps)
    
    def evaluate(self, define_op, bin_op=_BINARY_OPERATOR_MAP, un_op=_UNARY_OPERATOR_MAP):
        '''
        define_op is a callable that translates tokens into objects
        bin_op and un_op provide functions for performing binary and unary operations
        '''
        
        if self.right:
            #binary or implicit operator
            op_text = self.operator[1] if self.operator else ''
            if op_text not in bin_op:
                raise Exception('missing binary operator "%s"' % op_text)
            left = self.left.evaluate(define_op, bin_op, un_op)
            return bin_op[op_text](left, self.right.evaluate(define_op, bin_op, un_op))
        elif self.operator:
            #unary operator
            op_text = self.operator[1]
            if op_text not in un_op:
                raise Exception('missing unary operator "%s"' % op_text)
            return un_op[op_text](self.left.evaluate(define_op, bin_op, un_op))
        else:
            #single value
            return define_op(self.left)
        

def build_eval_tree(tokens, op_priority=_OP_PRIORITY, index=0, depth=0, prev_op=None, ):
    '''
    Params:
    Index, depth, and prev_op used recursively, so don't touch.
    Tokens is an iterable of tokens from an expression to be evaluated.
    
    Transform the tokens from an expression into a recursive parse tree, following order of operations.
    Operations can include binary ops (3 + 4), implicit ops (3 kg), or unary ops (-1).
    
    General Strategy:
    1) Get left side of operator
    2) If no tokens left, return final result
    3) Get operator
    4) Use recursion to create tree starting at token on right side of operator (start at step #1)
    4.1) If recursive call encounters an operator with lower or equal priority to step #2, exit recursion
    5) Combine left side, operator, and right side into a new left side
    6) Go back to step #2
    '''
    if depth == 0 and prev_op == None:
        #ensure tokens is list so we can access by index
        tokens = list(tokens)
        
    result = None
    
    while True:
        current_token = tokens[index]
        token_type = current_token[0]
        token_text = current_token[1]
        
        if token_type == tokenlib.OP:
            if token_text == ')':
                if prev_op == None:
                    raise Exception('unopened parentheses in tokens: %s' % current_token)
                elif prev_op == '(':
                    #close parenthetical group
                    return result, index
                else:
                    #parenthetical group ending, but we need to close sub-operations within group
                    return result, index - 1
            elif token_text == '(':
                #gather parenthetical group
                right, index = build_eval_tree(tokens, op_priority, index+1, 0, token_text)
                if not tokens[index][1] == ')':
                    raise Exception('weird exit from parentheses')
                if result:
                    #implicit op with a parenthetical group, i.e. "3 (kg ** 2)"
                    result = EvalTreeNode(left=result, right=right)
                else:
                    #get first token
                    result = right
            elif token_text in op_priority:
                if result:
                    #equal-priority operators are grouped in a left-to-right order, unless they're
                    #exponentiation, in which case they're grouped right-to-left
                    #this allows us to get the expected behavior for multiple exponents 
                    #    (2^3^4)  --> (2^(3^4))
                    #    (2 * 3 / 4) --> ((2 * 3) / 4)
                    if op_priority[token_text] <= op_priority.get(prev_op, -1) and token_text not in ['**', '^']:
                        #previous operator is higher priority, so end previous binary op
                        return result, index - 1
                    #get right side of binary op
                    right, index = build_eval_tree(tokens, op_priority, index+1, depth+1, token_text)
                    result = EvalTreeNode(left=result, operator=current_token, right=right)
                else:
                    #unary operator
                    right, index = build_eval_tree(tokens, op_priority, index+1, depth+1, 'unary')
                    result = EvalTreeNode(left=right, operator=current_token)
        elif token_type == tokenlib.NUMBER or token_type == tokenlib.NAME:
            if result:
                #tokens with an implicit operation i.e. "1 kg"
                if op_priority[''] <= op_priority.get(prev_op, -1):
                    #previous operator is higher priority than implicit, so end previous binary op
                    return result, index - 1
                right, index = build_eval_tree(tokens, op_priority, index, depth+1, '')
                result = EvalTreeNode(left=result, right=right)
            else:
                #get first token
                result = EvalTreeNode(left=current_token)
        
        if tokens[index][0] == tokenlib.ENDMARKER:
            if prev_op == '(':
                raise Exception('unclosed parentheses in tokens')
            if depth > 0 or prev_op:
                #have to close recursion
                return result, index
            else:
                #recursion all closed, so just return the final result
                return result
            
        if index + 1 >= len(tokens):
            #should hit ENDMARKER before this ever happens
            raise Exception('unexpected end to tokens')
        
        index += 1

def _test_build_tree(input_text):
    '''
    
    ####
    >>> _test_build_tree('3') #single number
    u'3'
    >>> _test_build_tree('1 + 2') #basic addition
    u'(1 + 2)'
    >>> _test_build_tree('2 * 3 + 4') #order of operations
    u'((2 * 3) + 4)'
    >>> _test_build_tree('2 * (3 + 4)') #parentheses
    u'(2 * (3 + 4))'
    >>> _test_build_tree('1 + 2 * 3 ** (4 + 3 / 5)') #more order of operations
    u'(1 + (2 * (3 ** (4 + (3 / 5)))))'
    >>> _test_build_tree('1 * ((3 + 4) * 5)') #nested parentheses at beginning
    u'(1 * ((3 + 4) * 5))'
    >>> _test_build_tree('1 * (5 * (3 + 4))') #nested parentheses at end
    u'(1 * (5 * (3 + 4)))'
    >>> _test_build_tree('1 * (5 * (3 + 4) / 6)') #nested parentheses in middle
    u'(1 * ((5 * (3 + 4)) / 6))'
    >>> _test_build_tree('-1') #unary
    u'(- 1)'
    >>> _test_build_tree('3 * -1') #unary
    u'(3 * (- 1))'
    >>> _test_build_tree('3 * --1') #double unary
    u'(3 * (- (- 1)))'
    >>> _test_build_tree('3 * -(2 + 4)') #parenthetical unary
    u'(3 * (- (2 + 4)))'
    >>> _test_build_tree('3 * -((2 + 4))') #parenthetical unary
    u'(3 * (- (2 + 4)))'
    >>> _test_build_tree('3 4') #implicit op
    u'(3 4)'
    >>> _test_build_tree('3 (2 + 4)') #implicit op, then parentheses
    u'(3 (2 + 4))'
    >>> _test_build_tree('(3 ** 4 ) 5') #parentheses, then implicit
    u'((3 ** 4) 5)'
    >>> _test_build_tree('3 4 ** 5') #implicit op, then exponentiation
    u'(3 (4 ** 5))'
    >>> _test_build_tree('3 4 + 5') #implicit op, then addition
    u'((3 4) + 5)'
    >>> _test_build_tree('3 ** 4 5') #power followed by implicit
    u'((3 ** 4) 5)'
    >>> _test_build_tree('3 (4 ** 5)') #implicit with parentheses
    u'(3 (4 ** 5))'
    >>> _test_build_tree('3e-1') #exponent with e
    u'3e-1'
    
    >>> _test_build_tree('kg ** 1 * s ** 2') #multiple units with exponents
    u'((kg ** 1) * (s ** 2))'
    >>> _test_build_tree('kg ** -1 * s ** -2') #multiple units with neg exponents
    u'((kg ** (- 1)) * (s ** (- 2)))'
    >>> _test_build_tree('kg^-1 * s^-2') #multiple units with neg exponents
    u'((kg ^ (- 1)) * (s ^ (- 2)))'
    >>> _test_build_tree('kg^-1 s^-2') #multiple units with neg exponents, implicit op
    u'((kg ^ (- 1)) (s ^ (- 2)))'
    
    >>> _test_build_tree('2 ^ 3 ^ 2') #nested power
    u'(2 ^ (3 ^ 2))'
    
    >>> _test_build_tree('gram * second / meter ** 2') #nested power
    u'((gram * second) / (meter ** 2))'
    >>> _test_build_tree('gram / meter ** 2 / second') #nested power
    u'((gram / (meter ** 2)) / second)'
    
    #units should behave like numbers, so we don't need a bunch of extra tests for them
    >>> _test_build_tree('3 kg + 5') #implicit op, then addition
    u'((3 kg) + 5)'
    '''
    return build_eval_tree(tokenizer(input_text)).to_string()

if __name__ == "__main__":
    import doctest, pint
    from pint.compat import tokenizer
    doctest.testmod()
