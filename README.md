## Extended Description

FaceID Server is a lightweight face recognition backend built with Python and Flask.  
It provides two main endpoints: `/register` for saving face encodings, and `/recognize` for identifying users.  
Encodings are generated using the `face_recognition` library and stored both as `.pkl` files and in a MySQL database.  

The system is designed for integration with mobile apps (e.g., Flutter), making it suitable for:
- Visitor management at security checkpoints
- Employee attendance verification
- Access control systems

This project demonstrates how to combine image processing, database storage, and REST APIs into a complete security solution.


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

📡 API Endpoints
🔹 Register Face
URL: /register
Method: POST
Description: Saves a new face encoding and links it to a user’s TC number.

🔹 Recognize Face
URL: /recognize
Method: POST
Description: Compares the uploaded face with saved encodings and returns the matched TC number if found.

<img width="500" height="1000" alt="1" src="https://github.com/user-attachments/assets/babc9dac-a299-4fdb-a642-fbb4592fb43e" />

<img width="500" height="1000" alt="2" src="https://github.com/user-attachments/assets/ace28dfc-923b-4f75-90c7-66a9d7cf2c26" />

