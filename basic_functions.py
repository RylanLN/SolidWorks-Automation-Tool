import subprocess as sb
import win32com.client
import pythoncom
import time
from part_properties import updateProperty


def start_sw():
    # start SW
    SW_PATH = r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe"
    # start SW
    sb.Popen(SW_PATH)
    time.sleep(5)  # wait for SW to start

    # force early-bound COM object
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.visible = True

    return sw


def get_open_docs(sw):
    docs = []
    model = sw.GetFirstDocument

    while model:
        docs.append(model)

        model = model.GetNext

    return docs


def shut_sw(sw):
    # close SW
    sw.ExitApp()


def update_part(model):
    # rebuild active part, assembly, or drawing
    model.EditRebuild3()


def process_model(model):
    print(f"Processing: {model.GetTitle}")

    updateProperty(model, "Drawn By", "Rylan")

    model.EditRebuild3
