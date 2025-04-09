# Instrukcja kompilacji aplikacji czasowej do pliku .exe

Ten dokument zawiera instrukcje dotyczące kompilacji aplikacji czasowej do samodzielnego pliku wykonywalnego (.exe) na systemie Windows.

## Wymagania wstępne

Przed rozpoczęciem kompilacji, upewnij się, że masz zainstalowane:

1. Python 3.8 lub nowszy
2. Biblioteki wymagane przez aplikację:
   - PyQt5
   - ntplib
   - pytz
   - (wszystkie inne zależności aplikacji)
3. PyInstaller - narzędzie do kompilacji (możesz go zainstalować za pomocą `pip install pyinstaller`)

## Metoda 1: Użycie skryptu automatyzującego

W pakiecie aplikacji znajduje się skrypt `compile_to_exe.py`, który automatyzuje proces kompilacji.

### Kroki:

1. Otwórz wiersz poleceń Windows (cmd) lub PowerShell
2. Przejdź do katalogu, w którym rozpakowałeś aplikację:
   ```
   cd ścieżka\do\katalogu\aplikacji
   ```
3. Zainstaluj PyInstaller, jeśli jeszcze tego nie zrobiłeś:
   ```
   pip install pyinstaller
   ```
4. Uruchom skrypt kompilacji:
   ```
   python compile_to_exe.py
   ```
5. Po zakończeniu kompilacji, skompilowany plik `.exe` będzie dostępny w katalogu `dist`

## Metoda 2: Ręczna kompilacja

Jeśli wolisz ręcznie skompilować aplikację, wykonaj następujące kroki:

1. Otwórz wiersz poleceń Windows (cmd) lub PowerShell
2. Przejdź do katalogu, w którym rozpakowałeś aplikację:
   ```
   cd ścieżka\do\katalogu\aplikacji
   ```
3. Wykonaj polecenie PyInstaller:
   ```
   pyinstaller --name=Aplikacja_Czasowa --windowed --onefile main.py
   ```
4. Po zakończeniu kompilacji, skompilowany plik `.exe` będzie dostępny w katalogu `dist`

## Dodatkowe opcje kompilacji

- `--windowed`: Tworzy aplikację bez konsoli (zalecane dla aplikacji GUI)
- `--onefile`: Pakuje wszystko do jednego pliku .exe (łatwiejsze do dystrybucji)
- `--icon=path\to\icon.ico`: Dodaje ikonę do pliku .exe (potrzebujesz pliku .ico)

## Rozwiązywanie problemów

Jeśli napotkasz problemy podczas kompilacji:

1. **Brakujące moduły**: Jeśli PyInstaller nie wykryje automatycznie wszystkich zależności, możesz je dodać ręcznie za pomocą opcji `--hidden-import=nazwa_modułu`
2. **Problemy z ikoną**: Upewnij się, że plik ikony jest w formacie .ico. Jeśli masz tylko plik .svg, możesz użyć narzędzi online do konwersji
3. **Inne błędy**: Sprawdź logi kompilacji i przeszukaj komunikaty błędów. Większość problemów z PyInstaller jest dobrze udokumentowana online