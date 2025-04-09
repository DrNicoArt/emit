# Aplikacja Czasowa

Interaktywna wizualizacja różnych systemów czasowych przedstawionych jako koncentryczne okręgi.

## Opis Projektu

Aplikacja Czasowa to narzędzie do wizualizacji różnych systemów mierzenia czasu w jednym spójnym interfejsie. Poszczególne systemy czasowe są przedstawione jako koncentryczne okręgi, co pozwala na jednoczesne porównanie i obserwację różnych sposobów postrzegania i mierzenia czasu przez ludzkość.

### Systemy czasowe

Aplikacja zawiera następujące systemy czasowe:

1. **Czas Lokalny** - klasyczny zegar analogowy pokazujący aktualny czas lokalny
2. **Kalendarz Hebrajski** - tradycyjny kalendarz hebrajski z miesiącami i dniami
3. **Czas Atomowy** - precyzyjny czas pobrany z serwerów NTP
4. **Czas Pulsarowy** - symulacja pulsarów jako naturalnych zegarów kosmicznych
5. **Obrót Ziemi** - wizualizacja obrotu Ziemi z podziałem na dzień i noc
6. **Rok Astronomiczny** - ruch Ziemi wokół Słońca z oznaczeniami pór roku i znaków zodiaku

## Instalacja i uruchomienie

### Wymagania systemowe

- Python 3.8 lub nowszy
- PyQt5
- Dodatkowe biblioteki: numpy, pytz, ntplib

### Instrukcja instalacji

1. Rozpakuj archiwum do wybranego katalogu
2. Otwórz terminal/konsolę i przejdź do rozpakowanego katalogu
3. Zainstaluj wymagane zależności:

```bash
pip install PyQt5 numpy pytz ntplib
```

4. Uruchom aplikację:

```bash
python main.py
```

## Używanie aplikacji

Po uruchomieniu aplikacji zobaczysz główne okno z wizualizacją systemów czasowych jako koncentryczne okręgi. Możesz:

- Przesuwać i powiększać widok za pomocą myszki
- Klikać na poszczególne elementy, aby uzyskać więcej informacji
- Konfigurować różne opcje wyświetlania przez menu i pasek narzędzi
- Zmieniać strefy czasowe i inne ustawienia

## Struktura kodu

Kod projektu jest zorganizowany w następujący sposób:

- `main.py` - główny plik uruchamiający aplikację
- `ui_mainwindow.py` - definicja głównego okna aplikacji
- `style.qss` - arkusz stylów dla interfejsu użytkownika
- `systemy_czasowe/` - katalog z modułami różnych systemów czasowych
- `widgets/` - katalog z niestandardowymi widgetami i komponentami
- `resources/` - katalog z zasobami (ikony, obrazy, itp.)
