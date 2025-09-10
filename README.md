
A **Flask-based REST API** for face registration and recognition.  
Built with **Python**, **Flask**, **MySQL**, and **face_recognition**.

---

## 🚀 Features
-📌 **Face Registration**: Accepts base64 images, generates face encodings, stores them as `.pkl`, and saves metadata in MySQL.  
-🔑 **Face Recognition**: Compares uploaded images with stored encodings and returns the matched **ID (TC number)**.  
-🗄️ **MySQL Integration**: Stores encoding filenames; updates on duplicate IDs.  
-🔒 **CORS Enabled**: Allows communication with Flutter apps. 

File Structure
faceid_server/
├── encodings/ # Saved encodings (.pkl, .jpg)
├── face_recognition_server.py
├── temp.jpg


<img width="500" height="1000" alt="1" src="https://github.com/user-attachments/assets/babc9dac-a299-4fdb-a642-fbb4592fb43e" />

<img width="500" height="1000" alt="2" src="https://github.com/user-attachments/assets/ace28dfc-923b-4f75-90c7-66a9d7cf2c26" />

