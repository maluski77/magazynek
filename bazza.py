import streamlit as st
import uuid  # Użyjemy uuid do generowania unikalnych ID dla towarów

# --- Konfiguracja i Inicjalizacja Stanu Sesji ---

# Ustawienie tytułu strony
st.set_page_config(page_title="Prosty Magazyn Towarów", layout="wide")

# Inicjalizacja listy towarów w stanie sesji, jeśli jeszcze nie istnieje.
# W Streamlit stan sesji (st.session_state) utrzymuje dane między interakcjami.
if 'towary' not in st.session_state:
    st.session_state.towary = []


# --- Funkcje do Zarządzania Towarami ---

def dodaj_towar(nazwa, ilosc, cena):
    """Dodaje nowy towar do listy."""
    try:
        ilosc_int = int(ilosc)
        cena_float = float(cena)
        
        # Walidacja, czy wartości są poprawne
        if ilosc_int <= 0 or cena_float <= 0:
            st.error("Ilość i cena muszą być wartościami dodatnimi.")
            return

        nowy_towar = {
            'id': str(uuid.uuid4()),  # Unikalne ID
            'nazwa': nazwa,
            'ilosc': ilosc_int,
            'cena': cena_float
        }
        st.session_state.towary.append(nowy_towar)
        st.success(f"Dodano towar: **{nazwa}**")
    except ValueError:
        st.error("Ilość musi być liczbą całkowitą, a cena musi być liczbą (np. 12.99).")

def usun_towar(towar_id):
    """Usuwa towar z listy na podstawie jego ID."""
    # Filtrujemy listę, zachowując tylko te towary, których ID nie pasuje
    st.session_state.towary = [
        towar for towar in st.session_state.towary 
        if towar['id'] != towar_id
    ]
    st.success("Towar usunięty pomyślnie.")


# --- Interfejs Użytkownika Streamlit ---

st.title("🛒 Prosty Magazyn Towarów (Streamlit Session State)")

st.warning("Pamiętaj: Towary są przechowywane **tylko w pamięci** przeglądarki podczas bieżącej sesji. Po odświeżeniu strony lista zostanie wyczyszczona.")

# Sekcja Dodawania Towaru
st.header("➕ Dodaj Nowy Towar")

with st.form("form_dodawania_towaru", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nazwa = st.text_input("Nazwa Towaru", key="input_nazwa")
    with col2:
        ilosc = st.text_input("Ilość (szt.)", key="input_ilosc")
    with col3:
        cena = st.text_input("Cena Jednostkowa (PLN)", key="input_cena")

    przycisk_dodaj = st.form_submit_button("Zatwierdź Dodanie Towaru")
    
    if przycisk_dodaj:
        if nazwa and ilosc and cena:
            dodaj_towar(nazwa, ilosc, cena)
        else:
            st.error("Wszystkie pola muszą być wypełnione.")

# --- Wyświetlanie Listy Towarów ---

st.header("📋 Aktualny Stan Magazynu")

if not st.session_state.towary:
    st.info("Magazyn jest pusty. Dodaj pierwszy towar powyżej!")
else:
    # Tworzenie kolumn dla wyświetlania danych i przycisku usuwania
    # Rozmiary kolumn: Nazwa (3), Ilość (1), Cena (2), Przycisk (1)
    cols_display = st.columns([3, 1, 2, 1])
    
    # Nagłówki
    cols_display[0].subheader("Nazwa")
    cols_display[1].subheader("Ilość")
    cols_display[2].subheader("Cena (PLN)")
    cols_display[3].subheader("Akcja")
    st.markdown("---") # Linia rozdzielająca nagłówki od listy

    # Pętla przez listę towarów i wyświetlanie ich
    for i, towar in enumerate(st.session_state.towary):
        # Tworzenie wiersza z kolumnami dla każdego towaru
        row_cols = st.columns([3, 1, 2, 1])
        
        # Wyświetlanie danych
        row_cols[0].write(towar['nazwa'])
        row_cols[1].write(towar['ilosc'])
        # Formatowanie ceny do dwóch miejsc po przecinku
        row_cols[2].write(f"{towar['cena']:.2f}")
        
        # Przycisk Usuń. Używamy unikalnego klucza (key) dla każdego przycisku
        if row_cols[3].button("Usuń", key=f"usun_{towar['id']}", help="Usuń ten towar z listy"):
            # Wywołanie funkcji usuwającej i automatyczne odświeżenie (Rerunning) Streamlit
            usun_towar(towar['id'])
            st.rerun() # Używamy st.rerun() by odświeżyć interfejs po usunięciu
