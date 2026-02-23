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
                    raise ValueError("\u001b[31mNumber must be greater than 0.\u001b[0m")
            return sorted(final_list)
        except ValueError:
            print("\u001b[31mInvalid input! Please enter a valid number above 0.\u001b[0m")


def rotation_function(page_number):
    rotation_angle = input(f"\u001b[36mPlease type the direction of the rotation; 'r' for 90 degrees to the right, 'l' for 90 degrees to the left, 'u' for upside-down and 'n' for none to rotate page {page_number}:\n\u001b[0m")
    while True:
        try:
            if rotation_angle.lower() == 'r' or rotation_angle.lower() == 'right':
                angle_output = "right"
                return angle_output
            elif rotation_angle.lower() == 'l' or rotation_angle.lower() == 'left':
                angle_output = "left"
                return angle_output
            elif rotation_angle.lower() == 'u' or rotation_angle.lower() == 'upside' or rotation_angle.lower() == 'upsidedown' or rotation_angle.lower() == 'upside down' or rotation_angle.lower() == 'upside-down':
                angle_output = "upside-down"
                return angle_output
            elif rotation_angle.lower() == 'n' or rotation_angle.lower() == 'none':
                angle_output = "none"
                return angle_output
            else:
                raise ValueError("\u001b[31Invalid input! Please enter either 'r', 'l', 'u' or 'n'.\u001b[0m")
        except ValueError:
            print("\u001b[31mInvalid input! Please enter either 'r', 'l', 'u' or 'n'.\u001b[0m")
        


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
page_rotate_num = []
current_page_rotations = []
Combined_data = []
while True:
    error_out_num = 0
    if Combined_data:
        print("\u001b[36mCurrent page number and Rotation of pages:\u001b[33m")
        [print(lis) for lis in Combined_data]
        correct_order = input("\u001b[36mAre these page rotations correct? (If you want to reset input 'reset')\n\u001b[0m")
    else:
        print(f"\u001b[33mThe selected pdf document: {pdf_files[0]} \u001b[0m")
        print("\u001b[36mCurrent number of pages:\u001b[33m")
        for pages in page_data: print(pages)
        correct_order = "n"
    if correct_order.lower() == 'no' or correct_order.lower() == 'n':
        while True:            
            print("\u001b[36mPlease type the page number you would like to rotate seperated by a comma. \u001b[0m")
            numbers = number_input()
            if all(num in page_data for num in numbers):
                for num in numbers:
                    page_rotate_num.append(num)
                page_rotate_num.sort()
                break
            elif error_out_num > 0:
                break
            else:
                print("\u001b[31mError: Page not found in pdf document.\u001b[0m")
                error_out_num = 1
        for pages in page_rotate_num:
            current_page_rotations.append(rotation_function(pages))
        if (num2 in Combined_data for num2[0] in numbers):
            for num2 in Combined_data:
                if num2[0] in page_rotate_num:
                    Combined_data[Combined_data.index(num2)][1] = current_page_rotations[page_rotate_num.index(num2[0])]
                    del current_page_rotations[page_rotate_num.index(num2[0])]
                    del page_rotate_num[page_rotate_num.index(num2[0])]
        Combined_data.extend([list(pair) for pair in zip(page_rotate_num, current_page_rotations)])
        page_rotate_num = []
        current_page_rotations = []
        Combined_data = [num3 for num3 in Combined_data if num3[1] != "none"]
    elif correct_order.lower() == 'yes' or correct_order.lower() == 'y':
        break
    elif correct_order.lower() == 'reset':
        page_data = list(range(1, len(pdf.pages) + 1))
        page_remove_num = []
        Combined_data = []
        print("\u001b[32mPage data restored.\u001b[0m")
    else:
        print('\u001b[31mPlease type "y" or "n".\u001b[0m')
        continue
for i in Combined_data:
    current_page = pdf.pages[i[0]-1]
    if i[1] == 'right':
        rotation = 90
    if i[1] == 'left':
        rotation = -90
    if i[1] == 'upside-down':
        rotation = 180
    current_page.rotate(rotation,relative=True)
new_pdf = Pdf.new()
new_pdf.pages.extend(pdf.pages)
new_pdf.remove_unreferenced_resources()
pdf.close()
new_pdf.save(name_of_PDF,min_version=version)
new_pdf.close()


