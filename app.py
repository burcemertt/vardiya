import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Vardiya Planlayıcı")
st.title("🛡️ Personel Vardiya ve İzin Planlayıcı")

# Vardiya Grupları ve Saatleri
VARDİYA_SAATLERİ = {
    "Sabah": "08:30-17:30",
    "Öğle": "12:00-21:00",
    "Akşam": "17:30-02:30",
    "Gece-1": "19:00-04:00",
    "Gece-2": "21:00-06:00",
    "Sabah-Erken": "00:00-08:30"
}

# Personel Listesi (Eksiksiz)
staff_list = [
    {"isim": "POLAT", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Sabah", "Öğle"]},
    {"isim": "İLKER", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Sabah", "Akşam"]},
    {"isim": "KORAY", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Öğle", "Gece-1"]},
    {"isim": "MUSTAFA", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Akşam", "Gece-2"]},
    {"isim": "YALIN", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Akşam", "Sabah-Erken"]},
    {"isim": "UĞUR", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Gece-2", "Sabah"]},
    {"isim": "CÜNEYT", "rol": "Kıdemli", "kurulum": 4, "v_opts": ["Gece-2", "Öğle"]},
    {"isim": "METİN", "rol": "Temsilci", "kurulum": 4, "v_opts": ["Sabah", "Gece-1"]},
    {"isim": "EMRE", "rol": "Temsilci", "kurulum": 2, "v_opts": ["Sabah", "Öğle"]},
    {"isim": "SENA", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Sabah", "Akşam"]},
    {"isim": "ILGAZ", "rol": "Temsilci", "kurulum": 4, "v_opts": ["Akşam", "Gece-2"]},
    {"isim": "OSMAN", "rol": "Temsilci", "kurulum": 3, "v_opts": ["Akşam", "Sabah-Erken"]},
    {"isim": "YASİN", "rol": "Temsilci", "kurulum": 3, "v_opts": ["Akşam", "Gece-1"]},
    {"isim": "CANER", "rol": "Temsilci", "kurulum": 2, "v_opts": ["Akşam", "Sabah"]},
    {"isim": "BURÇAK", "rol": "Temsilci", "kurulum": 2, "v_opts": ["Akşam", "Öğle"]},
    {"isim": "İBRAHİM", "rol": "Temsilci", "kurulum": 2, "v_opts": ["Gece-1", "Sabah-Erken"]},
    {"isim": "MÜGE", "rol": "Temsilci", "kurulum": 4, "v_opts": ["Sabah-Erken", "Gece-1"]},
    {"isim": "YALÇIN", "rol": "Temsilci", "kurulum": 4, "v_opts": ["Sabah-Erken", "Gece-2"]},
    {"isim": "MEHMET", "rol": "Temsilci", "kurulum": 4, "v_opts": ["Sabah-Erken", "Öğle"]},
    {"isim": "ARİF", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Sabah-Erken", "Sabah"]},
    {"isim": "ENİS", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Sabah-Erken", "Akşam"]},
    {"isim": "BARIŞ", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Sabah-Erken", "Gece-1"]},
    {"isim": "TOYGAR", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Gece-1", "Sabah"]},
    {"isim": "SELİN", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Gece-1", "Öğle"]},
    {"isim": "HAKAN", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Gece-1", "Akşam"]},
    {"isim": "EYLEM", "rol": "Temsilci", "kurulum": 1, "v_opts": ["Gece-1", "Gece-2"]},
    {"isim": "SEYFİ", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah", "Öğle"]},
    {"isim": "DEMET", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah", "Akşam"]},
    {"isim": "SEYİT", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah", "Gece-1"]},
    {"isim": "BERK", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah", "Gece-2"]},
    {"isim": "TAHİR", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah", "Sabah-Erken"]},
    {"isim": "RECEP", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah", "Öğle"]},
    {"isim": "TANJU", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Öğle", "Akşam"]},
    {"isim": "OLCAY", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Akşam", "Gece-1"]},
    {"isim": "ÖZCAN", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Akşam", "Gece-2"]},
    {"isim": "EDİZ", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Akşam", "Sabah-Erken"]},
    {"isim": "KEVSER", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Akşam", "Sabah"]},
    {"isim": "HARUN", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Akşam", "Öğle"]},
    {"isim": "KAZIM", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Akşam", "Gece-1"]},
    {"isim": "KUBİLAY", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah-Erken", "Sabah"]},
    {"isim": "KİRAZ", "rol": "Eğitim", "kurulum": 1, "v_opts": ["Sabah-Erken", "Öğle"]}
]

DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

if "talep" not in st.session_state:
    st.session_state.talep = {p['isim']: {"izinler": [], "secim": p['v_opts']} for p in staff_list}

st.sidebar.header("📝 Personel Tercihleri")
for p in staff_list:
    with st.sidebar.expander(f"{p['isim']} ({p['kurulum']} Kurulum)"):
        v1 = st.selectbox("1. Vardiya", p['v_opts'], key=f"{p['isim']}_v1")
        v2 = st.selectbox("2. Vardiya", p['v_opts'], key=f"{p['isim']
