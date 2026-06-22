import tkinter as tk
from tkinter import filedialog
import threading

import os
import time
import pythoncom
import win32com.client

from basic_functions import get_open_docs, process_model
from part_properties import updateProperty
from drawings import make_drawing

# functions


def select_part_folder():
    folder = filedialog.askdirectory()

    if folder:
        part_folder_label.config(text=folder)


def select_output_folder():
    folder = filedialog.askdirectory()

    if folder:
        output_folder_label.config(text=folder)


def run_automation():
    thread = threading.Thread(target=automation_worker)
    thread.start()


def automation_worker():
    status_text.delete(1.0, tk.END)

    sw = win32com.client.Dispatch("SldWorks.Application")
    part_folder = part_folder_label.cget("text")
    output_folder = output_folder_label.cget("text")

    # Open part files
    part_files = []
    for file in os.listdir(part_folder):
        if file.lower().endswith(".sldprt"):
            full_path = os.path.join(part_folder, file)
            part_files.append(full_path)
    status_text.insert(tk.END, f"Part files found: {len(part_files)}\n")

    for part_path in part_files:
        status_text.insert(tk.END, f"Opening: {os.path.basename(part_path)}\n")
        try:
            errors = win32com.client.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
            warnings = win32com.client.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
            sw.OpenDoc6(part_path, 1, 0, "", errors, warnings)
            time.sleep(3)
        except Exception as e:
            status_text.insert(tk.END, f"Error opening document: {e}\n")

    # Find open documents
    docs = get_open_docs(sw)
    paths = []
    for model in docs:
        paths.append(model.GetPathName)

    # output folder
    drawing_folder = os.path.join(output_folder, "Drawings")
    pdf_folder = os.path.join(output_folder, "PDFs")
    step_folder = os.path.join(output_folder, "STEPs")

    # create output folders if they don't already exist
    os.makedirs(drawing_folder, exist_ok=True)
    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(step_folder, exist_ok=True)

    # for summary data following processing
    successful_files = []
    failed_files = []

    for path in paths:

        model = None

        for doc in get_open_docs(sw):
            if doc.GetPathName == path:
                model = doc
                break
        if model is None:
            status_text.insert(tk.END, f"Skipping: {path}\n")
            continue

        try:
            name = model.GetTitle

            process_model(model)

            base_name = os.path.splitext(name)[0]
            drawing_path = os.path.join(drawing_folder, base_name + ".SLDDRW")
            pdf_path = os.path.join(pdf_folder, base_name + ".PDF")
            step_path = os.path.join(step_folder, base_name + ".STEP")

            make_drawing(sw, model, drawing_path, pdf_path, step_path,
                         log=lambda msg: status_text.insert(tk.END, msg + "\n"))

            successful_files.append(base_name)
            status_text.insert(tk.END, f"Finished: {base_name}\n")

        except Exception as e:
            failed_files.append(os.path.basename(path))
            status_text.insert(tk.END, f"Error processing file: {e}\n")

    status_text.insert(tk.END, "\nProcessing Summary:\n")

    status_text.insert(tk.END, f"Successful: {len(successful_files)}\n")
    status_text.insert(tk.END, f"Failed: {len(failed_files)}\n")

    status_text.insert(tk.END, "\nSuccessful files:\n")
    for file in successful_files:
        status_text.insert(tk.END, f"- {file}\n")

    if failed_files:
        status_text.insert(tk.END, "\nFailed files:\n")
        for file in failed_files:
            status_text.insert(tk.END, f"- {file}\n")

    status_text.insert(tk.END, f"\nDone.")


# window
root = tk.Tk()
root.title("SolidWorks Automation Tool")
root.geometry("700x500")

# part folder
part_button = tk.Button(root, text="Select Part Folder",
                        command=select_part_folder)
part_button.pack(pady=10)
part_folder_label = tk.Label(root, text="No folder selected")
part_folder_label.pack()

# Output folder
output_button = tk.Button(
    root, text="Select Output Folder", command=select_output_folder)
output_button.pack(pady=10)
output_folder_label = tk.Label(root, text="No folder selected")
output_folder_label.pack()

# run button
run_button = tk.Button(root, text="Run Automation", command=run_automation)
run_button.pack(pady=20)

# status box
status_text = tk.Text(root, height=15, width=80)
status_text.pack(pady=10)

# start GUI
root.mainloop()
