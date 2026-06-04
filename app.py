import streamlit as st
import pandas as pd
import json
import io
import requests

st.set_page_config(layout="wide", page_title="AI Vardiya Robotu")
st.title("🤖 AI Destekli Akıllı Vardiya Planlama")

openai_api_key = "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"

SHIFTS = {
    "Sabah (08:30-17:30)": "08:30-17:30",
    "12:00 Ara (12:00-21:00)": "12:00-21:00",
    "17:30 Ara (17:30-02:30)": "17:30-02:30",
    "19:00 Ara (19:00-04:00)": "19:00-04:00",
    "21:00 Ara (21:00-06:00)": "21:00-06:00",
    "Gece (00:00-08:30)": "00:00-08:30"
}
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

staff_list = [
    {"isim": "POLAT", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "İLKER", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "METİN", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "EMRE", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": False},
    {"isim": "SENA", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": False},
    {"isim": "SEYFİ", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "DEMET", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "SEYİT", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "BERK", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "TAHİR", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "RECEP", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "TANJU", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "KORAY", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "MUSTAFA", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "YALIN", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "ILGAZ", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "OSMAN", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": False},
    {"isim": "YASİN", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": False},
    {"isim": "CANER", "rol": "Temsilci", "teos": True, "as": True, "bon": False, "avi": False},
    {"isim": "SAMET", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "BİRKAN", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "OLCAY", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "ÖZCAN", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "KEVSER", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "HARUN", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "KAZIM", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "BURÇAK", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": False},
    {"isim": "İBRAHİM", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": False},
    {"isim": "TOYGAR", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "SELİN", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "HAKAN", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "EYLEM", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "UĞUR", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "CÜNEYT", "rol": "Kıdemli", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "MÜGE", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "YALÇIN", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "MEHMET", "rol": "Temsilci", "teos": True, "as": True, "bon": True, "avi": True},
    {"isim": "ARİF", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "ENİS", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "BARIŞ", "rol": "Temsilci", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "KUBİLAY", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False},
    {"isim": "KİRAZ", "rol": "Eğitim", "teos": True, "as": False, "bon": False, "avi": False}
]

if "preferences" not in st.session_state:
    st.session_state.preferences = {p['isim']: {"off_options": [], "v1": "Talep Yok", "v2": "Talep Yok"} for p in staff_list}

if st.button("🔮 Göktuğ ile Vardiya Üret"):
    with st.spinner("AI analiz ediyor..."):
        prompt = f"Personel listesi: {json.dumps(staff_list)}. Kurallar: Her vardiyada 1 kıdemli olsun, izinler adil dağılsın. Çıktı SADECE JSON formatında olmalı."
        headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "temperature": 0.2}
        
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            response_data = response.json()
            
            if "choices" in response_data:
                ai_content = response_data['choices'][0]['message']['content']
                clean_content = ai_content.replace("```json", "").replace("```", "").strip()
                df_result = pd.DataFrame(json.loads(clean_content))
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_result.to_excel(writer, index=False)
                
                st.success("✅ Vardiya planı başarıyla oluşturuldu!")
                st.download_button("📥 Excel Olarak İndir", buffer.getvalue(), "haftalik_shift.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.error(f"OpenAI API Hatası: {response_data}")
        except Exception as e:
            st.error(f"Sistem Hatası: {str(e)}")
