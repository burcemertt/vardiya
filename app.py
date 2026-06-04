import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Vardiya Planlayıcı")
st.title("🛡️ Kişisel Vardiya Raporu")

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

if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"v1": "Talep Yok", "v2": "Talep Yok", "izin": []} for p in staff_list}

st.sidebar.header("📝 Personel Tercihleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']}"):
        st.session_state.talep[p['isim']]['v1'] = st.selectbox("1. Tercih", ["Talep Yok"] + SHIFTS, key=f"{p['isim']}_v1")
        st.session_state.talep[p['isim']]['v2'] = st.selectbox("2. Tercih", ["Talep Yok"] + SHIFTS, key=f"{p['isim']}_v2")
        st.session_state.talep[p['isim']]['izin'] = st.multiselect("İzin Günü", DAYS, key=f"{p['isim']}_izin")

if st.button("🚀 Kişisel Vardiya Raporu Oluştur"):
    rows = []
    for p in staff_list:
        p_row = {"Personel": p['isim']}
        for day in DAYS:
            if day in st.session_state.talep[p['isim']]['izin']:
                p_row[day] = "OFF"
            elif st.session_state.talep[p['isim']]['v1'] != "Talep Yok":
                p_row[day] = st.session_state.talep[p['isim']]['v1']
            else:
                p_row[day] = "Belirsiz"
        rows.append(p_row)

    df = pd.DataFrame(rows)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps([df.columns.tolist()] + df.values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
