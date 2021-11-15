from fpdf import FPDF
import numpy as np

from AbstractDrill import AbstractDrill


class SkipCountingDrill(AbstractDrill):

    @classmethod
    def build_drill_pdf(cls, rand_seed, drill_name):
        np.random.seed(rand_seed)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', '', 16)
        y_step = 10
        order = np.random.permutation([2,3,4,5,6,7,8,9])
        start_cell = np.random.randint(4,8,8)
        start_num = np.random.randint(1,15,8)
        for i in range(8):
            pdf.cell(-2,0,"")
            pdf.cell(0, 5, "Count by " + str(order[i]) + "s!")
            pdf.ln(7)
            for j in range(12):
                if j != 0:
                    pdf.cell(6, y_step, '>', align='C')
                if j == start_cell[i]:
                    pdf.set_font('Helvetica', 'B', 16)
                    pdf.cell(10, y_step, str(start_num[i] + j * order[i]), border=1, align='C')
                    pdf.set_font('Helvetica', '', 16)
                else: pdf.cell(10, y_step, '', border=1, align='C')
            pdf.ln(25)

        pdf.add_page()

        for i in range(8):
            pdf.cell(-2,0,"")
            pdf.cell(0, 5, "Count by " + str(order[i]) + "s!")
            pdf.ln(7)
            for j in range(12):
                pdf.set_font('Helvetica', '', 16)
                if j != 0:
                    pdf.cell(6, y_step, '>', align='C')
                if j == start_cell[i]:
                    pdf.set_font('Helvetica', 'B', 16)
                pdf.cell(10, y_step, str(start_num[i] + j * order[i]), border=1, align='C')
            pdf.ln(25)

        pdf.output(drill_name + ".pdf", 'F')

    @classmethod
    def build_drill_tex(cls):
        print("TeX not implemented for this drill.")
        pass
