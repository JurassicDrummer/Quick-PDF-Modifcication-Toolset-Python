#Import modules
from pikepdf import Pdf
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from math import nan
import os

def number_input():
    """Repeatedly prompts the user for input until a valid number (int) is entered."""
    while True:
        number = input("\u001b[33m\u001b[0m")
        string_list = [item.strip() for item in number.split(',')]
        try:
            final_list = [int(item) for item in string_list if item != ""]
            for value in final_list:
                if value<1:
                    raise ValueError("Number must be greater than 0")
            return sorted(final_list)
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
    elif len(pdf_files)>=2:
        print("\u001b[31mError: Please select only one file.\u001b[0m")
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

pdf = Pdf.open(pdf_files[0])
version = pdf.pdf_version
page_data = list(range(1, len(pdf.pages) + 1))
page_remove_num = []
numbers = []
while True:
    error_out_num = 0
    print("\u001b[36mCurrent number of pages:\u001b[33m")
    for pages in page_data: print(pages)
    if not numbers:
        correct_order = "n"
    else:
        correct_order = input("\u001b[36mAre the pdf file pages that are left correct? (If you want to reset input 'reset')\n\u001b[0m")
    if correct_order.lower() == 'no' or correct_order.lower() == 'n':
        while True:
            print(f"\u001b[33mCurrent pages that will be removed: {page_remove_num}\u001b[0m")
            print("\u001b[36mPlease type the page number you would like to remove seperated by a comma. \u001b[0m")
            numbers = number_input()
            if all(num in page_data for num in numbers):
                for num in numbers:
                    page_remove_num.append(num)
                    page_data.remove(num)
                page_remove_num.sort()
                break
            elif error_out_num > 0:
                break
            else:
                print("\u001b[31mError: Page not found in pdf document.\u001b[0m")
                error_out_num = 1
    elif correct_order.lower() == 'yes' or correct_order.lower() == 'y':
        break
    elif correct_order.lower() == 'reset':
        page_data = list(range(1, len(pdf.pages) + 1))
        page_remove_num = []
        print("\u001b[32mPage data restored.\u001b[0m")
    else:
        print('\u001b[31mPlease type "y" or "n".\u001b[0m')
        continue
for i in range(0,len(page_remove_num)):
    print(i)
    del pdf.pages[page_remove_num[i] - 1 - i]
new_pdf = Pdf.new()
new_pdf.pages.extend(pdf.pages)
new_pdf.remove_unreferenced_resources()
pdf.close()
new_pdf.save(name_of_PDF,min_version=version)
new_pdf.close()


