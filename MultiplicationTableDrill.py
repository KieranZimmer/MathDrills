import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill

class MultiplicationTableDrill(AbstractDrill):
    drill_param_list = ["rand_ord", "max_num", "inc_one", "inc_ten", "tri"]
    drill_param_text = {"rand_ord": "Randomize number order in row and column",
                        "max_num": "Maximum number in drill (minimum 9, maximum 17, default 12)",
                         "inc_one":"Include one?", "inc_ten": "Include 10?", "tri": "Triangular layout"}
    #0: binary default no, 1: binary default yes, 2: text entry
    drill_param_input = {"rand_ord": 0, "max_num": 2, "inc_one": 0, "inc_ten": 0, "tri": 1}

    @classmethod
    def build_drill_pdf(cls, params):
        pdf = FPDF()
        np.random.seed(params["rand_seed"])

        max_num = params["max_num"]
        max_num = 12 if max_num == '' else min(max(int(max_num), 9), 17)

        orient = 'P'
        if max_num - int(not params["inc_one"]) - int(not params["inc_ten"]) > 12:
            orient = 'L'

        tri = params["tri"]

        x_step = 15
        y_step = 10
        row = np.arange(max_num) + 1
        if params["inc_one"] == 0:
            row = list(filter(lambda x: x != 1, row))
        if params["inc_ten"] == 0:
            row = list(filter(lambda x: x != 10, row))
        col = row

        for loop in range(params["num_drills"]):
            if params["rand_ord"] == 1:  #random order for each drill if parameter is active
                row = np.random.permutation(row)
                col = row

            pdf.add_page(orient)
            pdf.set_font('Helvetica', '', 16)
            pdf.cell(x_step, y_step, 'x', align='C')
            for r in row:
                pdf.cell(x_step, y_step, str(r), align='C')
            for i, c in enumerate(col):
                pdf.ln()
                if tri:
                    for blank in range(i):
                        pdf.cell(x_step, y_step, '')
                pdf.cell(x_step, y_step, str(c), align='C')
                for cell in range(len(col) - i * tri):
                    pdf.cell(x_step, y_step, '', border=1)

            #print answers on new page
            pdf.add_page(orient)
            pdf.cell(x_step, y_step, 'x', align='C')
            for r in row:
                pdf.cell(x_step, y_step, str(r), align='C')
            for i, c in enumerate(col):
                pdf.ln()
                if tri:
                    for blank in range(i):
                        pdf.cell(x_step, y_step, '')
                pdf.cell(x_step, y_step, str(c), align='C')
                for cell in range(len(col) - i * tri):
                    pdf.cell(x_step, y_step, str(c * row[cell + i * tri]), border=1)

        pdf.output(params["drill_name"] + ".pdf", 'F')

    @classmethod
    def build_drill_tex(cls, params):
        pass