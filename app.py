import streamlit as st
import pandas as pd
import random

# Sayfa Genişlik Ayarı
st.set_page_config(layout="wide", page_title="Akıllı Canlı Destek Vardiya Robotu")

st.title("📊 Akıllı Canlı Destek Vardiya Planlama Otomasyonu")
st.write("Personel tercihlerine, esnek çoklu izin taleplerine ve site yoğunluklarına göre optimize edilmiş şema.")

# Vardiyalar ve Saatleri
SHIFTS = {
    "Sabah (08:30-17:30)": "08:30-17:30",
    "12:00 Ara (12:00-21:00)": "12:00-21:00",
    "17:30 Ara (17:30-02:30)": "17:30-02:30",
    "19:00 Ara (19:00-04:00)": "19:00-04:00",
    "21:00 Ara (21:00-06:00)": "21:00-06:00",
    "Gece (00:00-08:30)": "00:00-08:30"
}
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# Sabit Personel Veritabanı
@st.cache_data
def get_initial_staff():
    return [
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

staff_list = get_initial_staff()

if "preferences" not in st.session_state:
    st.session_state.preferences = {p['isim']: {"off_options": [], "v1": "Talep Yok", "v2": "Talep Yok"} for p in staff_list}

# Yan Menü Tasarımı
st.sidebar.header("🔥 Haftalık Vardiya Yoğunluk Ayarları")
weights = {}
for shift in SHIFTS.keys():
    default_val = 4 if "17:30" in shift else 2
    weights[shift] = st.sidebar.slider(f"{shift} Ağırlığı", 1, 5, default_val)

tab1, tab2 = st.tabs(["📋 Haftalık Talep Girişi", "🚀 Vardiya Çizelgesini Üret"])

with tab1:
    st.subheader("Kişisel İzin (Çoklu Seçim) ve Vardiya Tercihleri Formu")
    for p in staff_list:
        name = p['isim']
        with st.expander(f"👤 {name} ({p['rol']})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.session_state.preferences[name]["off_options"] = st.multiselect(
                    f"{name} - Uygun İzin Günleri", DAYS, 
                    default=st.session_state.preferences[name]["off_options"], 
                    key=f"{name}_off"
                )
            with col2:
                st.session_state.preferences[name]["v1"] = st.selectbox(
                    f"{name} - Vardiya Tercihi 1", ["Talep Yok"] + list(SHIFTS.keys()), 
                    index=(["Talep Yok"] + list(SHIFTS.keys())).index(st.session_state.preferences[name]["v1"]),
                    key=f"{name}_v1"
                )
            with col3:
                st.session_state.preferences[name]["v2"] = st.selectbox(
                    f"{name} - Vardiya Tercihi 2", ["Talep Yok"] + list(SHIFTS.keys()), 
                    index=(["Talep Yok"] + list(SHIFTS.keys())).index(st.session_state.preferences[name]["v2"]),
                    key=f"{name}_v2"
                )

with tab2:
    st.subheader("Algoritmayı Çalıştır ve Excel Al")
    if st.button("🔮 Akıllı Algoritmayı Çalıştır ve Dağıtımı Yap"):
        with st.spinner("Hesaplanıyor..."):
            schedule = {day: {shift: [] for shift in SHIFTS.keys()} for day in DAYS}
            person_off_day = {}
            day_off_counts = {day: 0 for day in DAYS}
            current_prefs = st.session_state.preferences
            
            sorted_staff_by_flexibility = sorted(staff_list, key=lambda x: len(current_prefs[x['isim']]["off_options"]))
            
            for p in sorted_staff_by_flexibility:
                name = p['isim']
                options = current_prefs[name]["off_options"]
                if len(options) == 1:
                    chosen_day = options[0]
                    person_off_day[name] = chosen_day
                    day_off_counts[chosen_day] += 1
                elif len(options) > 1:
                    best_day = min(options, key=lambda d: day_off_counts[d])
                    person_off_day[name] = best_day
                    day_off_counts[best_day] += 1
            
            for p in staff_list:
                name = p['isim']
                if name not in person_off_day:
                    min_day = min(DAYS, key=lambda d: day_off_counts[d])
                    person_off_day[name] = min_day
                    day_off_counts[min_day] += 1
            
            for day in DAYS:
                active_staff = [p for p in staff_list if person_off_day[p['isim']] != day]
                shift_pool = []
                for shift, weight in weights.items():
                    shift_pool.extend([shift] * weight)
                while len(shift_pool) < len(active_staff):
                    shift_pool.extend(list(SHIFTS.keys()))
                
                random.shuffle(active_staff)
                active_staff.sort(key=lambda x: (x['avi'] + x['bon'] + x['as']), reverse=True)
                assigned_names = set()
                
                for shift in SHIFTS.keys():
                    for p in active_staff:
                        if p['isim'] in assigned_names:
                            continue
                        is_preferred = (current_prefs[p['isim']]["v1"] == shift or current_prefs[p['isim']]["v2"] == shift)
                        if is_preferred or (p['avi'] or p['bon'] or p['as']):
                            schedule[day][shift].append(p['isim'])
                            assigned_names.add(p['isim'])
                            break
                
                for p in active_staff:
                    if p['isim'] in assigned_names:
                        continue
                    v1 = current_prefs[p['isim']]["v1"]
                    v2 = current_prefs[p['isim']]["v2"]
                    chosen_shift = None
                    if v1 != "Talep Yok" and len(schedule[day][v1]) < (weights[v1] * 3):
                        chosen_shift = v1
                    elif v2 != "Talep Yok" and len(schedule[day][v2]) < (weights[v2] * 3):
                        chosen_shift = v2
                    else:
                        available_shifts = [s for s in shift_pool]
                        random.shuffle(available_shifts)
                        chosen_shift = available_shifts[0]
                    schedule[day][chosen_shift].append(p['isim'])
                    assigned_names.add(p['isim'])
            
            output_data = []
            for p in staff_list:
                row = {"Personel": p['isim'], "Rol": p['rol']}
                for day in DAYS:
                    if person_off_day[p['isim']] == day:
                        row[day] = "⚠️ OFF (İzinde)"
                    else:
                        assigned_shift = "Bulunamadı"
                        for shift in SHIFTS.keys():
                            if p['isim'] in schedule[day][shift]:
                                assigned_shift = shift.split(" ")[0] + f" ({SHIFTS[shift]})"
                                break
                        row[day] = assigned_shift
                output_data.append(row)
            
            df_result = pd.DataFrame(output_data)
            st.success("🎉 Vardiya tablosu başarıyla oluşturuldu!")
            st.dataframe(df_result, use_container_width=True)
            
            csv = df_result.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 Vardiya Tablosunu İndir", data=csv, file_name="haftalik_shift.csv", mime="text/csv")
            import streamlit as str

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .viewerBadge_container__1QS1h {display: none !important;} /* Streamlit logosunu uçurur */
        button[title="View source code"] {display: none !important;} /* GitHub kod butonunu gizler */
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
