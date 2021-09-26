# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:22:45 2021

@author: Kieran
"""

import numpy as np
import os

col_size = 9
rand_seed = 1
np.random.seed(rand_seed)

row = np.random.permutation(np.arange(2,10))
col = [x[0] * 100 + x[1] * 10 + x[2] for x in np.rot90([x for x in map(np.random.permutation, [list(np.arange(1,10))] * 3)])]
ans = [[x * y for x in row] for y in col]

row_str = "$\\times$"
col_str = ""
ans_str = ""

def build_row_str(num):
    global row_str
    row_str += " & " + str(num)
    
def build_col_str(num):
    global col_str
    col_str += str(num) + " \\\\\n"
    
list(map(build_row_str, row))
row_str += " \\\\"
list(map(build_col_str, col))
#print(row_str)
#print(col_str)

#print(ans)

for i in range(len(col)):
    ans_str += str(col[i])
    for j in ans[i]:
        ans_str += " & " + str(j)
    ans_str += " \\\\ "

#print(ans_str)

def build_drill_tex():
    grid_start = open("MathDrills/LatexGridStart.txt", "r").read()
    grid_end = open("MathDrills/LatexGridEnd.txt", "r").read()

    tex = ""
    tex += open("MathDrills/LatexStart.txt", "r").read()
    tex += grid_start
    tex += row_str
    tex += col_str
    tex += grid_end
    tex += "\n\\newpage\n"
    tex += grid_start
    tex += row_str
    tex += ans_str
    tex += grid_end    
    
    tex += open("MathDrills/LatexEnd.txt", "r").read()
    
    f = open("MathDrills/Drill" + str(rand_seed) + ".txt", "w")
    f.write(tex)
    f.close()
    
build_drill_tex()