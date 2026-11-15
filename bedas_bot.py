# Dosya Adi: bedas_bot.py - BEDAS ve ISKI Otomatik Kesinti Robotu
import json
import re
from datetime import datetime

def metinden_sokaklari_ayikla(ham_metin):
    sokaklar = []
    eslesme = re.search(r"mah\s+(.*?)\s+bölgelerinde", ham_metin, re.IGNORECASE)
    if eslesme:
        for s in eslesme.group(1).split(","):
            temiz = s.strip().replace(" sk", ". Sokak").replace(" cd", " Caddesi")
            if temiz:
                sokaklar.append(temiz)
    return sokaklar

def verileri_guncelle():
    ornek_duyuru = "İSTANBUL BAĞCILAR ilce MERKEZ-KİRAZLI mah 1198., 1200., 1205. sk, MEVLANA cd bölgelerinde planlı kesinti yapılacaktır."
    paket = {
        "son_guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "kaynak": "BEDAS & ISKI Otomatik Robotu",
        "kesintiler": [{
            "ilce": "BAĞCILAR",
            "mahalle": "Kirazlı Mahallesi",
            "baslangic": "09:00",
            "bitis": "15:00",
            "neden": "Şebeke Bakım ve Yenileme Çalışması",
            "etkilenen_sokaklar": metinden_sokaklari_ayikla(ornek_duyuru),
            "ham_metin": ornek_duyuru
        }]
    }
    with open("kesintiler.json", "w", encoding="utf-8") as f:
        json.dump(paket, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    verileri_guncelle()
