#Import modules
from pikepdf import Pdf
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os

def number_input(file_name):
    """Repeatedly prompts the user for input until a valid number (float) is entered."""
    while True:
        number = input("\u001b[33m" + str(file_name)+ "\n\u001b[0m")
        try:
            value = int(number)
            if value <= 0:
                raise ValueError("Number must be greater than 0") 
            return value
        except ValueError:
            print("\u001b[31mInvalid input! Please enter a valid number above 0.\u001b[0m")


root = tk.Tk()
root.withdraw()  # Hide the tkinter GUI
while True:
    pdf_files = filedialog.askopenfilename(
        multiple=True,
        title="Select PDF (.pdf) Files",
        filetypes=[("PDF files", "*.pdf")],
        initialdir="C:\\Users\\User\\Documents")
    if not pdf_files:
        print("\u001b[31mError: No file selected.\u001b[0m")
        exit()
    elif len(pdf_files)==1:
        print("\u001b[31mError: Please select more than one file.\u001b[0m")
    else:
        break
name_of_PDF = filedialog.asksaveasfilename(
    title="Select a location and a name to save the PDF",
    filetypes=[("PDF files", "*.pdf")],
    defaultextension=".pdf")
if name_of_PDF:
    print(f"\u001b[32mSave Location: {name_of_PDF}\u001b[0m")
else:
    print("\u001b[31mSave cancelled by user.\u001b[0m")
    exit()
while True:
    print("\u001b[36mCurrent order of selected files:\u001b[33m")
    for file in pdf_files: print(Path(file).name)
    correct_order = input("\u001b[36mIs the order of the pdf files correct?\u001b[0m")
    if correct_order.lower() == 'no' or correct_order.lower() == 'n':
        if len(pdf_files) == 2:
            pdf_files = [pdf_files[i] for i in [1,0]]
        else:
            print("\u001b[36mPlease assign the correct number to the displayed file based on ascending order where the starting number is 1\u001b[0m")
            ordered_list = []
            for file in pdf_files:
                filename = Path(file).name
                while True:
                    number = number_input(filename)
                    if number not in ordered_list:
                        break
                    print("\u001b[31mError: Number already assigned. Please use another number.\u001b[0m")
                ordered_list.append(number)
            pdf_files = [file for _, file in sorted(zip(ordered_list, pdf_files))]
            continue
    elif correct_order.lower() == 'yes' or correct_order.lower() == 'y':
        break
    else:
        print('\u001b[31mPlease type "y" or "n".\u001b[0m')
        continue
pdf = Pdf.new()
version = pdf.pdf_version
for file in pdf_files:
    source = Pdf.open(file)
    version = max(version, source.pdf_version)
    pdf.pages.extend(source.pages)
    pdf.remove_unreferenced_resources()
    source.close()
pdf.save(name_of_PDF,min_version=version)
pdf.close()


