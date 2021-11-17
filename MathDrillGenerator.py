# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:22:45 2021

@author: Kieran
"""

import numpy as np
import os
import subprocess
import platform
from fpdf import FPDF
import tkinter as tk
from AbstractDrill import AbstractDrill
from MultiplicationDrill import MultiplicationDrill as multi
from FractionAdditionDrill import FractionAdditionDrill as frac
from DivisionDrill import DivisionDrill as div
from SkipCountingDrill import SkipCountingDrill as skip
from DistributivePropertyDrill import DistributivePropertyDrill as distrib

rand_seed = 123
drill_type = "multi"
drill_types = AbstractDrill.drill_types
drill_type_name = AbstractDrill.drill_type_name
drill_name = drill_type_name[drill_type] + " Drill " + str(rand_seed)
drill = {"multi": multi, "frac": frac, "div": div, "skip": skip, "distrib": distrib}
comp_type = "pdf"     #build drill through latex or FPDF
row_len = 8
col_len = 9

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
        
def build_drill_pdf():
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    x_step = 20
    y_step = 10
    
    
    row, col, ans = drill[drill_type].gen_fpdf_strings(rand_seed)
    
    #generate drill
    for cell in row:
        pdf.cell(x_step, y_step, cell, border=1, align='C')
    pdf.ln()
    
    for i in range(col_len):
        pdf.cell(x_step, y_step, col[i], border=1, align='C')
        for j in range(row_len):
            pdf.cell(x_step, y_step, "", border = 1)
        pdf.ln()
        
    pdf.ln(20)
    #pdf.add_page()
    
    #generate drill answers
    for cell in row:
        pdf.cell(x_step, y_step, cell, border=1, align='C')
    pdf.ln()
    
    for i,ans_row in enumerate(ans):
        pdf.set_font('Arial','B',16)
        pdf.cell(x_step, y_step, col[i], border=1, align='C')
        pdf.set_font('Arial','',16)
        for ans_cell in ans_row:
            pdf.cell(x_step, y_step, ans_cell, border=1, align='C')
        pdf.ln()
    
    
    pdf.output(drill_name + ".pdf",'F')
            
def build_drill(compile_type = "latex"):
    """
    Build drill with parameters passed from user_prompt function in MathDrillGenerator
    """
    #build drill with latex
    if compile_type == "latex":
        build_drill_tex()
        compile_latex()
    elif compile_type == "pdf":
        drill[drill_type].build_drill_pdf(rand_seed, drill_name)

def build_drill_external(drill_type, compile_type, params):
    """
    Build drill with parameters passed in from an external UI function.
    """
    #set random seed
    params["rand_seed"] = int(params["rand_seed"]) if params["rand_seed"] not in (None, '') \
        else np.random.randint(9999999)
    params["drill_name"] = drill_type_name[drill_type] + " Drill " + str(params["rand_seed"])  #set drill name
    params["num_drills"] = int(params["num_drills"]) if params["num_drills"] not in (None, '') else 1

    # build drill with latex
    if compile_type == "latex":
        build_drill_tex()
        compile_latex()
    elif compile_type == "pdf":
        drill[drill_type].build_drill_pdf(params)

def user_prompt():
    """
    User interface for changing drill parameters. Currently supports
    changing drill seed and drill type.
    """
    root = tk.Tk()
    
    canvas = tk.Canvas(root, width = 400, height = 300)
    canvas.pack()
    
    label1 = tk.Label(root, text="Drill seed (leave blank for random)")
    entry1 = tk.Entry(root) 
    canvas.create_window(200, 10, window=label1)
    canvas.create_window(200, 40, window=entry1)
    
    label2 = tk.Label(root, text="Select drill type")
    
    var_drill_type = tk.StringVar(root)
    var_drill_type.set(drill_type)
    dropdown1 = tk.OptionMenu(root, var_drill_type, *drill_types)
    
    canvas.create_window(200,70, window=label2)
    canvas.create_window(200,100,window=dropdown1)
    
    var_compile_type = tk.StringVar(root)
    var_compile_type.set(comp_type)
    
    R1 = tk.Radiobutton(root, text="PDF", variable=var_compile_type, value="pdf")
    R2 = tk.Radiobutton(root, text="LaTeX", variable=var_compile_type, value="latex")
    
    canvas.create_window(170,130,window=R1)
    canvas.create_window(230,130,window=R2)
    
    def gen_drill_with_input():  
        #build_drill_pdf()
        x1 = entry1.get()
        x1 = int(x1) if x1 != '' else np.random.randint(9999999)
        x2 = var_drill_type.get()
        x3 = var_compile_type.get()
        print(x1, x2, x3)
        global rand_seed
        global drill_type
        global drill_name
        rand_seed = x1
        drill_type = x2
        drill_name = drill_type_name[drill_type] + " Drill " + str(rand_seed) 
        
        build_drill(x3)    
   
    button1 = tk.Button(text='Use random seed', command=gen_drill_with_input)
    canvas.create_window(200, 180, window=button1)

    root.mainloop()