from calendar import c
import numbers
import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.geometry("300x500")

def button_click(event):
    btn = event.widget
    num = int(btn["text"])
    tkm.showinfo(f"{num}", f"{num}のボタンが押されました")

r = 0 #行を表す
c = 0 #列を表す
for i, num in enumerate(range(9,-1,-1),1):
    btn = tk.Button(root,
                    text=str(num),
                    font = ("",30),
                    width = 4,
                    height = 2,
                    )
    btn.bind("<1>", button_click)
    btn.grid(row = r, column = c)
    c += 1
    if i%3 == 0:
        r += 1
        c = 0
        
root.mainloop()