# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:46:55 2021

@author: Kieran
"""

import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill


class MultiplicationDrill(AbstractDrill):
    col_len = 9
    row_len = 8

    @classmethod
    def gen_nums(cls,rand_seed, col_len = 9, row_len = 8):
        np.random.seed(rand_seed)
    
        row = np.random.permutation(np.arange(2,10))
        col = [x[0] * 100 + x[1] * 10 + x[2] for x in np.rot90([x for x in map(np.random.permutation, [list(np.arange(1,10))] * 3)])]
        ans = [[x * y for x in row] for y in col]
    
        return (row, col, ans)
    
    @classmethod
    def gen_latex_strings(cls, rand_seed, col_len = 9, row_len = 8):
        """
        Returns three strings, for the drill row, column, and answers, ready to
        be compiled into LaTeX.
        """
        row, col, ans = cls.gen_nums(rand_seed)

        row_str = "$\\times$"
        col_str = ""
        ans_str = ""

        def build_row_str(num):
            return " & \\textbf{" + str(num) + "}"

        def build_col_str(num):
            return "\\textbf{" + str(num) + "} \\\\\n"

        for x in map(build_row_str, row):
            row_str += x
        row_str += " \\\\\n"

        for x in map(build_col_str, col):
            col_str += x

        for i in range(len(col)):
            ans_str += "\\textbf{" + str(col[i]) + "}"
            for j in ans[i]:
                ans_str += " & " + str(j)
            ans_str += " \\\\ "

        return (row_str, col_str, ans_str)

    @classmethod
    def gen_fpdf_strings(cls,rand_seed, col_len = 9, row_len = 8):
        """
        Returns three lists of strings, for the drill row, column, and answers,
        ready to be set into a PDF using the FPDF library.
        """
        row, col, ans = cls.gen_nums(rand_seed)

        row = ['x'] + list(map(str, row))
        col = list(map(str, col))
        ans = [list(map(str, x)) for x in ans]

        return (row, col, ans)

    @classmethod
    def build_drill_pdf(cls, rand_seed, drill_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        x_step = 20
        y_step = 10

        row, col, ans = cls.gen_fpdf_strings(rand_seed)

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

        pdf.output(drill_name + ".pdf", 'F')

