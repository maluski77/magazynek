import streamlit as st
from supabase import create_client, Client
import uuid

# --- KONFIGURACJA POŁĄCZENIA ---
URL = "https://dvdtqcprpjhyltqracgl.supabase.co"
KEY = "sb_publishable_dcihPUrxU25U6s3V_1NSwA_Y0_1dXwO"

@st.cache_resource
def init_connection():
    """Inicjalizuje połączenie z bazą danych."""
    return create_client(URL, KEY)

supabase = init_connection()

# --- Konfiguracja Strony ---
st.set_page_config(page_title="Magazyn Supabase", layout="wide")

# Definiujemy dostępne kategorie
KATEGORIE = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- Funkcje Bazy Danych ---

def pobierz_towary():
    """Pobiera dane z tabeli 'towary'."""
    try:
        response = supabase.table("towary").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Nie udało się pobrać danych: {e}")
        return []

def dodaj_towar_db(nazwa, kategoria, ilosc, cena):
    """Wstawia nowy wiersz do tabeli 'towary'."""
    nowy_towar = {
        "nazwa": nazwa,
        "kategoria": kategoria,
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        supabase.table("towary").insert(nowy_towar).execute()
        st.success(f"Dodano towar: {nazwa}")
    except Exception as e:
        st.error(f"Błąd podczas dodawania: {e}")

def usun_towar_db(towar_id):
    """Usuwa wiersz na podstawie ID."""
    try:
        supabase.table("towary").delete().eq("id", towar_id).execute()
        st.success("Towar usunięty.")
    except Exception as e:
        st.error(f"Błąd podczas usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 Magazyn połączony z Supabase")

# Sekcja Dodawania Towaru
st.header("➕ Dodaj Nowy Towar")

with st.form("form_dodawania", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        nazwa = st.text_input("Nazwa Towaru") # Tutaj definiujemy 'nazwa'
    with col2:
        kategoria = st.selectbox("Kategoria", KATEGORIE)
    with col3:
        ilosc = st.number_input("Ilość (szt.)", min_value=1, step=1)
    with col4:
        cena = st.number_input("Cena (PLN)", min_value=0.0, step=0.01, format="%.2f")

    submit = st.form_submit_button("Dodaj do bazy")
    
    if submit:
        if nazwa: # Teraz 'nazwa' jest już znana w tym bloku
            dodaj_towar_db(nazwa, kategoria, ilosc, cena)
            st.rerun()
        else:
            st.error("Musisz podać nazwę towaru!")

# --- Wyświetlanie Listy ---
st.header("📋 Aktualny Stan Magazynu")
dane = pobierz_towary()

if not dane:
    st.info("Baza danych jest pusta lub brak połączenia.")
else:
    cols_h = st.columns([3, 2, 1, 1, 1])
    headers = ["Nazwa", "Kategoria", "Ilość", "Cena", "Akcja"]
    for col, h in zip(cols_h, headers):
        col.subheader(h)

    for towar in dane:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        c1.write(towar['nazwa'])
        c2.info(towar['kategoria'])
        c3.write(towar['ilosc'])
        c4.write(f"{towar['cena']:.2f}")
        
        # Ważne: używamy ID z bazy danych do usuwania
        if c5.button("Usuń", key=f"btn_{towar['id']}"):
            usun_towar_db(towar['id'])
            st.rerun()
