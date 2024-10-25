import tkinter as tk
import datetime as dt


root = tk.Tk(screenName=":1.0")
root.title("Atlantis dash")

width = 150
height = 45
widthScreen = root.winfo_screenwidth()
heightScreen = root.winfo_screenheight()

timeStr = tk.StringVar()
clock = tk.Label(
    root,
    text="--:--:--",
    font=("Tahoma", "24", "bold"),
    background="light sky blue",
    foreground="midnight blue",
)

clock.grid()


def tick():

    timeStr.set(dt.datetime.now(dt.UTC).strftime("%H:%M:%S"))
    clock.config(text=timeStr.get())
    # time.sleep(0.5)
    clock.after(500, tick)
    # print(f"height: {root.winfo_screenheight()}, width: {root.winfo_screenwidth()}")
    # print(root.winfo_screen())


tick()
root.geometry(f"{width}x{height}+-1930+0")
root.mainloop()
