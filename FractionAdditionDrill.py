# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 21:02:33 2021

@author: Kieran
"""

import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill

def add_fraction(f1,f2):
    f3 = (f1[0]*f2[1] + f1[1]*f2[0], f1[1]*f2[1])
    d = gcf(f3[0],f3[1])
    if d != 1:
        f3 /= d
        f3 = (int(f3[0]), int(f3[1]))
    return f3

def gen_fracs(denom): #generate a list of reduced fractions for use in rows
    return [(y,x) for x in np.arange(2,denom + 1) for y in coprime(x)]
    
def gcf(a,b):
    if a == 0:
        return b
    return gcf(b % a, a)

def coprime(n): #generates a list of numbers coprime with n
    return list(filter(lambda x: (gcf(x,n) == 1), np.arange(1,n)))

def gen_fracs_rand(denom, col_size, row_size): #select random fractions from list
    """
    Generates index row and column by randomly picking from list of possible
    options.
    """
    fracs = np.random.permutation(gen_fracs(col_size))
    col = fracs[0:col_size]
    row = fracs[col_size:col_size + row_size]
    
    return (col, row)
    
def gen_fracs_denom(denom, col_size, row_size): #select one fraction for each denom
    """
    creates an index row and column taking one fraction for each denominator.
    col_size should be one less than denom
    row_size should be one less than col_size
    """
    fracs = [[(y,x) for y in coprime(x)] for x in range(2, denom + 1)]
    col = []
    row = []
    
    for i in range(col_size):
        rem = np.random.randint(len(fracs[i]))
        col += [fracs[i][rem]]
        del fracs[i][rem]
        
    for i in range(1,row_size):
        rem = np.random.randint(len(fracs[i]))
        row += [fracs[i][rem]]

    return (col, row)        

def frac_str_latex(f):
    if f[0] % f[1] == 0:    #for whole numbers
        return str(int(f[0] / f[1]))
    if f[0] > f[1]:         #for improper fractions
        return "$" + str(int(f[0] / f[1])) + "\\frac{" + str(f[0] % f[1]) + "}{" + str(f[1]) + "}$"
    return "$\\frac{" + str(f[0]) + "}{" + str(f[1]) + "}$"  #otherwise

def frac_str_fpdf(f):
    if f[0] % f[1] == 0:    #for whole numbers
        return str(int(f[0] / f[1]))
    if f[0] > f[1]:         #for improper fractions
        return str(int(f[0] / f[1])) + "," + str(f[0] % f[1]) + "/" + str(f[1])
    return str(f[0]) + "/" + str(f[1])  #otherwise

def gen_latex_strings(rand_seed, col_size = 9, row_size = 8):
    np.random.seed(rand_seed)
    
    #generate index row and column
    col, row = gen_fracs_rand(col_size + 1, col_size, row_size)

    #calculate answers
    ans = [[add_fraction(x,y) for x in row] for y in col]
    
    row_str = "+"
    col_str = ""
    ans_str = ""
    
    def build_row_str(num):
        return " & " + frac_str_latex(num)
        
    def build_col_str(num):
        return frac_str_latex(num) + " \\\\\n"
        
    for x in map(build_row_str, row):
        row_str += x
    row_str += " \\\\\n"
    for x in map(build_col_str, col):
        col_str += x
    #print(row_str)
    #print(col_str)
    
    #print(ans)
    
    for i in range(len(col)):
        ans_str += frac_str_latex(col[i])
        for j in ans[i]:
            ans_str += " & " + frac_str_latex(j)
        ans_str += " \\\\ "
    
    return (row_str, col_str, ans_str)

def gen_fpdf_strings(col_size = 9, row_size = 8):
    
    #generate index row and column
    col, row = gen_fracs_rand(col_size + 1, col_size, row_size)

    #calculate answers
    ans = [[add_fraction(x,y) for x in row] for y in col]
    
    row = ['+'] + list(map(frac_str_fpdf, row))
    col = list(map(frac_str_fpdf, col))
    ans = [list(map(frac_str_fpdf, x)) for x in ans]
    
    return (row, col, ans)

class FractionAdditionDrill(AbstractDrill):

    col_len = 9
    row_len = 8

    @classmethod
    def build_drill_pdf(cls, params):
        pdf = FPDF()
        np.random.seed(params["rand_seed"])

        for loop in range(params["num_drills"]):
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 16)
            x_step = 20
            y_step = 10

            row, col, ans = gen_fpdf_strings()

            # generate drill
            for cell in row:
                pdf.cell(x_step, y_step, cell, border=1, align='C')
            pdf.ln()

            for i in range(cls.col_len):
                pdf.cell(x_step, y_step, col[i], border=1, align='C')
                for j in range(cls.row_len):
                    pdf.cell(x_step, y_step, "", border=1)
                pdf.ln()

            pdf.ln(20)
            # pdf.add_page()

            # generate drill answers
            for cell in row:
                pdf.cell(x_step, y_step, cell, border=1, align='C')
            pdf.ln()

            for i, ans_row in enumerate(ans):
                pdf.set_font('Helvetica', 'B', 16)
                pdf.cell(x_step, y_step, col[i], border=1, align='C')
                pdf.set_font('Helvetica', '', 16)
                for ans_cell in ans_row:
                    pdf.cell(x_step, y_step, ans_cell, border=1, align='C')
                pdf.ln()

        pdf.output(params["drill_name"] + ".pdf", 'F')