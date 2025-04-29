import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from jinja2 import Template
from weasyprint import HTML
import matplotlib.pyplot as plt
import io
import numpy as np
from datetime import datetime
import sys
import os

# ------------------- DISC İÇERİK VERİLERİ ------------------- #
DISC_ICERIK = {
   "D": {
        "baslik": "D (Dominance) - Dominant",
        "aciklama": """tipi detaylara, analize ve kurallara bağlı kalırken, D tipi büyük resmi görür, hızlı stratejiler geliştirir ve detayları delegasyonla yönetmeye eğilimlidir. </p>
<p><span class="siyah-kalin"> Özetle: </span> <p>
D tipi, DISC modelinin "hareket" ve "liderlik" temsilcisidir. Güçlü irade, özgüven ve sonuç alma odaklılıklarıyla, değişime öncülük eden, zorlukları fırsata çeviren bir profil çizerler. Ancak empati ve işbirliği konusunda diğer tiplerden öğrenebilecekleri çok şey vardır.
""",

        "davranislar": """
•<span class="siyah-kalin"> Sabırsızlık:  </span> Süreçlerin yavaş ilerlemesi, bürokratik engeller ya da ayrıntılarda oyalanmak onları çabucak huzursuz edebilir. Zamanı etkili kullanma konusunda hassas olduklarından, ertelemelere ya da belirsizliklere tahammülleri düşüktür.
•<span class="siyah-kalin"> Detaylara Karşı İlgisizlik:  </span> Büyük resmi görme eğiliminde oldukları için mikro yönetimden kaçınırlar. Detaylarla uğraşmak yerine genel stratejiyi belirlemeye ve uygulamaya odaklanırlar. Bu özellikleri, detay gerektiren işlerde hata yapma riskini artırabilir.
•<span class="siyah-kalin"> Bağımsızlık: </span> Bağımsız karar alma ve kendi yöntemleriyle çalışma arzusu, D tipi bireylerin temel karakteristiklerinden biridir. Emir almaktansa yön vermeyi tercih ederler. Otonomi, onların verimliliğini ve iş doyumunu doğrudan etkiler.
""",

        "guclu": """
<span class="kirmizi-kalin">5. Yüksek Enerji ve Azim:</span>
Fiziksel ve zihinsel dayanıklılıkları sayesinde uzun süre yoğun tempoda çalışabilirler. Hedeflerine ulaşmak için gösterdikleri kararlılık ve ısrar, onları yüksek performans gerektiren görevlerde başarılı kılar.

<span class="kirmizi-kalin">6. Stratejik Düşünme Yetisi:</span>
Geniş perspektiften bakabilme becerileri gelişmiştir. Uzun vadeli planlamalar yapabilir ve bu doğrultuda kısa vadeli adımları etkili bir şekilde yönetebilirler. Strateji geliştirme ve uygulamada doğuştan bir yatkınlığa sahiptirler.""",

        "zayif": """
<span class="kirmizi-kalin">7. Yüksek Rekabet Düzeyi:</span>
Rekabetçi doğaları, iş birliği gerektiren ortamlarda sürtüşmelere neden olabilir. Kendi başarılarına odaklanırken ekip başarısını arka plana atma riski taşırlar.
<span class="kirmizi-kalin">8. Katı Hedef Takibi:</span>
Belirledikleri hedefe ulaşma arzusu o kadar baskın olabilir ki, esneklik ve adaptasyon gerektiren durumlara ayak uydurmakta zorlanabilirler. Bu da çevresel faktörlerin değişkenliğine karşı direnç yaratabilir.
<span class="kirmizi-kalin">9. Aşırı Baskı Oluşturma:</span>
Kendilerinden olduğu kadar çevrelerinden de yüksek performans beklerler. Bu durum, ekip arkadaşlarında stres, motivasyon kaybı veya tükenmişlik yaratabilir.
<span class="kirmizi-kalin">10. İş-Yaşam Dengesi Sorunları:</span>
Yoğun iş temposu ve hedef odaklılıkları, özel yaşamlarını geri plana atmalarına neden olabilir. Bu dengesizlik, uzun vadede duygusal yorgunluk veya sosyal ilişkilerde kopukluk yaratabilir.
""",

        "gelisim": """
<span class="kirmizi-kalin">6. Takım Çalışmasına Açık Olmak </span> 
<span class="siyah-kalin">*Neden Önemli?</span> 
Bağımsız hareket etme arzusu, ekip ruhunu zedeleyebilir. Etkili liderlik, takım uyumunu teşvik etmeyi gerektirir.
<span class="siyah-kalin">* Nasıl Geliştirilebilir?</span> 
•	Karar alma süreçlerine başkalarını aktif olarak dahil etmek.
•	“Biz” dilini kullanma alışkanlığı geliştirmek.
•	Görev dağılımında güven duymayı öğrenmek.

<span class="kirmizi-kalin">7. Kontrol İhtiyacını Azaltmak </span> 
<span class="siyah-kalin">*Neden Önemli?</span>
Her şeyi kontrol etme arzusu, çevredeki bireyleri baskı altında hissettirebilir. Delege etmek, hem lideri hem takımı güçlendirir.
<span class="siyah-kalin">* Nasıl Geliştirilebilir?</span> 
•	Küçük görevleri başkalarına devrederek başlamak.
•	Güven temelli bir iş ilişkisi inşa etmek.
•	Kontrolün bazen ilerlemeyi yavaşlattığını kabul etmek.
<span class="kirmizi-kalin">10. İş-Yaşam Dengesi Kurmak </span> 
<span class="siyah-kalin">*Neden Önemli?</span> 
Aşırı odaklanma ve çalışma temposu, duygusal ve fiziksel tükenmeye neden olabilir. Uzun vadeli performans için denge esastır.
<span class="siyah-kalin">* Nasıl Geliştirilebilir?</span> 
•	Çalışma saatlerini sınırlandırmak ve boş zaman aktivitelerine zaman ayırmak.
•	Haftalık “kendin için bir şey yap” hedefleri koymak.
•	Tatil ve mola planlarını iş hedefleri kadar ciddiye almak.

<span class="kirmizi-kalin"> Ek Öneriler </span>
<span class="siyah-kalin">Yansıtıcı Günlük Tutmak:</span> Duygusal ve davranışsal farkındalığı artırmak için günlük yazmak.
<span class="siyah-kalin">Mentorluk Almak: </span> Özellikle empati, iletişim ve liderlik dengesi gibi konularda deneyimli kişilerden rehberlik almak.
<span class="siyah-kalin">Gelişim Günlüğü Oluşturmak:</span> Öğrenilen her davranışsal kazanımı not ederek ilerlemeyi görmek ve kutlamak.
<span class="siyah-kalin"> Psikolojik Dayanıklılık Geliştirmek:</span> Mindfulness, stres yönetimi ve duygusal dayanıklılık egzersizleri ile iç dengeyi artırmak.""",

        "iletisim": """

<span class="kirmizi-kalin"> Ek Sosyal Davranışlar:</span>
<span class="siyah-kalin"> Rekabetçi Yapı:  </span> Kendini ve başkalarını motive etmek için rekabet ortamı yaratabilir. “Hadi bunu ilk bitiren olalım” gibi ifadeler kullanır.
<span class="siyah-kalin"> Hızlı Karar Alma: </span> Sosyal ilişkilerde de karar verici bir rolde bulunur. Grup içinde “Ne yapılacağına” hızlıca karar verebilir.
<span class="siyah-kalin"> Geribildirim Vermekte Aktiftir: </span> Gözlemlediği eksiklikleri doğrudan dile getirir, gelişimi bu şekilde hızlandırmayı amaçlar.

<span class="siyah-kalin"> Örnek Senaryo:</span> 
Takımda işler aksadığında, D tipi birey duruma müdahale ederek “Bu şekilde zaman kaybediyoruz. Şu adımları hemen uygulayalım” diyerek sürece yön verir. Ardından, ekip üyelerinin rollerini net şekilde belirleyip hızlı aksiyon alınmasını sağlar.
""",

        "liderlik": """
<span class="kirmizi-kalin"> 5. Rekabetçilik ve Yüksek Motivasyon </span>
<span class="siyah-kalin"> Kazanmaya Odaklılık:</span> 
D tipi liderler için başarı bir ihtiyaçtır. Bu yüzden doğal olarak rekabetçidirler.
<span class="siyah-kalin"> Motivasyon Bulaşıcılığı:</span> 
Yüksek enerjileri ve kazanma arzuları ekip içinde motivasyonu artırabilir.
<span class="siyah-kalin"> Öneri: </span> 
Rekabeti işbirliğiyle dengelemek, ekip içindeki uyumu artırır.

<span class="kirmizi-kalin"> 6. Doğrudan Geri Bildirim</span>
<span class="siyah-kalin"> Açık Sözlülük:</span> 
Geri bildirimi doğrudan, hatta zaman zaman sert şekilde verirler. Bu, bazıları için netlik sağlarken, bazıları için yıpratıcı olabilir.
<span class="siyah-kalin"> Hızlı Gelişim: </span> 
Net geri bildirimler, gelişim sürecini hızlandırabilir. Ancak empatik bir tonla sunulması daha etkili olabilir.
<span class="siyah-kalin"> Öneri: </span> 
Eleştirileri yapıcı ve dengeli şekilde iletmek, ekip içi güveni güçlendirir.

<span class="kirmizi-kalin"> 7. İnisiyatif Almayı Teşvik Etme </span>
<span class="siyah-kalin"> Özgür Alan:</span> 
D tipi liderler kendi başlarına düşünen ve harekete geçen bireylerle çalışmayı severler. Ekibin sorumluluk almasını desteklerler.
<span class="siyah-kalin"> Kendi Kendine Yönelim:</span> 
Takım üyelerinin bireysel inisiyatif almalarını teşvik ederler. Bu, özgüveni artırır ve liderin üzerindeki yükü azaltır.
<span class="siyah-kalin"> Öneri: </span> 
Destek mekanizmaları oluşturarak inisiyatif almanın risklerini azaltmak ekip bağlılığını artırabilir.""",

        "motivasyon": """
<span class="kirmizi-kalin">3. Hız ve Sonuç Odaklılık</span>
<span class="siyah-kalin">Hızlı İlerleme:</span>
Yavaşlayan, ayrıntılara boğulan süreçler D tipi bireyleri demotive edebilir. Bu nedenle kararların hızlı alındığı ve aksiyonun çabuk alındığı ortamlar onlar için daha uygundur.
<span class="siyah-kalin">Sonuçların Görülmesi:</span>
Uzun süren projelerden ziyade, somut çıktılar üreten, gözle görülür sonuçlar yaratan işler D tipi bireylerin motive olmasını sağlar.
<span class="siyah-kalin">Engelleri Aşmak:</span>
Karşılarına çıkan zorlukları aşmak ve rekabetin üstesinden gelmek, D tipi bireylerde güçlü bir tatmin ve motivasyon yaratır.

<span class="kirmizi-kalin">4. Yetkinlik ve Kendi Alanında Uzmanlık</span>
<span class="siyah-kalin">Güçlü Yönlerin Tanınması:</span>
Kendi güçlü yanlarının, liderlik becerilerinin ve karar alma yetilerinin takdir edilmesi, D tipi bireyler için önemlidir.
<span class="siyah-kalin">Yetkin Olmak ve Gelişim Fırsatları:</span>
Kendilerini sürekli geliştirebilecekleri, liderliklerini derinleştirecek eğitimler, seminerler ve mentorluk süreçleri D tipi bireylerin iç motivasyonunu artırır.
<span class="siyah-kalin">Otonomi:</span>
D tipi bireyler bağımsız çalışmaya ve kendi yöntemlerini uygulamaya ihtiyaç duyarlar. Fazla denetlenmek ve mikro yönetilmek, motivasyonlarını azaltabilir.""",

        "meslekler": """
<span class="kirmizi-kalin">Yaratıcı ve Teknik Alanlar:</span> 
<span class="siyah-kalin">Reklam Strateji Uzmanı:</span> Yaratıcı ama aynı zamanda sonuç odaklı düşünebilen D tipi bireyler, stratejik kampanya yönetimi konusunda öne çıkabilirler.
<span class="siyah-kalin">Girişimci / Startup Kurucusu:</span> Risk alma cesaretleri, inisiyatif kullanmaları ve liderlik potansiyelleri sayesinde kendi işlerini kurmak için güçlü bir adaydırlar.
<span class="siyah-kalin">Endüstri Mühendisi:</span> Süreçleri optimize etme, karar verme ve sistemli yönetim yetenekleri bu teknik alanda avantaj sağlar.

<span class="kirmizi-kalin">Tekstil Sektöründe Üretim Alanındaki Meslekler:</span>
<span class="siyah-kalin">Üretim Müdürü:</span> Üretim süreçlerini yönetmek, hedeflere ulaşmak ve aksaklıkları çözmek konusunda doğuştan liderlik özellikleri gösterirler.
<span class="siyah-kalin">Planlama ve Lojistik Müdürü:</span> Sürecin tamamına hâkim olmak ve stratejik planlama yapmak D tipi bireyler için motivasyon vericidir.
<span class="siyah-kalin">Tedarik Zinciri Yöneticisi:</span> Büyük resme odaklanmak, karmaşık sistemleri kontrol etmek ve verimliliği artırmak onların güçlü yanıdır.
<span class="siyah-kalin">Satış ve Pazarlama Direktörü (Tekstil):</span> Sonuç ve performans odaklılıkları sayesinde, pazarda rekabet üstünlüğü sağlamaya yönelik stratejiler geliştirebilirler.""",

        "takim": """

<span class="kirmizi-kalin">D Tipi Bireylerin Takım İçinde Dikkat Etmesi Gerekenler:</span>
<span class="siyah-kalin">Empati ve dinleme becerisi:</span>
Baskın yapılarına rağmen, takım arkadaşlarını dikkatle dinlemek ve onların duygularını anlamaya çalışmak takım uyumunu güçlendirir.
<span class="siyah-kalin">İşbirliğine açıklık:</span>
Sürekli yöneten pozisyonda olmak yerine, zaman zaman takım arkadaşlarının fikirlerine de alan tanımak önemlidir. Katılımcı bir ortam yaratmak, liderliğin gücünü artırır.
<span class="siyah-kalin">Sabırlı olmak:</span>
Her bireyin hızının ve yaklaşımının farklı olduğunu kabul ederek daha sabırlı olmak, takım içinde güven oluşturur.
<span class="siyah-kalin">Geribildirim alma:</span>
Eleştirilerden kaçmak yerine, gelişim fırsatı olarak görmek; kişisel büyümeye ve takım ilişkilerinin güçlenmesine katkı sağlar.
<span class="siyah-kalin">Baskı kurmaktan kaçınmak:</span>
Yüksek beklenti ve kontrol eğilimleri, diğer takım üyeleri üzerinde stres yaratabilir. Bu nedenle dengeleyici ve destekleyici bir yaklaşım benimsemeleri faydalı olur.""",
    },
    "I": {
        "baslik": "I (Influence) - Etkileyici",
        "aciklama": """<p><span class="siyah-kalin"> S (Steadiness)  </span> tipi bireyler güvenlik, istikrar ve sadakat ararken, I tipi bireyler dinamizm, değişim ve heyecan peşindedir. S tipi içe dönük bir uyum sergilerken, I tipi dışa dönük bir canlılık sunar.</p>
<p><span class="siyah-kalin"> C (Conscientiousness) </span> tipi bireyler analitik düşünür, kurallara bağlı kalır ve detayları önemserken, I tipi bireyler spontane hareket eder, insan ilişkilerine öncelik verir ve bazen detayları ikinci plana atabilir.</p>
<p> <span class="siyah-kalin"> Özetle: </span></p> 
I tipi, DISC modelinin "iletişim" ve "ilham" temsilcisidir.
Pozitif enerjileri, ikna güçleri ve sosyal becerileri ile grupları bir araya getiren, motivasyonu canlı tutan ve çevrelerine hareket katan bireylerdir. Ancak, detaylara dikkat, uzun vadeli planlama ve eleştirilere açık olma konularında gelişim göstermeleri, potansiyellerini daha da ileri taşımalarına yardımcı olabilir.""",

        "davranislar": """

• <span class="siyah-kalin"> Ayrıntılardan Uzaklaşma:</span> Büyük resme ve genel atmosfere odaklandıkları için detaylarla ilgilenmekte zorlanabilirler. Uzun ve detaylı işlemlerden çabuk sıkılabilir, önemli küçük ayrıntıları atlayabilirler. Bu nedenle, detay odaklı görevlerde destek almaları faydalı olabilir.
• <span class="siyah-kalin"> Duygusal Karar Verme Eğilimi:</span> Karar süreçlerinde çoğu zaman sezgilerini ve duygularını rehber edinirler. Mantıksal analiz yerine "hissettikleri doğru"ya yönelme eğilimindedirler. Bu, onları hızlı ve cesur kılarken, bazen riskli veya eksik değerlendirmelere yol açabilir.""",

        "guclu": """
<span class="kirmizi-kalin">8. Kriz Anlarında Moral Sağlama:</span>
Zorlu zamanlarda bile moralin ve motivasyonun korunmasına yardımcı olurlar. Panik yerine umut aşılayarak, grubun daha dirençli ve çözüm odaklı kalmasını sağlarlar.

<span class="kirmizi-kalin">9. İyimser Bakış Açısı:</span>
Engelleri aşılabilir, hataları öğrenme fırsatı ve geleceği umut dolu bir alan olarak görürler. Bu olumlu bakış açısı, kişisel başarılarının yanı sıra, takım içindeki verimliliği de artırır.

<span class="kirmizi-kalin">10. Sosyal Ağ Oluşturma Becerisi:</span>
I tipi bireyler doğal network kuruculardır. Güçlü sosyal ilişkiler geliştirerek hem iş hem özel yaşamlarında geniş ve destekleyici bir çevre oluştururlar. Bu sosyal ağlar, fırsatların fark edilmesi ve değerlendirilmesi açısından büyük avantaj sağlar.""",

        "zayif": """
<span class="kirmizi-kalin">9. Aşırı İltifat ve Onay İhtiyacı:</span>
Çevreden gelen onay ve takdir, motivasyonları için önemli bir kaynaktır. Ancak bu ihtiyaç fazlalaştığında, bağımsız hareket etme yetenekleri zayıflayabilir ve dışarıdan gelen tepkilere aşırı duyarlı hale gelebilirler.

<span class="kirmizi-kalin">10. Zaman Yönetimi Problemleri:</span>
Heyecan verici görevler ve sosyal etkileşimler arasında önceliklendirme yapmada zorlanabilirler. Bu da işleri zamanında tamamlama konusunda gecikmelere ve planlama hatalarına neden olabilir.""",

        "gelisim": """
<span class="kirmizi-kalin">6. Eleştiriye Açık Olmak</span>
<span class="siyah-kalin">Neden Önemli?</span>
Yapıcı eleştiriler, gelişim için önemli bir geri bildirim kaynağıdır. Eleştiriden kaçmak, kişisel ve profesyonel gelişimi engelleyebilir.
<span class="siyah-kalin">Nasıl Geliştirilebilir?</span>
Eleştirileri kişisel algılamadan önce mesajın içeriğine odaklanmak, geri bildirimi gelişim fırsatı olarak görmek ve düzenli geribildirim almak için açık kapı politikası benimsemek yararlı olur.

<span class="kirmizi-kalin">7. Karar Verme Süreçlerinde Netlik Sağlamak</span>
<span class="siyah-kalin">Neden Önemli?</span>
Belirsizlik karar süreçlerini yavaşlatabilir ve fırsatların kaçırılmasına neden olabilir. Net kararlar, güven ve ilerleme sağlar.
<span class="siyah-kalin">Nasıl Geliştirilebilir?</span>
Seçenekleri hızlıca değerlendirmek için artı-eksi listeleri hazırlamak ve her kararı belirli bir zaman limiti içinde sonuçlandırmak yardımcı olabilir.""",

        "iletisim": """
<span class="kirmizi-kalin">Geri Bildirimde Yumuşak ve Teşvik Edicidir</span>
<span class="siyah-kalin">Özellik:</span> Başkalarının duygularını önemseyerek, nazik ve motive edici bir şekilde geri bildirim verir.
<span class="siyah-kalin">Sosyal Etki:</span> İnsanların savunmaya geçmeden gelişim alanlarını görmesini sağlar. İlişkilerde güven oluşturur.
<span class="siyah-kalin">Öneri:</span> Gerektiğinde doğrudan ve net geri bildirim verme becerisi de geliştirilmelidir. “Yapıcı samimiyet” dengesi önemlidir.""",

        "liderlik": """
<span style="color: black;"> <b>Olumlu Pekiştirme: </b></span>
Başarıları ve olumlu davranışları anında takdir ederek, motivasyonu yükseltir.
<span style="color: black;"> <b>Özgüven Aşılamak: </b></span>
İnsanlara güçlü yönlerini hatırlatarak öz güvenlerini artırır.
<span style="color: black;"> <b>Öneri: </b></span>
Sadece olumlu değil, gelişim alanlarına yönelik yapıcı geribildirimler vermeyi ihmal etmemek gerekir.
<span style="color: red;"><b>6. Vizyoner Bakış Açısı</b></span>
<span style="color: black;"> <b>Gelecek Odaklılık: </b></span>
I tipi liderler büyük resme bakar, insanlara umut dolu bir gelecek tasviri sunar.
<span style="color: black;"> <b>Hayal Gücüyle Yön Verme: </b></span>
Sadece bugünü değil, yarını da düşünerek stratejiler geliştirir.
<span style="color: black;"> <b>Ağ Kurma Yeteneği: </b></span>
Geniş bir sosyal çevre oluşturur, farklı insanlarla güçlü bağlar kurar.
<span style="color: black;"> <b>Öneri: </b></span>
İkna süreçlerinde karşı tarafın ihtiyaçlarını da gözetmek uzun vadeli başarı getirir.
<span style="color: red;"><b>10. Enerji ve Moral Yönetimi</b></span>
<span style="color: black;"> <b>Moral Kaynağı: </b></span>
Kriz anlarında bile pozitif kalmayı başarır ve çevresine de bu enerjiyi yayar.
<span style="color: black;"> <b>Takımı Canlı Tutma: </b></span>
Zor zamanlarda bile ekibin motivasyonunu yüksek tutarak ilerlemeye destek olur.
<span style="color: black;"> <b>Öneri: </b></span>
Sürekli yüksek enerji beklentisi bazen gerçeklikten kopmaya neden olabilir; bu yüzden duygusal dalgalanmaları da yönetmek önemlidir.""",

        "motivasyon": """
<span class="kirmizi-kalin">5. Heyecan ve Yenilik Arayışı</span> 
<span class="siyah-kalin">Monotonluktan Kaçınma:</span> 
Tekdüze işler I tipi bireyler için sıkıcı olabilir. Sürekli değişen, yenilik içeren görevler onların ilgisini çeker.
<span class="siyah-kalin">Yeni Projelere Dahil Olmak:</span> 
Yeni girişimlerde yer almak, farklı ekiplerle çalışmak ve proje üretmek I tipi bireyleri harekete geçirir.
<span class="siyah-kalin">Enerjik Aktiviteler:</span> 
Hareketli, dinamik ve sosyal aktivite içeren görevler I tipi bireyleri motive eder ve performanslarını artırır.""",

        "meslekler": """
<span class="siyah-kalin">Yaratıcı Proje Yöneticisi:</span>
Fikir üretimi, projelerin tasarlanması ve yaratıcı ekiplerin yönetilmesi gibi konularda enerjileri ve sosyal becerileriyle öne çıkarlar.

<span class="kirmizi-kalin">Tekstil Sektöründe İletişim ve Satış Odaklı Meslekler:</span>
<span class="siyah-kalin">Moda Pazarlama Uzmanı:</span>
İnsanlarla güçlü bağ kurarak, moda sektöründe marka bilinirliğini ve müşteri bağlılığını artırma konusunda etkili olabilirler.
<span class="siyah-kalin">Satış Temsilcisi (Showroom / Fuar):</span>
Etkili iletişim yetenekleri ile doğrudan müşteri temasının yoğun olduğu ortamlarda başarı sağlarlar.
<span class="siyah-kalin">Müşteri Deneyimi Yöneticisi:</span>
Müşterilere unutulmaz deneyimler yaşatmak, sadakati artırmak ve pozitif imaj yaratmak I tipi bireylerin güçlü olduğu alanlardır.
<span class="siyah-kalin">Kurumsal İletişim Uzmanı (Tekstil Firmaları için):</span>
Marka hikâyesini etkili şekilde anlatmak, medya ilişkilerini yönetmek ve şirket imajını güçlendirmek konusunda önemli katkılar sunabilirler.""",

        "takim": """
Büyük resmi görmekte çok başarılı olsalar da, süreçteki detayları ihmal etmemeye dikkat etmeleri gerekir.
<span class="siyah-kalin">Sürekli sosyal odaklı olmaktan kaçınmak:</span>
Takım içindeki ilişkileri güçlendirmek değerli olsa da, iş süreçleri ve sonuçlara ulaşma konusuna da yeterli önem vermeleri gerekir.
""",
    },
    
    "S": {
    "baslik": "S (Steadiness) - Sabit",
    "aciklama": """<p>S tipi kişiler, genel olarak çatışmadan kaçınır, uzlaşmacı çözümler sunar ve bulunduğu çevrede denge unsuru olur. Onların varlığı, hızlı kararların ve ani değişimlerin baskın olduğu ortamlarda sakinleştirici bir rol oynar. Sadakatleri, güvenilirlikleri ve yüksek empati yetenekleri sayesinde hem bireysel ilişkilerde hem de takım çalışmalarında değerli bir denge unsuru oluştururlar.</p>""",

        "davranislar": """	
•	<span class="siyah-kalin"> Güven arayışı: </span>  İlişkilerde ve iş ortamlarında "istikrar"ı temel alır. Güvenilir olmayan kişi veya durumlardan içgüdüsel olarak uzaklaşır.""",

        "guclu": """

<span class="kirmizi-kalin">7. Sorumluluk Sahibi;</span>
Sadece kendisine değil, takım arkadaşlarına karşı da sorumluluk hisseder.
Sık sık başkalarının yükünü hafifletmeye gönüllü olur.""",
        "zayif": """
Duygusal geri bildirimler karşısında kendini suçlu ya da yetersiz hissedebilir.
<span class="kirmizi-kalin">9. Rutinlere Aşırı Bağlılık</span>
Her şeyin alışılmış düzende olmasını ister.
Değişim, yaratıcılık ve risk gerektiren görevlerde performansı düşebilir.
""",

        "gelisim": """
<span class="siyah-kalin">*Nasıl Geliştirilebilir?</span>
"Hayır" demeyi öğrenmek ve bunu nazikçe ifade etmek (örneğin, "Şu an bu konuda yardımcı olamayacağım, ancak...").
Zaman ve enerjiyi önceliklendirmek için günlük plan yapmak.
Kendi ihtiyaçlarını düzenli olarak değerlendirmek (örneğin, haftalık öz-değerlendirme).

<span class="kirmizi-kalin">4. Çatışma Yönetimi</span>
<span class="siyah-kalin">*Neden Önemli?</span>
Çatışmalardan kaçınmak, sorunların birikmesine ve ilişkilerde gerilime neden olabilir.

<span class="siyah-kalin">*Nasıl Geliştirilebilir?</span>
"Ben" dili kullanarak duyguları açıklamak (örneğin, "Ben bu durumda kendimi... hissediyorum").
Aktif dinleme yaparak karşı tarafın perspektifini anlamaya çalışmak.
Arabuluculuk eğitimleri almak veya çatışma çözüm tekniklerini öğrenmek.

<span class="kirmizi-kalin">Ek Öneriler</span>
<span class="siyah-kalin">Geribildirim Alma: </span>Düzenli olarak güvenilir kişilerden geribildirim istemek, gelişim sürecini hızlandırır.
<span class="siyah-kalin">Kademeli Adımlar: </span>Değişim için kendine zaman tanımak ve küçük başarıları kutlamak motivasyonu artırır.
<span class="siyah-kalin">Destek Sistemleri: </span>Koçluk, terapist veya meslektaş gruplarından destek almak, bu alanlarda ilerlemeyi kolaylaştırır.
""",

        "iletisim": """
<span class="kirmizi-kalin">Dolaylı İfadeler Kullanmayı Sever</span>
<span class="siyah-kalin">Özellik: </span>Direkt eleştiri yerine yapıcı geri bildirimler verir. Örneğin, "Bu fikir iyi, ancak şu açıdan geliştirilebilir" gibi yumuşak bir dil kullanır.
<span class="siyah-kalin">Sosyal Etki: </span>İlişkilerde incitici olmadan gerçekleri aktarır, bu da saygı ve anlayışı korur.
<span class="siyah-kalin">Öneri: </span>"Sandviç metodu" kullanmak (olumlu + gelişim alanı + olumlu) iletişimi daha kabul edilebilir kılar.


Bu özellikler, S tipi bireylerin iletişimde dengeli ve destekleyici bir rol üstlenmesini sağlar. """,

        "liderlik": """
<span class="siyah-kalin"> Süreç Odaklılık: </span> İşlerin nasıl yapıldığına dair net süreçler ve prosedürler oluştururlar. Bu süreçlere titizlikle uyulmasını sağlayarak, hataları en aza indirirler ve verimliliği artırırlar. Herkesin rolünü ve sorumluluklarını net bir şekilde bilmesini sağlarlar.
<span class="siyah-kalin"> Tutarlılık: </span> Kararlarında ve uygulamalarında tutarlı davranırlar. Aynı durumda aynı tepkiyi vererek, adil ve güvenilir bir lider imajı çizerler. Bu, takım üyelerinin onlara olan saygısını ve güvenini artırır.

<span class="kirmizi-kalin">8. Uyum Sağlayıcı </span>
<span class="siyah-kalin"> Esneklik: </span> Değişen koşullara ve farklılıklara kolayca uyum sağlarlar. Yeni durumlara hızla adapte olabilirler ve farklı kişiliklerle etkili bir şekilde iletişim kurabilirler.   
<span class="siyah-kalin"> Çeşitliliğe Saygı: </span> Ekip içindeki çeşitliliği bir zenginlik olarak görürler. Farklı bakış açılarına değer verirler ve herkesin kendini rahatça ifade edebileceği bir ortam yaratırlar.
<span class="siyah-kalin"> Uyumluluk: </span> Farklı görüşleri uzlaştırma ve ortak bir noktada buluşma konusunda yeteneklidirler. Çatışmaları en aza indirerek uyumlu bir çalışma ortamı sağlarlar.

<span class="kirmizi-kalin">9. Dengeli Yaklaşım </span>
<span class="siyah-kalin"> Objektiflik: </span> Karar alırken hem duygusal hem de mantıksal faktörleri dikkate alırlar. Duygusal tepkilere kapılmak yerine, objektif bir bakış açısıyla durumu değerlendirirler.
<span class="siyah-kalin"> Adil Olma: </span> Herkese karşı adil ve eşit davranmaya özen gösterirler. Kayırmacılık veya ayrımcılık yapmaktan kaçınarak, ekip içinde güven ve saygı oluştururlar.
<span class="siyah-kalin"> Sağduyu: </span> Pratik ve mantıklı çözümler üretme konusunda başarılıdırlar. Duygusal zeka ve analitik düşünme becerilerini birleştirerek etkili kararlar alırlar.""",

        "motivasyon": """
<span class="siyah-kalin"> Gönüllülük: </span> Gönüllü çalışmalara katılmak veya sosyal yardım projelerinde yer almak, S tipi kişilerin motivasyonunu yükseltebilir. Başkalarına yardım etmek, onlara tatmin ve mutluluk sağlar.
""",

        "meslekler": """
<span class="siyah-kalin"> Depo Yöneticisi (Tekstil): </span> Tekstil ürünlerinin depolanması, düzenlenmesi ve sevkiyatını yönetmek, düzenli ve organize olmayı gerektiren bu alanda başarılı olabilirler.

""",

        "takim": """
Özetle, S tipi bireyler takımlara uyum, işbirliği, güven ve istikrar getirirler. Bu özellikleri sayesinde, takımın başarısına önemli katkıda bulunurlar.
""",
    },
    "C": {
    "baslik": "C (Conscientiousness) - Sorumlu ve Titiz",
    "aciklama": """<p> <span class="siyah-kalin">S (Steadiness)</span> tipi bireyler insan ilişkilerinde uyumu korumaya çalışırken, C tipi bireyler işin ve sürecin doğruluğuna sadık kalır. S tipi duygusal destek sağlamaya eğilimliyken, C tipi gerçekler ve standartlar doğrultusunda destek olur.</p>

Özetle:
C tipi, DISC modelinin "kalite", "doğruluk" ve "mükemmellik" temsilcisidir. Analitik zekâları, titiz yaklaşımları ve yüksek standartlara olan bağlılıkları ile süreçleri güvence altına alır, hatasız sonuçlar üretir ve organizasyonların uzun vadeli başarısında kritik bir rol oynarlar. Ancak, esneklik, mükemmeliyetçilikten kaynaklanan aşırı eleştiri eğilimi ve duygusal esnekliği artırma konusunda gelişim göstermeleri, potansiyellerini daha da etkin kullanmalarına katkı sağlayabilir.""",

    
         "davranislar": """
<span class="siyah-kalin">• Geri Bildirime ve Eleştiriye Duyarlılık:</span>Kendi çalışmalarında titizlikle ilerledikleri için eleştirilere karşı hassas olabilirler. Yapıcı geri bildirimler aldıklarında kendilerini geliştirmeye açık olsalar da, haksız veya yüzeysel eleştiriler onları olumsuz etkileyebilir. Detaylı ve saygılı geri bildirim süreçlerini tercih ederler.
""",
"guclu": """


<span class="kirmizi-kalin">10. Risk Analizi ve Önleyici Yaklaşım:</span>
Karar vermeden önce olası riskleri analiz eder ve önleyici tedbirler geliştirirler. Riskleri minimize ederek daha güvenli, sağlam ve sürdürülebilir sonuçlar elde etmeye çalışırlar.""",
"zayif": """
<span class="kirmizi-kalin">10. Empati Eksikliği:</span>
Veri ve mantığa odaklanmaları, duygusal unsurları ikinci plana itmelerine sebep olabilir. Başkalarının duygusal ihtiyaçlarını göz ardı etme eğilimleri zaman zaman iletişim problemlerine yol açabilir.""",
"gelisim": """

<span class="kirmizi-kalin">10. Duygusal Zekayı Geliştirmek</span>
<span class="siyah-kalin">Neden Önemli?</span>
Sadece mantıksal düşünceye dayanmak, insanların duygusal ihtiyaçlarını gözden kaçırmaya neden olabilir.
<span class="siyah-kalin">Nasıl Geliştirilebilir?</span>
Empati kurmak için aktif dinleme teknikleri geliştirmek, duygusal tepkilere daha duyarlı olmak ve ilişkilerde anlayışlı bir yaklaşım benimsemek faydalı olur.""",
"iletisim": """
<span class="siyah-kalin">Örnek Senaryo:</span>
Bir proje toplantısında herkes fikir sunarken C tipi birey, sessizce notlar alır. Tartışmanın sonunda söz alarak "Bu fikirlerin güçlü ve zayıf yönlerini şöyle sıralayabiliriz…" diyerek analitik bir özet yapar. Ekibe hem netlik hem de yapı kazandırır, tartışmanın verimli şekilde ilerlemesini sağlar.
""",
"liderlik": """
<span class="kirmizi-kalin">10. Profesyonellik ve Güvenilirlik</span>
<span class="siyah-kalin">Ciddiyet ve Güven:</span>
C tipi liderler tutarlı davranışları ve profesyonel yaklaşımları ile güven oluşturur.
<span class="siyah-kalin">Sözünü Tutma:</span>
Verdikleri sözleri zamanında ve eksiksiz yerine getirerek örnek olurlar.
<span class="siyah-kalin">Öneri:</span>
Profesyonellik ile samimiyet arasında denge kurmak, insan ilişkilerini daha sıcak hale getirir.""",
"motivasyon": """
<span class="siyah-kalin">Güvenilir İletişim:</span>
Doğru, açık ve samimi iletişim C tipi bireylerin güven duygusunu artırır ve işlerine daha fazla bağlanmalarını sağlar.""",
"meslekler": """
<span class="siyah-kalin">Teknik Dokümantasyon Uzmanı:</span>
Ürün süreçlerinin belgelenmesi, kalite raporlarının hazırlanması gibi işler C tipi bireylerin detaylı çalışma tarzına uygundur.""",
"takim": """
<span class="siyah-kalin">Takım dinamiklerine uyum sağlamak:</span>
Kendi standartlarını dayatmaktan ziyade, takımın genel ritmine ve hedeflerine uyum göstermek uzun vadede daha etkili bir iş birliği sağlar.""",
    },
}


# ------------------- GRAFİK FONKSİYONLARI ------------------- #
def grafik_svg_uret(puanlar):
    labels = ['D', 'I', 'S', 'C']
    sizes = [puanlar['D'], puanlar['I'], puanlar['S'], puanlar['C']]
    colors = ['#e53935', '#fb8c00', '#43a047', '#1e88e5']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='svg')
    plt.close(fig)
    img_data.seek(0)
    return img_data.read().decode('utf-8')

def duygusal_zeka_skoru_hesapla(puanlar):
    # EQ = (I + S) - (D/2 + C/2) formülü örneği
    eq = (puanlar['I'] + puanlar['S']) - (puanlar['D']/2 + puanlar['C']/2)
    return max(0, min(100, int(eq * 10)))  # 0-100 aralığına normalize

def takim_dinamigi_analizi(en_yuksek_tip):
    etkilesimler = {
        "D": {"D": "Rekabet", "I": "Hızlı Sonuç", "S": "Gerilim", "C": "Veri Odaklı"},
        "I": {"D": "Enerji", "I": "Yaratıcılık", "S": "Uyum", "C": "Planlama"},
        "S": {"D": "Destek", "I": "Motivasyon", "S": "İstikrar", "C": "Detay"},
        "C": {"D": "Veri Paylaşımı", "I": "Esneklik", "S": "Sabır", "C": "Mükemmeliyetçilik"}
    }
    return etkilesimler[en_yuksek_tip]

def karsilastirma_grafigi_uret(puanlar):
    GENEL_ORTALAMALAR = {"D": 6.2, "I": 5.8, "S": 7.1, "C": 6.5}
    kategoriler = list(puanlar.keys())
    kullanici_puan = list(puanlar.values())
    genel_ortalama = [GENEL_ORTALAMALAR[k] for k in kategoriler]

    fig, ax = plt.subplots(figsize=(8.27, 4), dpi=100)
    bar_width = 0.3
    index = np.arange(len(kategoriler))

    rects1 = ax.bar(index - bar_width/2, kullanici_puan, bar_width, 
                   label='Sizin Puanlarınız', color='#1e88e5', edgecolor='black')
    rects2 = ax.bar(index + bar_width/2, genel_ortalama, bar_width, 
                   label='Genel Ortalama', color='#43a047', edgecolor='black')

    ax.set_xlabel('DiSK Kategorileri', fontsize=9, labelpad=10)
    ax.set_ylabel('Puan', fontsize=9, labelpad=10)
    ax.set_title('DiSK Puanlarınız vs Genel Ortalama', fontsize=11, pad=15)
    
    ax.set_xticks(index)
    ax.set_xticklabels(kategoriler, fontsize=8)
    ax.set_yticks(np.arange(0, max(max(kullanici_puan), max(genel_ortalama)) + 4, 2))
    ax.set_yticklabels(ax.get_yticks(), fontsize=7)
    
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=8, loc='upper right', framealpha=0.9)
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=7)
    
    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout(pad=1.5)

    img_data = io.BytesIO()
    plt.savefig(img_data, format='svg', bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    img_data.seek(0)
    return img_data.read().decode('utf-8')

# ------------------- PDF OLUŞTURMA FONKSİYONU ------------------- #
def pdf_olustur(kullanici_bilgisi, puanlar):
    try:
        # 1. Şablonu Yükle
        with open("disc_rapor_12_sayfa_template_with_intro.html", "r", encoding="utf-8") as f:
            sablon = Template(f.read())
    except Exception as e:
        messagebox.showerror("Hata", f"HTML şablonu yüklenemedi: {str(e)}")
        return # Fonksiyondan çık

    try:
        # 2. Gerekli Verileri Hesapla
        en_yuksek_tip = max(puanlar, key=puanlar.get)
        disc_tip = DISC_ICERIK[en_yuksek_tip]
        grafik_svg = grafik_svg_uret(puanlar)
        karsilastirma_grafik = karsilastirma_grafigi_uret(puanlar)
        eq_skor = duygusal_zeka_skoru_hesapla(puanlar)
        takim_dinamigi_verileri = takim_dinamigi_analizi(en_yuksek_tip)

        # Takım dinamikleri verisini HTML listesi olarak formatla
        takim_dinamigi_html = "<ul>"
        for diger_tip, etkilesim in takim_dinamigi_verileri.items():
            takim_dinamigi_html += f"<li><strong>{diger_tip} Tipi ile Etkileşim:</strong> {etkilesim}</li>"
        takim_dinamigi_html += "</ul>"

    except Exception as e:
        messagebox.showerror("Hata", f"Rapor verileri veya grafikler oluşturulamadı: {str(e)}")
        return # Fonksiyondan çık

    try:
        # 3. HTML'i Render Et
        html = sablon.render(
            ad=kullanici_bilgisi["ad"],
            yil=kullanici_bilgisi["yil"],
            cinsiyet=kullanici_bilgisi["cinsiyet"],
            D=puanlar["D"],
            I=puanlar["I"],
            S=puanlar["S"],
            C=puanlar["C"],
            grafik_svg=grafik_svg,
            karsilastirma_grafik=karsilastirma_grafik,
            disc_tip=disc_tip,
            now=datetime.now().strftime("%d.%m.%Y"),
            eq_skor=eq_skor,
            takim_dinamigi_html=takim_dinamigi_html,
            en_yuksek_tip=en_yuksek_tip
        )

        # 4. PDF'i Kaydetme Yolunu Sor ve Oluştur
        dosya_adi = f"{kullanici_bilgisi['ad'].replace(' ', '_')}_DISC_Raporu.pdf"
        kaydetme_yolu = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Dosyaları", "*.pdf")],
            initialfile=dosya_adi
        )
        if not kaydetme_yolu:
            # Kullanıcı kaydetmekten vazgeçtiyse fonksiyondan çık
            return

        # PDF Oluştur
        HTML(string=html, base_url=os.path.abspath(".")).write_pdf(kaydetme_yolu)

        # Oluşturulan PDF'i Aç
        os.startfile(kaydetme_yolu)

    except Exception as e:
        messagebox.showerror("Hata", f"PDF oluşturma veya kaydetme sırasında hata: {str(e)}")

# ------------------- SORULAR VE GUI ------------------- #
SORULAR = [
    {"soru": "1. Aşağıdakilerden hangisi sizi en iyi tanımlar?", "secenekler": ["Kararlı", "Eğlenceli", "Sabırlı", "Dikkatli"]},
    {"soru": "2. Baskı altında nasıl davranırsınız?", "secenekler": ["Hızlı karar alırım", "Mizah yaparım", "Sakin kalırım", "Analiz ederim"]},
    {"soru": "3. Bir ekipte hangi rol size daha uygundur?", "secenekler": ["Liderlik", "Motivasyon", "Destek", "Planlama"]},
]

SECENEK_TIPLERI = ["D", "I", "S", "C"]

class KisilikTesti:
    def __init__(self, root):
        self.root = root
        self.root.title("DiSC Kişilik Testi")
        self.root.geometry("550x600")  # Yükseklik artırıldı
        self.root.configure(bg="#e0f7fa")
        self.index = 0
        self.puanlar = {"D": 0, "I": 0, "S": 0, "C": 0}
        self.kullanici = {}
        self.giris_ekrani()

    def giris_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Başlık
        tk.Label(self.root, text="DiSC Kişilik Testi", font=("Helvetica", 20, "bold"), 
                bg="#e0f7fa", fg="#00796b").pack(pady=10)

        # Açıklama Metni
        aciklama_frame = tk.Frame(self.root, bg="#e0f7fa")
        aciklama_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        text_scroll = tk.Scrollbar(aciklama_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        aciklama_text = tk.Text(aciklama_frame, height=8, wrap=tk.WORD, 
                               yscrollcommand=text_scroll.set,
                               font=("Arial", 10), bg="white")
        aciklama_text.pack(fill="both", expand=True)
        text_scroll.config(command=aciklama_text.yview)

        aciklama_icerik = """
        Bu test, DISC modeline dayalı kişilik analizi yapmak için tasarlanmıştır. 
        Aşağıdaki soruları cevaplarken:

        1. Size en yakın hissettiğiniz seçeneği işaretleyin
        2. İçgüdülerinize göre hızlıca karar verin
        3. "Doğru" cevap aramayın, samimi olun

        Verdiğiniz cevaplar; liderlik tarzınız, iletişim tercihleriniz ve takım dinamiklerindeki 
        rolünüz hakkında öngörüler sunacaktır. Analiz sonucu otomatik PDF rapor olarak oluşturulacaktır.
        """
        aciklama_text.insert(tk.END, aciklama_icerik.strip())
        aciklama_text.configure(state="disabled")

        # Onay Kutusu
        self.onay_var = tk.BooleanVar(value=False)
        onay_kutusu = tk.Checkbutton(
            self.root, 
            text="Yukarıdaki açıklamayı okudum ve kişilik analizim için verdiğim cevapların kullanılacağını kabul ediyorum.",
            variable=self.onay_var,
            bg="#e0f7fa",
            activebackground="#e0f7fa",
            wraplength=400,
            command=self.onay_durumu_kontrol
        )
        onay_kutusu.pack(pady=10)

        # Kullanıcı Bilgi Formu
        form_frame = tk.Frame(self.root, bg="#e0f7fa")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Ad Soyad:", bg="#e0f7fa").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ad_entry = tk.Entry(form_frame, width=30)
        self.ad_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Doğum Yılı:", bg="#e0f7fa").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.yil_var = tk.StringVar()
        self.yil_combo = ttk.Combobox(form_frame, textvariable=self.yil_var, 
                                     values=[str(y) for y in range(1965,2017)], state="readonly")
        self.yil_combo.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Cinsiyet:", bg="#e0f7fa").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cinsiyet_var = tk.StringVar()
        self.cinsiyet_combo = ttk.Combobox(form_frame, textvariable=self.cinsiyet_var, 
                                          values=["Kadın", "Erkek", "Diğer"], state="readonly")
        self.cinsiyet_combo.grid(row=2, column=1, pady=5)

        # Teste Başla Butonu
        self.basla_button = ttk.Button(self.root, text="Teste Başla", 
                                      command=self.sorulara_basla, state="disabled")
        self.basla_button.pack(pady=20)

    def onay_durumu_kontrol(self):
        """Onay ve form kontrolü"""
        form_dolu = all([
            self.ad_entry.get().strip(),
            self.yil_var.get(),
            self.cinsiyet_var.get()
        ])
        
        if self.onay_var.get() and form_dolu:
            self.basla_button.config(state="normal")
        else:
            self.basla_button.config(state="disabled")

    def sorulara_basla(self):
        ad = self.ad_entry.get().strip()
        yil = self.yil_var.get()
        cinsiyet = self.cinsiyet_var.get()
        
        if not self.onay_var.get():
            messagebox.showwarning("Onay Gerekli", "Lütfen açıklamayı okuyup onay kutusunu işaretleyin")
            return

        if not ad or not yil or not cinsiyet:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        
        self.kullanici = {"ad": ad, "yil": yil, "cinsiyet": cinsiyet}
        self.soru_ekrani()

    def soru_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.soru_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#e0f7fa")
        self.soru_label.pack(pady=10)

        self.secenek_var = tk.StringVar()
        self.secenekler = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.secenek_var, value="", font=("Arial", 12), bg="#e0f7fa")
            rb.pack(anchor="w", padx=20)
            self.secenekler.append(rb)

        self.ileri_button = tk.Button(self.root, text="İleri", command=self.sonraki_soru)
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
        secenek_index = SORULAR[self.index]["secenekler"].index(secim)
        secenek_tipi = SECENEK_TIPLERI[secenek_index]
        self.puanlar[secenek_tipi] += 1
        self.index += 1
        if self.index < len(SORULAR):
            self.guncelle()
        else:
            self.rapor_ekrani()

    def rapor_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Kişilik analiz testiniz bitmiştir.", font=("Arial", 14), bg="#e0f7fa").pack(pady=20)
        tk.Button(self.root, text="PDF'e Kaydet", command=lambda: pdf_olustur(self.kullanici, self.puanlar)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = KisilikTesti(root)
    root.mainloop()

    def raporu_kaydet(self):
        try:
            html = sablon.render(
                ad=kullanici_bilgisi["ad"],
                yil=kullanici_bilgisi["yil"],
                cinsiyet=kullanici_bilgisi["cinsiyet"],
                D=puanlar["D"],
                I=puanlar["I"],
                S=puanlar["S"],
                C=puanlar["C"],
                grafik_svg=grafik_svg,
                karsilastirma_grafik=karsilastirma_grafik,
                disc_tip=disc_tip,
                now=datetime.now().strftime("%d.%m.%Y"),
                eq_skor=eq_skor,  # Yeni parametre
                takim_dinamigi=takim_dinamigi,  # Yeni parametre
                en_yuksek_tip=en_yuksek_tip,  # Yeni parametre
                puanlar=puanlar  # Yeni parametre
            )
        except Exception as e:
            messagebox.showerror("Hata", f"HTML oluşturulamadı: {str(e)}")
            return  # Hata durumunda fonksiyondan çık

        try:
            dosya_adi = f"{kullanici_bilgisi['ad'].replace(' ', '_')}_DISC_Raporu.pdf"
            kaydetme_yolu = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Dosyaları", "*.pdf")],
                initialfile=dosya_adi
            )
            if not kaydetme_yolu:
                return
            HTML(string=html, base_url=os.path.dirname(os.path.abspath("disc_rapor_12_sayfa_template_with_intro.html"))).write_pdf(kaydetme_yolu)
            os.startfile(kaydetme_yolu)
        except Exception as e:
            messagebox.showerror("Hata", f"PDF oluşturulamadı: {str(e)}")