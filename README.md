# Advanced Steganography Suite – Image Edition

A professional dark-themed GUI application built with Python and Tkinter for secure image steganography.

This tool allows users to hide encrypted text messages inside image files using LSB (Least Significant Bit) steganography. The system ensures reliable message embedding by using lossless image formats.

---

## 🔐 Features

- Image-only steganography (PNG, JPG, JPEG, BMP)
- Password-protected message encryption (SHA-256 based XOR layer)
- Dynamic expanding message input fields
- Real-time progress percentage display
- Image preview before encryption/decryption
- Clean hacker-themed dark UI
- Reset system functionality
- Fast and reliable LSB embedding
- Download encrypted image after processing

---

## 🖼 Supported Formats

- PNG (Recommended – Lossless)
- JPG / JPEG
- BMP

⚠ For best reliability, use PNG format to prevent data loss.

---

## 🛠 Technologies Used

- Python 3
- Tkinter (GUI)
- Pillow (Image Processing)
- Hashlib (Security Layer)

---

## 💻 Installation Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/gvpofficial/Steganography-Image-Encrypt-Decrypt-Tool.git
cd Steganography-Image-Encrypt-Decrypt-Tool
```

### 2️⃣ Install Required Dependencies

```bash
pip install pillow
```

Tkinter usually comes pre-installed with Python.

### 3️⃣ Run the Application

```bash
python steg_tool.py
```

---

## 🚀 How It Works

1. Upload an image.
2. Enter your secret message.
3. Optionally set a password.
4. Click **Encrypt**.
5. Download the encrypted image.
6. To retrieve the message, upload the encrypted image and click **Decrypt**.

---

## 📌 Notes

- Only image files are supported.
- Encrypted images should be saved as PNG for maximum reliability.
- Larger images can store more hidden data.
- This project is intended for educational and research purposes.

---

## 📜 License (MIT License)

MIT License

Copyright (c) 2026 Gupthan Vishnu Prasad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👨‍💻 Author

Developed by **Gupthan Vishnu Prasad**  
Assisted by ChatGPT
