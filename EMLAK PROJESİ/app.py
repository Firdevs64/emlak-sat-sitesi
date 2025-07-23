from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import auth, db
from firebase_config import firestore_db
from firebase_admin import firestore
import os
import random
from werkzeug.security import check_password_hash
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        phone = data.get('phone')

        # Firebase Authentication ile kullanıcı oluştur
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name,
            phone_number=phone
        )

        # Firestore'a kullanıcı bilgilerini kaydet
        user_data = {
            'uid': user.uid,
            'email': email,
            'name': name,
            'phone': phone,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        firestore_db.collection('users').document(user.uid).set(user_data)

        return jsonify({
            'success': True,
            'message': 'Kullanıcı başarıyla oluşturuldu',
            'user': {
                'uid': user.uid,
                'email': user.email,
                'name': user.display_name
            }
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    try:
        # Firebase Authentication ile giriş
        user = auth.get_user_by_email(email)
        # Burada doğrudan şifre kontrolü yapılamaz!
        # Şifre kontrolü için frontendde Firebase JS SDK ile signInWithEmailAndPassword kullanılmalı
        return jsonify({'success': True, 'user': {'email': user.email, 'name': user.display_name}})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 401

@app.route('/api/featured-listings', methods=['GET'])
def get_featured_listings():
    try:
        ref = db.reference('ilanlar')
        all_listings = ref.get()
        print("Tüm ilanlar:", all_listings)
        if not all_listings:
            return jsonify([])

        listings = []
        for key, value in all_listings.items():
            value['id'] = key  # Anahtarı id olarak ekle
            listings.append(value)
        random.shuffle(listings)
        featured = listings[:6]
        print("Seçilen ilanlar:", featured)

        return jsonify(featured)
    except Exception as e:
        print("Hata:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/all-listings', methods=['GET'])
def get_all_listings():
    try:
        ref = db.reference('ilanlar')
        all_listings = ref.get()
        if not all_listings:
            return jsonify([])
        listings = []
        for key, value in all_listings.items():
            value['id'] = key
            listings.append(value)
        return jsonify(listings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_email(to_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'seninmail@gmail.com'
    smtp_pass = 'uygulama-şifresi'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())

@app.route('/api/send-reset-email', methods=['POST'])
def send_reset_email():
    data = request.get_json()
    email = data.get('email')
    try:
        # Firebase ile şifre sıfırlama linki oluştur
        link = auth.generate_password_reset_link(email)
        # Firebase kendi başına e-posta göndermez, sadece linki üretir!
        # Eğer frontendde kullanıcının mailine göndermek istiyorsan, bu linki send_email ile gönderebilirsin.
        # Ama en kolayı: linki response olarak dönmek ve frontendde kullanıcıya göstermek.
        return jsonify({'success': True, 'message': 'Şifre sıfırlama bağlantısı oluşturuldu.', 'link': link})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/add-favorite', methods=['POST'])
def add_favorite():
    data = request.json
    email = data['email']
    ilan_id = data['ilanId']
    user_ref = firestore_db.collection('users').where('email', '==', email).get()
    if not user_ref:
        return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'})
    user_doc = user_ref[0]
    favoriler = user_doc.to_dict().get('favoriler', [])
    if ilan_id not in favoriler:
        favoriler.append(ilan_id)
        user_doc.reference.update({'favoriler': favoriler})
    return jsonify({'success': True})

@app.route('/api/get-favorites')
def get_favorites():
    email = request.args.get('email')
    user_ref = firestore_db.collection('users').where('email', '==', email).get()
    if not user_ref:
        return jsonify({'favoriler': []})
    user_doc = user_ref[0]
    favoriler = user_doc.to_dict().get('favoriler', [])
    return jsonify({'favoriler': favoriler})

if __name__ == '__main__':
    app.run(debug=True, port=5000)