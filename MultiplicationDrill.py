# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:46:55 2021

@author: Kieran
"""

import numpy as np

def gen_nums(rand_seed, col_size = 9, row_size = 8):
    np.random.seed(rand_seed)
    
    row = np.random.permutation(np.arange(2,10))
    col = [x[0] * 100 + x[1] * 10 + x[2] for x in np.rot90([x for x in map(np.random.permutation, [list(np.arange(1,10))] * 3)])]
    ans = [[x * y for x in row] for y in col]
    
    return (row, col, ans)
    

def gen_latex_strings(rand_seed, col_size = 9, row_size = 8):
    """
    Returns three strings, for the drill row, column, and answers, ready to
    be compiled into LaTeX.
    """
    row, col, ans = gen_nums(rand_seed)
    
    row_str = "$\\times$"
    col_str = ""
    ans_str = ""
    
    def build_row_str(num):
        return " & " + str(num)
        
    def build_col_str(num):
        return str(num) + " \\\\\n"
        
    for x in map(build_row_str, row):
        row_str += x
    row_str += " \\\\\n"
    
    for x in map(build_col_str, col):
        col_str += x
    
    for i in range(len(col)):
        ans_str += str(col[i])
        for j in ans[i]:
            ans_str += " & " + str(j)
        ans_str += " \\\\ "
    
    return (row_str, col_str, ans_str)

def gen_fpdf_strings(rand_seed, col_size = 9, row_size = 8):
    """
    Returns three lists of strings, for the drill row, column, and answers,
    ready to be set into a PDF using the FPDF library.
    """
    row, col, ans = gen_nums(rand_seed)
    
    row = ['x'] + list(map(str, row))
    col = list(map(str, col))
    ans = [list(map(str, x)) for x in ans]
    
    return (row, col, ans)