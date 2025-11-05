import tkinter as tk
from PIL import Image, ImageTk

oyun_agaci = {
    'soru': 'Aklındaki kişinin saçı uzun mu?',
    'evet': {
        'soru': 'Gözlük takıyor mu?',
        'evet': { 'sonuc': 'Nil' },
        'hayır': {
            'soru': 'Arabası var mı?',
            'evet': { 'sonuc': 'İnci' },
            'hayır': {
                'soru': 'Kapibarası var mı?',
                'evet': { 'sonuc': 'Aybüke' },
                'hayır': { 'sonuc': 'Listede böyle biri yok' }
            }
        }
    },
    'hayır': {
        'soru': 'Gözlük takıyor mu?',
        'evet': {
            'soru': 'Sakalı var mı?',
            'evet': { 'sonuc': 'Listede böyle biri yok' },
            'hayır': {
                'soru': 'Saçı kıvırcık mı?',
                'evet': { 'sonuc': 'Utku' },
                'hayır': {
                    'soru': '30 yaşından büyük mü?',
                    'evet': { 'sonuc': 'Orçun Hoca' },
                    'hayır': { 'sonuc': 'Umut' }
                }
            }
        },
        'hayır': { 'sonuc': 'Listede böyle biri yok' }
    }
}

onay_sorulari = {
    'Nil': [
        ('Sarışın mı?', 'evet'),
        ('Sinirli mi?', 'evet'),
        ('Domatesten nefret ediyor mu?', 'evet')
    ],
    'İnci': [
        ('Renkli gözlü mü?', 'evet'),
        ("Ex'inin adı Ömer mi?", 'evet')
    ],
    'Aybüke': [
        ('Sürekli meşgul mü?', 'evet'),
        ('Bilecikli mi?', 'evet')
    ],
    'Utku': [
        ('Çok iyi matcha yapıyor mu?', 'evet')
    ],
    'Orçun Hoca': [
        ('Öğrencileri zorbalıyor mu?', 'evet')
    ],
    'Umut': [
        ('Roblox karakteri mi?', 'evet'),
        ("Sevgilisinin adı Beyza mı?", 'evet')
    ]
}

RENK_ARKA_PLAN = "#fdfaff"
RENK_YAZI_NORMAL = "#634b66"
RENK_YAZI_SONUC = "#a082b8"
RENK_YAZI_HATA = "#e08d9b"
RENK_EVET_BG = "#f7c0c7"
RENK_EVET_YAZI = "#634b66"
RENK_HAYIR_BG = "#d3b5e5"
RENK_HAYIR_YAZI = "#634b66"
RENK_YENIDEN_BG = "#e1e3f0"
RENK_YENIDEN_YAZI = "#634b66"

FOTO_BOYUT = (150, 150) 

FOTO_DOSYALARI = {
    'Orçun Hoca': "orcun.jpg", 
    'Nil': "nil.jpg",
    'İnci': "inci.jpg",
    'Aybüke': "aybuke.jpg",
    'Umut': "umut.jpg",
    'Utku': "utku.jpg",
    'Bilmiyorum': "bilmiyorum.jpg" 
}

guncel_dal = {}
oyun_modu = "eleme"
onay_kisisi = None
onay_soru_indexi = 0
current_photo = None 

def oyunu_baslat():
    global guncel_dal, oyun_modu, onay_kisisi, onay_soru_indexi, current_photo
    
    guncel_dal = oyun_agaci
    oyun_modu = "eleme"
    onay_kisisi = None
    onay_soru_indexi = 0
    
    buton_cercevesi.pack(pady=10)
    evet_buton.config(state=tk.NORMAL)
    hayir_buton.config(state=tk.NORMAL)
    
    sonuc_etiketi.config(text="", fg=RENK_YAZI_SONUC)
    soru_etiketi.config(text=guncel_dal['soru'])

    foto_etiket.config(image='')
    foto_etiket.pack_forget() 
    current_photo = None 

def goster_foto(isim):
    global current_photo
    
    dosya_adi = FOTO_DOSYALARI.get(isim, FOTO_DOSYALARI.get('Bilmiyorum'))

    if not dosya_adi:
        print("Hata: Varsayılan 'Bilmiyorum' fotoğrafı bile bulunamadı.")
        return

    try:
        img = Image.open(dosya_adi) 
        img = img.resize(FOTO_BOYUT, Image.LANCZOS)
        current_photo = ImageTk.PhotoImage(img)
        foto_etiket.config(image=current_photo)
        foto_etiket.pack(pady=10)
    except FileNotFoundError:
        print(f"Hata: Fotoğraf bulunamadı: {dosya_adi}")
        sonuc_etiketi.config(text=f"Fotoğraf bulunamadı: {dosya_adi}", fg=RENK_YAZI_HATA)
    except Exception as e:
        print(f"Fotoğraf yüklenirken bir hata oluştu: {e}")
        sonuc_etiketi.config(text="Fotoğraf yüklenemedi!", fg=RENK_YAZI_HATA)

def cevap_ver(cevap):
    global guncel_dal, oyun_modu, onay_kisisi, onay_soru_indexi

    if oyun_modu == "eleme":
        try:
            guncel_dal = guncel_dal[cevap]
        except KeyError:
            oyun_bitti("Bu cevaba göre birini bulamadım.", hata=True)
            return

        if 'soru' in guncel_dal:
            soru_etiketi.config(text=guncel_dal['soru'])
            
        elif 'sonuc' in guncel_dal:
            bulunan_isim = guncel_dal['sonuc']
            
            if bulunan_isim in onay_sorulari:
                oyun_modu = "onaylama"
                onay_kisisi = bulunan_isim
                onay_soru_indexi = 0
                
                ilk_onay_sorusu = onay_sorulari[onay_kisisi][onay_soru_indexi][0]
                soru_etiketi.config(text=ilk_onay_sorusu)
            else:
                oyun_bitti(f"Sonuç: {bulunan_isim}", hata=True)
    
    elif oyun_modu == "onaylama":
        soru_metni, beklenen_cevap = onay_sorulari[onay_kisisi][onay_soru_indexi]
        
        if cevap != beklenen_cevap:
            oyun_bitti(f"Eyvah! Cevapların {onay_kisisi} ile uyuşmadı. \nYeniden başla.", hata=True)
            return
            
        onay_soru_indexi += 1
        
        if onay_soru_indexi < len(onay_sorulari[onay_kisisi]):
            sonraki_soru = onay_sorulari[onay_kisisi][onay_soru_indexi][0]
            soru_etiketi.config(text=sonraki_soru)
        else:
            goster_foto(onay_kisisi) 
            oyun_bitti(f"Tebrikler! Tüm cevaplar eşleşti. \nAklındaki kişi: {onay_kisisi}!", basarili=True)


def oyun_bitti(mesaj, hata=False, basarili=False):
    if hata:
        sonuc_etiketi.config(text=mesaj, fg=RENK_YAZI_HATA)
        if not basarili:
             goster_foto('Bilmiyorum')
    elif basarili:
        sonuc_etiketi.config(text=mesaj, fg=RENK_YAZI_SONUC)
    else: 
        sonuc_etiketi.config(text=mesaj, fg=RENK_YAZI_HATA)
        
    soru_etiketi.config(text="Oyun Bitti!")
    buton_cercevesi.pack_forget() 

pencere = tk.Tk()
pencere.title("Arkadaş Tahmin Oyunu")
pencere.geometry("450x550")
pencere.config(bg=RENK_ARKA_PLAN)

soru_etiketi = tk.Label(pencere, text="Oyuna Hoş Geldin!", 
                        font=("Arial", 14), wraplength=400, height=4,
                        bg=RENK_ARKA_PLAN,
                        fg=RENK_YAZI_NORMAL)
soru_etiketi.pack(pady=10) 

foto_etiket = tk.Label(pencere, bg=RENK_ARKA_PLAN)

buton_cercevesi = tk.Frame(pencere, bg=RENK_ARKA_PLAN)
buton_cercevesi.pack(pady=10)

evet_buton = tk.Button(buton_cercevesi, text="Evet", font=("Arial", 12), width=12,
                       bg=RENK_EVET_BG,
                       fg=RENK_EVET_YAZI,
                       command=lambda: cevap_ver('evet'))
evet_buton.pack(side=tk.LEFT, padx=15) 

hayir_buton = tk.Button(buton_cercevesi, text="Hayır", font=("Arial", 12), width=12,
                        bg=RENK_HAYIR_BG,
                        fg=RENK_HAYIR_YAZI,
                        command=lambda: cevap_ver('hayır'))
hayir_buton.pack(side=tk.LEFT, padx=15) 

sonuc_etiketi = tk.Label(pencere, text="", font=("Arial", 16, "bold"), wraplength=400,
                         bg=RENK_ARKA_PLAN,
                         fg=RENK_YAZI_SONUC)
sonuc_etiketi.pack(pady=10)

yeniden_basla_buton = tk.Button(pencere, text="Yeniden Başla", font=("Arial", 10, "bold"),
                                bg=RENK_YENIDEN_BG,
                                fg=RENK_YENIDEN_YAZI,
                                command=oyunu_baslat)
yeniden_basla_buton.pack(side=tk.BOTTOM, pady=10) 

oyunu_baslat()
pencere.mainloop()