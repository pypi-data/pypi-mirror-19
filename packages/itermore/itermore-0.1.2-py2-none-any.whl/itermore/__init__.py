#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 11:41:05 2017

@author: Ahmad Albaqsami

University of California Irvine,
Department of Electrical and Computer Science Engineering
Advanced Computer Architecture Group
"""

__author__ = "Ahamd Albaqsami (aalbaqsa@uci.edu)"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2017 Ahmad Albaqsami"
__license__ = "MIT"


def gpermutations(iterable, grouping):
    """
    Same as itertools' permutation but with grouping permutations

    Args:
        iterable -- The list or iterable that will be permuted
        grouping -- a list, with groups listed

    Returns:
        generator -- generator for all possible permutations
                     with given restrictions

    example:
    # A and D are permuted together
    # while B and C are permuted together

    >>> gp = gpermutations(['A','B','C','D'],[1,0,0,1])

    >>> for p in gp:
    ...     print p

    ('A', 'B', 'C', 'D')
    ('A', 'C', 'B', 'D')
    ('D', 'B', 'C', 'A')
    ('D', 'C', 'B', 'A')
    """
    import itertools
    from collections import defaultdict
    import random
    import copy
    groups = list(set(grouping))
    layer_iterable = defaultdict(list)
    group_pos = defaultdict(list)

    for i, (group, elem) in enumerate(zip(grouping, iterable)):
        # print i,group,elem
        layer_iterable[group].append(elem)
        group_pos[group].append(i)

    def par_temp(l_iterable, g_pos):
        select_top_group = random.choice(list(g_pos))
        group_pos_b = copy.deepcopy(g_pos)
        top_group_list = group_pos_b.pop(select_top_group)
        layer_iterable_b = copy.deepcopy(l_iterable)
        top_group_elem = layer_iterable_b.pop(select_top_group)

        if len(g_pos) == 1:
            output = [0]*len(top_group_list)
            for t in itertools.permutations(top_group_elem):
                for i, e in enumerate(t):
                    output[i] = (top_group_list[i], e)
                yield output
        else:
            output = [0]*len(top_group_list)
            for t in itertools.permutations(top_group_elem):
                for i, e in enumerate(t):
                    output[i] = (top_group_list[i], e)
                for t2 in par_temp(layer_iterable_b, group_pos_b):
                    yield output + t2

    if len(groups) == 1:
        for i in itertools.permutations(iterable):
            yield i
    else:
        select_top_group = random.choice(list(group_pos))
        group_pos_b = copy.deepcopy(group_pos)
        top_group_list = group_pos_b.pop(select_top_group)
        layer_iterable_b = copy.deepcopy(layer_iterable)
        top_group_elem = layer_iterable_b.pop(select_top_group)
        n = len(iterable)
        for x in itertools.permutations(top_group_elem):
            output = [0]*n
            for i, elm in enumerate(x):
                output[top_group_list[i]] = elm

            for x2 in par_temp(layer_iterable_b, group_pos_b):
                for i2, elem2 in x2:
                    output[i2] = elem2
                yield tuple(output)
