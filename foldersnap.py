import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

SPLASH_DURATION = 2000  # milissegundos
SPLASH_IMAGE = "splash.png"
ICON_PATH = "folder_creator_icon_fixed.ico"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def mostrar_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)

    largura = 400
    altura = 400
    x = (splash.winfo_screenwidth() // 2) - (largura // 2)
    y = (splash.winfo_screenheight() // 2) - (altura // 2)
    splash.geometry(f"{largura}x{altura}+{x}+{y}")

    try:
        img = Image.open(resource_path(SPLASH_IMAGE)).resize((400, 400))
        splash.imgtk = ImageTk.PhotoImage(img)
        tk.Label(splash, image=splash.imgtk).pack()
    except Exception as e:
        tk.Label(splash, text="FolderSnap v1.0", font=("Arial", 24)).pack(expand=True)

    splash.after(SPLASH_DURATION, lambda: (splash.destroy(), mostrar_interface()))
    splash.mainloop()

def mostrar_interface():
    root = tk.Tk()
    root.title("FolderSnap v1.0")
    root.geometry("360x280")
    root.resizable(False, False)

    try:
        root.iconbitmap(resource_path(ICON_PATH))
    except:
        pass

    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo de estrutura",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, caminho)

    def selecionar_pasta_destino():
        caminho = filedialog.askdirectory(title="Selecione onde criar as pastas")
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, caminho)

    def criar_pastas():
        arquivo = entry_arquivo.get()
        destino = entry_destino.get()
        if not arquivo or not destino:
            messagebox.showerror("Erro", "Por favor, selecione o arquivo e a pasta de destino.")
            return
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.readlines()
            for linha in linhas:
                pasta = linha.strip()
                caminho = os.path.join(destino, pasta)
                os.makedirs(caminho, exist_ok=True)
            messagebox.showinfo("Sucesso", "Pastas criadas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Label(root, text="Arquivo de estrutura (.txt):").pack(pady=(15, 0))
    entry_arquivo = tk.Entry(root, width=45)
    entry_arquivo.pack(padx=20)
    tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo).pack(pady=5)

    tk.Label(root, text="Pasta de destino:").pack(pady=(20, 0))
    entry_destino = tk.Entry(root, width=45)
    entry_destino.pack(padx=20)
    tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta_destino).pack(pady=5)

    tk.Button(root, text="Criar Pastas", command=criar_pastas, bg="green", fg="white").pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    mostrar_splash()
