#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplikacja Czasowa - główny punkt wejścia
Wizualizacja różnych systemów czasowych w postaci koncentrycznych okręgów
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QFont, QIcon
from ui_mainwindow import MainWindow

def setup_environment():
    """Konfiguracja środowiska aplikacji"""
    # Ustawienie wysokiej jakości renderowania
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    # Ustawienie ścieżki zasobów i ikon
    QDir.addSearchPath('app', os.path.join(os.path.dirname(__file__), 'resources'))
    QDir.addSearchPath('icons', os.path.join(os.path.dirname(__file__), 'resources', 'icons'))
    print(f"Zarejestrowano przewodnik 'app:' dla ścieżki: {os.path.join(os.path.dirname(__file__), 'resources')}")
    print(f"Zarejestrowano przewodnik 'icons:' dla ścieżki: {os.path.join(os.path.dirname(__file__), 'resources', 'icons')}")

def main():
    """Funkcja główna aplikacji"""
    # Utworzenie aplikacji QT
    app = QApplication(sys.argv)
    app.setApplicationName("Aplikacja Czasowa")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Time Systems")
    
    # Konfiguracja środowiska
    setup_environment()
    
    # Zastosowanie stylów
    try:
        # Próba otwarcia pliku ze stylem w bieżącym katalogu (dla normalnej pracy)
        style_path = os.path.join(os.path.dirname(__file__), 'style.qss')
        
        # Sprawdzenie czy aplikacja jest uruchomiona z PyInstaller (frozen)
        if getattr(sys, 'frozen', False):
            # Kiedy uruchamiamy skompilowaną aplikację
            base_dir = os.path.dirname(sys.executable)
            style_path = os.path.join(base_dir, 'style.qss')
            
            # Jeśli nie znaleziono w katalogu głównym, szukaj w katalogu _MEIXXXX (tymczasowy folder PyInstaller)
            if not os.path.exists(style_path):
                # Dla PyInstaller _MEIXXXX
                base_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
                style_path = os.path.join(base_dir, 'style.qss')
                
                # Jeśli nadal brak, spróbuj ścieżki względnej
                if not os.path.exists(style_path):
                    style_path = 'style.qss'
        
        print(f"Ładowanie stylu z: {style_path}")
        
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as style_file:
                app.setStyleSheet(style_file.read())
        else:
            print(f"UWAGA: Nie znaleziono pliku stylu: {style_path}")
            
    except Exception as e:
        print(f"Błąd podczas ładowania pliku stylu: {e}")
    
    # Domyślna czcionka aplikacji - elegancka i czytelna
    default_font = QFont("Segoe UI", 10)
    app.setFont(default_font)
    
    # Włączenie wysokiej jakości antyaliasingu
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    # Utworzenie i wyświetlenie głównego okna
    window = MainWindow()
    window.show()
    
    # Uruchomienie pętli zdarzeń aplikacji
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
