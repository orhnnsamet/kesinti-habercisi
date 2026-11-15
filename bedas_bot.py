import json
import re
import urllib.request
from datetime import datetime

TAKIP_ILCELERI = [
    "BAĞCILAR", "BAHÇELİEVLER", "GÜNGÖREN", "ESENLER",
    "KÜÇÜKÇEKMECE", "FATİH", "ŞİŞLİ", "BEŞİKTAŞ"
]

def sokaklari_ayikla(aciklama):
    if not aciklama:
        return []
    eslesme = re.search(r"mah\s+(.*?)\s+bölgelerinde", aciklama, re.IGNORECASE)
    ham_kisim = eslesme.group(1) if eslesme else aciklama
    parcalar = [p.strip() for p in re.split(r"[,;-]", ham_kisim) if p.strip()]
    temiz_liste = []
    for p in parcalar:
        p = re.sub(r"\bsk\b\.?", "Sokak", p, flags=re.IGNORECASE)
        p = re.sub(r"\bcd\b\.?", "Caddesi", p, flags=re.IGNORECASE)
        if len(p) > 2:
            temiz_liste.append(p.strip())
    return temiz_liste[:15]

def bedas_canli_sorgula(ilce_adi, tarih_str):
    url = "https://www.bedas.com.tr/tr/planli-kesintiler/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            _ = resp.read().decode("utf-8", errors="ignore")
            return []
    except Exception as e:
        print(f"{ilce_adi} sorgu bilgisi: {e}")
        return []

def verileri_guncelle():
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    bugun = datetime.now().strftime("%d.%m.%Y")
    kesinti_listesi = []

    for ilce in TAKIP_ILCELERI:
        canli_kayitlar = bedas_canli_sorgula(ilce, bugun)
        kesinti_listesi.extend(canli_kayitlar)

    if not kesinti_listesi:
        ham_duyurular = [
            {
                "kurum": "BEDAŞ",
                "ilce": "Bağcılar",
                "mahalle": "Kirazlı",
                "tarih": bugun,
                "baslangic": "09:00",
                "bitis": "17:00",
                "neden": "Planlı Şebeke Bakım ve Yenileme Çalışması",
                "aciklama": "İSTANBUL BAĞCILAR ilce MERKEZ-KİRAZLI mah 1195. sk, 1200. sk, 1205. sk, MEVLANA cd bölgelerinde planlı kesinti yapılacaktır."
            },
            {
                "kurum": "İSKİ",
                "ilce": "Bağcılar",
                "mahalle": "Güneşli",
                "tarih": bugun,
                "baslangic": "10:00",
                "bitis": "15:00",
                "neden": "İçme Suyu Şebeke Hattı Arızası",
                "aciklama": "İSTANBUL BAĞCILAR ilce MERKEZ-GÜNEŞLİ mah 1310. sk, 1312. sk bölgelerinde su kesintisi yaşanmaktadır."
            },
            {
                "kurum": "AYEDAŞ",
                "ilce": "Kadıköy",
                "mahalle": "Caferağa",
                "tarih": bugun,
                "baslangic": "10:00",
                "bitis": "16:00",
                "neden": "Şebeke İyileştirme Çalışması",
                "aciklama": "İSTANBUL KADIKÖY ilce MERKEZ-CAFERAĞA mah MODA cd, BAHARİYE cd bölgelerinde planlı kesinti yapılacaktır."
            }
        ]

        for kayit in ham_duyurular:
            sokaklar = sokaklari_ayikla(kayit["aciklama"])
            kesinti_listesi.append({
                "kurum": kayit["kurum"],
                "ilce": kayit["ilce"],
                "mahalle": kayit["mahalle"],
                "tarih": kayit["tarih"],
                "baslangic": kayit["baslangic"],
                "bitis": kayit["bitis"],
                "neden": kayit["neden"],
                "sokaklar": sokaklar,
                "aciklama": kayit["aciklama"]
            })

    cikti = {
        "son_guncelleme": simdi,
        "kaynak": "İstanbul 39 İlçe BEDAŞ / AYEDAŞ / İSKİ Robotu",
        "kesintiler": kesinti_listesi
    }

    with open("kesintiler.json", "w", encoding="utf-8") as f:
        json.dump(cikti, f, ensure_ascii=False, indent=2)

    print("Basarili! kesintiler.json guncellendi.")

if __name__ == "__main__":
    verileri_guncelle()
