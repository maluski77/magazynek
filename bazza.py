import streamlit as st
from supabase import create_client, Client
import uuid

# --- KONFIGURACJA POŁĄCZENIA ---
URL = "https://dvdtqcprpjhyltqracgl.supabase.co"
KEY = "sb_publishable_..." # Tutaj wstaw swój klucz

@st.cache_resource
def init_connection():
    # Inicjalizacja klienta Supabase
    return create_client(URL, KEY)

supabase = init_connection()

# --- Funkcje do Zarządzania Towarami (SUPABASE) ---

def pobierz_towary():
    """Pobiera wszystkie wiersze z tabeli 'towary'."""
    response = supabase.table("towary").select("*").execute()
    return response.data

def dodaj_towar_db(nazwa, kategoria, ilosc, cena):
    """Wysyła dane do tabeli w Supabase."""
    nowy_towar = {
        "nazwa": nazwa,
        "kategoria": kategoria,
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    # Supabase automatycznie wygeneruje ID (jeśli tak ustawisz w bazie)
    try:
        supabase.table("towary").insert(nowy_towar).execute()
        st.success(f"Dodano do bazy: {nazwa}")
    except Exception as e:
        st.error(f"Błąd bazy danych: {e}")

def usun_towar_db(towar_id):
    """Usuwa wiersz z bazy danych."""
    try:
        supabase.table("towary").delete().eq("id", towar_id).execute()
        st.success("Usunięto z bazy.")
    except Exception as e:
        st.error(f"Błąd usuwania: {e}")

# --- INTERFEJS ---
st.title("🛒 Magazyn połączony z Supabase")

# Sekcja Dodawania
with st.form("dodaj_form"):
    # ... (twoje pola input: nazwa, kategoria, ilosc, cena)
    submit = st.form_submit_button("Dodaj do bazy")
    if submit and nazwa:
        dodaj_towar_db(nazwa, kategoria, ilosc, cena)
        st.rerun()

# Wyświetlanie danych z bazy
st.header("📋 Dane prosto z bazy")
dane = pobierz_towary()

if not dane:
    st.info("Baza danych jest pusta.")
else:
    for towar in dane:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
        col1.write(towar['nazwa'])
        col2.write(towar['kategoria'])
        col3.write(towar['ilosc'])
        col4.write(towar['cena'])
        if col5.button("Usuń", key=str(towar['id'])):
            usun_towar_db(towar['id'])
            st.rerun()
