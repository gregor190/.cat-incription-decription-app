import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# 🔐 ENCRYPTION FUNCTION
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

    current_input = "layer0_input"
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
    os.remove(f"{current_input}.tar.gz")
    messagebox.showinfo("Success ✅", f"Encrypted archive created:\n{final}")

# 🔓 DECRYPTION FUNCTION
def decrypt_cat_file():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted GPG Archive", "*.tar.gz.gpg")])
    if not filepath:
        return

    password = simpledialog.askstring("Password", "Enter decryption password:", show='*')
    if not password:
        return

    base = os.path.basename(filepath).replace(".tar.gz.gpg", "")
    decrypted_tar = base + ".tar.gz"

    decrypt_cmd = f"echo {password} | gpg --batch --yes --passphrase-fd 0 -o \"{decrypted_tar}\" -d \"{filepath}\""
    if os.system(decrypt_cmd) != 0 or not os.path.exists(decrypted_tar):
        messagebox.showerror("Error", "Decryption failed.")
        return

    extract_dir = filedialog.askdirectory(title="Choose folder to extract contents")
    if not extract_dir:
        return

    extract_cmd = f"tar -xzf \"{decrypted_tar}\" -C \"{extract_dir}\""
    if os.system(extract_cmd) != 0:
        messagebox.showerror("Error", "Extraction failed.")
    else:
        messagebox.showinfo("Success ✅", f"Decrypted & extracted to:\n{extract_dir}")
        os.remove(decrypted_tar)

# 🐾 GUI SETUP
root = tk.Tk()
root.title("Subuntu LayerCryptor 🐾")

encrypt_btn = tk.Button(root, text="🔐 Encrypt File/Folder (.tar.gz.gpg)", command=encrypt_layers, width=40, height=3)
encrypt_btn.pack(padx=20, pady=10)

decrypt_btn = tk.Button(root, text="🧩 Decrypt Encrypted Archive", command=decrypt_cat_file, width=40, height=3)
decrypt_btn.pack(padx=20, pady=10)

root.mainloop()
