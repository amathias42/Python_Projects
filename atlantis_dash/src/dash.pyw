import data_usage_tracker as dat_track
import tkinter as tk
from PIL import ImageTk, Image
import datetime as dt
import threading
from time import sleep


class AtlantisDash:
    def __init__(self):
        self.webThread = threading.Thread(target=self.update_usage, daemon=True)

        self.root = tk.Tk()
        self.root.title("Atlantis dash")

        self.tk_height = 200
        self.tk_width = 150
        self.tk_widthScreen = self.root.winfo_screenwidth()
        self.tk_heightScreen = self.root.winfo_screenheight()

        self.clock = tk.Label(
            self.root,
            text="--:--:--",
            font=("Tahoma", "24", "bold"),
            background="light sky blue",
            foreground="midnight blue",
        )
        self.clock.grid(
            column=0,
            row=0,
            sticky=tk.E + tk.W,
        )

        chart = Image.open("basic_usage_chart.png")
        chart = chart.resize((150, 150))
        chartImg = ImageTk.PhotoImage(chart)

        self.ring = tk.Label(
            self.root,
            height=150,
            width=150,
            bg="light sky blue",
            image=chartImg,
        )
        self.ring.grid(column=0, row=1)

    def fetch_chart(self):
        if not self.webThread.is_alive():
            self.webThread = threading.Thread(target=self.update_usage, daemon=True)
            self.webThread.start()

        chart = Image.open("basic_usage_chart.png")
        chart = chart.resize((150, 150))
        chartImg = ImageTk.PhotoImage(chart)
        self.ring.config(image=chartImg)
        self.ring.image = chartImg

        self.ring.after(20 * 1000, self.fetch_chart)

    def tick(self):

        self.clock.config(text=dt.datetime.now(dt.UTC).strftime("%H:%M:%S"))
        # time.sleep(0.5)
        self.clock.after(500, self.tick)
        # print(f"height: {root.winfo_screenheight()}, width: {root.winfo_screenwidth()}")
        # print(root.winfo_screen())

    def update_usage(self):

        while 1:
            with dat_track.DataUsageWatcher() as w:
                p = dat_track.DataUsagePlotter(w)
                p.make_ring_chart()
                sleep(60 * 5)

    def run(self):

        self.webThread.start()

        self.tick()
        self.fetch_chart()
        # self.root.geometry(f"{self.tk_width}x{self.tk_height}+795+-1080")

        self.root.mainloop()


if __name__ == "__main__":
    a = AtlantisDash()
    a.run()
