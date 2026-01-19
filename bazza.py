import streamlit as st
from supabase import create_client, Client

# --- KONFIGURACJA POŁĄCZENIA ---
URL = "https://dvdtqcprpjhyltqracgl.supabase.co"
KEY = "sb_publishable_dcihPUrxU25U6s3V_1NSwA_Y0_1dXwO"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Magazyn Supabase", layout="wide")

# Mapowanie tekstu na ID dla bazy danych (aby uniknąć błędu bigint)
MAPA_KATEGORII = {
    "Elektronika": 1,
    "Żywność": 2,
    "Dom i Ogród": 3,
    "Odzież": 4,
    "Inne": 5
}
LISTA_KATEGORII = list(MAPA_KATEGORII.keys())

# --- FUNKCJE BAZY DANYCH ---

def pobierz_produkty():
    try:
        response = supabase.table("produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd pobierania danych: {e}")
        return []

def dodaj_produkt_db(nazwa, kategoria_tekst, ilosc, cena):
    id_kategorii = MAPA_KATEGORII.get(kategoria_tekst, 5)
    nowy_produkt = {
        "nazwa": nazwa,
        "kategorie": id_kategorii,
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        supabase.table("produkty").insert(nowy_produkt).execute()
        st.success(f"Pomyślnie dodano: {nazwa}")
        st.rerun()
    except Exception as e:
        st.error(f"Błąd zapisu w bazie: {e}")

def usun_produkt_db(id_produktu):
    try:
        supabase.table("produkty").delete().eq("id", id_produktu).execute()
        st.rerun()
    except Exception as e:
        st.error(f"Błąd podczas usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 System Zarządzania Magazynem")

# --- SEKCJA DODAWANIA ---
st.header("➕ Dodaj Nowy Produkt")
with st.form("form_dodawania"):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        nazwa_input = st.text_input("Nazwa Produktu")
    with col2:
        kat_input = st.selectbox("Kategoria", LISTA_KATEGORII)
    with col3:
        ilosc_input = st.number_input("Ilość (szt.)", min_value=1, step=1)
    with col4:
        cena_input = st.number_input("Cena (PLN)", min_value=0.0, step=0.01, format="%.2f")

    submit = st.form_submit_button("Zapisz w bazie danych")
    
    if submit and nazwa_input:
        dodaj_produkt_db(nazwa_input, kat_input, ilosc_input, cena_input)

st.divider()

# --- SEKCJA PODGLĄDU I USUWANIA ---
st.header("📋 Podgląd i Zarządzanie Produktami")

produkty = pobierz_produkty()

if not produkty:
    st.info("Baza danych jest pusta.")
else:
    c_h = st.columns([3, 2, 1, 1, 1])
    c_h[0].write("**Nazwa**")
    c_h[1].write("**Kategoria (ID)**")
    c_h[2].write("**Ilość**")
    c_h[3].write("**Cena**")
    c_h[4].write("**Akcja**")
    
    st.markdown("---")

    for p in produkty:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        
        # Nazwa
        c1.write(p.get('nazwa', '---'))
        
        # Kategoria
        kat_id = p.get('kategorie')
        c2.info(f"ID: {kat_id}" if kat_id is not None else "Brak")
        
        # Ilość
        il_val = p.get('ilosc')
        c3.write(il_val if il_val is not None else 0)
        
        # Cena (BEZPIECZNE FORMATOWANIE)
        cena_raw =
