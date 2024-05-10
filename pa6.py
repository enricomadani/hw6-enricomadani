#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:12:44 2024

@author: enricoalmadani
"""


def make_change(total):
    '''generate all possible coin changes'''
    coins = [1, 5, 10, 25, 100]
   
    def generate_changes(total, index, current_change):
        if total == 0:
            result.append(current_change)
            return
        for i in range(index, len(coins)):
            if total - coins[i] >= 0:
                generate_changes(total - coins[i], i,
                                 current_change + [coins[i]])
    result = []
    generate_changes(total, 0, [])
    return result


def dict_filter(function, dictionary):
    '''filtering dictionary using function'''
    filtered_dict = {}
    for key, value in dictionary.items():
        if function(key, value):
            filtered_dict[key] = value
    return filtered_dict


def treemap(function, tree):
    '''modify tree using function'''
    tree.key, tree.value = function(tree.key, tree.value)
    if not tree.children:
        return
    for child in tree.children:
        treemap(function, child)


class DTree():
    def __init__(self, variable, threshold, lessequal, greater, outcome):
        '''constructing tree'''
        if (variable is None and threshold is None and lessequal
            is None and greater is None) and (outcome is None):
            raise ValueError("Either all four of the first four \
                             arguments should be None or the last argument \
                             should be None, but not both.")
        if (variable is not None or threshold is not None or 
            lessequal is not None or greater is 
            not None) and (outcome is not None):
            raise ValueError("Either all four of the first four arguments \
                             should be None or the last argument \
                             should be None, but not both.")
        self.variable = variable
        self.threshold = threshold
        self.lessequal = lessequal
        self.greater = greater
        self.outcome = outcome

    def tuple_atleast(self):
        '''determine the minimum size of tuple depending \
            on the variable used'''
        variables = set()
        
        def traverse(node):
            if node is None:
                return
            if node.variable is not None:
                variables.add(node.variable)
            traverse(node.lessequal)
            traverse(node.greater)
        traverse(self)
        return max(variables) + 1 if variables else 0

    def find_outcome(self, observations):
        '''finding the outcome given observations'''
        if self.outcome is not None:
            return self.outcome
        var = observations[self.variable]
        if var <= self.threshold:
            return self.lessequal.find_outcome(observations)
        else:
            return self.greater.find_outcome(observations)

    def no_repeats(self):
        '''return True if variable is inspected more than \
            once, and False otherwise'''
        def helper(node, variable_counts={}):
            if node.outcome is not None:
                return True
            variable_counts[node.variable] = variable_counts.get(node.variable, 0) + 1
            if node.lessequal and not helper(node.lessequal, variable_counts):
                return False
            if node.greater and not helper(node.greater, variable_counts):
                return False
            for count in variable_counts.values():
                if count > 1:
                    return False
            return True
        return helper(self)
