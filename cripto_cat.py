import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def encrypt_layers():
    path = filedialog.askopenfilename() or filedialog.askdirectory()
    if not path:
        return

    base = os.path.basename(path.rstrip("/"))
    layers = simpledialog.askinteger("Layers", "How many encryption layers? (1–10)", minvalue=1, maxvalue=10)
    if not layers:
        return

    passwords = []
    for i in range(1, layers + 1):
        pw = simpledialog.askstring(f"Layer {i} Password", f"Enter password for Layer {i}:", show='*')
        if not pw:
            messagebox.showerror("Cancelled", "Encryption aborted.")
            return
        passwords.append(pw)

    current_input = f"layer0_input"
    if os.path.isdir(path):
        os.system(f'tar -czf {current_input}.tar.gz "{path}"')
    else:
        os.system(f'tar -czf {current_input}.tar.gz "{path}"')

    for i in range(1, layers + 1):
        prev = f"layer{i-1}_input.tar.gz.gpg" if i > 1 else f"{current_input}.tar.gz"
        curr = f"layer{i}_input"
        os.system(f'tar -czf {curr}.tar.gz "{prev}"')
        echo = f'echo "{passwords[i-1]}"'
        gpg_cmd = f'{echo} | gpg --batch --yes --passphrase-fd 0 -c {curr}.tar.gz'
        os.system(gpg_cmd)
        os.remove(f"{curr}.tar.gz")
        if i > 1:
            os.remove(prev)

    final = f"{base}.cat.gpg"
    os.rename(f"layer{layers}_input.tar.gz.gpg", final)
    messagebox.showinfo("Done", f"Created encrypted file:\n{final}")

# GUI
root = tk.Tk()
root.title("Subuntu LayerCryptor 🐾")
tk.Button(root, text="Encrypt File or Folder (.tar.gz.gpg)", command=encrypt_layers, width=40, height=3).pack(padx=20, pady=40)
root.mainloop()
