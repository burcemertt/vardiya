import streamlit as st
import pandas as pd
import random
import io

st.set_page_config(layout="wide", page_title="Vardiya Planlayıcı")
st.title("🛡️ Akıllı Vardiya Planlama Robotu")

# Personel Listesi
staff_list = [
    {"isim": "POLAT", "rol": "Kıdemli"}, {"isim": "İLKER", "rol": "Kıdemli"},
    {"isim": "KORAY", "rol": "Kıdemli"}, {"isim": "MUSTAFA", "rol": "Kıdemli"},
    {"isim": "YALIN", "rol": "Kıdemli"}, {"isim": "UĞUR", "rol": "Kıdemli"},
    {"isim": "CÜNEYT", "rol": "Kıdemli"}, {"isim": "METİN", "rol": "Temsilci"},
    {"isim": "EMRE", "rol": "Temsilci"}, {"isim": "SENA", "rol": "Temsilci"},
    {"isim": "ILGAZ", "rol": "Temsilci"}, {"isim": "OSMAN", "rol": "Temsilci"},
    {"isim": "YASİN", "rol": "Temsilci"}, {"isim": "CANER", "rol": "Temsilci"},
    {"isim": "BURÇAK", "rol": "Temsilci"}, {"isim": "İBRAHİM", "rol": "Temsilci"},
    {"isim": "MÜGE", "rol": "Temsilci"}, {"isim": "YALÇIN", "rol": "Temsilci"},
    {"isim": "MEHMET", "rol": "Temsilci"}, {"isim": "ARİF", "rol": "Temsilci"},
    {"isim": "ENİS", "rol": "Temsilci"}, {"isim": "BARIŞ", "rol": "Temsilci"},
    {"isim": "TOYGAR", "rol": "Temsilci"}, {"isim": "SELİN", "rol": "Temsilci"},
    {"isim": "HAKAN", "rol": "Temsilci"}, {"isim": "EYLEM", "rol": "Temsilci"},
    {"isim": "SEYFİ", "rol": "Eğitim"}, {"isim": "DEMET", "rol": "Eğitim"},
    {"isim": "SEYİT", "rol": "Eğitim"}, {"isim": "BERK", "rol": "Eğitim"},
    {"isim": "TAHİR", "rol": "Eğitim"}, {"isim": "RECEP", "rol": "Eğitim"},
    {"isim": "TANJU", "rol": "Eğitim"}, {"isim": "OLCAY", "rol": "Eğitim"},
    {"isim": "ÖZCAN", "rol": "Eğitim"}, {"isim": "KEVSER", "rol": "Eğitim"},
    {"isim": "HARUN", "rol": "Eğitim"}, {"isim": "KAZIM", "rol": "Eğitim"},
    {"isim": "KUBİLAY", "rol": "Eğitim"}, {"isim": "KİRAZ", "rol": "Eğitim"}
]

SHIFTS = ["Sabah", "12:00 Ara", "17:30 Ara", "19:00 Ara", "21:00 Ara", "Gece"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# Kenar Çubuğu Ayarları
st.sidebar.header("🎯 Kilit Personel Seçimi")
selected_kilit = st.sidebar.multiselect(
    "Bu hafta vardiyayı yönetecek kilit isimleri seçin:",
    options=[p['isim'] for p in staff_list],
    default=[p['isim'] for p in staff_list if p['rol'] == "Kıdemli"]
)

if st.button("🚀 Vardiyayı Oluştur"):
    kilit_personel = [p for p in staff_list if p['isim'] in selected_kilit]
    digerleri = [p for p in staff_list if p['isim'] not in selected_kilit]
    
    schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
    
    # Kilitleri dağıt
    for day in DAYS:
        random.shuffle(kilit_personel)
        for i, shift in enumerate(SHIFTS):
            if i < len(kilit_personel):
                schedule[day][shift].append(kilit_personel[i]['isim'] + " (Kilit)")
    
    # Diğerlerini dağıt
    for day in DAYS:
        for shift in SHIFTS:
            while len(schedule[day][shift]) < 2:
                if digerleri:
                    p = digerleri.pop(0)
                    schedule[day][shift].append(p['isim'] + " (" + p['rol'] + ")")
                    digerleri.append(p)

    # DataFrame'e dök
    rows = []
    for day in DAYS:
        for shift in SHIFTS:
            for p in schedule[day][shift]:
                rows.append({"Gün": day, "Vardiya": shift, "Personel": p})
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    
    # Excel oluşturma
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    
    st.download_button("📥 Excel İndir", buffer.getvalue(), "haftalik_vardiya.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
