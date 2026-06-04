import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Vardiya Robotu")
st.title("🛡️ Akıllı Vardiya ve İzin Dengeleyici")

# Supervisor'lar hariç liste (Kurulum sayıları ve vardiya grupları ile)
staff_list = [
    {"isim": "ENES", "rol": "Kıdemli", "kurulum": 4, "v_options": ["08:30-17:30"]},
    {"isim": "POLAT", "rol": "Kıdemli", "kurulum": 4, "v_options": ["08:30-17:30"]},
    {"isim": "İLKER", "rol": "Kıdemli", "kurulum": 4, "v_options": ["08:30-17:30"]},
    {"isim": "METİN", "rol": "Temsilci", "kurulum": 2, "v_options": ["08:30-17:30"]},
    {"isim": "EMRE", "rol": "Temsilci", "kurulum": 2, "v_options": ["08:30-17:30"]},
    {"isim": "SENA", "rol": "Temsilci", "kurulum": 1, "v_options": ["08:30-17:30"]},
    {"isim": "SEYFİ", "rol": "Eğitim", "kurulum": 1, "v_options": ["08:30-17:30"]},
    {"isim": "KORAY", "rol": "Kıdemli", "kurulum": 4, "v_options": ["12:00-21:00"]},
    {"isim": "MUSTAFA", "rol": "Kıdemli", "kurulum": 4, "v_options": ["17:30-02:30"]},
    {"isim": "YALIN", "rol": "Kıdemli", "kurulum": 2, "v_options": ["17:30-02:30"]},
    {"isim": "UĞUR", "rol": "Kıdemli", "kurulum": 1, "v_options": ["21:00-06:00"]},
    {"isim": "CÜNEYT", "rol": "Kıdemli", "kurulum": 1, "v_options": ["21:00-06:00"]},
    {"isim": "MÜGE", "rol": "Temsilci", "kurulum": 1, "v_options": ["00:00-08:30"]}
]

DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# Session State
if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"izinler": []} for p in staff_list}

st.sidebar.header("📝 Personel İzin Talepleri")
for p in staff_list:
    st.session_state.talep[p['isim']]['izinler'] = st.sidebar.multiselect(
        f"{p['isim']} ({p['rol']} | {p['kurulum']} Kurulum)", DAYS, key=p['isim']
    )

if st.button("🚀 Vardiyayı Dengele ve Raporla"):
    günlük_4_site_izin = {day: 0 for day in DAYS}
    rows = []
    
    # Hiyerarşi: Kıdemli > Temsilci > Eğitim
    role_prio = {"Kıdemli": 0, "Temsilci": 1, "Eğitim": 2}
    sorted_staff = sorted(staff_list, key=lambda x: role_prio[x['rol']])

    for p in sorted_staff:
        tercihler = st.session_state.talep[p['isim']]['izinler']
        is_4_site = p['kurulum'] == 4
        
        # İzin günü (4 kurulumlular için çakışma önleyici)
        secilen_izin = None
        for day in tercihler:
            if is_4_site and günlük_4_site_izin[day] > 0:
                continue
            secilen_izin = day
            break
        if is_4_site and secilen_izin: günlük_4_site_izin[secilen_izin] += 1
        
        # Tablo satırı oluştur
        p_row = {"Personel": p['isim'], "Rol": p['rol'], "Kurulum": p['kurulum']}
        for day in DAYS:
            p_row[day] = "OFF" if day == secilen_izin else p['v_options'][0]
        rows.append(p_row)

    df = pd.DataFrame(rows)
    st.table(df)
    
    st.subheader("📋 Google Sheets AppScript Kodu")
    script = f"function olusturVardiya() {{\n  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();\n  var data = {json.dumps([df.columns.tolist()] + df.values.tolist())};\n  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);\n}}"
    st.code(script, language="javascript")
