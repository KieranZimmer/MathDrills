import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill

def cor_float(f):   #round off floating point inaccuracies to at most two decimal places
    r1 = round(f)
    r2 = round(f, 1)
    r3 = round(f, 2)
    if (r1 == r2):
        return r1
    elif (r2 == r3):
        return r2
    else:
        return r3


class PercentageDrill(AbstractDrill):
    num_probs = 15

    @classmethod
    def build_drill_pdf(cls, params):
        pdf=FPDF()
        np.random.seed(params["rand_seed"])

        # a = 20, b = 50, c = 40%
        # a / b * 100 = c

        # 40% of 50 is what number?   20     50 * 40 / 100
        # What number is 40% of 50?   20     b * c / 100

        # 20 is what percent of 50?   40%    20 / 50 * 100
        # What percent of 50 is 20?   40%    a / b * 100

        # 40% of what number is 20?   50     20 / 40 * 100
        # 20 is 40% of what number?   50     a / c * 100
        # What number is 20 40% of?   50

        # advanced: percent more, percent less

        # numbers represent a, b, and c
        q_text = [[["What number is ", 2, "% of ", 1, "?"], ["", 2, "% of ", 1, " is what number?"]],
                  [["What percent of ", 1, " is ", 0, "?"], ["", 0, " is what percent of ", 1, "?"]],
                  [["", 0, " is ", 2, "% of what number?"], ["", 2, "% of what number is ", 0, "?"]]]

        x_step = 95
        y_step = 14

        for loop in range(params["num_drills"]):
            pdf.add_page()

            num_qs = 18  #Should be divisible by 6
            q_type = np.random.permutation([0] * (num_qs // 3) + [1] * (num_qs // 3) + [2] * (num_qs // 3))  #Random question order
            q_text_type = np.random.randint(0, 2, num_qs)  #Randomize text variety
            nums = []

            for i in range(num_qs):
                d = np.random.randint(1, 100)
                a = np.random.randint(1, 100) * d
                b = 1 * 2 ** np.random.randint(0, 4) * 5 ** np.random.randint(0, 4) * d  #Ensures no infinite decimals
                c = cor_float(a / b * 100)

                nums += [[a,b,c]]  #creates the three numbers for each question

                pdf.set_font('Courier', '', 16)
                pdf.cell(15, y_step, str(i + 1) + ".")
                pdf.set_font('Helvetica', '', 16)
                if q_type[i] == 0:
                    pdf.cell(x_step, y_step, q_text[q_type[i]][q_text_type[i]][0]  #question text
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][1]]) + q_text[q_type[i]][q_text_type[i]][2]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][3]]) + q_text[q_type[i]][q_text_type[i]][4])
                    pdf.set_font('Helvetica', 'U', 16)  #underline for answer space
                    pdf.cell(x_step, y_step, " " * 45)
                    pdf.set_font('Helvetica', '', 16)
                elif q_type[i] == 1:
                    pdf.cell(x_step, y_step, q_text[q_type[i]][q_text_type[i]][0]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][1]]) + q_text[q_type[i]][q_text_type[i]][2]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][3]]) + q_text[q_type[i]][q_text_type[i]][4])
                    pdf.set_font('Helvetica', 'U', 16)
                    pdf.cell(x_step, y_step, " " * 45)
                    pdf.set_font('Helvetica', '', 16)
                elif q_type[i] == 2:
                    pdf.cell(x_step, y_step, q_text[q_type[i]][q_text_type[i]][0]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][1]]) + q_text[q_type[i]][q_text_type[i]][2]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][3]]) + q_text[q_type[i]][q_text_type[i]][4])
                    pdf.set_font('Helvetica', 'U', 16)
                    pdf.cell(x_step, y_step, " " * 45)
                    pdf.set_font('Helvetica', '', 16)
                pdf.ln()

            pdf.add_page()

            for i in range(num_qs):
                pdf.set_font('Courier', '', 16)
                pdf.cell(15, y_step, str(i + 1) + ".")
                pdf.set_font('Helvetica', '', 16)
                if q_type[i] == 0:
                    pdf.cell(x_step, y_step, q_text[q_type[i]][q_text_type[i]][0]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][1]]) + q_text[q_type[i]][q_text_type[i]][2]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][3]]) + q_text[q_type[i]][q_text_type[i]][4])
                    pdf.cell(100, y_step, str(nums[i][1]) + " x " + str(nums[i][2]) #answers
                             + " ÷ 100 = " + str(nums[i][0]))
                elif q_type[i] == 1:
                    pdf.cell(x_step, y_step, q_text[q_type[i]][q_text_type[i]][0]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][1]]) + q_text[q_type[i]][q_text_type[i]][2]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][3]]) + q_text[q_type[i]][q_text_type[i]][4])
                    pdf.cell(100, y_step, str(nums[i][0]) + " ÷ " + str(nums[i][1])
                             + " x 100 = " + str(nums[i][2]) + "%")
                elif q_type[i] == 2:
                    pdf.cell(x_step, y_step, q_text[q_type[i]][q_text_type[i]][0]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][1]]) + q_text[q_type[i]][q_text_type[i]][2]
                             + str(nums[i][q_text[q_type[i]][q_text_type[i]][3]]) + q_text[q_type[i]][q_text_type[i]][4])
                    pdf.cell(100, y_step, str(nums[i][0]) + " ÷ " + str(nums[i][2])
                             + " x 100 = " + str(nums[i][1]))
                pdf.ln()

        pdf.output(params["drill_name"] + ".pdf", 'F')