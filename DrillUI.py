import tkinter as tk
import MathDrillGenerator
from AbstractDrill import AbstractDrill

drill_settings = dict.fromkeys(["rand_seed", "drill_name"])
drill_types = AbstractDrill.drill_types
comp_type = "pdf"     #build drill through latex or FPDF

def user_prompt():
    """
    User interface for changing drill parameters. Currently supports
    changing drill seed and drill type.
    """
    root = tk.Tk()

    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack()

    label1 = tk.Label(root, text="Drill seed (leave blank for random)")
    entry1 = tk.Entry(root)
    canvas.create_window(200, 10, window=label1)
    canvas.create_window(200, 40, window=entry1)

    label2 = tk.Label(root, text="Select drill type")

    var_drill_type = tk.StringVar(root)
    var_drill_type.set(drill_types[0])
    dropdown1 = tk.OptionMenu(root, var_drill_type, *drill_types)

    canvas.create_window(200, 70, window=label2)
    canvas.create_window(200, 100, window=dropdown1)

    var_compile_type = tk.StringVar(root)
    var_compile_type.set(comp_type)

    R1 = tk.Radiobutton(root, text="PDF", variable=var_compile_type, value="pdf")
    R2 = tk.Radiobutton(root, text="LaTeX", variable=var_compile_type, value="latex")

    canvas.create_window(170, 130, window=R1)
    canvas.create_window(230, 130, window=R2)

    def gen_drill_with_input():
        drill_settings["rand_seed"] = entry1.get()
        drill_type = var_drill_type.get()
        compile_type = var_compile_type.get()

        MathDrillGenerator.build_drill_external(drill_type, compile_type, drill_settings)

    button1 = tk.Button(text='Use random seed', command=gen_drill_with_input)
    canvas.create_window(200, 180, window=button1)

    root.mainloop()


user_prompt()

