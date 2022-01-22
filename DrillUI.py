import tkinter as tk
import MathDrillGenerator
from AbstractDrill import AbstractDrill

drill_settings = dict.fromkeys(AbstractDrill.global_params_list)
drill_types = AbstractDrill.drill_types
drill_names = AbstractDrill.drill_names
comp_type = "pdf"     #build drill through latex or FPDF

def user_prompt():
    """
    User interface for changing drill parameters. Currently supports
    changing drill seed and drill type.
    """
    root = tk.Tk()

    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    label1 = tk.Label(root, text="Drill seed (leave blank for random)")
    entry1 = tk.Entry(root)
    canvas.create_window(250, 10, window=label1)
    canvas.create_window(250, 40, window=entry1)

    label3 = tk.Label(root, text="Number of drill pages to generate")
    entry3 = tk.Entry(root)
    canvas.create_window(250, 70, window=label3)
    canvas.create_window(250, 100, window=entry3)

    label2 = tk.Label(root, text="Select drill type")

    var_drill_name = tk.StringVar(root)
    drill_specific_params = []

    def drill_changed(*args):   #called when the user selects a different drill on the dropdown list
        canvas.delete("specific")   #clear previous drill-specific UI elements
        drill_specific_params.clear()

        drill_type = AbstractDrill.drill_type_name_reversed[var_drill_name.get()]
        drill_cls = AbstractDrill.import_drill(drill_type)
        drill_params = drill_cls.drill_param_list
        i = 0
        for param in drill_params:  #still needs to destroy these when it gets changed
            param_text = drill_cls.drill_param_text[param]
            param_input = drill_cls.drill_param_input[param]
            if param_input <= 1:    #binary parameter
                entry_var = tk.IntVar(root)
                entry_var.set(param_input)
                check = tk.Checkbutton(root, text=param_text, variable=entry_var)   #binary input
                canvas.create_window(250, 220 + 30 * i, tags="specific", window=check)
                drill_specific_params.append((param, entry_var))
                i += 1  #increase spacing
            elif param_input == 2:  #text entry parameter
                entry = tk.Entry(root)  #text input
                label = tk.Label(root, text=param_text)
                canvas.create_window(250, 220 + 30 * i, tags="specific", window=label)
                canvas.create_window(250, 250 + 30 * i, tags="specific", window=entry)
                drill_specific_params.append((param, entry))
                i += 2  #increase spacing

    dropdown1 = tk.OptionMenu(root, var_drill_name, *drill_names, command=drill_changed)

    canvas.create_window(250, 130, window=label2)
    canvas.create_window(250, 160, window=dropdown1)

    var_compile_type = tk.StringVar(root)
    var_compile_type.set(comp_type)

    R1 = tk.Radiobutton(root, text="PDF", variable=var_compile_type, value="pdf")
    R2 = tk.Radiobutton(root, text="LaTeX", variable=var_compile_type, value="latex")

    canvas.create_window(220, 190, window=R1)
    canvas.create_window(280, 190, window=R2)

    def gen_drill_with_input():
        drill_settings["rand_seed"] = entry1.get()
        drill_settings["num_drills"] = entry3.get()
        drill_type = AbstractDrill.drill_type_name_reversed[var_drill_name.get()]
        compile_type = var_compile_type.get()

        for param, entry in drill_specific_params:
            drill_settings[param] = entry.get()

        MathDrillGenerator.build_drill(drill_type, compile_type, drill_settings)

        canvas.delete("success")
        label = tk.Label(root, text=var_drill_name.get() + " with seed " + entry1.get() + " created successfully.")
        canvas.create_window(250, 470, tags="success", window=label)

    button1 = tk.Button(text='Generate drill', command=gen_drill_with_input)
    canvas.create_window(250, 440, window=button1)

    root.mainloop()


user_prompt()

