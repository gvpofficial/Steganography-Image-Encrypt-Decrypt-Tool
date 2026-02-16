import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os, hashlib

# ---------------- SECURITY LAYER ----------------

def secure_text(text,password):
    if not password:
        return text
    key=hashlib.sha256(password.encode()).hexdigest()[:16]
    return "".join(chr(ord(text[i]) ^ ord(key[i%len(key)])) for i in range(len(text)))

# ---------------- STEGANOGRAPHY ----------------

END_MARK="#####END#####"

def text_to_binary(text):
    return ''.join(format(ord(i),'08b') for i in text)

def binary_to_text(binary):
    chars=[binary[i:i+8] for i in range(0,len(binary),8)]
    return ''.join(chr(int(c,2)) for c in chars)

def capacity_ok(img,msg):
    max_bits=img.width*img.height*3
    return len(text_to_binary(msg+END_MARK))<=max_bits

def encode_image(image,message):
    binary_msg=text_to_binary(message+END_MARK)
    data_index=0
    img=image.copy()
    pixels=img.load()

    for y in range(img.height):
        for x in range(img.width):
            r,g,b=pixels[x,y]
            if data_index<len(binary_msg):
                r=(r&~1)|int(binary_msg[data_index]); data_index+=1
            if data_index<len(binary_msg):
                g=(g&~1)|int(binary_msg[data_index]); data_index+=1
            if data_index<len(binary_msg):
                b=(b&~1)|int(binary_msg[data_index]); data_index+=1
            pixels[x,y]=(r,g,b)
            if data_index>=len(binary_msg):
                return img
    return img

def decode_image(image):
    pixels=image.load()
    binary=""
    for y in range(image.height):
        for x in range(image.width):
            r,g,b=pixels[x,y]
            binary+=str(r&1)+str(g&1)+str(b&1)
    text=binary_to_text(binary)
    if END_MARK in text:
        return text.split(END_MARK)[0]
    return ""

# ---------------- COLORS ----------------

BG="#0b0f0b"
PANEL="#101610"
FG="#39ff14"
BTN="#0f1a0f"
ENTRY="#0d130d"

# ---------------- GLOBALS ----------------

enc_img=None
dec_img=None
encrypted_result=None

# ---------------- LOG ----------------

def log(msg):
    log_box.config(state="normal")
    log_box.insert(tk.END,msg+"\n")
    log_box.see(tk.END)
    log_box.config(state="disabled")

# ---------------- PREVIEW ----------------

def show_preview(image,label):
    preview=image.copy()
    preview.thumbnail((170,170))
    tk_img=ImageTk.PhotoImage(preview)
    label.config(image=tk_img)
    label.image=tk_img

def show_info(path,img,label):
    name=os.path.basename(path)
    ext=os.path.splitext(name)[1].upper().replace(".","")
    label.config(text=f"{name} | {ext} | {img.width}x{img.height}")

# ---------------- ENCRYPT ----------------

def upload_enc():
    global enc_img
    path=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
    if path:
        enc_img=Image.open(path).convert("RGB")
        show_preview(enc_img,enc_preview)
        show_info(path,enc_img,enc_info)
        log("Encryption image loaded.")

def remove_enc():
    global enc_img,encrypted_result
    enc_img=None; encrypted_result=None
    enc_preview.config(image=""); enc_info.config(text="")
    download_btn.config(state="disabled")
    log("Encryption image removed.")

def encrypt():
    global encrypted_result
    if not enc_img:
        log("Upload image first."); return

    msg=enc_text.get("1.0",tk.END).strip()
    pwd=pwd_entry.get()

    if not msg:
        log("Enter message."); return

    msg=secure_text(msg,pwd)

    if not capacity_ok(enc_img,msg):
        log("Message too large for image."); return

    encrypted_result=encode_image(enc_img,msg)
    download_btn.config(state="normal")
    log("Encryption successful.")

def download():
    if encrypted_result:
        path=filedialog.asksaveasfilename(defaultextension=".png",
                                          filetypes=[("PNG","*.png")])
        if path:
            encrypted_result.save(path)
            log("Encrypted image saved.")

def clear_enc_text():
    enc_text.delete("1.0",tk.END)

# ---------------- DECRYPT ----------------

def upload_dec():
    global dec_img
    path=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
    if path:
        dec_img=Image.open(path).convert("RGB")
        show_preview(dec_img,dec_preview)
        show_info(path,dec_img,dec_info)
        log("Encrypted image loaded.")

def remove_dec():
    global dec_img
    dec_img=None
    dec_preview.config(image=""); dec_info.config(text="")
    dec_text.delete("1.0",tk.END)
    log("Decryption image removed.")

def decrypt():
    if not dec_img:
        log("Upload encrypted image first."); return

    pwd=pwd_dec_entry.get()
    msg=decode_image(dec_img)

    if not msg:
        log("No message found."); return

    msg=secure_text(msg,pwd)
    dec_text.delete("1.0",tk.END)
    dec_text.insert(tk.END,msg)
    log("Decryption successful.")

def clear_dec_text():
    dec_text.delete("1.0",tk.END)

# ---------------- ROOT ----------------

root=tk.Tk()
root.title("Steganography Hacker Tool - Final")
root.geometry("980x640")
root.configure(bg=BG)
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)

# ---------- ENCRYPT FRAME ----------
enc=tk.LabelFrame(root,text=" ENCRYPTION ",bg=PANEL,fg=FG,font=("Consolas",11,"bold"))
enc.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

tk.Button(enc,text="Upload Image",bg=BTN,fg=FG,command=upload_enc).pack(pady=3)
tk.Button(enc,text="Remove Image",bg=BTN,fg=FG,command=remove_enc).pack()

enc_preview=tk.Label(enc,bg=PANEL); enc_preview.pack(pady=5)
enc_info=tk.Label(enc,bg=PANEL,fg=FG,font=("Consolas",9)); enc_info.pack()

tk.Label(enc,text="Password (optional)",bg=PANEL,fg=FG).pack()
pwd_entry=tk.Entry(enc,show="*",bg=ENTRY,fg=FG,insertbackground=FG); pwd_entry.pack()

enc_text=tk.Text(enc,height=8,width=42,bg=ENTRY,fg=FG,insertbackground=FG)
enc_text.pack(pady=5)

tk.Button(enc,text="Encrypt",bg=BTN,fg=FG,command=encrypt).pack(pady=2)
download_btn=tk.Button(enc,text="Download Image",bg=BTN,fg=FG,state="disabled",command=download)
download_btn.pack()
tk.Button(enc,text="Clear Message",bg=BTN,fg=FG,command=clear_enc_text).pack(pady=2)

# ---------- DECRYPT FRAME ----------
dec=tk.LabelFrame(root,text=" DECRYPTION ",bg=PANEL,fg=FG,font=("Consolas",11,"bold"))
dec.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")

tk.Button(dec,text="Upload Encrypted Image",bg=BTN,fg=FG,command=upload_dec).pack(pady=3)
tk.Button(dec,text="Remove Image",bg=BTN,fg=FG,command=remove_dec).pack()

dec_preview=tk.Label(dec,bg=PANEL); dec_preview.pack(pady=5)
dec_info=tk.Label(dec,bg=PANEL,fg=FG,font=("Consolas",9)); dec_info.pack()

tk.Label(dec,text="Password (if used)",bg=PANEL,fg=FG).pack()
pwd_dec_entry=tk.Entry(dec,show="*",bg=ENTRY,fg=FG,insertbackground=FG); pwd_dec_entry.pack()

tk.Button(dec,text="Decrypt",bg=BTN,fg=FG,command=decrypt).pack(pady=3)

dec_text=tk.Text(dec,height=8,width=42,bg=ENTRY,fg=FG,insertbackground=FG)
dec_text.pack()

tk.Button(dec,text="Clear Text",bg=BTN,fg=FG,command=clear_dec_text).pack(pady=2)

# ---------- LOG ----------
log_box=tk.Text(root,height=7,bg="#050805",fg=FG,insertbackground=FG,state="disabled")
log_box.grid(row=1,column=0,columnspan=2,padx=10,pady=(0,10),sticky="ew")

log("System ready. Final polished version loaded.")

root.mainloop()
