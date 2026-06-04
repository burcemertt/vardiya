import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Vardiya Planlayıcı")
st.title("🛡️ Esnek ve Tam Kapsamlı Vardiya Planlayıcı")

# Vardiya Grupları
VARDİYA_SAATLERİ = {
    "Sabah": "08:30-17:30",
    "Öğle": "12:00-21:00",
    "Akşam": "17:30-02:30",
    "Gece-1": "19:00-04:00",
    "Gece-2": "21:00-06:00",
    "Sabah-Erken": "00:00-08:30"
}
VARDİYA_LISTESI = list(VARDİYA_SAATLERİ.keys())

# Tüm personeller (Kurulum bilgileri korunuyor)
staff_list = [
    {"isim": "POLAT", "rol": "Kıdemli", "kurulum": 4}, {"isim": "İLKER", "rol": "Kıdemli", "kurulum": 4},
    {"isim": "KORAY", "rol": "Kıdemli", "kurulum": 4}, {"isim": "MUSTAFA", "rol": "Kıdemli", "kurulum": 4},
    {"isim": "YALIN", "rol": "Kıdemli", "kurulum": 4}, {"isim": "UĞUR", "rol": "Kıdemli", "kurulum": 4},
    {"isim": "CÜNEYT", "rol": "Kıdemli", "kurulum": 4}, {"isim": "METİN", "rol": "Temsilci", "kurulum": 4},
    {"isim": "EMRE", "rol": "Temsilci", "kurulum": 2}, {"isim": "SENA", "rol": "Temsilci", "kurulum": 1},
    {"isim": "ILGAZ", "rol": "Temsilci", "kurulum": 4}, {"isim": "OSMAN", "rol": "Temsilci", "kurulum": 3},
    {"isim": "YASİN", "rol": "Temsilci", "kurulum": 4}, {"isim": "CANER", "rol": "Temsilci", "kurulum": 2},
    {"isim": "BURÇAK", "rol": "Temsilci", "kurulum": 2}, {"isim": "İBRAHİM", "rol": "Temsilci", "kurulum": 2},
    {"isim": "MÜGE", "rol": "Temsilci", "kurulum": 4}, {"isim": "YALÇIN", "rol": "Temsilci", "kurulum": 4},
    {"isim": "MEHMET", "rol": "Temsilci", "kurulum": 4}, {"isim": "ARİF", "rol": "Temsilci", "kurulum": 1},
    {"isim": "ENİS", "rol": "Temsilci", "kurulum": 1}, {"isim": "BARIŞ", "rol": "Temsilci", "kurulum": 1},
    {"isim": "TOYGAR", "rol": "Temsilci", "kurulum": 1}, {"isim": "SELİN", "rol": "Temsilci", "kurulum": 1},
    {"isim": "HAKAN", "rol": "Temsilci", "kurulum": 1}, {"isim": "EYLEM", "rol": "Temsilci", "kurulum": 1},
    {"isim": "SEYFİ", "rol": "Eğitim", "kurulum": 1}, {"isim": "DEMET", "rol": "Eğitim", "kurulum": 1},
    {"isim": "SEYİT", "rol": "Eğitim", "kurulum": 1}, {"isim": "BERK", "rol": "Eğitim", "kurulum": 1},
    {"isim": "TAHİR", "rol": "Eğitim", "kurulum": 1}, {"isim": "RECEP", "rol": "Eğitim", "kurulum": 1},
    {"isim": "TANJU", "rol": "Eğitim", "kurulum": 1}, {"isim": "OLCAY", "rol": "Eğitim", "kurulum": 1},
    {"isim": "ÖZCAN", "rol": "Eğitim", "kurulum": 1}, {"isim": "EDİZ", "rol": "Eğitim", "kurulum": 1},
    {"isim": "KEVSER", "rol": "Eğitim", "kurulum": 1}, {"isim": "HARUN", "rol": "Eğitim", "kurulum": 1},
    {"isim": "KAZIM", "rol": "Eğitim", "kurulum": 1}, {"isim": "KUBİLAY", "rol": "Eğitim", "kurulum": 1},
    {"isim": "KİRAZ", "rol": "Eğitim", "kurulum": 1}
]

DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"izinler": [], "v1": VARDİYA_LISTESI[0], "v2": VARDİYA_LISTESI[1]} for p in staff_list}

st.sidebar.header("📝 Personel Tercihleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']} ({p['kurulum']} Kurulum)"):
        v1 = st.selectbox("1. Vardiya", VARDİYA_LISTESI, key=f"{p['isim']}_v1")
        v2 = st.selectbox("2. Vardiya", VARDİYA_LISTESI, key=f"{p['isim']}_v2")
        izinler = st.multiselect("İzin Tercihleri", DAYS, key=f"{p['isim']}_izin")
        st.session_state.talep[p['isim']] = {"v1": v1, "v2": v2, "izinler": izinler}

if st.button("🚀 Vardiyayı Çakışmasız Raporla"):
    günlük_4_site_izin = {day: 0 for day in DAYS}
    vardiya_yükü = {day: {s: 0 for s in VARDİYA_SAATLERİ.values()} for day in DAYS}
    
    role_prio = {"Kıdemli": 0, "Temsilci": 1, "Eğitim": 2}
    sorted_staff = sorted(staff_list, key=lambda x: role_prio[x['rol']])
    
    rows = []
    for p in sorted_staff:
        data = st.session_state.talep[p['isim']]
        v1_s, v2_s = VARDİYA_SAATLERİ[data['v1']], VARDİYA_SAATLERİ[data['v2']]
        
        is_4_site = p['kurulum'] == 4
        secilen_izin = None
        for day in data['izinler']:
            if is_4_site and günlük_4_site_izin.get(day, 0) > 0: continue
            secilen_izin = day
            break
        if is_4_site and secilen_izin: günlük_4_site_izin[secilen_izin] += 1
            
        p_row = {"Personel": p['isim'], "Rol": p['rol'], "Kurulum": p['kurulum']}
        for day in DAYS:
            if day == secilen_izin:
                p_row[day] = "OFF"
            else:
                # Vardiya dengesi: Yükü az olanı seç
                s = v1_s if vardiya_yükü[day][v1_s] <= vardiya_yükü[day][v2_s] else v2_s
                vardiya_yükü[day][s] += 1
                p_row[day] = s
        rows.append(p_row)

    df = pd.DataFrame(rows)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps([df.columns.tolist()] + df.values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
