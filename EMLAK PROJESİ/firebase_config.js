// Firebase modüllerini import et (modül linkleri CDN'den alınıyor)
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-firestore.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-analytics.js";

// Firebase yapılandırma nesnesi (senin verdiğin bilgilerle)
const firebaseConfig = {
  apiKey: "AIzaSyAP0Ine5bUjy1TNTsjw_7jggdAbIElG_04",
  authDomain: "emlakdunyasi-aed77.firebaseapp.com",
  projectId: "emlakdunyasi-aed77",
  storageBucket: "emlakdunyasi-aed77.firebasestorage.app",
  messagingSenderId: "457595408651",
  appId: "1:457595408651:web:865529927b8ffaee60920e",
  measurementId: "G-4J7VBZXVHX"
};

// Firebase'i başlat
const app = initializeApp(firebaseConfig);

// Firestore (veri tabanı) ve Analytics'i başlat
const db = getFirestore(app);
const analytics = getAnalytics(app);

console.log("Firebase frontend bağlantısı başarılı");
