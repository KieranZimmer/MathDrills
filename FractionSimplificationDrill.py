import numpy as np
from fpdf import FPDF
from AbstractDrill import AbstractDrill

def gcf(a, b):
    if a == 0:
        return b
    return gcf(b % a, a)


def coprime(n, *upto):  # generates a list of numbers coprime with n
    return list(filter(lambda x: (gcf(x, n) == 1), np.arange(1, n if upto == () else upto[0] + 1)))


def gen_fracs(max_denom=9, max_mult=20):
    fracs = [np.array((x, y)) for y in np.arange(2, max_denom + 1) for x in coprime(y, max_denom)]
    np.random.shuffle(fracs)
    fracs_mult = [x * np.random.randint(2, max_mult + 1) for x in fracs]
    return fracs_mult, fracs


def print_frac_pdf(pdf, f, x, y):
    flen = max(len(str(f[0])), len(str(f[1])))
    pdf.set_xy(x, y)
    pdf.cell(0.001, 0, str(f[0]), align="C")
    pdf.set_xy(x, y)
    pdf.cell(0.001, 0, "_" * flen, align="C")
    pdf.set_xy(x, y + 6)
    pdf.cell(0.001, 0, str(f[1]), align="C")


def print_str_pdf(pdf, s, x, y):
    pdf.set_xy(x,y)
    pdf.write(0, s)

class FractionSimplificationDrill(AbstractDrill):
    drill_param_list = ["max_gcd"]
    drill_param_text = {"max_gcd": "Maximum common factor to reduce by (default 12)"}
    #0: binary default no, 1: binary default yes, 2: text entry
    drill_param_input = {"max_gcd": 2}

    @classmethod
    def build_drill_pdf(cls, params):
        pdf = FPDF()
        np.random.seed(params["rand_seed"])

        max_gcd = params["max_gcd"]
        max_gcd = 12 if max_gcd == '' else max(min(int(max_gcd), 4), 111)

        pdf.set_font('Helvetica', '', 16)

        for loop in range(params["num_drills"]):
            qfracs, afracs = gen_fracs(max_mult=max_gcd)
            pdf.add_page()

            i = 0
            for qfrac in qfracs:
                pdf.set_font('Courier', '', 16)

                print_str_pdf(pdf, str(i + 1) + ".", 9 + i % 4 * 50, 17 + i // 4 * 15)

                pdf.set_font('Helvetica', '', 16)

                print_frac_pdf(pdf, qfrac, 25 + i % 4 * 50, 15 + i // 4 * 15)
                print_str_pdf(pdf, "=", 32 + i % 4 * 50, 17 + i // 4 * 15)
                i += 1

            pdf.add_page()

            i = 0
            for qfrac, afrac in zip(qfracs, afracs):
                pdf.set_font('Courier', '', 16)

                print_str_pdf(pdf, str(i + 1) + ".", 9 + i % 4 * 50, 17 + i // 4 * 15)

                pdf.set_font('Helvetica', '', 16)

                print_frac_pdf(pdf, qfrac, 25 + i % 4 * 50, 15 + i // 4 * 15)
                print_str_pdf(pdf, "=", 32 + i % 4 * 50, 17 + i // 4 * 15)
                print_frac_pdf(pdf, afrac, 44 + i % 4 * 50, 15 + i // 4 * 15)
                i += 1

        pdf.output(params["drill_name"] + ".pdf", 'F')