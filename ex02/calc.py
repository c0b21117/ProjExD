from calendar import c
import numbers
import tkinter as tk

def click_number(event):#ボタンを押した時入力する関数
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END, num)


def click_equal(event):#=を押したときに答えを出す関数
    eqn = entry.get()
    res = eval(eqn)
    entry.delete(0, tk.END)
    entry.insert(tk.END, res)

def click_clear(event):
    entry.delete(0,tk.END)


root = tk.Tk()
root.geometry("500x500")

entry = tk.Entry(root, width=10, font=(", 40"), justify="right")
entry.grid(row=0, column=0, columnspan=3)

r = 0 #列を表す (row)
c = 0 #行を表す (column)
numbers = list(range(9, -1, -1)) # 数字だけのリスト
operators = ["+","-","*","/","."] # 演算子だけのリスト

for i, num in enumerate(numbers+operators, 1):
    btn = tk.Button(root, text=f"{num}", font=("", 20), width=4, height=2)
    btn.bind("<1>", click_number)
    btn.grid(row=r+1, column=c)
    c += 1
    if c >=5:
        r += 1
        c = 4
    if i%3 == 0:
        r += 1
        c = 0
        if r>=4:
            r = 0
            c = 4

btn = tk.Button(root, text=f"=", font=("", 20), width=4, height=2)
btn.bind("<1>", click_equal)
btn.grid(row=r, column=c+3)

btn = tk.Button(root, text=f"C", font=("", 20), width=4, height=2)
btn.bind("<1>", click_clear)
btn.grid(row=0, column=5)

root.mainloop()