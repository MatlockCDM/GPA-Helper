# 📚 README: GPA Helper - Language Class Organizer

### **📌 Overview**
**GPA Helper** is a tool designed to help students and teachers quickly access **recent language class materials**.

- The program organizes class folders by **session number**, where each new class is assigned the next number.  
  - Example:  
    ```
    1 Feb 10
    2 Feb 15
    3 Feb 20
    ```
- It automatically finds:
  - The **most recent class folder** (highest number).
  - **Previous class sessions** based on learning intervals (**1, 3, 5, 10, 20, 40, 105, 365 classes ago**).  

When clicking a folder, it **opens it in File Explorer** and **marks it as "Opened"**.

---

## **📝 Installation & Running the Program**
### **🔹 Windows Users**
1. **Download `folder_browser.exe`** (provided by your instructor).  
2. Place it in a folder where your class materials are stored.  
3. **Double-click `folder_browser.exe`** to launch the program.  

### **🔹 macOS Users**
1. **Download `folder_browser.app`** (if provided).  
2. If necessary, grant permission:  
   ```sh
   chmod +x folder_browser.app
   ```
3. **Double-click `folder_browser.app`** to open it.  
4. If macOS blocks it as an unidentified developer, go to:  
   **System Preferences → Security & Privacy → Allow Anyway**.  

### **🔹 Running from Source Code (Python)**
If you have Python installed and want to run the script manually:  
1. Download `folder_browser.py`.  
2. Make sure your Python installation includes Tkinter. On macOS, the installer
   from python.org includes it; Homebrew users can install `python-tk` if needed.
3. Open a terminal or command prompt, navigate to the script’s location, and run:
   ```sh
   python folder_browser.py
   ```

---

## **📌 How to Use the Program**
### **Step 1: Select Your Base Directory**
- Click **"Select Base Directory"** and choose the folder where your **class session folders** are stored.  
- The program **remembers your selection** for future use.  

### **Step 2: Viewing Class Folders**
- The program detects **numerically ordered class folders**, displaying them in **descending order** (newest first).  
- It finds:
  - **The most recent class folder** (highest number).
  - **Past class sessions** that align with review intervals:  
    - **1 class ago**
    - **3 classes ago**
    - **5 classes ago**
    - **10 classes ago**
    - **20 classes ago**
    - **40 classes ago**
    - **105 classes ago**
    - **365 classes ago**
  
### **Step 3: Opening Folders**
- Click a folder's **button** to open it.  
- The button will turn **yellow** to show that it has been opened.  

### **Searching Notes and Documents**
- Search is case-insensitive and supports `.txt`, `.text`, `.md`, `.csv`,
  `.tsv`, `.log`, `.pdf`, `.docx`, `.odt`, and `.rtf` files.
- Legacy `.doc` files require antiword, LibreOffice, or macOS `textutil`.
- Double-click a result to open it in the default application.

---

## **📌 Folder Naming Guidelines**
To ensure the program detects your folders correctly:  
✅ **Each class session folder must start with a number** (session number).  
✅ **After the number, you can add a date or description** (optional).  
✅ Example folder names:
   ```
   1 Feb 10
   2 Feb 15
   3 Feb 20
   4 Feb 25
   5 Mar 1
   ```
🚫 **Incorrect format (will not be detected):**
   ```
   English Class 1
   February 10 Class
   Spanish Lesson 2
   ```

---

## **🛠 Troubleshooting**
### **❌ No folders are displayed**
✅ **Fix:** Ensure your folders are inside the selected **base directory** and follow the **correct naming format** (`1 Date`).  

### **❌ The program doesn't open folders when clicked**
✅ **Fix:** Check if the folder path exists. Manually try:  
- **Windows:**
  ```sh
  explorer "C:\Path\To\Your\Folder"
  ```
- **macOS:**
  ```sh
  open "/Path/To/Your/Folder"
  ```

### **❌ The program crashes on startup**
✅ **Fix:** Try running the executable from **Command Prompt** to see error messages:
   ```sh
   folder_browser.exe
   ```
✅ **Fix:** If using Python, install a Python build with Tkinter support. On
macOS, use the installer from python.org or install Homebrew's `python-tk`.

### **❌ Mac says the app is from an “unidentified developer”**
✅ **Fix:** Go to **System Preferences → Security & Privacy → General** and click **Allow Anyway**.  

---

## **📌 Frequently Asked Questions**
### **Q: How does the program determine which folders to display?**
- It **identifies the highest-numbered folder** (latest class session).  
- It **includes past class folders** at **review intervals** (**1, 3, 5, 10, 20, 40, 105, 365 sessions ago**).  

### **Q: Will the program delete or modify my folders?**
- **No.** The program **only reads folder names** and does not change anything.

### **Q: Can I change the base directory later?**
- Yes! Just click **"Select Base Directory"** again.

### **Q: Do I need an internet connection to use this program?**
- **No.** Everything runs locally on your computer.

---

## **📌 About This Program**
- **Purpose:** Help students and teachers access recent and past language class materials easily.  
- **Developed with:** Python & Tkinter  
- **Platform Compatibility:** Windows, macOS (Linux may work with minor modifications)  

---

