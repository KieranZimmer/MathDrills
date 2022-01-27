# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:46:55 2021

@author: Kieran
"""

import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill

def dec_ex(num, den):
    ans = ["","",""] #integer part, non-repeating fraction, repeating fraction
    ans[0] = str(num // den)
    if num % den == 0:
        return ans

    rem = [num % den]
    quo = []
    crem = num % den * 10
    while True:
        quo += [crem // den]
        crem = crem % den
        if crem == 0: #if the decimal terminates
            ans[1] = "".join([str(a) for a in quo])
            return ans
        elif crem in rem:   #if it begins to repeat
            ind = rem.index(crem)
            ans[1] = "".join([str(a) for a in quo[:ind]])
            ans[2] = "".join([str(a) for a in quo[ind:]])
            return ans
        else:
            rem += [crem]
        crem = crem * 10

def test(): #utility function to test correctness of dec_ex()
    fails = []
    for i in range(1,400):
        for j in range(1,400):
            ex = dec_ex(i,j)
            s1 = ""
            s2 = str(i/j)
            if ex[1] == "" and ex[2] == "":  #integer case
                s1 = str(ex[0]) + ".0"
            elif ex[2] == "":   #termination decimal case
                s1 = str(ex[0]) + "." + str(ex[1])
            else:   #repeating decimal case
                s1 = str(ex[0]) + "." + str(ex[1]) + str(ex[2]) * 20
                mlen = min(len(s1), len(s2))
                s1 = s1[:mlen - 2]  #peel off last two digits to account for rounding
                s2 = s2[:mlen - 2]
            if s1 != s2:
                fails += [(i,j)]
    print(len(fails))
    return fails

def print_dec_pdf(pdf, dec, x, y):
    pdf.set_xy(x, y)
    if dec[1] == dec[2] == "":
        pdf.write(0, dec[0])
    else:
        pdf.write(0, dec[0] + "." + dec[1] + dec[2])
    pdf.set_xy(x + pdf.get_string_width(dec[0] + "." + dec[1]), y - 5.5)
    pdf.write(0, "_" * len(dec[2]))

class DecimalExpansionDrill(AbstractDrill):

    @classmethod
    def gen_nums(cls):
        row = np.random.permutation([1,2,3,4,5,6,7,8,9,10,11])[:10]
        col = np.random.permutation([2,3,4,5,6,7,8,9,10,11,12])
        ans = [[dec_ex(x,y) for x in row] for y in col]

        return row, col, ans

    @classmethod
    def build_drill_pdf(cls, params):
        np.random.seed(params["rand_seed"])
        pdf = FPDF()

        for loop in range(params["num_drills"]):
            pdf.add_page('L')
            pdf.set_font('Helvetica', 'B', 16)
            x_step = 26
            y_step = 10

            row, col, ans = cls.gen_nums()

            # generate drill
            pdf.cell(15, y_step, "/", border=1, align='C')
            for cell in row:
                pdf.cell(x_step, y_step, str(cell), border=1, align='C')
            pdf.ln()

            for c in col:
                pdf.cell(15, y_step, str(c), border=1, align='C')
                for d in row:
                    pdf.cell(x_step, y_step, "", border=1)
                pdf.ln()

            pdf.add_page('L')

            # generate drill answers
            pdf.set_font('Helvetica', 'B', 16)
            pdf.cell(15, y_step, "/", border=1, align='C')
            for cell in row:
                pdf.cell(x_step, y_step, str(cell), border=1, align='C')
            pdf.ln()

            for i, ans_row in enumerate(ans):
                pdf.set_font('Helvetica', 'B', 16)
                pdf.cell(15, y_step, str(col[i]), border=1, align='C')
                pdf.set_font('Helvetica', '', 16)
                for ans_cell in ans_row:
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.cell(x_step, y_step, "", border=1, align='C')
                    print_dec_pdf(pdf, ans_cell, x, y + y_step / 2)
                    pdf.set_xy(x + x_step, y)
                pdf.ln(y_step)

        pdf.output(params["drill_name"] + ".pdf", 'F')

