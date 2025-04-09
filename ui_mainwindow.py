#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Główne okno aplikacji - zarządza wszystkimi komponentami UI
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QDockWidget, QAction, QToolBar, 
                            QStatusBar, QLabel, QComboBox, QWidget, 
                            QVBoxLayout, QHBoxLayout, QSplitter)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap

from widgets.koncentryczne_okregi import KoncentryczneOkregi
from widgets.narzedzia import PasekNarzedzi

class MainWindow(QMainWindow):
    """
    Klasa głównego okna aplikacji
    Zarządza wszystkimi elementami interfejsu użytkownika
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikacja Czasowa")
        self.resize(1200, 800)
        
        # Inicjalizacja komponentów UI
        self.init_ui()
        
        # Timer do aktualizacji statusu
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Aktualizacja co sekundę
    
    def init_ui(self):
        """Inicjalizacja elementów interfejsu użytkownika"""
        # Centralny widget - wizualizacja koncentrycznych okręgów
        self.koncentryczne_okregi = KoncentryczneOkregi(self)
        self.setCentralWidget(self.koncentryczne_okregi)
        
        # Utworzenie menu
        self.create_menu()
        
        # Utworzenie paska narzędzi
        self.create_toolbar()
        
        # Utworzenie panelu bocznego
        self.create_sidebar()
        
        # Utworzenie paska statusu
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
        # Domyślny komunikat w pasku statusu
        self.status_label = QLabel("Aplikacja Czasowa uruchomiona")
        self.statusbar.addWidget(self.status_label)
        
        # Dodanie widgetu synchronizacji w pasku statusu (po prawej)
        self.sync_label = QLabel("Synchronizacja: OK")
        self.statusbar.addPermanentWidget(self.sync_label)
    
    def create_menu(self):
        """Utworzenie głównego menu aplikacji"""
        # Menu Plik
        file_menu = self.menuBar().addMenu("&Plik")
        
        # Akcja Zamknij
        exit_action = QAction("&Zamknij", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Zamknij aplikację")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Widok
        view_menu = self.menuBar().addMenu("&Widok")
        
        # Podmenu Systemy Czasowe
        time_systems_menu = view_menu.addMenu("Systemy Czasowe")
        
        # Akcje dla każdego systemu czasowego
        self.toggle_actions = {}
        systems = [
            ("Czas Lokalny", "local_time"),
            ("Czas Hebrajski", "hebrew_time"),
            ("Czas Atomowy", "atomic_time"),
            ("Czas Pulsarowy", "pulsar_time"),
            ("Ruch Obrotowy Ziemi", "earth_rotation"),
            ("Rok Astronomiczny", "astronomical_year")
        ]
        
        for name, system_id in systems:
            action = QAction(name, self, checkable=True)
            action.setChecked(True)  # Domyślnie wszystkie systemy są włączone
            action.triggered.connect(lambda checked, sys_id=system_id: 
                                    self.koncentryczne_okregi.toggle_system(sys_id, checked))
            time_systems_menu.addAction(action)
            self.toggle_actions[system_id] = action
        
        # Menu Ustawienia
        settings_menu = self.menuBar().addMenu("&Ustawienia")
        
        # Akcja Strefa Czasowa
        timezone_action = QAction("&Strefa Czasowa", self)
        timezone_action.setStatusTip("Zmień strefę czasową")
        timezone_action.triggered.connect(self.change_timezone)
        settings_menu.addAction(timezone_action)
        
        # Akcja Ustawienia Synchronizacji
        sync_action = QAction("&Ustawienia Synchronizacji", self)
        sync_action.setStatusTip("Konfiguruj serwery synchronizacji czasu")
        sync_action.triggered.connect(self.configure_sync)
        settings_menu.addAction(sync_action)
        
        # Menu Pomoc
        help_menu = self.menuBar().addMenu("Pomo&c")
        
        # Akcja O programie
        about_action = QAction("&O Programie", self)
        about_action.setStatusTip("Informacje o aplikacji")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Utworzenie paska narzędzi aplikacji"""
        self.toolbar = QToolBar("Główny pasek narzędzi")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        
        # Akcja Reset widoku
        reset_action = QAction("Reset widoku", self)
        reset_action.setStatusTip("Przywróć domyślny widok")
        reset_action.triggered.connect(self.koncentryczne_okregi.reset_view)
        self.toolbar.addAction(reset_action)
        
        # Dodanie separatora
        self.toolbar.addSeparator()
        
        # Akcje przybliżania/oddalania
        zoom_in_action = QAction("Przybliż", self)
        zoom_in_action.setStatusTip("Przybliż widok")
        zoom_in_action.triggered.connect(self.koncentryczne_okregi.zoom_in)
        self.toolbar.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Oddal", self)
        zoom_out_action.setStatusTip("Oddal widok")
        zoom_out_action.triggered.connect(self.koncentryczne_okregi.zoom_out)
        self.toolbar.addAction(zoom_out_action)
        
        # Dodanie separatora
        self.toolbar.addSeparator()
        
        # Wybór strefy czasowej
        self.toolbar.addWidget(QLabel("Strefa czasowa: "))
        
        self.timezone_combo = QComboBox()
        self.timezone_combo.addItems(["Lokalna", "UTC", "UTC+1", "UTC+2", "UTC-5", "UTC-8"])
        self.timezone_combo.setCurrentIndex(0)
        self.timezone_combo.currentTextChanged.connect(self.koncentryczne_okregi.update_timezone)
        self.toolbar.addWidget(self.timezone_combo)
    
    def create_sidebar(self):
        """Utworzenie panelu bocznego z kontrolkami"""
        # Utworzenie doku bocznego
        self.sidebar_dock = QDockWidget("Kontrolki", self)
        self.sidebar_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sidebar_dock.setMinimumWidth(250)
        
        # Utworzenie widgetu pasek narzędzi (kontrolek)
        self.pasek_narzedzi = PasekNarzedzi(self.koncentryczne_okregi)
        
        # Ustawienie widgetu jako zawartości doku
        self.sidebar_dock.setWidget(self.pasek_narzedzi)
        
        # Dodanie doku do głównego okna (po lewej stronie)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar_dock)
        
        # Podłączenie sygnału przełączania systemów
        self.koncentryczne_okregi.system_toggled.connect(self.pasek_narzedzi.update_checkbox)
    
    def update_status(self):
        """Aktualizacja paska statusu"""
        # Aktualizacja czasu w pasku statusu
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_label.setText(f"Czas: {current_time}")
        
        # Aktualizacja statusu synchronizacji (dla czasu atomowego)
        # W rzeczywistej aplikacji ta informacja pochodziłaby z modułu czasu atomowego
        # Tutaj tylko symulujemy
        sync_ok = True  # W rzeczywistej aplikacji byłoby to sprawdzane
        
        if sync_ok:
            self.sync_label.setText("Synchronizacja: OK")
        else:
            self.sync_label.setText("Synchronizacja: Błąd")
    
    def change_timezone(self):
        """Obsługa zmiany strefy czasowej"""
        # To jest tylko stub - w rzeczywistości otworzyłoby to okno dialogowe
        # z wyborem strefy czasowej
        pass
    
    def configure_sync(self):
        """Konfiguracja synchronizacji z serwerami czasu"""
        # To jest tylko stub - w rzeczywistości otworzyłoby to okno dialogowe
        # z konfiguracją serwerów NTP
        pass
    
    def show_about(self):
        """Wyświetlenie informacji o programie"""
        # To jest tylko stub - w rzeczywistości otworzyłoby to okno dialogowe
        # z informacjami o programie
        pass
    
    def closeEvent(self, event):
        """Obsługa zdarzenia zamknięcia okna"""
        # Czyszczenie zasobów przy zamknięciu
        self.koncentryczne_okregi.cleanup()
        event.accept()