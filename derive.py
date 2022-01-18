"""
Illiasse Mounjim 102277520
CSCI 3415 - Program 1 - Sep 23

This program reads in grammar from a file
asks user to enter a sentence and returns a left most derivation that sentence
if no match is found then NO derivation found .

this program is NOT working with example 3.2.txt and 3.4
sometimes sentences return no derivation is found although a derivation could be derived

"""

import os
import re
import sys
# import pprint

def isnonterminal(non_terminal):
    """ determines if the element is a nonterminal by matching with < >. """
    return isinstance(non_terminal, str) and re.match(r'^<.*>$', non_terminal) is not None


def isterminal(terminal):
    """ if is NOT nonterminal then its terminal. """
    return isinstance(terminal, str) and not isnonterminal(terminal)


def read_grammar(filepath):
    """ Reads in a grammar from a filepath. """
    grammar = []
    current_lhs = None

    def make_rule(lhs, rhs):
        if not isnonterminal(lhs):
            raise Exception(f'LHS {lhs} is not a nonterminal')
        if not rhs:
            raise Exception('Empty RHS')
        return (lhs, rhs)

    def parse_rhs(lexemes):
        rules = []
        rhs = []
        for lex in lexemes:
            if lex == '|':
                rules.append(make_rule(current_lhs, rhs))
                rhs = []
            else:
                rhs.append(lex)
        rules.append(make_rule(current_lhs, rhs))
        return rules

    with open(filepath) as file_path:
        for line in file_path:
            lexemes = line.split()
            if not lexemes:
                pass
            elif len(lexemes) == 1:
                raise Exception(f'Illegal rule {line}')
            elif isnonterminal(lexemes[0]) and lexemes[1] == '->':
                current_lhs = lexemes[0]
                grammar.extend(parse_rhs(lexemes[2:]))
            elif lexemes[0] == '|':
                grammar.extend(parse_rhs(lexemes[1:]))
            else:
                raise Exception(f'Illegal rule {line}')

    return grammar

def print_grammar(grammar):
    """ Prints the grammar in a readable format. """
    for rule in grammar:
        print(f'{rule[0]} -> {" ".join(rule[1])}')


def applicable_rules(grammar, nonterminal):
    """ Return a list of grammar rules for nonterminal. """
    return list(filter(lambda rule: rule[0] == nonterminal, grammar))


def match_form(form, sentence):
    """ return an integer that is the length of the prefix or -1 if no prefix exists. """
    for i, lex in enumerate(form):
        if i == len(sentence):
            return -1
        if isnonterminal(lex):
            return i
        if lex != sentence[i]:
            return -1
    return len(sentence) if len(sentence) == len(form) else -1


def subst(rule, form, match):
    """ Returns the successor sentential form by applying a rule to a form given a match. """
    return form[:match] + rule[1] + form[match + 1:]


def leftmost_derivation(grammar, form, sentence, derivation):
    """ applies recursive depth first search algorithm
     returns the result when it match else it returns none. """
    match = match_form(form, sentence)
    if match == -1:
        return None
    if match == len(sentence):
        return []
    for rule in applicable_rules(grammar, form[match]):
        form = subst(rule, form, match)
        derivation.append(form)
        result = leftmost_derivation(grammar, form, sentence, derivation)
        if result is not None:
            return derivation
    return None


def print_derivation(grammar, derivation):
    """ Prints the left most derivation of a grammar  """
    start = grammar[0][0]
    blank = ' ' * len(start)
    if derivation is None:
        print('No derivation found')
    else:
        for i, form in enumerate(derivation, 1):
            print(f'{i:4d}: {start if i == 1 else blank} -> {" ".join(form)}')


def main():
    """ main function makes calls to all other functions, reads user input and prints. """
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        raise Exception(f'File path {filepath} does not exist.')

    print(f'Reading grammar from {filepath}')
    grammar = read_grammar(filepath)
    print(grammar)
    print_grammar(grammar)
    derivation = []
    form = grammar[0][0]

    while True:
        print('---')
        try:
            sentence_string = input('Enter a sentence:\n')
        except EOFError:
            sys.exit()
        sentence = sentence_string.split()
        # print(sentence)
        derivation = leftmost_derivation(grammar, [form], sentence, derivation)
        # print(derivation)
        print(' '.join(sentence))
        print('Derivation:')
        print_derivation(grammar, derivation)


if __name__ == '__main__':
    main()
