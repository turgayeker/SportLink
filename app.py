from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# 1. Ana Sayfa (Kayıt Ekranı)
@app.route('/')
def ana_sayfa():
    return render_template('kayit.html')

# 2. Kayıt Verilerini Alan Yer
@app.route('/kaydet', methods=['POST'])
def kaydet():
    eposta = request.form.get('eposta')
    sifre = request.form.get('sifre')
    rol = request.form.get('rol')
    
    with open("kullanicilar.txt", "a", encoding="utf-8") as dosya:
        dosya.write(f"E-posta: {eposta} | Şifre: {sifre} | Rol: {rol}\n")
        
    # Kayıt olunca kullanıcının verilerini alıp direkt profil sayfasına paslıyoruz
    return redirect(url_for('profil_sayfasi', eposta=eposta, rol=rol))

# 3. Kişiye Özel Profil Sayfası
@app.route('/profil')
def profil_sayfasi():
    eposta = request.args.get('eposta', 'Ziyaretçi')
    rol = request.args.get('rol', 'Belirtilmemiş')
    
    kullanıcı_verisi = {
        "eposta": eposta,
        "rol": rol
    }
    return render_template('profil.html', kullanıcı=kullanıcı_verisi)

# 4. İlanları Listeleyen Pazar Yeri Ekranı
@app.route('/ilanlar', methods=['GET'])
def ilanlar_sayfasi():
    arama_brans = request.args.get('arama_brans', '').strip().lower()
    arama_sehir = request.args.get('arama_sehir', '').strip().lower()

    liste = []
    if os.path.exists("ilanlar.txt"):
        with open("ilanlar.txt", "r", encoding="utf-8") as dosya:
            for satir in dosya:
                if satir.strip():
                    parcalar = satir.strip().split(" | ")
                    baslik = parcalar[0].split(": ")[1]
                    brans = parcalar[1].split(": ")[1]
                    sehir = parcalar[2].split(": ")[1]
                    detay = parcalar[3].split(": ")[1]
                    
                    if arama_brans and arama_brans not in brans.lower():
                        continue
                    if arama_sehir and arama_sehir not in sehir.lower():
                        continue

                    liste.append({
                        "baslik": baslik,
                        "brans": brans,
                        "sehir": sehir,
                        "detay": detay
                    })
    
    return render_template('ilanlar.html', gelen_ilanlar=liste)

# 5. İlan Verme Sayfası
@app.route('/ilan_ver')
def ilan_ver_sayfasi():
    return render_template('ilan_ver.html')

# 6. İlan Kaydeden Yer
@app.route('/ilan_kaydet', methods=['POST'])
def ilan_kaydet():
    baslik = request.form.get('baslik')
    brans = request.form.get('brans')
    sehir = request.form.get('sehir')
    detay = request.form.get('detay')
    
    with open("ilanlar.txt", "a", encoding="utf-8") as dosya:
        dosya.write(f"Başlık: {baslik} | Branş: {brans} | Şehir: {sehir} | Detay: {detay}\n")
        
    return redirect('/ilanlar')

if __name__ == '__main__':
    app.run(debug=True)