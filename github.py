import tkinter as tk
from tkinter import messagebox
from weasyprint import HTML
import tempfile
import os

# ------------------ SORULAR ------------------ #
SORULAR = [
    {"soru": "1. Aşağıdakilerden hangisi sizi en iyi tanımlar?", "secenekler": ["Kararlı", "Eğlenceli", "Sabırlı", "Dikkatli"]},
    {"soru": "2. Baskı altında nasıl davranırsınız?", "secenekler": ["Hızlı karar alırım", "Mizah yaparım", "Sakin kalırım", "Analiz ederim"]},
    {"soru": "3. Bir ekipte hangi rol size daha uygundur?", "secenekler": ["Liderlik", "Motivasyon", "Destek", "Planlama"]},
    {"soru": "4. İş yerinde başarıyı ne belirler?", "secenekler": ["Sonuçlar", "İlişkiler", "İstikrar", "Kurallar"]},
    {"soru": "5. Yeni bir işe başladığınızda ne yaparsınız?", "secenekler": ["Hemen sorumluluk alırım", "Herkesle tanışırım", "Ortamı gözlemlerim", "Kuralları öğrenirim"]},
    {"soru": "6. Zor kararlar alırken neye odaklanırsınız?", "secenekler": ["Sonuç", "İnsanlar", "Uyum", "Veri"]},
    {"soru": "7. İletişim tarzınız nasıldır?", "secenekler": ["Direkt", "Canlı", "Sakin", "Düşünceli"]},
    {"soru": "8. Takım arkadaşınızın sizden en çok beklediği nedir?", "secenekler": ["Hedefe ulaşmak", "Moral vermek", "Sadakat", "Titizlik"]},
    {"soru": "9. Sizi ne motive eder?", "secenekler": ["Başarı", "Sosyal çevre", "Güvence", "Kalite"]},
    {"soru": "10. Kriz anlarında nasıl davranırsınız?", "secenekler": ["Yönlendiririm", "Morali yüksek tutarım", "Destek olurum", "Strateji kurarım"]},
    {"soru": "11. Hedeflerinize ulaşmak için ne yaparsınız?", "secenekler": ["Risk alırım", "İkna ederim", "Destek isterim", "Plan yaparım"]},
    {"soru": "12. Yeni fikirleri nasıl karşılarsınız?", "secenekler": ["Uygulamak isterim", "Paylaşırım", "Düşünürüm", "Sorgularım"]},
    {"soru": "13. Ne tür ortamlarda verimli çalışırsınız?", "secenekler": ["Hızlı ve dinamik", "Eğlenceli", "Sakin", "Düzenli"]},
    {"soru": "14. İş yerinde sizi ne rahatsız eder?", "secenekler": ["Yavaşlık", "Soğuk ortam", "Gerginlik", "Belirsizlik"]},
    {"soru": "15. Bir projeye nasıl yaklaşırsınız?", "secenekler": ["Hemen başlarım", "Destek toplarım", "Uyum sağlarım", "Araştırırım"]},
    {"soru": "16. Eleştiri aldığınızda ne yaparsınız?", "secenekler": ["Kabul ederim", "Savunurum", "Üzülürüm", "Değerlendiririm"]},
    {"soru": "17. İdeal yöneticiniz nasıl biri olmalı?", "secenekler": ["Kararlı", "İlham verici", "Destekleyici", "Organize"]},
    {"soru": "18. Gününüzü nasıl planlarsınız?", "secenekler": ["Hedef odaklı", "Doğal akışta", "İnsanlarla birlikte", "Listelerle"]},
    {"soru": "19. Başarıyı neye borçlusunuz?", "secenekler": ["İrade", "İletişim", "Sadakat", "Disiplin"]},
    {"soru": "20. Sizi en çok ne tatmin eder?", "secenekler": ["Zafer", "Takdir", "İlişkiler", "Doğruluk"]},
]

SECENEK_TIPLERI = ["D", "I", "S", "C"]

puanlar = {"D": 0, "I": 0, "S": 0, "C": 0}

# ------------------ GUI ------------------ #
class KisilikTesti:
    def __init__(self, root):
        self.root = root
        self.root.title("DiSC Kişilik Testi")
        self.index = 0
        self.cevaplar = []

        self.soru_label = tk.Label(root, text="", font=("Arial", 14))
        self.soru_label.pack(pady=10)

        self.secenek_var = tk.StringVar()
        self.secenekler = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.secenek_var, value="", font=("Arial", 12))
            rb.pack(anchor="w", padx=20)
            self.secenekler.append(rb)

        self.ileri_button = tk.Button(root, text="İleri", command=self.sonraki_soru)
        self.ileri_button.pack(pady=20)

        self.guncelle()

    def guncelle(self):
        soru = SORULAR[self.index]
        self.soru_label.config(text=soru["soru"])
        self.secenek_var.set(None)
        for i, secenek in enumerate(soru["secenekler"]):
            self.secenekler[i].config(text=secenek, value=secenek)

    def sonraki_soru(self):
        secim = self.secenek_var.get()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen bir seçenek seçin.")
            return
        self.cevaplar.append(secim)
        self.index += 1
        if self.index < len(SORULAR):
            self.guncelle()
        else:
            self.testi_bitir()

    def testi_bitir(self):
        for i, cevap in enumerate(self.cevaplar):
            secenek_index = SORULAR[i]["secenekler"].index(cevap)
            secenek_tipi = SECENEK_TIPLERI[secenek_index]
            puanlar[secenek_tipi] += 1

        self.root.destroy()
        raporu_olustur(puanlar)

# ------------------ PDF RAPOR ------------------ #
def raporu_olustur(puanlar):
    html_icerik = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; padding: 40px; }}
            h1 {{ color: #2c3e50; }}
            .tip {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>DiSC Kişilik Testi Sonucu</h1>
        <div class="tip"><strong>D (Dominant):</strong> {puanlar['D']}</div>
        <div class="tip"><strong>I (Etkileyici):</strong> {puanlar['I']}</div>
        <div class="tip"><strong>S (Sadık):</strong> {puanlar['S']}</div>
        <div class="tip"><strong>C (Titiz):</strong> {puanlar['C']}</div>

        <h2>Yorum</h2>
        <p>
    """

    en_yuksek = max(puanlar, key=puanlar.get)
    yorumlar = {
        "D": "Lider ruhlusunuz, sonuç odaklısınız ve zorluklardan korkmazsınız.",
        "I": "İletişimi güçlü, sosyal ve motive edici bir kişiliğiniz var.",
        "S": "İstikrarlı, güvenilir ve uyumlu bir yapıya sahipsiniz.",
        "C": "Detaycı, planlı ve analiz yeteneği yüksek birisiniz."
    }

    html_icerik += yorumlar[en_yuksek]
    html_icerik += "</p></body></html>"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        HTML(string=html_icerik).write_pdf(tmp_pdf.name)
        os.startfile(tmp_pdf.name)  # Otomatik aç

# ------------------ BAŞLAT ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    app = KisilikTesti(root)
    root.mainloop()
