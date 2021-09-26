# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:46:55 2021

@author: Kieran
"""

import numpy as np

def create_drill(rand_seed):
    col_size = 9
    np.random.seed(rand_seed)
    
    row = np.random.permutation(np.arange(2,10))
    col = [x[0] * 100 + x[1] * 10 + x[2] for x in np.rot90([x for x in map(np.random.permutation, [list(np.arange(1,10))] * 3)])]
    ans = [[x * y for x in row] for y in col]
    
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
    #print(row_str)
    #print(col_str)
    
    #print(ans)
    
    for i in range(len(col)):
        ans_str += str(col[i])
        for j in ans[i]:
            ans_str += " & " + str(j)
        ans_str += " \\\\ "
    
    return (row_str, col_str, ans_str)