import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

def get_gs_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Berjalan sebagai file .exe hasil kompilasi Pyinstaller
        return os.path.join(sys._MEIPASS, "gs", "bin", "gswin32c.exe")
    else:
        # Berjalan sebagai script python biasa
        return r"C:\Program Files (x86)\gs\gs10.07.0\bin\gswin32c.exe"

def compress_pdf(input_file, output_file, level="ebook"):
    gs_path = get_gs_path()
    
    if not os.path.isfile(gs_path):
        raise FileNotFoundError(
            f"Ghostscript tidak ditemukan di: {gs_path}"
        )

    quality_settings = {
        "screen": "/screen",
        "ebook": "/ebook",
        "printer": "/printer",
        "prepress": "/prepress",
        "default": "/default"
    }

    if level not in quality_settings:
        raise ValueError(f"Level tidak valid: {level}")

    command = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality_settings[level]}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_file}",
        input_file
    ]

    # Use CREATE_NO_WINDOW to prevent a black command prompt box popping up
    creationflags = 0
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NO_WINDOW

    subprocess.run(command, check=True, creationflags=creationflags)

class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Compressor")
        self.root.geometry("600x350")
        self.root.resizable(False, False)
        
        # Load Icon
        icon_path = get_resource_path(os.path.join("assets", "app_icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass # Fail silently if icon cannot be loaded
        
        self.style = ttk.Style(self.root)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
            
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.slider_var = tk.DoubleVar(value=50.0)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame utama untuk menengahkan konten
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        padding_options = {'padx': 10, 'pady': 10}
        
        # --- Title ---
        title_label = ttk.Label(main_frame, text="PDF Compressor", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # --- Input File ---
        ttk.Label(main_frame, text="Pilih PDF:").grid(row=1, column=0, sticky="e", **padding_options)
        ttk.Entry(main_frame, textvariable=self.input_file, width=40, state="readonly").grid(row=1, column=1, **padding_options)
        ttk.Button(main_frame, text="Browse...", command=self.select_input).grid(row=1, column=2, **padding_options)
        
        # --- Output File ---
        ttk.Label(main_frame, text="Simpan Ke:").grid(row=2, column=0, sticky="e", **padding_options)
        ttk.Entry(main_frame, textvariable=self.output_file, width=40, state="readonly").grid(row=2, column=1, **padding_options)
        ttk.Button(main_frame, text="Save As...", command=self.select_output).grid(row=2, column=2, **padding_options)
        
        # --- Quality Level ---
        ttk.Label(main_frame, text="Kekuatan Kompresi:").grid(row=3, column=0, sticky="e", **padding_options)
        
        slider_frame = ttk.Frame(main_frame)
        slider_frame.grid(row=3, column=1, sticky="w", **padding_options)
        
        self.slider = ttk.Scale(slider_frame, from_=1, to=100, orient="horizontal", 
                                variable=self.slider_var, command=self.update_percentage_label, length=240)
        self.slider.pack(side="left")
        
        self.percentage_label = ttk.Label(slider_frame, text="50%", width=5, font=("Helvetica", 10, "bold"))
        self.percentage_label.pack(side="left", padx=(10,0))
        
        # --- Description Label ---
        self.desc_label = ttk.Label(main_frame, text="(Kualitas sedang, cocok di layar, preset: ebook)", font=("Helvetica", 9, "italic"), foreground="gray")
        self.desc_label.grid(row=4, column=1, sticky="w", padx=10, pady=(0, 10))
        
        # --- Process Button ---
        self.process_btn = ttk.Button(main_frame, text="Mulai Kompresi", command=self.process_compression)
        self.process_btn.grid(row=5, column=0, columnspan=3, pady=10, ipadx=15, ipady=5)

    def update_percentage_label(self, event=None):
        val = int(self.slider_var.get())
        self.percentage_label.config(text=f"{val}%")
        
        if val >= 75:
            desc = "(Ukuran sekecil mungkin, preset: screen)"
        elif val >= 40:
            desc = "(Kualitas sedang, cocok di layar, preset: ebook)"
        elif val >= 15:
            desc = "(Kualitas tinggi, reduksi sedikit, preset: printer)"
        else:
            desc = "(Kualitas maksimal, seperti file asli, preset: prepress)"
            
        if hasattr(self, 'desc_label'):
            self.desc_label.config(text=desc)

    def get_compression_level_from_percentage(self, percentage):
        if percentage >= 75:
            return "screen" # 75 - 100% (Ukuran terkecil)
        elif percentage >= 40:
            return "ebook" # 40 - 74% (Kualitas sedang)
        elif percentage >= 15:
            return "printer" # 15 - 39% (Kualitas tinggi)
        else:
            return "prepress" # 1 - 14% (Kualitas maksimal / origin)

    def select_input(self):
        filepath = filedialog.askopenfilename(
            title="Pilih File PDF",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        if filepath:
            self.input_file.set(filepath)
            
            # Secara otomatis mengubah nama output berdasarkan input
            if not self.output_file.get():
                dir_name = os.path.dirname(filepath)
                base_name = os.path.basename(filepath)
                name, ext = os.path.splitext(base_name)
                default_out = os.path.join(dir_name, f"{name}_hasil_kompres{ext}")
                self.output_file.set(default_out)

    def select_output(self):
        filepath = filedialog.asksaveasfilename(
            title="Simpan PDF Sebagai",
            defaultextension=".pdf",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        if filepath:
            self.output_file.set(filepath)

    def process_compression(self):
        in_file = self.input_file.get()
        out_file = self.output_file.get()
        percentage = int(self.slider_var.get())
        lvl = self.get_compression_level_from_percentage(percentage)
        
        if not in_file or not out_file:
            messagebox.showwarning("Data Tidak Lengkap", "Silakan pilih file input dan lokasi penyimpanan terlebih dahulu.")
            return
            
        self.process_btn.config(state="disabled", text="Sedang Mengkompres...")
        self.root.update()
        
        try:
            compress_pdf(in_file, out_file, lvl)
            messagebox.showinfo("Sukses!", f"File PDF berhasil dikompres!\nTersimpan di: {out_file}")
            # Membuka folder tempat file disimpan setelah berhasil
            os.startfile(os.path.dirname(out_file))
        except FileNotFoundError as e:
            messagebox.showerror("Error Ghostscript", str(e))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error Kompresi", f"Gagal saat kompres.\nDetail: {e}")
        except Exception as e:
            messagebox.showerror("Error Tidak Terduga", str(e))
        finally:
            self.process_btn.config(state="normal", text="Mulai Kompresi")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()
