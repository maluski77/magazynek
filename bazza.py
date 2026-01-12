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

KATEGORIE = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- Funkcje Bazy Danych (zmienione na 'produkty') ---

def pobierz_produkty():
    try:
        # Zmiana z 'towary' na 'produkty'
        response = supabase.table("produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd pobierania: {e}")
        return []

def dodaj_produkt_db(nazwa, kategoria, ilosc, cena):
    nowy_produkt = {
        "nazwa": nazwa,
        "kategoria": kategoria,
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        # Zmiana z 'towary' na 'produkty'
        supabase.table("produkty").insert(nowy_produkt).execute()
        st.success(f"Dodano produkt: {nazwa}")
    except Exception as e:
        st.error(f"Błąd dodawania: {e}")

def usun_produkt_db(produkt_id):
    try:
        # Zmiana z 'towary' na 'produkty'
        supabase.table("produkty").delete().eq("id", produkt_id).execute()
        st.success("Produkt usunięty.")
    except Exception as e:
        st.error(f"Błąd usuwania: {e}")

# --- INTERFEJS ---
st.title("🛒 Magazyn Produkty (Supabase)")

st.header("➕ Dodaj Nowy Produkt")
with st.form("form_dodawania", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        nazwa_input = st.text_input("Nazwa Produktu")
    with col2:
        kat_input = st.selectbox("Kategoria", KATEGORIE)
    with col3:
        ilosc_input = st.number_input("Ilość (szt.)", min_value=1, step=1)
    with col4:
        cena_input = st.number_input("Cena (PLN)", min_value=0.0, step=0.01, format="%.2f")

    submit = st.form_submit_button("Dodaj do bazy")
    
    if submit:
        if nazwa_input:
            dodaj_produkt_db(nazwa_input, kat_input, ilosc_input, cena_input)
            st.rerun()
        else:
            st.error("Podaj nazwę produktu!")

# --- Wyświetlanie Listy ---
st.header("📋 Stan Magazynu")
dane = pobierz_produkty()

if not dane:
    st.info("Baza 'produkty' jest pusta lub nie istnieje.")
else:
    cols_h = st.columns([3, 2, 1, 1, 1])
    for col, h in zip(cols_h, ["Nazwa", "Kategoria", "Ilość", "Cena", "Akcja"]):
        col.subheader(h)

    for prod in dane:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        c1.write(prod['nazwa'])
        c2.info(prod['kategoria'])
        c3.write(prod['ilosc'])
        c4.write(f"{prod['cena']:.2f}")
        
        if c5.button("Usuń", key=f"del_{prod['id']}"):
            usun_produkt_db(prod['id'])
            st.rerun()
