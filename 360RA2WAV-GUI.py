import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

CONFIG_FILE = "config.txt"

# Diccionario de textos por idioma
textos = {
    "es": {
        "titulo": "360RA2WAV-GUI",
        "exe_label": "Ruta del ejecutable ia_mpeghd_testbench.exe:",
        "buscar_exe": "Buscar ejecutable",
        "m4a_label": "Archivo .m4a a convertir:",
        "buscar_m4a": "Buscar archivo .m4a",
        "ejecutar": "Ejecutar conversión",
        "error": "Debes seleccionar el ejecutable y el archivo .m4a",
        "exito": "¡Archivo convertido!",
        "fallo": "La conversión falló. Verifica los archivos.",
        "guardado": "Guardado como:"
    },
    "en": {
        "titulo": "360RA2WAV-GUI",
        "exe_label": "Path to ia_mpeghd_testbench.exe:",
        "buscar_exe": "Browse executable",
        "m4a_label": "M4A file to convert:",
        "buscar_m4a": "Browse .m4a file",
        "ejecutar": "Run conversion",
        "error": "You must select both the executable and the .m4a file",
        "exito": "File converted!",
        "fallo": "Conversion failed. Check your files.",
        "guardado": "Saved as:"
    }
}

# Funciones de GUI
def seleccionar_exe():
    exe_path = filedialog.askopenfilename(title=textos[idioma]["buscar_exe"], filetypes=[("Executables", "*.exe")])
    if exe_path:
        entry_exe.delete(0, tk.END)
        entry_exe.insert(0, exe_path)
        guardar_config(exe_path)

def seleccionar_m4a():
    m4a_path = filedialog.askopenfilename(title=textos[idioma]["buscar_m4a"], filetypes=[("M4A files", "*.m4a")])
    if m4a_path:
        entry_m4a.delete(0, tk.END)
        entry_m4a.insert(0, m4a_path)

def ejecutar_conversion():
    exe_path = entry_exe.get()
    m4a_path = entry_m4a.get()

    if not exe_path or not m4a_path:
        messagebox.showerror("Error", textos[idioma]["error"])
        return

    output_path = os.path.splitext(m4a_path)[0] + ".wav"
    comando = f'"{exe_path}" -ifile:"{m4a_path}" -ofile:"{output_path}"'

    try:
        subprocess.run(comando, shell=True, check=True)
        messagebox.showinfo(textos[idioma]["exito"], f"{textos[idioma]['guardado']}\n{output_path}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", textos[idioma]["fallo"])

def guardar_config(ruta_exe):
    try:
        with open(CONFIG_FILE, "w") as f:
            f.write(ruta_exe)
    except Exception as e:
        print("Error al guardar configuración:", e)

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return f.read().strip()
        except:
            return ""
    return ""

# Selector de idioma
def iniciar_programa(idioma_seleccionado):
    global idioma
    idioma = idioma_seleccionado
    selector.destroy()

    ventana = tk.Tk()
    ventana.title(textos[idioma]["titulo"])
    ventana.geometry("500x250")
    ventana.resizable(False, False)

    tk.Label(ventana, text=textos[idioma]["exe_label"]).pack(pady=5)
    global entry_exe
    entry_exe = tk.Entry(ventana, width=60)
    entry_exe.pack()
    ruta_guardada = cargar_config()
    if ruta_guardada:
        entry_exe.insert(0, ruta_guardada)
    tk.Button(ventana, text=textos[idioma]["buscar_exe"], command=seleccionar_exe).pack(pady=5)

    tk.Label(ventana, text=textos[idioma]["m4a_label"]).pack(pady=5)
    global entry_m4a
    entry_m4a = tk.Entry(ventana, width=60)
    entry_m4a.pack()
    tk.Button(ventana, text=textos[idioma]["buscar_m4a"], command=seleccionar_m4a).pack(pady=5)

    tk.Button(ventana, text=textos[idioma]["ejecutar"], command=ejecutar_conversion, bg="#4CAF50", fg="white").pack(pady=20)

    ventana.mainloop()

# Ventana inicial de idioma
selector = tk.Tk()
selector.title("Selecciona idioma / Select language")
selector.geometry("300x150")
selector.resizable(False, False)

tk.Label(selector, text="¿En qué idioma quieres usar el programa?\nWhich language do you want to use?", font=("Arial", 10)).pack(pady=20)
tk.Button(selector, text="Español", width=15, command=lambda: iniciar_programa("es")).pack(pady=5)
tk.Button(selector, text="English", width=15, command=lambda: iniciar_programa("en")).pack(pady=5)

selector.mainloop()
