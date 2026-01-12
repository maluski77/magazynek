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
st.set_page_config(page_title="Magazyn Supabase", layout="wide")

LISTA_KATEGORII = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- FUNKCJE BAZY DANYCH ---

def pobierz_produkty():
    try:
        # Zmieniono na małe litery 'produkty'
        response = supabase.table("produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd pobierania danych: {e}")
        return []

def dodaj_produkt_db(nazwa, kategoria, ilosc, cena):
    # Upewnij się, że klucze poniżej są identyczne jak nazwy kolumn w Supabase!
    nowy_produkt = {
        "nazwa": nazwa,
        "kategorie": kategoria, # Używamy małej litery 'kategorie'
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        response = supabase.table("produkty").insert(nowy_produkt).execute()
        if response:
            st.success(f"Pomyślnie dodano: {nazwa}")
            st.rerun()
    except Exception as e:
        # Wyświetlamy błąd i NIE robimy rerun, żebyś mógł go zobaczyć
        st.error(f"Błąd zapisu w bazie: {e}")
        st.info("Sprawdź, czy nazwy kolumn w Supabase to: nazwa, kategorie, ilosc, cena")

def usun_produkt_db(id_produktu):
    try:
        supabase.table("produkty").delete().eq("id", id_produktu).execute()
        st.success("Produkt został usunięty.")
        st.rerun()
    except Exception as e:
        st.error(f"Błąd podczas usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 System Zarządzania Magazynem")

# --- SEKCJA DODAWANIA ---
st.header("➕ Dodaj Nowy Produkt")
with st.form("form_dodawania", clear_on_submit=False): # Zmieniono na False, by dane nie znikały przy błędzie
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
    
    if submit:
        if nazwa_input:
            dodaj_produkt_db(nazwa_input, kat_input, ilosc_input, cena_input)
        else:
            st.error("Nazwa produktu jest wymagana!")

st.divider()

# --- SEKCJA PODGLĄDU I USUWANIA ---
st.header("📋 Podgląd i Zarządzanie Produktami")

produkty = pobierz_produkty()

if not produkty:
    st.info("Baza danych jest pusta.")
else:
    c_h = st.columns([3, 2, 1, 1, 1])
    c_h[0].write("**Nazwa**")
    c_h[1].write("**Kategoria**")
    c_h[2].write("**Ilość**")
    c_h[3].write("**Cena**")
    c_h[4].write("**Akcja**")
    
    st.markdown("---")

    for p in produkty:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        
        c1.write(p.get('nazwa', '---'))
        # Próba pobrania pod kluczem 'kategorie' (małe litery)
        kat = p.get('kategorie', 'Brak')
        c2.info(kat)
        c3.write(p.get('ilosc', 0))
        c4.write(f"{p.get('cena', 0.0):.2f}")
        
        if c5.button("🗑️ Usuń", key=f"del_{p['id']}"):
            usun_produkt_db(p['id'])
