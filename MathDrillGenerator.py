# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:22:45 2021

@author: Kieran
"""

import numpy as np
import os
import subprocess
import platform
from AbstractDrill import AbstractDrill
from MultiplicationDrill import MultiplicationDrill as multi
from FractionAdditionDrill import FractionAdditionDrill as frac
from DivisionDrill import DivisionDrill as div
from SkipCountingDrill import SkipCountingDrill as skip
from DistributivePropertyDrill import DistributivePropertyDrill as distrib
from MultiplicationTableDrill import MultiplicationTableDrill as multi_tab

rand_seed = 123
drill_type = "multi"
drill_types = AbstractDrill.drill_types
drill_type_name = AbstractDrill.drill_type_name
drill_name = drill_type_name[drill_type] + ' ' + str(rand_seed)
drill = {"multi": multi, "frac": frac, "div": div, "skip": skip, "distrib": distrib, "multi_tab": multi_tab}

def build_drill_tex():
    """
    Create a .tex file that will build the drill
    """
    row_str, col_str, ans_str = drill[drill_type].gen_latex_strings(rand_seed)
    
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
    
    f = open(drill_name + ".tex", "w")
    f.write(tex)
    f.close()
    
def compile_latex():
    """
    Use command line argument to compile the generated tex file with pdflatex
    """
    if platform.system() == 'Windows':
        ret = subprocess.run(['pdflatex', drill_name + ".tex"], shell=True)
    elif platform.system() == 'Linux':
        ret = subprocess.run(['pdflatex', drill_name + ".tex"])
        
    if ret.returncode != 0:
        print("Call to pdflatex failed, drill not created as pdf. Please ensure that pdflatex is installed.")
    elif os.path.isfile(drill_name + ".pdf") == False:
        print("Call to pdflatex successful but drill not produced. Please check TeX packages.")
    else:
        print("Drill pdf successfully produced.")

def build_drill(drill_type, compile_type, params):
    """
    Build drill with parameters passed in from an external UI function.
    """
    #set random seed
    params["rand_seed"] = int(params["rand_seed"]) if params["rand_seed"] not in (None, '') \
        else np.random.randint(9999999)
    params["drill_name"] = drill_type_name[drill_type] + ' ' + str(params["rand_seed"])  #set drill name
    params["num_drills"] = int(params["num_drills"]) if params["num_drills"] not in (None, '') else 1

    #print("MathDrilLGenerator parameters: ", params)

    # build drill with latex
    if compile_type == "latex":
        build_drill_tex()
        compile_latex()
    elif compile_type == "pdf":
        drill[drill_type].build_drill_pdf(params)