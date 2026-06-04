import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Akıllı Vardiya Planlayıcı")
st.title("🛡️ Akıllı Vardiya ve İzin Dengeleyici")

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

SHIFTS = ["08:30-17:30", "12:00-21:00", "17:30-02:30", "19:00-04:00", "21:00-06:00", "00:00-09:00"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"v1": SHIFTS[0], "v2": SHIFTS[1], "izinler": []} for p in staff_list}

st.sidebar.header("📝 Personel Tercihleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']} ({p['rol']})"):
        st.session_state.talep[p['isim']]['v1'] = st.selectbox("1. Vardiya", SHIFTS, key=f"{p['isim']}_v1")
        st.session_state.talep[p['isim']]['v2'] = st.selectbox("2. Vardiya", SHIFTS, key=f"{p['isim']}_v2")
        st.session_state.talep[p['isim']]['izinler'] = st.multiselect("İzin Tercihleri", DAYS, key=f"{p['isim']}_izin")

if st.button("🚀 Vardiyayı Dengeleyerek Raporla"):
    günlük_izin_sayaci = {day: 0 for day in DAYS}
    vardiya_yükü = {day: {s: 0 for s in SHIFTS} for day in DAYS}
    
    role_priority = {"Kıdemli": 0, "Temsilci": 1, "Eğitim": 2}
    sorted_staff = sorted(staff_list, key=lambda x: role_priority[x['rol']])
    
    rows = []
    for p in sorted_staff:
        tercihler = st.session_state.talep[p['isim']]['izinler']
        
        # 1. İzin Günü Seçimi (En az izinli gün)
        secilen_izin = min(tercihler, key=lambda d: günlük_izin_sayaci[d]) if tercihler else None
        if secilen_izin: günlük_izin_sayaci[secilen_izin] += 1
            
        # 2. Vardiya Seçimi (En az kişi olan vardiya)
        v1, v2 = st.session_state.talep[p['isim']]['v1'], st.session_state.talep[p['isim']]['v2']
        
        p_row = {"Personel": p['isim'], "Rol": p['rol']}
        for day in DAYS:
            if day == secilen_izin:
                p_row[day] = "OFF"
            else:
                # İki vardiyadan yükü az olanı seç
                secilen_vardiya = v1 if vardiya_yükü[day][v1] <= vardiya_yükü[day][v2] else v2
                vardiya_yükü[day][secilen_vardiya] += 1
                p_row[day] = secilen_vardiya
        rows.append(p_row)

    df = pd.DataFrame(rows)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps([df.columns.tolist()] + df.values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
