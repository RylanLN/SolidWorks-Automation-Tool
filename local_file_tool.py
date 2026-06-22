import os
import win32com.client
import time
import pythoncom
from basic_functions import get_open_docs, process_model
from part_properties import updateProperty
from drawings import make_drawing

sw = win32com.client.Dispatch("SldWorks.Application")

# Open part files
project_folder = r"C:\Users\13312\OneDrive\SolidWorks_Auto_Project"
part_folder = os.path.join(project_folder, "SW_Test_Parts")
part_files = []
for file in os.listdir(part_folder):
    if file.lower().endswith(".sldprt"):
        full_path = os.path.join(part_folder, file)
        part_files.append(full_path)
print(f"Part files found: {len(part_files)}")

for part_path in part_files:
    print(f"Opening: {os.path.basename(part_path)}")
    try:
        errors = win32com.client.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warnings = win32com.client.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        sw.OpenDoc6(part_path, 1, 0, "", errors, warnings)
        time.sleep(3)
    except Exception as e:
        print(f"Error opening document: {e}")

# Find open documents
docs = get_open_docs(sw)
paths = []
for model in docs:
    paths.append(model.GetPathName)

# output folder
base_output = os.path.join(project_folder, "SW_Test_Drawings")
drawing_folder = os.path.join(base_output, "Drawings")
pdf_folder = os.path.join(base_output, "PDFs")
step_folder = os.path.join(base_output, "STEPs")

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
        print(f"Skipping: {path}")
        continue

    try:
        name = model.GetTitle

        process_model(model)

        base_name = os.path.splitext(name)[0]
        drawing_path = os.path.join(drawing_folder, base_name + ".SLDDRW")
        pdf_path = os.path.join(pdf_folder, base_name + ".PDF")
        step_path = os.path.join(step_folder, base_name + ".STEP")

        make_drawing(sw, model, drawing_path, pdf_path, step_path)

        successful_files.append(base_name)
        print(f"Finished: {base_name}")

    except Exception as e:
        failed_files.append(os.path.basename(path))
        print(f"Error processing file: {e}")

print("\nProcessing Summary:")

print(f"Successful: {len(successful_files)}")
print(f"Failed: {len(failed_files)}")

print(f"\nSuccessful files:")
for file in successful_files:
    print(f"- {file}")

if failed_files:
    print(f"\nFailed files:")
    for file in failed_files:
        print(f"- {file}")

print(f"\nDone.")
