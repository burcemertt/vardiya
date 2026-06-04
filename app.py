import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Akıllı Vardiya Planlayıcı")
st.title("🛡️ Site Kurulum Dengeli Vardiya Planlayıcı")

# Personel Listesi (Kurulum sayıları eklendi)
staff_list = [
    {"isim": "POLAT", "rol": "Kıdemli", "kurulum": 4}, {"isim": "İLKER", "rol": "Kıdemli", "kurulum": 4},
    {"isim": "KORAY", "rol": "Kıdemli", "kurulum": 4}, {"isim": "MUSTAFA", "rol": "Kıdemli", "kurulum": 2},
    {"isim": "YALIN", "rol": "Kıdemli", "kurulum": 2}, {"isim": "UĞUR", "rol": "Kıdemli", "kurulum": 1},
    {"isim": "CÜNEYT", "rol": "Kıdemli", "kurulum": 1}, {"isim": "METİN", "rol": "Temsilci", "kurulum": 4},
    {"isim": "EMRE", "rol": "Temsilci", "kurulum": 4}, {"isim": "SENA", "rol": "Temsilci", "kurulum": 2},
    {"isim": "ILGAZ", "rol": "Temsilci", "kurulum": 2}, {"isim": "OSMAN", "rol": "Temsilci", "kurulum": 1},
    {"isim": "YASİN", "rol": "Temsilci", "kurulum": 1}, {"isim": "CANER", "rol": "Temsilci", "kurulum": 1},
    {"isim": "BURÇAK", "rol": "Temsilci", "kurulum": 4}, {"isim": "İBRAHİM", "rol": "Temsilci", "kurulum": 1},
    {"isim": "MÜGE", "rol": "Temsilci", "kurulum": 1}, {"isim": "YALÇIN", "rol": "Temsilci", "kurulum": 1},
    {"isim": "MEHMET", "rol": "Temsilci", "kurulum": 1}, {"isim": "ARİF", "rol": "Temsilci", "kurulum": 1},
    {"isim": "ENİS", "rol": "Temsilci", "kurulum": 1}, {"isim": "BARIŞ", "rol": "Temsilci", "kurulum": 1},
    {"isim": "TOYGAR", "rol": "Temsilci", "kurulum": 1}, {"isim": "SELİN", "rol": "Temsilci", "kurulum": 1},
    {"isim": "HAKAN", "rol": "Temsilci", "kurulum": 1}, {"isim": "EYLEM", "rol": "Temsilci", "kurulum": 1},
    {"isim": "SEYFİ", "rol": "Eğitim", "kurulum": 1}, {"isim": "DEMET", "rol": "Eğitim", "kurulum": 1},
    {"isim": "SEYİT", "rol": "Eğitim", "kurulum": 1}, {"isim": "BERK", "rol": "Eğitim", "kurulum": 1},
    {"isim": "TAHİR", "rol": "Eğitim", "kurulum": 1}, {"isim": "RECEP", "rol": "Eğitim", "kurulum": 1},
    {"isim": "TANJU", "rol": "Eğitim", "kurulum": 1}, {"isim": "OLCAY", "rol": "Eğitim", "kurulum": 1},
    {"isim": "ÖZCAN", "rol": "Eğitim", "kurulum": 1}, {"isim": "KEVSER", "rol": "Eğitim", "kurulum": 1},
    {"isim": "HARUN", "rol": "Eğitim", "kurulum": 1}, {"isim": "KAZIM", "rol": "Eğitim", "kurulum": 1},
    {"isim": "KUBİLAY", "rol": "Eğitim", "kurulum": 1}, {"isim": "KİRAZ", "rol": "Eğitim", "kurulum": 1}
]

SHIFTS = ["08:30-17:30", "12:00-21:00", "17:30-02:30", "19:00-04:00", "21:00-06:00", "00:00-09:00"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"v1": SHIFTS[0], "v2": SHIFTS[1], "izinler": []} for p in staff_list}

st.sidebar.header("📝 Personel Tercihleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']} ({p['rol']} | {p['kurulum']} Site)"):
        st.session_state.talep[p['isim']]['v1'] = st.selectbox("1. Vardiya", SHIFTS, key=f"{p['isim']}_v1")
        st.session_state.talep[p['isim']]['v2'] = st.selectbox("2. Vardiya", SHIFTS, key=f"{p['isim']}_v2")
        st.session_state.talep[p['isim']]['izinler'] = st.multiselect("İzin Tercihleri", DAYS, key=f"{p['isim']}_izin")

if st.button("🚀 Vardiyayı Çakışmasız Raporla"):
    günlük_4_site_izin = {day: 0 for day in DAYS}
    vardiya_yükü = {day: {s: 0 for s in SHIFTS} for day in DAYS}
    
    # Sıralama: Kıdemli > Temsilci > Eğitim
    role_priority = {"Kıdemli": 0, "Temsilci": 1, "Eğitim": 2}
    sorted_staff = sorted(staff_list, key=lambda x: role_priority[x['rol']])
    
    rows = []
    for p in sorted_staff:
        tercihler = st.session_state.talep[p['isim']]['izinler']
        is_4_site = p['kurulum'] == 4
        
        # İzin günü seçimi (4 site kurulumu olanlar için çakışma kontrolü)
        secilen_izin = None
        for day in tercihler:
            if is_4_site and günlük_4_site_izin[day] > 0:
                continue # Bu gün dolu, başka güne bak
            secilen_izin = day
            break
            
        if is_4_site and secilen_izin:
            günlük_4_site_izin[secilen_izin] += 1
            
        # Vardiya seçimi
        v1, v2 = st.session_state.talep[p['isim']]['v1'], st.session_state.talep[p['isim']]['v2']
        p_row = {"Personel": p['isim'], "Rol": p['rol'], "Kurulum": p['kurulum']}
        
        for day in DAYS:
            if day == secilen_izin:
                p_row[day] = "OFF"
            else:
                secilen_vardiya = v1 if vardiya_yükü[day][v1] <= vardiya_yükü[day][v2] else v2
                vardiya_yükü[day][secilen_vardiya] += 1
                p_row[day] = secilen_vardiya
        rows.append(p_row)

    df = pd.DataFrame(rows)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps([df.columns.tolist()] + df.values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
