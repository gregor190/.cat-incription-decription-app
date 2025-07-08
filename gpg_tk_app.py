import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def decrypt_cat_file():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted .gpg files", "*.tar.gz.gpg")])
    if not filepath:
        return

    # Prompt for decryption password
    password = simpledialog.askstring("Password", "Enter decryption password:", show='*')
    if not password:
        return

    base = os.path.basename(filepath).replace(".tar.gz.gpg", "")
    decrypted_tar = base + ".tar.gz"

    # Step 1: Decrypt with gpg using os.system and passphrase in env
    decrypt_cmd = f"echo {password} | gpg --batch --yes --passphrase-fd 0 -o {decrypted_tar} -d \"{filepath}\""
    result = os.system(decrypt_cmd)

    if result != 0 or not os.path.exists(decrypted_tar):
        messagebox.showerror("Error", "Decryption failed.")
        return

    # Step 2: Extract .tar.gz
    extract_dir = filedialog.askdirectory(title="Choose folder to extract contents")
    if not extract_dir:
        return

    extract_cmd = f"tar -xzf \"{decrypted_tar}\" -C \"{extract_dir}\""
    if os.system(extract_cmd) != 0:
        messagebox.showerror("Error", "Extraction failed.")
    else:
        messagebox.showinfo("Success", f"File decrypted and extracted to:\n{extract_dir}")
        os.remove(decrypted_tar)

# Basic GUI
root = tk.Tk()
root.title(".cat Protocol Decryptor")
tk.Button(root, text="Decrypt .tar.gz.gpg", command=decrypt_cat_file, width=40, height=2).pack(padx=20, pady=50)
root.mainloop()
