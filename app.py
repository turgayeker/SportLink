from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# İlanların kaydedileceği dosya yolu
ILAN_DOSYASI = 'ilanlar.txt'

def ilanlari_oku():
    if not os.path.exists(ILAN_DOSYASI):
        return []
    with open(ILAN_DOSYASI, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
    
    ilanlar = []
    for satir in satirlar:
        if satir.strip():
            parcalar = satir.strip().split('|')
            if len(parcalar) == 4:
                ilanlar.append({
                    'baslik': parcalar[0],
                    'brans': parcalar[1],
                    'sehir': parcalar[2],
                    'detay': parcalar[3]
                })
    return ilanlar

def ilan_ekle(baslik, brans, sehir, detay):
    # Yeni ilanı aralarına dikey çizgi koyarak dosyaya ekliyoruz
    with open(ILAN_DOSYASI, 'a', encoding='utf-8') as f:
        f.write(f"{baslik}|{brans}|{sehir}|{detay}\n")

@app.route('/')
def ana_sayfa():
    # Arama ve filtreleme parametrelerini alıyoruz
    arama_sorgusu = request.args.get('search', '').lower()
    brans_filtresi = request.args.get('brans', '').lower()
    sehir_filtresi = request.args.get('sehir', '').lower()
    
    tum_ilanlar = ilanlari_oku()
    filtrelenmiş_ilanlar = []
    
    for ilan in tum_ilanlar:
        # Arama ve filtreleme kontrolleri
        ust_ust_üste = True
        if arama_sorgusu and arama_sorgusu not in ilan['baslik'].lower() and arama_sorgusu not in ilan['detay'].lower():
            ust_ust_üste = False
        if brans_filtresi and brans_filtresi != ilan['brans'].lower():
            ust_ust_üste = False
        if sehir_filtresi and sehir_filtresi != ilan['sehir'].lower():
            ust_ust_üste = False
            
        if ust_ust_üste:
            filtrelenmiş_ilanlar.append(ilan)
            
    return render_template('index.html', ilanlar=filtrelenmiş_ilanlar)

@app.route('/ilan-ekle', methods=['POST'])
def yeni_ilan_ekle():
    # Formdan gelen verileri yakalıyoruz
    baslik = request.form.get('baslik')
    brans = request.form.get('brans')
    sehir = request.form.get('sehir')
    detay = request.form.get('detay')
    
    if baslik and brans and sehir and detay:
        ilan_ekle(baslik, brans, sehir, detay)
        
    return redirect(url_for('ana_sayfa'))

if __name__ == '__main__':
    app.run(debug=True)