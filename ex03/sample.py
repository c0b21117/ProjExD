from cProfile import label
import tkinter as tk
import tkinter.messagebox as tkm

def key_down(event):
    global jid
    if jid != None:
        root.after_cancel(jid)
        jid = None
        return
    key = event.keysym
    tkm.showinfo("キー押下",f"{key}キーがおされました")
    jid = root.after(1000,count_up)

def count_up():
    global tmr, jid
    tmr = tmr+1
    label["text"] = tmr
    root.after(1000, count_up)

if __name__ == "__main__":
    root =tk.Tk()
    label = tk.Label(root,font = ("",80))

    label.pack()

    tmr = 0
    #root.after(5000, count_up)
    root.bind("<KeyPress>",key_down)
    root.mainloop