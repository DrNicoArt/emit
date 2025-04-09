"""
Skrypt do kompilacji aplikacji czasowej do pliku .exe
Wymaga zainstalowania biblioteki PyInstaller: pip install pyinstaller
"""
import os
import platform
import subprocess

def kompiluj_do_exe():
    """Kompilacja aplikacji do pliku .exe za pomocą PyInstaller"""
    print("Rozpoczynam kompilację aplikacji do pliku .exe...")
    
    # Sprawdzenie systemu operacyjnego
    if platform.system() != "Windows":
        print("UWAGA: Ten skrypt jest przeznaczony do kompilacji aplikacji na systemie Windows.")
        odpowiedz = input("Czy chcesz kontynuować mimo to? (t/n): ")
        if odpowiedz.lower() != 't':
            print("Przerwano kompilację.")
            return
    
    # Polecenie kompilacji z PyInstaller
    command = [
        "pyinstaller",
        "--name=Aplikacja_Czasowa",
        "--windowed",  # Aplikacja okienkowa bez konsoli
        "--onefile",   # Jeden plik .exe
        "--add-data=style.qss;.",  # Dodanie pliku style.qss do głównego katalogu
        "--icon=resources/icons/app_icon.ico",  # Ikona aplikacji
        "main.py"      # Punkt wejścia aplikacji
    ]
    
    # Sprawdzenie czy plik ikony istnieje, a jeśli nie, to konwersja SVG na ICO
    if not os.path.exists("resources/icons/app_icon.ico"):
        print("Nie znaleziono pliku ikony app_icon.ico")
        svg_file = "resources/icons/app_icon.svg"
        if os.path.exists(svg_file):
            print("Znaleziono plik SVG, ale musisz przekonwertować go na format ICO")
            print("Możesz użyć narzędzi online lub bibliotek Python jak cairosvg i PIL")
            
            # Utwórz domyślny plik ikony
            try:
                import cairosvg
                from PIL import Image
                
                print("Konwertuję SVG na ICO...")
                # Konwersja SVG na PNG
                png_temp = "app_icon_temp.png"
                cairosvg.svg2png(url=svg_file, write_to=png_temp, output_width=256, output_height=256)
                
                # Konwersja PNG na ICO
                img = Image.open(png_temp)
                icon_path = "resources/icons/app_icon.ico"
                os.makedirs(os.path.dirname(icon_path), exist_ok=True)
                img.save(icon_path)
                
                # Usunięcie pliku tymczasowego
                os.remove(png_temp)
                print("Pomyślnie utworzono plik ikony.")
            except ImportError:
                print("Brak wymaganych bibliotek do konwersji (cairosvg, PIL)")
                print("Kontynuuję bez ikony...")
                command.remove("--icon=resources/icons/app_icon.ico")
        else:
            print("Nie znaleziono pliku SVG. Kontynuuję bez ikony...")
            command.remove("--icon=resources/icons/app_icon.ico")
    
    # Uruchomienie polecenia PyInstaller
    try:
        subprocess.run(command, check=True)
        print("\nKompilacja zakończona pomyślnie!")
        print(f"Plik wykonywalny znajduje się w katalogu: {os.path.abspath('dist')}")
    except subprocess.CalledProcessError as e:
        print(f"\nBłąd podczas kompilacji: {e}")
        print("\nSprawdź, czy masz zainstalowany PyInstaller: pip install pyinstaller")
    except FileNotFoundError:
        print("\nNie znaleziono polecenia PyInstaller.")
        print("Zainstaluj PyInstaller za pomocą komendy: pip install pyinstaller")

if __name__ == "__main__":
    kompiluj_do_exe()