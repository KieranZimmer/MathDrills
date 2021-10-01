# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:22:45 2021

@author: Kieran
"""

import numpy as np
import os
import subprocess
import platform
import fpdf
import MultiplicationDrill as multi
import FractionAdditionDrill as frac
import DivisionDrill as div

rand_seed = 100
#multi or frac
drill_type = "div"
drill_type_name = {"multi":"Multiplication", "frac":"Fraction Addition", "div":"Division"}
drill_name = drill_type_name[drill_type] + " Drill " + str(rand_seed) 
drill = {"multi":multi, "frac":frac, "div":div}   
comp_type = "latex"     #build drill through latex or FPDF
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
    #build drill with latex
    if compile_type == "latex":
        build_drill_tex()
        compile_latex()
    elif compile_type == "pdf":
        build_drill_pdf()
    
build_drill(comp_type)