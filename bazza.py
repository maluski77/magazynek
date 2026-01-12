import streamlit as st
import uuid

# --- Konfiguracja i Inicjalizacja Stanu Sesji ---

st.set_page_config(page_title="Prosty Magazyn Towarów", layout="wide")

if 'towary' not in st.session_state:
    st.session_state.towary = []

# Definiujemy dostępne kategorie
KATEGORIE = ["Elektronika", "Żywność", "Dom i Ogród", "Odzież", "Inne"]

# --- Funkcje do Zarządzania Towarami ---

def dodaj_towar(nazwa, kategoria, ilosc, cena):
    """Dodaje nowy towar do listy z uwzględnieniem kategorii."""
    try:
        ilosc_int = int(ilosc)
        cena_float = float(cena)
        
        if ilosc_int <= 0 or cena_float <= 0:
            st.error("Ilość i cena muszą być wartościami dodatnimi.")
            return

        nowy_towar = {
            'id': str(uuid.uuid4()),
            'nazwa': nazwa,
            'kategoria': kategoria, # Nowe pole
            'ilosc': ilosc_int,
            'cena': cena_float
        }
        st.session_state.towary.append(nowy_towar)
        st.success(f"Dodano towar: **{nazwa}** do kategorii **{kategoria}**")
    except ValueError:
        st.error("Błędny format danych numerycznych.")

def usun_towar(towar_id):
    st.session_state.towary = [t for t in st.session_state.towary if t['id'] != towar_id]
    st.success("Towar usunięty.")

# --- Interfejs Użytkownika Streamlit ---

st.title("🛒 Magazyn z Kategoriami")

# Sekcja Dodawania Towaru
st.header("➕ Dodaj Nowy Towar")

with st.form("form_dodawania_towaru", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        nazwa = st.text_input("Nazwa Towaru")
    with col2:
        # Używamy selectbox dla wyboru kategorii
        kategoria = st.selectbox("Wybierz Kategorię", KATEGORIE)
    with col3:
        ilosc = st.number_input("Ilość (szt.)", min_value=1, step=1)
    with col4:
        cena = st.number_input("Cena Jednostkowa (PLN)", min_value=0.0, step=0.01, format="%.2f")

    submit = st.form_submit_button("Zatwierdź Dodanie Towaru")
    
    if submit:
        if nazwa:
            dodaj_towar(nazwa, kategoria, ilosc, cena)
        else:
            st.error("Nazwa towaru jest wymagana.")

# --- Wyświetlanie Listy Towarów ---

st.header("📋 Aktualny Stan Magazynu")

if not st.session_state.towary:
    st.info("Magazyn jest pusty.")
else:
    # Dodajemy jedną kolumnę więcej na kategorię [Nazwa, Kategoria, Ilość, Cena, Akcja]
    cols_display = st.columns([3, 2, 1, 1.5, 1])
    
    headers = ["Nazwa", "Kategoria", "Ilość", "Cena (PLN)", "Akcja"]
    for col, header in zip(cols_display, headers):
        col.subheader(header)
    
    st.markdown("---")

    for towar in st.session_state.towary:
        row_cols = st.columns([3, 2, 1, 1.5, 1])
        
        row_cols[0].write(towar['nazwa'])
        row_cols[1].info(towar['kategoria']) # Wyróżnienie kategorii kolorem
        row_cols[2].write(towar['ilosc'])
        row_cols[3].write(f"{towar['cena']:.2f}")
        
        if row_cols[4].button("Usuń", key=f"del_{towar['id']}"):
            usun_towar(towar['id'])
            st.rerun()
