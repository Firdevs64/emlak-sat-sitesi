import firebase_admin
from firebase_admin import credentials, db, firestore

cred = credentials.Certificate("C:\\Users\\Firdevs\\OneDrive\\Masaüstü\\EMLAK PROJESİ\\emlakdunyasi-aed77-firebase-adminsdk-fbsvc-750af0dd9f.json")
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://emlakdunyasi-aed77-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# Firestore ve Realtime Database objelerini dışa aktar
firestore_db = firestore.client()
# db zaten bir modül, ekstra bir şey yapmana gerek yok

print("Firebase bağlantısı başarılı.")
