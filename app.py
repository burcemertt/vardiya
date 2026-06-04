import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Akıllı Vardiya Planlayıcı")
st.title("🛡️ Öncelikli ve Dengeli Vardiya Planlayıcı")

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
    st.session_state.talep = {p['isim']: {"v1": SHIFTS[0], "v2": SHIFTS[1], "izin": DAYS[0]} for p in staff_list}

st.sidebar.header("📝 Personel Tercihleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']} ({p['rol']})"):
        st.session_state.talep[p['isim']]['v1'] = st.selectbox("1. Vardiya", SHIFTS, key=f"{p['isim']}_v1")
        st.session_state.talep[p['isim']]['v2'] = st.selectbox("2. Vardiya", SHIFTS, key=f"{p['isim']}_v2")
        st.session_state.talep[p['isim']]['izin'] = st.selectbox("İzin Günü (Haftada 1)", DAYS, key=f"{p['isim']}_izin")

if st.button("🚀 Öncelikli Vardiyayı Raporla"):
    # Rol öncelik sırası: Kıdemli > Temsilci > Eğitim
    role_priority = {"Kıdemli": 0, "Temsilci": 1, "Eğitim": 2}
    sorted_staff = sorted(staff_list, key=lambda x: role_priority[x['rol']])
    
    rows = []
    for p in sorted_staff:
        p_row = {"Personel": p['isim'], "Rol": p['rol']}
        izin = st.session_state.talep[p['isim']]['izin']
        
        for day in DAYS:
            if day == izin:
                p_row[day] = "OFF"
            else:
                # Kıdemli önceliği ile vardiya ataması
                p_row[day] = f"{st.session_state.talep[p['isim']]['v1']}"
        rows.append(p_row)

    df = pd.DataFrame(rows)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps([df.columns.tolist()] + df.values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
