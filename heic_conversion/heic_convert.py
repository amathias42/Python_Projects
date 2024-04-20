"""Module - heic_convert: converts .heic image files to different formats"""

import argparse
import os
import tkinter as tk
import time

# from tkinter import ttk

from tkinter import filedialog  # type: ignore pylint: disable=import-error
from PIL import Image
from pillow_heif import register_heif_opener  # pylint: disable=import-error
from tqdm import tqdm  # type: ignore pylint: disable=import-error


parser = argparse.ArgumentParser(
    description="Bulk converter for .heic images to choice of .png or .jpeg"
)
parser.add_argument(
    "-f", "--format", help="Format to convert to", default="png", choices=["png", "jpg"]
)
parser.add_argument(
    "-o", "--outdir", help="Output directory for converted files", default="./"
)

args = parser.parse_args()


def select_images(initialdir="C:/Users/Andy Mathias/OneDrive - UW/Pictures/"):
    return tk.filedialog.askopenfilenames(
        title="Select Images",
        initialdir=initialdir,
        filetypes=[("HEIC images", "*.heic")],
    )


def convert_images():
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    register_heif_opener()
    imgList = select_images()
    for i in tqdm(imgList):
        img = Image.open(i)
        filename = os.path.splitext(i)[0]  # remove file extension
        filename = filename[filename.rfind("/") :]  # remove path leading up to file
        img.save(args.outdir + filename + "." + args.format, format=args.format)

    root.destroy()


root = tk.Tk()
root.title("Select .heic Images to Convert")
# TODO: add progress bar
# TODO: add image generic renamability
root.after_idle(convert_images)
root.mainloop()
