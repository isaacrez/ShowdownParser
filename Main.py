from tkinter import *
from tkinter.ttk import *

from Parser import Parser
from Writer import StatsWriter

def parse_file():
    parser.start(match_filename_var.get())
    if custom_save_var.get():
        data_filename = data_filename_var.get()
    else:
        data_filename = match_filename_var.get().split('.')[0]
    StatsWriter.StatsWriter(parser.get_data(), data_filename)

parser = Parser.Parser()

root = Tk()
root.title("Showdown Parser")
root.geometry("300x130")
root.resizable(False, False)
Grid.columnconfigure(root, 0, weight=1)
padding = {"x": 5, "y": 3}

match_filename_var = StringVar()
data_filename_var = StringVar()
custom_save_var = BooleanVar()

styling = ('cambria', 12, 'normal')

btn_style = Style()
btn_style.configure("TButton", font=styling)

lbl_entry_pairs = [["Read From:", match_filename_var, "matchData.html"],
                   ["Save As:", data_filename_var, "matchData"]]

def make_label_entry_pair(configs, row):
    lbl = Label(root, text=configs[0], font=styling, justify="left")
    lbl.grid(column=0, row=row, padx=padding["x"], pady=padding["y"], sticky=W)

    entry = Entry(root, textvariable=configs[1], font=styling)
    entry.insert(0, configs[2])
    entry.grid(column=1, row=row, padx=padding["x"], pady=padding["y"], sticky=E+W)

    row += 1

make_label_entry_pair(lbl_entry_pairs[0], 0)
make_label_entry_pair(lbl_entry_pairs[1], 2)

radio_buttons = {
    "Default Save": False,
    "Custom Name Save": True
}

col = 0
for (text, value) in radio_buttons.items():
    r_btn = Radiobutton(root, text=text, variable=custom_save_var, value=value)
    r_btn.grid(column=col, row=1)
    col += 1

submission = Button(root, text="Parse it!", style="TButton", command=parse_file)
submission.grid(columnspan=2, padx=padding["x"], pady=padding["y"])

root.mainloop()
