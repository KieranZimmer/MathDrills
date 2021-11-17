import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill

class polynomial:

    def __init__(self, terms):
        self.terms = []
        for term in terms:
            if term[0] != 0:
                self.terms.append(term)

    @classmethod
    def multiply(cls,f1, f2):
        res_terms = {}
        res = []
        for term1 in f1.terms:
            for term2 in f2.terms:
                key = ''.join(sorted(term1[1] + term2[1]))
                if key in res_terms:
                    res_terms[key] += term1[0] * term2[0]
                else:
                    res_terms[key] = term1[0] * term2[0]
        for key,val in res_terms.items():
            res.append((val,key))
        return polynomial(res)

    def __str__(self):
        s = ''
        for ind,term in enumerate(self.terms):
            if term[0] == -1 and term[1] != '':
                s += '-'
            elif term[0] != 1 or term[1] == '':
                s += str(term[0])
            var = term[1]
            while len(var) > 0:
                cnt = var.count(var[0])
                s += var[0]
                if cnt == 2:
                    s += '²'
                elif cnt == 3:
                    s += '³'
                elif cnt > 3:
                    s += '^' + str(cnt)
                var = var[cnt:]
            if ind < len(self.terms) - 1 and self.terms[ind + 1][0] > 0:
                s += '+'
        return s

def rand_sign():
    return 2 * np.random.randint(2) - 1

def gen_probs(num_probs):
    probs = []
    ans = []
    for i in range(num_probs):
        polys = (polynomial([(np.random.randint(1,4) * rand_sign(),'x'),(np.random.randint(1,10) * rand_sign(),'')]),
                 polynomial([(np.random.randint(1,4) * rand_sign(),'x'),(np.random.randint(1,10) * rand_sign(),'')]))
        probs.append(polys)
        ans.append(polynomial.multiply(polys[0],polys[1]))

    return (probs, ans)

class DistributivePropertyDrill(AbstractDrill):
    num_probs = 40

    @classmethod
    def build_drill_pdf(cls, params):
        pdf=FPDF()
        np.random.seed(params["rand_seed"])
        probs, ans = gen_probs(cls.num_probs)

        for loop in range(params["num_drills"]):
            pdf.add_page()
            pdf.set_font('Helvetica','',16)
            x_step = 90
            y_step = 10

            for i in range(cls.num_probs):
                pdf.set_font('Courier', 'B', 14)
                pdf.cell(10, y_step, str(i + 1) + ".")
                pdf.set_font('Helvetica', '', 16)
                pdf.cell(38, y_step, '(' + str(probs[i][0]) + ')(' + str(probs[i][1]) + ')')
                pdf.cell(50, y_step, '=')
                if i % 2 == 1:
                    pdf.ln()

            pdf.add_page()
            for i in range(cls.num_probs):
                pdf.set_font('Courier', 'B', 14)
                pdf.cell(10, y_step, str(i + 1) + ".")
                pdf.set_font('Helvetica', '', 16)
                pdf.cell(38, y_step, '(' + str(probs[i][0]) + ')(' + str(probs[i][1]) + ')')
                pdf.cell(6, y_step, '=')
                pdf.set_font('Courier', 'B', 16)
                pdf.cell(51, y_step, str(ans[i]))
                if i % 2 == 1:
                    pdf.ln()

        pdf.output(params["drill_name"] + ".pdf", 'F')