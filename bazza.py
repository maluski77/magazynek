import streamlit as st
from supabase import create_client, Client

# --- KONFIGURACJA POŁĄCZENIA ---
URL = "https://dvdtqcprpjhyltqracgl.supabase.co"
KEY = "sb_publishable_dcihPUrxU25U6s3V_1NSwA_Y0_1dXwO"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

# --- Konfiguracja Strony ---
st.set_page_config(page_title="Magazyn Produkty", layout="wide")

# Lista opcji dla użytkownika
LISTA_KATEGORII = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- Funkcje Bazy Danych ---

def pobierz_produkty():
    try:
        # Zmieniono nazwę tabeli na 'Produkty' (zgodnie z Twoim screenem)
        response = supabase.table("Produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd pobierania danych: {e}")
        return []

def dodaj_produkt_db(nazwa, kategoria, ilosc, cena):
    nowy_produkt = {
        "nazwa": nazwa,
        "Kategorie": kategoria,  # Zmieniono klucz na 'Kategorie' (zgodnie z prośbą)
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        supabase.table("Produkty").insert(nowy_produkt).execute()
        st.success(f"Dodano produkt: {nazwa}")
    except Exception as e:
        st.error(f"Błąd dodawania do bazy: {e}")

def usun_produkt_db(produkt_id):
    try:
        supabase.table("Produkty").delete().eq("id", produkt_id).execute()
        st.success("Produkt usunięty.")
    except Exception as e:
        st.error(f"Błąd usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 Magazyn Produkty (Supabase)")

st.header("➕ Dodaj Nowy Produkt")
with st.form("form_dodawania", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        nazwa_input = st.text_input("Nazwa Produktu")
    with col2:
        # Wybór kategorii z listy
        kat_input = st.selectbox("Wybierz kategorię", LISTA_KATEGORII)
    with col3:
        ilosc_input = st.number_input("Ilość (szt.)", min_value=1, step=1)
    with col4:
        cena_input = st.number_input("Cena (PLN)", min_value=0.0, step=0.01, format="%.2f")

    submit = st.form_submit_button("Dodaj do bazy")
    
    if submit:
        if nazwa_input:
            dodaj_produkt_db(nazwa_input, kat_input, ilosc_input, cena_input)
            st.rerun()
