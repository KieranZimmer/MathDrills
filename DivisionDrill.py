# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 15:53:46 2021

@author: Kieran
"""

import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill


class DivisionDrill(AbstractDrill):
    drill_param_list = ["#perpage"]
    drill_param_text = {"#perpage": "Two drills per page"}
    #0: binary default no, 1: binary default yes, 2: text entry
    drill_param_input = {"#perpage": 1}

    col_len = 9
    row_len = 8

    @classmethod
    def gen_nums(cls):

        row = np.random.permutation(np.arange(2,10))
        col = [x[0] * 100 + x[1] * 10 + x[2] for x in np.rot90([x for x in map(np.random.permutation, [list(np.arange(1,10))] * 3)])]
        ans = [[(y//x,y%x) for x in row] for y in col]

        return (row, col, ans)

    @classmethod
    def str_div(cls, div):
        """
        Represent quotients with remainders as strings.
        """
        if div[1] == 0:
            return str(div[0])
        return str(div[0]) + ',' + str(div[1])

    @classmethod
    def gen_latex_strings(cls):
        """
        Returns three strings, for the drill row, column, and answers, ready to
        be compiled into LaTeX.
        """
        row, col, ans = cls.gen_nums()

        row_str = "$\\div$"
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
                ans_str += " & " + cls.str_div(j)
            ans_str += " \\\\ "

        return (row_str, col_str, ans_str)

    @classmethod
    def gen_fpdf_strings(cls):
        """
        Returns three lists of strings, for the drill row, column, and answers,
        ready to be set into a PDF using the FPDF library.
        """
        row, col, ans = cls.gen_nums()

        row = ['x'] + list(map(str, row))
        col = list(map(str, col))
        ans = [list(map(cls.str_div, x)) for x in ans]

        return (row, col, ans)

    @classmethod
    def build_drill_pdf(cls, params):
        pdf = FPDF()
        np.random.seed(params["rand_seed"])

        for loop in range(params["num_drills"]):
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 16)
            x_step = 20
            y_step = 10

            drill_nums = [cls.gen_fpdf_strings()]
            if params["#perpage"]:
                drill_nums.append(cls.gen_fpdf_strings())

            # generate drill
            for row, col, ans in drill_nums:
                for cell in row:
                    pdf.cell(x_step, y_step, cell, border=1, align='C')
                pdf.ln()

                for i in range(cls.col_len):
                    pdf.cell(x_step, y_step, col[i], border=1, align='C')
                    for j in range(cls.row_len):
                        pdf.cell(x_step, y_step, "", border=1)
                    pdf.ln()

                pdf.ln(20)

            pdf.add_page()

            # generate drill answers
            for row, col, ans in drill_nums:
                pdf.set_font('Helvetica', 'B', 16)
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

                pdf.ln(20)

        pdf.output(params["drill_name"] + ".pdf", 'F')