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

LISTA_KATEGORII = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- Funkcje Bazy Danych ---

def pobierz_produkty():
    """Pobiera wszystkie produkty z bazy Supabase."""
    try:
        # Pobieramy dane z tabeli 'Produkty'
        response = supabase.table("Produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd podczas pobierania danych: {e}")
        return []

def dodaj_produkt_db(nazwa, kategoria, ilosc, cena):
    """Dodaje produkt do tabeli 'Produkty'."""
    nowy_produkt = {
        "nazwa": nazwa,
        "Kategorie": kategoria,
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        supabase.table("Produkty").insert(nowy_produkt).execute()
        st.success(f"Dodano produkt: {nazwa}")
    except Exception as e:
        st.error(f"Błąd podczas dodawania: {e}")

def usun_produkt_db(produkt_id):
    """Usuwa produkt z bazy na podstawie ID."""
    try:
        supabase.table("Produkty").delete().eq("id", produkt_id).execute()
        st.success("Produkt został trwale usunięty z bazy.")
    except Exception as e:
        st.error(f"Błąd podczas usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 System Zarządzania Magazynem")

# --- SEKCJA 1: DODAWANIE ---
st.header("➕ Dodaj Nowy Produkt")
with st.form("form_dodawania", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        nazwa_input = st.text_input("Nazwa Produktu")
    with col2:
        kat_input = st.selectbox("Wybierz kategorię", LISTA_KATEGORII)
    with col3:
        ilosc_input = st.number_input("Ilość (szt.)", min_value=1, step=1)
    with col4:
        cena_input = st.number_input("Cena (PLN)", min_value=0.0, step=0.01, format="%.2f")

    submit = st.form_submit_button("Zapisz w bazie danych")
    
    if submit:
        if nazwa_input:
            dodaj_produkt_db(nazwa_input, kat_input, ilosc_input, cena_input)
            st.rerun() # Odświeżamy, aby zobaczyć nowy produkt na liście
        else:
            st.error("Pole 'Nazwa Produktu' nie może być puste!")

st.divider()

# --- SEKCJA 2: PODGLĄD I USUWANIE ---
st.header("📋 Podgląd i Zarządzanie Produktami")

produkty = pobierz_produkty()

if not produkty:
    st.info("Obecnie nie ma żadnych produktów w bazie.")
else:
    # Tworzymy nagłówki tabeli
    # Kolumny: Nazwa (3), Kategoria (2), Ilość (1), Cena (1), Akcja (1)
    h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([3, 2, 1, 1, 1])
    h_col1.write("**Nazwa**")
    h_col2.write("**Kategoria**")
    h_col3.write("**Ilość**")
    h_col4.write("**Cena (PLN)**")
    h_col5.write("**Akcja**")
    
    st.markdown("---")

    # Wyświetlamy każdy produkt w osobnym wierszu
    for p in produkty:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        
        c1.write(p.get('nazwa', 'Brak nazwy'))
        # Wyświetlamy kategorię w kolorowym boksie (info)
        c2.info(p.get('Kategorie', 'Brak'))
        c3.write(p.get('ilosc', 0))
        c4.write(f"{p.get('cena', 0.0):.2f}")
        
        # Przycisk usuwania - każdy musi mieć unikalny klucz (key)
        if c5.button("🗑️ Usuń", key=f"btn_del_{p['id']}"):
            usun_produkt_db(p['id'])
            st.rerun() # Odświeżamy widok po usunięciu
