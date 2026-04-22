# PDF Compressor

A desktop application to compress PDF files using Ghostscript.

## Features
- Percentage-based compression quality.
- Automatic output filename suggestion.
- Integrated packaging tools to build standalone executables.
- Modern UI using Tkinter with a clean layout.

## Project Structure
- `src/`: Main Python source code.
- `assets/`: Icons and static resources.
- `packaging/`: Scripts and configurations to build the `.exe` and Installer.
- `dist/`: Output folder for build results (generated after building).

## How to Build the Executable (.exe)
1. Navigate to the `packaging/` folder.
2. Double-click `build_exe.bat`.
3. The executable will be generated in the `dist/` folder at the project root.

## Dependencies
- Python 3.x
- Ghostscript (Must be installed at `C:\Program Files (x86)\gs\gs10.07.0\`)
- PyInstaller (for building .exe)

---
*Created by Pedeep Creator*
# KompresPDF
