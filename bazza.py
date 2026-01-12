import streamlit as st
from supabase import create_client, Client

# --- KONFIGURACJA POŁĄCZENIA ---
URL = "https://dvdtqcprpjhyltqracgl.supabase.co"
KEY = "sb_publishable_dcihPUrxU25U6s3V_1NSwA_Y0_1dXwO"

@st.cache_resource
def init_connection():
    """Inicjalizacja połączenia z Supabase."""
    return create_client(URL, KEY)

supabase = init_connection()

# --- Konfiguracja Strony ---
st.set_page_config(page_title="Magazyn Supabase", layout="wide")

# Lista kategorii (możesz ją też pobierać z bazy, jeśli tabela 'kategorie' ma dane)
LISTA_KATEGORII = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- FUNKCJE BAZY DANYCH ---

def pobierz_produkty():
    """Pobiera wszystkie rekordy z tabeli 'produkty'."""
    try:
        response = supabase.table("produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd pobierania danych: {e}")
        return []

def dodaj_produkt_db(nazwa, kategoria, ilosc, cena):
    """Wstawia nowy produkt do tabeli 'produkty'."""
    nowy_produkt = {
        "nazwa": nazwa,
        "kategorie": kategoria,  # Używamy małej litery zgodnie z Twoją bazą
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        supabase.table("produkty").insert(nowy_produkt).execute()
        st.success(f"Pomyślnie dodano: {nazwa}")
    except Exception as e:
        st.error(f"Błąd zapisu w bazie: {e}")

def usun_produkt_db(id_produktu):
    """Usuwa produkt na podstawie ID."""
    try:
        supabase.table("produkty").delete().eq("id", id_produktu).execute()
        st.success("Produkt został usunięty.")
    except Exception as e:
        st.error(f"Błąd podczas usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 System Zarządzania Magazynem")

# --- SEKCJA DODAWANIA ---
st.header("➕ Dodaj Nowy Produkt")
with st.form("form_dodawania", clear_on_submit=True):
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
    
    if
