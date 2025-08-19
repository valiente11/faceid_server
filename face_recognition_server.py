import os                                       #dosya işlemleri
import base64                                   #string formatında görüntü için decoder
import face_recognition                         #yüz tanımlama algoritmaları için
import pickle                                   #pkl formatında kaydetmek içim
from flask import Flask, request, jsonify       #server için
from flask_cors import CORS                     #flutter ile iletişim için 

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sagsagrfh00.",
    database="qr_security"
)
cursor = db.cursor() #gösterge


app = Flask(__name__) #flask uyguşamasını başlat
CORS(app)  #fluttera istekte bulunabilmesi için izin ver 


ENCODING_DIR = "encodings"
if not os.path.exists(ENCODING_DIR):
    os.makedirs(ENCODING_DIR)

@app.route("/register", methods=["POST"])
def register_face():
    print("✅ /register endpoint çağrıldı")
    data = request.get_json() 
    image_data = data.get("image")
    tc = data.get("tc")

    if not image_data or not tc:
        return jsonify({"status": "error", "message": "Eksik veri"}), 400

    try:
        # Görseli diske kaydet
        image_bytes = base64.b64decode(image_data)
        image_path = os.path.join(ENCODING_DIR, f"{tc}.jpg") #encoding dosyasına tc.jpg olarak ekle
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # Yüz encoding üret
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            return jsonify({"status": "error", "message": "Yüz bulunamadı"}), 400

        encoding = encodings[0]
        pkl_path = os.path.join(ENCODING_DIR, f"{tc}.pkl")
        with open(pkl_path, "wb") as f:
            pickle.dump(encoding, f)

        sql = "INSERT INTO face_encodings (tc, encoding_filename) VALUES (%s, %s) ON DUPLICATE KEY UPDATE encoding_filename=%s"#aynı tc varsa güncelle
        val = (tc, f"{tc}.pkl", f"{tc}.pkl")
        cursor.execute(sql, val)
        db.commit()

        return jsonify({"status": "success", "message": "Yüz kaydedildi"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#login için flutterdan alınan base64 formatındaki verinin post edilmesi
@app.route("/recognize", methods=["POST"])
def recognize_face():
    data = request.get_json()
    image_data = data.get("image")

    if not image_data:
        return jsonify({"status": "error", "message": "Görüntü eksik"}), 400

    try:
        # 1. Görüntüyü geçici olarak kaydet
        image_bytes = base64.b64decode(image_data)
        with open("temp.jpg", "wb") as f:
            f.write(image_bytes)

        # 2. Yüz encoding'ini al
        unknown_image = face_recognition.load_image_file("temp.jpg")
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:
            return jsonify({"status": "error", "message": "Yüz algılanamadı"}), 400

        unknown_encoding = unknown_encodings[0]

        # 3. Kayıtlı encoding'lerle karşılaştır
        min_distance = 1.0
        matched_filename = None

        for file in os.listdir(ENCODING_DIR):
            if file.endswith(".pkl"):
                file_path = os.path.join(ENCODING_DIR, file)
                with open(file_path, "rb") as f:
                    known_encoding = pickle.load(f)

                distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
                print(f"📏 {file} → mesafe: {distance}")

                if distance < min_distance and distance < 0.5:
                    min_distance = distance
                    matched_filename = file
                    print(f"✅ Yeni en yakın eşleşme bulundu: {matched_filename} (mesafe: {min_distance})")

        # 4. Eşleşme bulunduysa veritabanından TC'yi al
        if matched_filename:
            print(f"[DEBUG] Eşleşen dosya adı: {matched_filename}")
            sql = "SELECT tc FROM face_encodings WHERE encoding_filename = %s"
            cursor.execute(sql, (matched_filename,))
            result = cursor.fetchone()
            if result:
                print(f"[DEBUG] Veritabanından dönen TC: {result[0]}")
                return jsonify({"status": "success", "tc": result[0]})

        return jsonify({"status": "fail", "message": "Yüz tanınamadı"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
