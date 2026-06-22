import pythoncom
import win32com.client
import os
from datetime import datetime


def make_drawing(sw, model, drawing_path, pdf_path, step_path, log=None):

    # logging helper
    def write(message):
        if log:
            log(message)
        else:
            print(message)

    model_path = model.GetPathName
    part_name = model.GetTitle

    # define material
    try:
        material_name = model.GetMaterialPropertyName2("", "")
        if not material_name:
            material = "Unknown"
    except:
        material = "Unknown"

    date = datetime.now().strftime("%Y-%m-%d")
    rev = "A"

    # part dimensions
    try:
        box = model.GetPartBox(True)
        minX, minY, minZ, maxX, maxY, maxZ = box

        length = maxX - minX
        width = maxY - minY
        height = maxZ - minZ
    except:
        length = width = height = 0

    sheetWidth = 0.42
    sheetHeight = 0.297

    # create drawing
    drawing = sw.NewDocument(
        r"C:\ProgramData\SolidWorks\SOLIDWORKS 2024\templates\Drawing.drwdot",
        12, sheetWidth, sheetHeight)

    # create views
    drawing.Create3rdAngleViews2(model_path)

    # get first actual view (sheet, front, top, right)
    view = drawing.GetFirstView     # sheet view
    view = view.GetNextView         # fron view
    write(f"View found: {view.GetName2}")
    drawing.ActivateView(view.GetName2)

    # create text
    note_text = f"""part: {part_name}
Date: {date}
Material: {material}
Rev: {rev}

length: {length*1000:.1f} mm
width: {width*1000:.1f} mm
height: {height*1000:.1f} mm
"""

    note = drawing.InsertNote(note_text)

    if note:
        annotation = note.GetAnnotation
        annotation.SetPosition2(0.3, 0.05, 0)

    # save draw file
    write(f"Saving drawing to: {drawing_path}")
    drawing.SaveAs(drawing_path)

    # save PDF
    write(f"Saving PDF to: {pdf_path}")
    drawing.SaveAs(pdf_path)

    # verificiation
    if os.path.exists(pdf_path):
        write("PDF saved successfully.")
    else:
        write("Error: PDF was not saved.")

    # Export STEP file

    try:

        write(f"Saving STEP to: {step_path}")

        part = model

        part.ForceRebuild3(False)

        success = part.SaveAs(step_path)

        if success:
            write("STEP file saved successfully.")
        else:
            write("STEP export failed.")

    except Exception as e:
        write(f"STEP export error: {e}")

    # close drawing
    sw.CloseDoc(drawing.GetTitle)
