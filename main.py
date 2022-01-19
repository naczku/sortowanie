import time
from tkinter import Tk, Frame, BOTH, Label, Button, StringVar, messagebox, ttk
from tkinter import filedialog as fd

import heapSort
import bubbleSort
import quickSort
import insertionSort
import mergeSort


sorting_list = {'heapSort': lambda x: heapSort.heapSorting(x),
                'bubbleSort': lambda x: bubbleSort.bubbleSorting(x),
                'quickSort': lambda x: quickSort.quickSorting(x),
                'mergeSort': lambda x: mergeSort.mergeSorting(x),
                'insertionSort': lambda x: insertionSort.insertSorting(x)
                }


class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder

        self.field_style = kwargs.pop("style", "TEntry")
        self.placeholder_style = kwargs.pop("placeholder_style", self.field_style)
        self["style"] = self.placeholder_style

        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, e):
        if self["style"] == self.placeholder_style and self.get() == self.placeholder:
            self.delete("0", "end")
            self["style"] = self.field_style

    def _add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = self.placeholder_style


def sorttest(name, repeat, array):
    sort_times = []

    for i in range(repeat):
        start = time.perf_counter()
        sorting_list.get(name)(array.copy())
        end = time.perf_counter()
        sort_times.append(end - start)

    return [round(min(sort_times), 10), round(sum(sort_times) / len(sort_times), 10), round(max(sort_times), 10)]


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.pack(fill=BOTH, expand=1)

        exitButton = Button(self, text="Start test", command=self.clickStartTestBtn)
        exitButton.place(x=80, y=10)

        loadBtn = Button(self, text="Load data", command=self.loadTxtBtn)
        loadBtn.place(x=10, y=10)

        global mintime
        mintime = Label(self, text="<Min>")
        mintime.place(x=70, y=40)

        global avgtime
        avgtime = Label(self, text="<Avg>")
        avgtime.place(x=70, y=60)

        global maxtime
        maxtime = Label(self, text="<Max>")
        maxtime.place(x=70, y=80)

        global numOfLoop
        numOfLoop = PlaceholderEntry(self, "<Number Of Loops>", show=None, font=('Arial', 9))
        numOfLoop.place(x=20, y=145, width=120)

        global values
        global v
        v = StringVar()
        values = PlaceholderEntry(self, "<Values>", show=None, font=('Arial', 9), text=v)
        values.place(x=20, y=120, width=120)

        n = StringVar()
        global typeOfSorting
        typeOfSorting = ttk.Combobox(self, width=27, textvariable=n, state="readonly")
        typeOfSorting['values'] = list(sorting_list.keys())
        typeOfSorting.pack()
        typeOfSorting.place(x=150, y=120)

    def loadTxtBtn(self):
        filename = fd.askopenfilename()
        if filename != "":
            try:
                with open(f'{filename}', "r+") as file1:
                    data = list(map(int, [i.replace("\n", "") for i in file1.readlines()]))
                v.set(" ".join(list(map(str, data))))
            except ValueError:
                messagebox.showerror(title="błąd", message="wybrany plik zabiera błędne informacje")

    def clickStartTestBtn(self):
        if numOfLoop.get().isdecimal() and all(ele.isdecimal() for ele in v.get().split()):
            sorts = sorttest(typeOfSorting.get(), int(numOfLoop.get()), list(map(int, v.get().split())))
            mintime.configure(text=f'Min: {sorts[0]}')
            avgtime.configure(text=f'Avg: {sorts[1]}')
            maxtime.configure(text=f'Max: {sorts[2]}')
        else:
            messagebox.showerror("błąd", "nieprawidłowe informacje")


root = Tk()
app = Window(root)
root.wm_title("Loop tester")
root.geometry("350x200")
typeOfSorting.current(0)
root.mainloop()
