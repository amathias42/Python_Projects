import tkinter as tk

from tkinter import filedialog  # type: ignore pylint: disable=unused-import


class TkFileSelect:

    def __init__(self, title="Select files", initialdir="."):
        self.results = []
        self.title = title
        self.initialdir = initialdir
        self.fileWindow(title)
        self.root = None

    def select_files(self):
        self.results = tk.filedialog.askopenfilenames(
            title=self.title, initialdir=self.initialdir
        )
        self.root.destroy()

    def fileWindow(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.after_idle(self.select_files)
        self.root.mainloop()

    def get_files(self):
        return self.results
