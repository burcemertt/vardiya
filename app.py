import streamlit as st
import pandas as pd
import random
import json

st.set_page_config(layout="wide", page_title="Vardiya Planlayıcı")
st.title("🛡️ Profesyonel Vardiya Planlayıcı")

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

SHIFTS = ["Sabah (08:30)", "12:00 Ara", "17:30 Ara", "19:00 Ara", "21:00 Ara", "Gece (00:00)"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# Session state'i başlat
if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"v1": "Talep Yok", "v2": "Talep Yok"} for p in staff_list}

st.sidebar.header("🎯 Kilit Personel")
selected_kilit = st.sidebar.multiselect("Vardiya liderleri:", options=[p['isim'] for p in staff_list], default=[p['isim'] for p in staff_list if p['rol'] == "Kıdemli"])

st.sidebar.header("📝 Personel Talepleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']} ({p['rol']})"):
        st.session_state.talep[p['isim']]['v1'] = st.selectbox(f"{p['isim']} 1. Tercih", ["Talep Yok"] + SHIFTS, key=f"{p['isim']}_v1")
        st.session_state.talep[p['isim']]['v2'] = st.selectbox(f"{p['isim']} 2. Tercih", ["Talep Yok"] + SHIFTS, key=f"{p['isim']}_v2")

if st.button("🚀 Vardiyayı Matris Olarak Oluştur"):
    data = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
    
    # Basit atama mantığı
    for day in DAYS:
        for shift in SHIFTS:
            # Önce tercih edenleri ata
            for p in staff_list:
                if st.session_state.talep[p['isim']]['v1'] == shift:
                    data[day][shift].append(p['isim'])
            
            # Boşlukları doldur
            if len(data[day][shift]) < 2:
                data[day][shift].append("Boş")
            
            data[day][shift] = " / ".join(data[day][shift])

    df = pd.DataFrame(data)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps(df.reset_index().values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
