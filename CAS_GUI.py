from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from fpdf import FPDF
from os import remove
import numpy as np
from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import sympy as sp
from sympy import groebner
from sympy import integrate
from sympy import diff
from sympy import limit
from sympy.solvers import solve
from sympy import nonlinsolve
from sympy import nsolve

arr = []
sp.var("x y z n m k a b c d")
count = 0

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)


def draw_plot(func: str) -> None:
    """Plot function

    :str func: function for plot
    """
    global count
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    fig = Figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot(111)
    for i in func:
        x1 = np.linspace(-10, 10, 501)
        y1 = x1
        x, y = np.meshgrid(x1, y1)
        f1 = i[:i.index("=")]
        f = ""
        for s in f1:
            if s == "^":
                f += "**"
            else:
                f += s
        f = eval(f)
        g = float(i[i.index("=") + 1:])
        ax.contour(x, y, f - g, [0])
    ax.grid(True)
    fig.savefig(f"plot{count}.png", bbox_inches='tight', dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=LEFT, fill=NONE, expand=0)


def Solve(func: str) -> list:
    """Logic function for calculate expression

    :str func: expression for calculation
    :return: solved expression
    """
    s = ["="]
    if len(func) == 1:
        f1 = func[0]
        f = ""
        for i in f1:
            if i == "^":
                f += "**"
            elif i in s:
                break
            else:
                f += i
        print(f)
        if "Integral" in f:
            f = f.split(",")
            res = integrate(sp.parse_expr(f[0][9:]), sp.var(f[1][0:len(f[1]) - 1]))
        elif "Derivative" in f:
            f = f.split(",")
            res = diff(sp.parse_expr(f[0][11:]), sp.var(f[1][0:len(f[1]) - 1]))
        elif "lim" in f:
            f = f.split(",")
            res = limit(sp.parse_expr(f[0][4:]), sp.var(f[1]), f[2][0:len(f[2]) - 1])
        elif not "x" in f1 and not "y" in f1:
            res = eval(f1)
        elif "y" in f1:
            try:
                res = solve(sp.parse_expr(f), y)
            except:
                res = nsolve(sp.parse_expr(f), 0)
        elif "x" in f1:
            try:
                res = solve(sp.parse_expr(f), x)
            except:
                res = nsolve(sp.parse_expr(f), 0)
        else:
            try:
                res = solve(sp.parse_expr(f))
            except:
                res = nsolve(sp.parse_expr(f), 0)
    else:
        res = ""
        res0 = list(groebner([sp.parse_expr(i) for i in func]))
        res += str(res0) + ", "
        res1 = nonlinsolve([sp.parse_expr(i) for i in func], [x, y])
        res += str(res1)
    print(res)
    return res


def get_func() -> None:
    """
    Function for GUI
    """
    global count
    global img
    temp = 1
    func = text.get(1.0, END)
    arr = func.split("\n")
    arr.pop()
    try:
        draw_plot(arr)
    except:
        temp = 0
    if len(arr) == 1:
        res_txt = " ".join(arr)
        res = f"In[{count}]: [" + res_txt + "]\n"
    else:
        res_txt = ", ".join(arr)
        res = f"In[{count}]: [" + res_txt + "]\n"
    pdf.cell(200, 10, txt=res, ln=1)
    try:
        res += f"Out[{count}]: " + str(Solve(arr)) + "\n"
        pdf.cell(200, 10, txt=f"Out[{count}]: " + str(Solve(arr)) + "\n", ln=1)
    except:
        res += f"Out[{count}]: " + "Error" + "\n"
        pdf.cell(200, 10, txt=f"Out[{count}]: " + "Error" + "\n", ln=1)
    res_text.configure(state='normal')
    res_text.insert(END, res)
    if temp == 1:
        pdf.image(f"plot{count}.png", w=60)
        remove(f"plot{count}.png")
        pdf.ln(1)
    res_text.configure(state='disabled')
    count += 1


def del_txt() -> None:
    """
    Function for deleting input textbox
    """
    text.delete(1.0, END)


def del_txt_res() -> None:
    """
    Function for deleting result textbox
    """
    global count
    count = 0
    res_text.configure(state='normal')
    res_text.delete(1.0, END)
    res_text.configure(state='disabled')


def Exit() -> None:
    """
    Exit function
    """
    root.destroy()


def Help() -> None:
    """
    GUI Help function
    """
    mb.showinfo("Помощь", "Ввод в виде:\nP(x1,x2,...,xn)=0")


def Info() -> None:
    """
    GUI Info function
    """
    mb.showinfo("О программе", "Программа ver2.6\nСакович Никита, 2023")


def open_file() -> None:
    """
    Function for opening files
    """
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "r") as file:
            text1 = file.read()
            text.delete("1.0", END)
            text.insert("1.0", text1)


def save_file() -> None:
    """
    Function for saving files of input
    """
    filepath = filedialog.asksaveasfilename()
    if filepath != "":
        text1 = text.get("1.0", END)
        with open(filepath, "w") as file:
            file.write(text1)


def save_file_res() -> None:
    """
    Function for saving files of output
    """
    filepath = filedialog.asksaveasfilename()
    if filepath != "":
        text1 = res_text.get("1.0", END)
        with open(filepath, "w") as file:
            file.write(text1)
    pdf.output(filepath + ".pdf")


root = Tk()
root.title("Program")
root.geometry("520x700")

canvas = None
img = None

mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command=open_file)
filemenu_save = Menu(filemenu, tearoff=0)
filemenu_save.add_command(label="Сохранить ввод", command=save_file)
filemenu_save.add_command(label="Сохранить вывод", command=save_file_res)
filemenu.add_cascade(label="Сохранить...", menu=filemenu_save)
filemenu.add_command(label="Выход", command=Exit)

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=Help)
helpmenu.add_command(label="О программе", command=Info)

mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)

text = Text(width=65, height=8.5)
text.pack(anchor=NW, padx=10, pady=10)

res_text = Text(width=61, height=7.5)
res_text.configure(state='disabled')
res_text.pack(anchor=NW, padx=10, pady=10)

scroll = Scrollbar(command=res_text.yview)
scroll.pack(side=RIGHT, fill=Y)
res_text.config(yscrollcommand=scroll.set)
scroll.place(in_=res_text, relx=1.0, relheight=1.025)

frame = Frame()
frame.pack(anchor=NW, padx=10, pady=20)

btn_get = Button(frame, text="calc", width=23, height=3, command=get_func).pack(side=LEFT)
btn_del = Button(frame, text="delete", width=23, height=3, command=del_txt).pack(side=LEFT)
btn_del_res = Button(frame, text="delete result", width=23, height=3, command=del_txt_res).pack(side=LEFT)

root.mainloop()
