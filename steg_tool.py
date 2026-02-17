import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os, hashlib, time

# ================= COLORS =================
BG = "#0b0f0b"
PANEL = "#101610"
FG = "#39ff14"
BTN = "#0f1a0f"
ENTRY = "#0d130d"

END_MARK = "#####END#####"

# ================= ROOT =================
root = tk.Tk()
root.title("Advanced Steganography Suite - Image Edition by GVP")
root.geometry("1200x850")
root.configure(bg=BG)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# ================= SECURITY =================
def secure_text(text, password):
    if not password:
        return text
    key = hashlib.sha256(password.encode()).hexdigest()[:16]
    return "".join(chr(ord(text[i]) ^ ord(key[i % len(key)])) for i in range(len(text)))

def text_to_binary(text):
    return ''.join(format(ord(i), '08b') for i in text)

# ================= GLOBALS =================
enc_path = None
dec_path = None
encrypted_result = None

# ================= LOG =================
def log(msg):
    log_box.config(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.config(state="disabled")

# ================= PERCENT DISPLAY =================
def update_percent(value):
    percent_label.config(text=f"Progress: {int(value)}%")
    root.update_idletasks()

# ================= PREVIEW =================
def show_image_preview(path, label):
    img = Image.open(path).convert("RGB")
    img.thumbnail((220, 220))
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img

def show_file_info(path, label):
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].upper().replace(".", "")
    label.config(text=f"{name} | {ext}")

# ================= IMAGE STEGANOGRAPHY =================
def encode_image(img, message):
    binary_msg = text_to_binary(message + END_MARK)
    data_index = 0
    pixels = img.load()
    total = img.width * img.height
    processed = 0

    for y in range(img.height):
        for x in range(img.width):
            r,g,b = pixels[x,y]

            if data_index < len(binary_msg):
                r = (r & 254) | int(binary_msg[data_index]); data_index+=1
            if data_index < len(binary_msg):
                g = (g & 254) | int(binary_msg[data_index]); data_index+=1
            if data_index < len(binary_msg):
                b = (b & 254) | int(binary_msg[data_index]); data_index+=1

            pixels[x,y]=(r,g,b)

            processed+=1
            if processed % 3000==0:
                update_percent((processed/total)*100)

            if data_index>=len(binary_msg):
                update_percent(100)
                return img
    return img

def decode_image(img):
    pixels=img.load()
    binary=""
    extracted=""
    total=img.width*img.height
    processed=0

    for y in range(img.height):
        for x in range(img.width):
            r,g,b=pixels[x,y]
            binary+=str(r&1)+str(g&1)+str(b&1)

            processed+=1
            if processed % 3000==0:
                update_percent((processed/total)*100)

            while len(binary)>=8:
                byte=binary[:8]
                binary=binary[8:]
                extracted+=chr(int(byte,2))
                if END_MARK in extracted:
                    update_percent(100)
                    return extracted.split(END_MARK)[0]
    return ""

# ================= FUNCTIONS =================
def upload_enc():
    global enc_path

    path = filedialog.askopenfilename(
        title="Select Image for Encryption",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg *.jpeg"),
            ("Bitmap Image", "*.bmp")
        ],
        defaultextension=".png"
    )

    if not path:
        return

    enc_path = path
    show_image_preview(path, enc_preview)
    show_file_info(path, enc_info)
    log("Encryption image loaded.")

def upload_dec():
    global dec_path

    path = filedialog.askopenfilename(
        title="Select Image for Decryption",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg *.jpeg"),
            ("Bitmap Image", "*.bmp")
        ],
        defaultextension=".png"
    )

    if not path:
        return

    dec_path = path
    show_image_preview(path, dec_preview)
    show_file_info(path, dec_info)
    log("Decryption image loaded.")

def remove_enc():
    global enc_path
    enc_path=None
    enc_preview.config(image="")
    enc_info.config(text="")
    log("Encryption image removed.")

def remove_dec():
    global dec_path
    dec_path=None
    dec_preview.config(image="")
    dec_info.config(text="")
    dec_text.delete("1.0",tk.END)
    log("Decryption image removed.")

def encrypt():
    global encrypted_result

    if not enc_path:
        log("Upload image first.")
        return

    start = time.time()
    update_percent(0)

    msg = secure_text(enc_text.get("1.0", tk.END).strip(), enc_pwd.get())

    try:
        img = Image.open(enc_path).convert("RGB")
    except:
        log("Invalid image file.")
        return

    encrypted_result = encode_image(img, msg)
    download_btn.config(state="normal")
    log("Image encrypted successfully.")

    end = time.time()
    log(f"Encryption completed in {round(end-start,3)} sec.")

def decrypt():
    if not dec_path:
        log("Upload image first.")
        return

    start = time.time()
    update_percent(0)

    try:
        img = Image.open(dec_path).convert("RGB")
    except:
        log("Invalid image file.")
        return

    msg = decode_image(img)
    msg = secure_text(msg, dec_pwd.get())

    dec_text.delete("1.0", tk.END)
    dec_text.insert(tk.END, msg)

    end = time.time()
    log(f"Decryption completed in {round(end-start,3)} sec.")

def download():
    global encrypted_result
    if encrypted_result:
        save = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if save:
            encrypted_result.save(save)
            log("Encrypted image saved.")

def reset_all():
    global enc_path,dec_path,encrypted_result
    enc_path=None
    dec_path=None
    encrypted_result=None
    enc_preview.config(image="")
    dec_preview.config(image="")
    enc_text.delete("1.0",tk.END)
    dec_text.delete("1.0",tk.END)
    enc_pwd.delete(0,tk.END)
    dec_pwd.delete(0,tk.END)
    update_percent(0)
    log_box.config(state="normal")
    log_box.delete("1.0",tk.END)
    log_box.config(state="disabled")
    log("System reset.")

# ================= UI PANELS =================
enc=tk.LabelFrame(root,text=" ENCRYPTION ",bg=PANEL,fg=FG,font=("Consolas",12,"bold"))
enc.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

dec=tk.LabelFrame(root,text=" DECRYPTION ",bg=PANEL,fg=FG,font=("Consolas",12,"bold"))
dec.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")

# Encryption UI
tk.Button(enc,text="Upload Image",bg=BTN,fg=FG,command=upload_enc).pack()
tk.Button(enc,text="Remove",bg=BTN,fg=FG,command=remove_enc).pack()

enc_preview=tk.Label(enc,bg=PANEL)
enc_preview.pack(pady=5)
enc_info=tk.Label(enc,bg=PANEL,fg=FG)
enc_info.pack()

tk.Label(enc,text="🗝️Password",bg=PANEL,fg=FG).pack()
enc_pwd=tk.Entry(enc,show="*",bg=ENTRY,fg=FG,insertbackground=FG)
enc_pwd.pack()

def auto_resize_enc(event=None):
    lines = int(enc_text.index('end-1c').split('.')[0])
    enc_text.config(height=min(max(lines,3),12))

enc_text = tk.Text(enc,height=3,bg=ENTRY,fg=FG,insertbackground=FG)
enc_text.pack(fill="x", padx=10, pady=5)
enc_text.bind("<KeyRelease>", auto_resize_enc)

tk.Button(enc,text="Encrypt",bg=BTN,fg=FG,command=encrypt).pack(pady=2)
download_btn=tk.Button(enc,text="Download",bg=BTN,fg=FG,state="disabled",command=download)
download_btn.pack()
tk.Button(enc,text="Clear Message",bg=BTN,fg=FG,
          command=lambda:enc_text.delete("1.0",tk.END)).pack()

# Decryption UI
tk.Button(dec,text="Upload Image",bg=BTN,fg=FG,command=upload_dec).pack()
tk.Button(dec,text="Remove",bg=BTN,fg=FG,command=remove_dec).pack()

dec_preview=tk.Label(dec,bg=PANEL)
dec_preview.pack(pady=5)
dec_info=tk.Label(dec,bg=PANEL,fg=FG)
dec_info.pack()

tk.Label(dec,text="🗝️Password",bg=PANEL,fg=FG).pack()
dec_pwd=tk.Entry(dec,show="*",bg=ENTRY,fg=FG,insertbackground=FG)
dec_pwd.pack()

def auto_resize_dec(event=None):
    lines = int(dec_text.index('end-1c').split('.')[0])
    dec_text.config(height=min(max(lines,3),12))

dec_text = tk.Text(dec,height=3,bg=ENTRY,fg=FG,insertbackground=FG)
dec_text.pack(fill="x", padx=10, pady=5)
dec_text.bind("<KeyRelease>", auto_resize_dec)

tk.Button(dec,text="Decrypt",bg=BTN,fg=FG,command=decrypt).pack()
tk.Button(dec,text="Clear Output",bg=BTN,fg=FG,
          command=lambda:dec_text.delete("1.0",tk.END)).pack()

# Bottom
percent_label=tk.Label(root,text="Progress: 0%",bg=BG,fg=FG,font=("Consolas",10))
percent_label.grid(row=1,column=0,columnspan=2,pady=5)

log_box=tk.Text(root,height=6,bg="#050805",fg=FG,state="disabled")
log_box.grid(row=2,column=0,columnspan=2,sticky="ew",padx=10)

tk.Button(root,text="RESET SYSTEM",bg="#1a0000",fg="#ff4444",
          font=("Consolas",10,"bold"),command=reset_all)\
.grid(row=3,column=0,columnspan=2,pady=10)

author=tk.Label(root,
    text="Developed by Gupthan Vishnu Prasad | Assisted by ChatGPT",
    bg=BG,fg="#1aff1a",font=("Consolas",9,"italic"))
author.grid(row=4,column=0,columnspan=2,pady=5)

log("System Ready. Image-Only Polished Version Loaded.")

root.mainloop()
