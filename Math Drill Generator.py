# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:22:45 2021

@author: Kieran
"""

import numpy as np
import os
import MultiplicationDrill as multi
import FractionAdditionDrill as frac

rand_seed = 7
#multi or frac
drill_type = "frac"
drills = {"multi":multi.create_drill, "frac":frac.create_drill}  

row_str, col_str, ans_str = drills[drill_type](rand_seed)

def build_drill_tex():
    grid_start = open("LatexGridStart.txt", "r").read()
    grid_end = open("LatexGridEnd.txt", "r").read()

    tex = ""
    tex += open("LatexStart.txt", "r").read()
    tex += grid_start
    tex += row_str
    tex += col_str
    tex += grid_end
    tex += "\n\\newpage\n"
    tex += grid_start
    tex += row_str
    tex += ans_str
    tex += grid_end    
    
    tex += open("LatexEnd.txt", "r").read()
    
    f = open("Drill" + str(rand_seed) + ".txt", "w")
    f.write(tex)
    f.close()
    
build_drill_tex()