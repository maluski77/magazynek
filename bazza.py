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

# --- FUNKCJE BAZY DANYCH ---

def pobierz_kategorie_z_bazy():
    """
    Pobiera aktualne kategorie z tabeli 'kategorie' w Supabase.
    Zwraca słownik: {"Nazwa kategorii": ID_kategorii}
    """
    try:
        # Zakładam, że w tabeli 'kategorie' masz kolumny 'id' oraz 'nazwa'.
        # Jeśli kolumna nazywa się inaczej (np. 'name'), zmień 'nazwa' poniżej.
        response = supabase.table("kategorie").select("id, nazwa").execute()
        dane = response.data
        
        if not dane:
            return {}
            
        # Tworzymy mapę: Klucz to nazwa, Wartość to ID
        # np. {'Elektronika': 1, 'Żywność': 2}
        return {item['nazwa']: item['id'] for item in dane}
        
    except Exception as e:
        st.error(f"Błąd pobierania kategorii: {e}")
        st.info("Upewnij się, że tabela 'kategorie' istnieje i ma kolumnę 'nazwa'.")
        return {}

def pobierz_produkty():
    try:
        response = supabase.table("produkty").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd pobierania produktów: {e}")
        return []

def dodaj_produkt_db(nazwa, id_kategorii, ilosc, cena):
    nowy_produkt = {
        "nazwa": nazwa,
        "kategorie": id_kategorii, # Tutaj wysyłamy poprawne ID pobrane z bazy
        "ilosc": int(ilosc),
        "cena": float(cena)
    }
    try:
        supabase.table("produkty").insert(nowy_produkt).execute()
        st.success(f"Pomyślnie dodano: {nazwa}")
        st.rerun()
    except Exception as e:
        st.error(f"Błąd zapisu w bazie: {e}")
        st.warning("Jeśli widzisz błąd 'violates foreign key constraint', oznacza to, że wybrane ID kategorii nie istnieje w tabeli 'kategorie'.")

def usun_produkt_db(id_produktu):
    try:
        supabase.table("produkty").delete().eq("id", id_produktu).execute()
        st.rerun()
    except Exception as e:
        st.error(f"Błąd podczas usuwania: {e}")

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🛒 System Zarządzania Magazynem")

# POBIERAMY KATEGORIE Z BAZY (DYNAMICZNIE)
mapa_kategorii = pobierz_kategorie_z_bazy()

# --- SEKCJA DODAWANIA ---
st.header("➕ Dodaj Nowy Produkt")

if not mapa_kategorii:
    st.error("⚠️ Tabela 'kategorie' w Supabase jest pusta lub nie można jej pobrać!")
    st.info("Wejdź do Supabase -> Table Editor -> tabela 'kategorie' i dodaj wiersze (np. id:1, nazwa:Elektronika).")
else:
    with st.form("form_dodawania"):
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        with col1:
            nazwa_input = st.text_input("Nazwa Produktu")
        with col2:
            # Dropdown wyświetla nazwy, ale my potrzebujemy ID
            wybrana_nazwa_kat = st.selectbox("Kategoria", list(mapa_kategorii.keys()))
        with col3:
            ilosc_input = st.number_input("Ilość (szt.)", min_value=1, step=1)
        with col4:
            cena_input = st.number_input("Cena (PLN)", min_value=0.0, step=0.01, format="%.2f")

        submit = st.form_submit_button("Zapisz w bazie danych")
        
        if submit:
            if nazwa_input:
                # Pobieramy ID na podstawie wybranej nazwy
                id_do_zapisu = mapa_kategorii[wybrana_nazwa_kat]
                dodaj_produkt_db(nazwa_input, id_do_zapisu, ilosc_input, cena_input)
            else:
                st.error("Nazwa produktu jest wymagana!")

st.divider()

# --- SEKCJA PODGLĄDU I USUWANIA ---
st.header("📋 Podgląd i Zarządzanie Produktami")

produkty = pobierz_produkty()

if not produkty:
    st.info("Baza danych produktów jest pusta.")
else:
    # Nagłówki tabeli
    c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
    c1.write("**Nazwa**")
    c2.write("**Kategoria (ID)**")
    c3.write("**Ilość**")
    c4.write("**Cena**")
    c5.write("**Akcja**")
    
    st.markdown("---")

    for p in produkty:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        
        # Nazwa
        c1.write(p.get('nazwa', '---'))
        
        # Kategoria
        kat_val = p.get('kategorie')
        c2.info(f"ID: {kat_val}" if kat_val is not None else "Brak")
        
        # Ilość
        il_val = p.get('ilosc')
        c3.write(il_val if il_val is not None else 0)
        
        # Cena (bezpieczne wyświetlanie)
        cena_raw = p.get('cena')
        if cena_raw is not None:
            c4.write(f"{float(cena_raw):.2f}")
        else:
            c4.write("0.00")
        
        # Przycisk usuwania
        p_id = p.get('id')
        if p_id is not None:
            if c5.button("🗑️ Usuń", key=f"del_{p_id}"):
                usun_produkt_db(p_id)
