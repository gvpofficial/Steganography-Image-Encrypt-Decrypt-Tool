# 🔐 Steganography Hacker Tool

A dark-themed GUI-based image steganography application built with
**Python (Tkinter + Pillow)**.

This tool allows users to securely hide secret messages inside images
using LSB (Least Significant Bit) steganography with optional password
protection.

------------------------------------------------------------------------

## 🚀 Features

### 🖼 Image Handling

-   Upload image (PNG, JPG, JPEG)
-   Remove image
-   Image preview thumbnail
-   Displays filename, format, and resolution
-   Download encrypted image

### 🔐 Encryption

-   Hide secret message inside image
-   Optional password protection (SHA-256 based XOR encryption)
-   Capacity check (prevents overflow)
-   Re-encrypt multiple times

### 🔓 Decryption

-   Extract hidden message from encrypted image
-   Optional password support
-   Clear decrypted text option

### 🧑‍💻 UI Features

-   Dark hacker-style theme
-   Live terminal-style log panel
-   Clean and stable layout
-   Fully GUI-based (no console needed)

------------------------------------------------------------------------

## 🛠 Technologies Used

-   Python 3.x
-   Tkinter (GUI)
-   Pillow (Image Processing)
-   hashlib (Password hashing)

------------------------------------------------------------------------

## 📂 Project Structure

    Steganography-Hacker-Tool/
    │
    ├── steg_tool.py
    ├── README.md
    └── requirements.txt

------------------------------------------------------------------------

## ⚙ Installation

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/your-username/Steganography-Hacker-Tool.git
cd Steganography-Hacker-Tool
```

### 2️⃣ Install dependencies

``` bash
pip install pillow
```

### 3️⃣ Run the application

``` bash
python steg_tool.py
```

------------------------------------------------------------------------

## 🖥 Convert to Portable EXE (Windows)

Install PyInstaller:

``` bash
pip install pyinstaller
```

Build executable:

``` bash
pyinstaller --onefile --windowed --clean --collect-all PIL steg_tool.py
```

Your portable `.exe` file will be inside:

    dist/

------------------------------------------------------------------------

## 🔒 How It Works

### 1️⃣ Steganography (LSB Method)

-   Each pixel has 3 color channels (RGB)
-   The least significant bit of each channel is modified
-   Secret message is converted to binary and embedded
-   A unique end marker (`#####END#####`) is added

### 2️⃣ Password Security

-   Password is hashed using SHA-256
-   XOR encryption is applied to the message
-   During decryption, same password restores original message

------------------------------------------------------------------------

## 🎓 Academic Use

This project is suitable for:

-   Cybersecurity demonstrations
-   Information security coursework
-   Final year mini project
-   Steganography practical lab
-   Python GUI projects

------------------------------------------------------------------------

## ⚠ Disclaimer

This project is developed for **educational purposes only**.\
Do not use it for malicious or illegal activities.

------------------------------------------------------------------------

## 👨‍💻 Author

Your Name\
GitHub: https://github.com/your-username

------------------------------------------------------------------------

## ⭐ If you like this project

Give it a ⭐ on GitHub!
