# SolidWorks Automation Tool

## Overview

A Python-based automation tool designed to streamline repetitive SolidWorks documentation workflows. The program automates the processing of part files, generation of engineering drawings, export of manufacturing files, and organization of project outputs.

The goal of this project was to reduce manual CAD documentation steps by integrating Python automation with the SolidWorks API.

## How to Run

1. Clone the repository:
   git clone https://github.com/RylanLN/SolidWorks-Automation-Tool.git

2. Open the folder in VS Code

3. Install dependencies:
   pip install pywin32

4. Run one of the entry scripts:
   - gui_main.py (recommended)
   - terminal_main.py

## Features

- Batch processes SolidWorks part files from a selected folder
- Automatically generates SolidWorks drawing documents
- Exports PDF drawings and STEP models
- Extracts and updates part metadata
- Creates organized output folders for generated files
- Provides a graphical user interface for user-controlled automation
- Provides processing summaries and error reporting

## Project Structure

- gui_main.py → User interface for running automation
- terminal_main.py → Command-line version of automation
- drawings.py → Handles SolidWorks drawing generation
- basic_functions.py → Core SolidWorks API utilities
- part_properties.py → Updates material and metadata
- screenshots/ → Output images for documentation

## Technologies Used

- Python
- SolidWorks API
- COM automation through pywin32
- Tkinter GUI framework
- SolidWorks 2024

## Workflow

1. User selects a folder containing SolidWorks part files
2. The program opens and processes each part automatically
3. Part information is extracted and updated
4. Engineering drawings are generated
5. Drawings are exported as PDFs
6. Parts are exported as STEP files
7. Outputs are organized into designated folders

## Screenshots

### User Interface

![GUI](screenshots/gui.png)

### Generated Drawing

![Drawing](screenshots/drawing.png)

### Output Organization

![Output](screenshots/output.png)

## Skills Demonstrated

- Python automation and scripting
- SolidWorks API (COM automation)
- CAD workflow automation
- File system automation (batch processing)
- GUI development using Tkinter
- Error handling for external software integration
- Engineering documentation generation

## Future Improvements

Potential improvements include:
- Additional drawing dimension automation
- Support for assemblies
- Enhanced user interface features

## Notes

This project evolved through iterative development, including debugging COM interface issues, refining batch processing logic, and transitioning from manual file handling to fully automated workflows.