from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.units import cm
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import platform
import subprocess

def open_file(filepath):
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":
        subprocess.call(["open", filepath])
    else:
        subprocess.call(["xdg-open", filepath])


# ---------------------------- AYARLAR ----------------------------
try:
    pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", "DejaVuSans-Bold.ttf"))
    main_font = "DejaVu"
    bold_font = "DejaVu-Bold"
except:
    main_font = "Helvetica"
    bold_font = "Helvetica-Bold"

sorular = [
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

# ---------------------------- PDF FONKSİYONLARI ----------------------------
def create_cover_page(c, width, height, user_data):
    """1. Sayfa: Kapak"""
    c.setFont(bold_font, 24)
    c.drawCentredString(width/2, height-150, "DISC KİŞİLİK PROFİL RAPORU")
    
    c.setFont(bold_font, 18)
    c.drawCentredString(width/2, height-220, user_data["ad"])
    
    c.setFont(main_font, 14)
    c.drawCentredString(width/2, height-280, f"Doğum Yılı: {user_data['dogum_yili']} | Cinsiyet: {user_data['cinsiyet']}")
    
    c.setFont(main_font, 12)
    c.drawCentredString(width/2, height-320, datetime.datetime.now().strftime("Rapor Tarihi: %d.%m.%Y"))

def create_analysis_page(c, width, height, user_data):
    """2. Sayfa: Analiz"""
    c.setFont(bold_font, 18)
    c.drawString(50, height-50, "DISC ANALİZ SONUÇLARI")
    
    # Grafik
    draw_disc_graph(c, 50, height-150, user_data["skorlar"])
    
    # Tablo
    data = [
        ["D (Dominant)", user_data["skorlar"]["D"], "Liderlik, kararlılık"],
        ["I (İkna Edici)", user_data["skorlar"]["I"], "Sosyal iletişim, enerji"],
        ["S (Sabit)", user_data["skorlar"]["S"], "İstikrar, sabır"],
        ["C (Titiz)", user_data["skorlar"]["C"], "Detay odaklılık"]
    ]
    
    table = Table(data, colWidths=[150, 50, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), bold_font),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    
    table.wrapOn(c, width-100, height)
    table.drawOn(c, 50, height-350)

def create_recommendations_page(c, width, height, user_data):
    """3. Sayfa: Öneriler"""
    c.setFont(bold_font, 18)
    c.drawString(50, height-50, "KİŞİSEL GELİŞİM ÖNERİLERİ")
    
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = main_font
    
    # Güçlü Yönler
    ptext = f"""<b>Güçlü Yönleriniz ({user_data['sonuc_tipi']}):</b><br/>
    {get_strengths(user_data['sonuc_tipi'])}"""
    p = Paragraph(ptext, styleN)
    p.wrapOn(c, width-100, height)
    p.drawOn(c, 50, height-100)
    
    # Gelişim Alanları
    weak_type = min(user_data['skorlar'], key=user_data['skorlar'].get)
    ptext = f"""<b><br/><br/>Gelişim Alanlarınız ({weak_type}):</b><br/>
    {get_improvements(weak_type)}"""
    p = Paragraph(ptext, styleN)
    p.wrapOn(c, width-100, height)
    p.drawOn(c, 50, height-250)

def draw_disc_graph(c, x, y, scores):
    """DISC grafiği çizer"""
    drawing = Drawing(400, 200)
    
    # Eksen çizgileri
    drawing.add(Line(x, y+50, x+300, y+50, strokeColor=colors.black))
    drawing.add(Line(x, y+80, x+300, y+80, strokeColor=colors.black, strokeDashArray=[2,2]))
    drawing.add(Line(x, y+20, x+300, y+20, strokeColor=colors.black, strokeDashArray=[2,2]))
    
    # Noktalar
    disc_positions = [
        (x+50, y+50 + (scores['D']*3)),   # D
        (x+125, y+50 + (scores['I']*3)),  # I
        (x+200, y+50 + (scores['S']*3)),  # S
        (x+275, y+50 + (scores['C']*3))   # C
    ]
    
    for px, py in disc_positions:
        drawing.add(Line(px-5, py-5, px+5, py+5, strokeColor=colors.red, strokeWidth=2))
        drawing.add(Line(px-5, py+5, px+5, py-5, strokeColor=colors.red, strokeWidth=2))
    
    # Etiketler
    drawing.add(String(x+50, y+30, "D", fontName=main_font, fontSize=10))
    drawing.add(String(x+125, y+30, "I", fontName=main_font, fontSize=10))
    drawing.add(String(x+200, y+30, "S", fontName=main_font, fontSize=10))
    drawing.add(String(x+275, y+30, "C", fontName=main_font, fontSize=10))
    
    drawing.drawOn(c, 0, 0)

def get_strengths(disc_type):
    """Güçlü yönler"""
    strengths = {
        "D": "• Hızlı karar verme\n• Liderlik vasıfları\n• Sonuç odaklılık",
        "I": "• İkna kabiliyeti\n• Sosyal iletişim\n• Enerjik tavır",
        "S": "• Takım uyumu\n• Sabırlı yaklaşım\n• Dinleme becerisi",
        "C": "• Analitik düşünme\n• Detaylara hakimiyet\n• Planlama yeteneği"
    }
    return strengths.get(disc_type, "")

def get_improvements(weak_type):
    """Gelişim önerileri"""
    improvements = {
        "D": "• Dinleme becerilerini geliştir\n• Empati kurma pratikleri yap\n• Takım çalışmasına açık ol",
        "I": "• Detaylara dikkat et\n• Planlı çalışma alışkanlığı edin\n• Sabırlı olmayı öğren",
        "S": "• Risk alma becerisi geliştir\n• İnisiyatif kullan\n• Değişime adapte ol",
        "C": "• Esnek davranış modelleri geliştir\n• Mükemmeliyetçilik dengesi kur\n• Sosyal iletişim pratikleri yap"
    }
    return improvements.get(weak_type, "")

def generate_pdf(user_data):
    """PDF oluştur"""
    file_name = f"{user_data['ad']}_DISC_Raporu.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    
    create_cover_page(c, width, height, user_data)
    c.showPage()
    
    create_analysis_page(c, width, height, user_data)
    c.showPage()
    
    create_recommendations_page(c, width, height, user_data)
    c.save()
    
    return file_name

# ---------------------------- TEST FONKSİYONLARI ----------------------------
def analyze_answers(answers):
    """Cevapları analiz eder"""
    scores = {"D": 0, "I": 0, "S": 0, "C": 0}
    for answer in answers:
        if answer in ["Kararlı", "Hızlı karar alırım", "Liderlik"]: scores["D"] += 1
        elif answer in ["Eğlenceli", "Mizah yaparım", "Motivasyon"]: scores["I"] += 1
        elif answer in ["Sabırlı", "Sakin kalırım", "Destek"]: scores["S"] += 1
        elif answer in ["Dikkatli", "Analiz ederim", "Planlama"]: scores["C"] += 1
    
    result_type = max(scores, key=scores.get)
    return result_type, scores

# ---------------------------- GUI ----------------------------
class DiscTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DISC Kişilik Testi")
        self.root.geometry("600x500")
        
        self.current_question = 0
        self.answers = []
        self.user_data = {}
        
        self.create_welcome_screen()
    
    def create_welcome_screen(self):
        """Başlangıç ekranı"""
        self.clear_screen()
        
        tk.Label(self.root, text="DISC Kişilik Testi", font=(bold_font, 20)).pack(pady=20)
        
        tk.Label(self.root, text="Ad Soyad:", font=(main_font, 12)).pack()
        self.name_entry = tk.Entry(self.root, font=(main_font, 12))
        self.name_entry.pack(pady=5)
        
        tk.Label(self.root, text="Doğum Yılı:", font=(main_font, 12)).pack()
        self.year_entry = tk.Entry(self.root, font=(main_font, 12))
        self.year_entry.pack(pady=5)
        
        tk.Label(self.root, text="Cinsiyet:", font=(main_font, 12)).pack()
        self.gender_combo = ttk.Combobox(self.root, values=["Erkek", "Kadın", "Diğer"], font=(main_font, 12))
        self.gender_combo.pack(pady=5)
        
        tk.Button(self.root, text="Teste Başla", command=self.start_test, 
                 font=(bold_font, 12), bg="#4CAF50", fg="white").pack(pady=20)
    
    def start_test(self):
        """Testi başlat"""
        self.user_data = {
            "ad": self.name_entry.get(),
            "dogum_yili": self.year_entry.get(),
            "cinsiyet": self.gender_combo.get()
        }
        
        if not all(self.user_data.values()):
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return
        
        self.current_question = 0
        self.answers = []
        self.show_question()
    
    def show_question(self):
        """Soru göster"""
        self.clear_screen()
        
        if self.current_question < len(sorular):
            question = sorular[self.current_question]
            
            tk.Label(self.root, text=question["soru"], 
                    font=(bold_font, 12), wraplength=550).pack(pady=20)
            
            self.answer_var = tk.StringVar()
            for option in question["secenekler"]:
                tk.Radiobutton(self.root, text=option, variable=self.answer_var, 
                              value=option, font=(main_font, 11)).pack(anchor="w", padx=50, pady=5)
            
            next_text = "Sonraki" if self.current_question < len(sorular)-1 else "Bitir"
            tk.Button(self.root, text=next_text, command=self.next_question,
                     font=(bold_font, 12), bg="#2196F3", fg="white").pack(pady=20)
        else:
            self.show_results()
    
    def next_question(self):
        """Sonraki soru"""
        if not self.answer_var.get():
            messagebox.showwarning("Uyarı", "Lütfen bir seçenek işaretleyin!")
            return
        
        self.answers.append(self.answer_var.get())
        self.current_question += 1
        self.show_question()
    
    def show_results(self):
        """Sonuçları göster"""
        result_type, scores = analyze_answers(self.answers)
        self.user_data.update({
            "sonuc_tipi": result_type,
            "skorlar": scores
        })
        
        # PDF oluştur
        pdf_file = generate_pdf(self.user_data)
        
        # Sonuç ekranı
        self.clear_screen()
        
        tk.Label(self.root, text="TEST TAMAMLANDI", 
                font=(bold_font, 16), fg="#4CAF50").pack(pady=20)
        
        tk.Label(self.root, text=f"Sayın {self.user_data['ad']}, kişilik tipiniz:", 
                font=(main_font, 14)).pack()
        
        tk.Label(self.root, text=result_type, 
                font=(bold_font, 24), fg="#2196F3").pack(pady=10)
        
        tk.Button(self.root, text="PDF Raporunu Aç", 
                 command=lambda: os.startfile(pdf_file),
                 font=(bold_font, 12), bg="#F44336", fg="white").pack(pady=10)
        
        tk.Button(self.root, text="Yeni Test Başlat", 
                 command=self.create_welcome_screen,
                 font=(bold_font, 12), bg="#FF9800", fg="white").pack(pady=10)
    
    def clear_screen(self):
        """Ekranı temizle"""
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------------------------- UYGULAMAYI BAŞLAT ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DiscTestApp(root)
    root.mainloop()