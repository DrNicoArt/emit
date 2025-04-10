#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pasek narzędzi - dodatkowe kontrolki do zarządzania wizualizacją
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, 
                            QLabel, QComboBox, QGroupBox, QPushButton, 
                            QSlider, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal

class PasekNarzedzi(QWidget):
    """
    Pasek narzędzi z kontrolkami do zarządzania wizualizacją systemów czasowych
    """
    
    def __init__(self, koncentryczne_okregi, parent=None):
        super().__init__(parent)
        self.koncentryczne_okregi = koncentryczne_okregi
        
        # Utworzenie głównego układu
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)
        
        # Dodanie kontrolek widoczności warstw
        self.add_visibility_controls()
        
        # Dodanie kontrolek animacji
        self.add_animation_controls()
        
        # Dodanie opcji wyświetlania
        self.add_display_options()
        
        # Dodanie elastycznej przestrzeni na końcu
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        
        # Połączenie sygnałów
        self.connect_signals()
    
    def add_visibility_controls(self):
        """Dodanie kontrolek do włączania/wyłączania warstw"""
        # Utworzenie grupy dla kontrolek warstw
        layers_group = QGroupBox("Systemy czasowe")
        layers_layout = QVBoxLayout()
        
        # Lista systemów czasowych
        self.systems = [
            ("Czas Lokalny", "local_time"),
            ("Czas Hebrajski", "hebrew_time"),
            ("Czas Atomowy", "atomic_time"),
            ("Czas Pulsarowy", "pulsar_time"),
            ("Ruch Obrotowy Ziemi", "earth_rotation"),
            ("Rok Astronomiczny", "astronomical_year")
        ]
        
        # Utworzenie checkboxów dla każdego systemu
        self.system_checkboxes = {}
        for name, system_id in self.systems:
            checkbox = QCheckBox(name)
            checkbox.setChecked(True)  # Domyślnie włączone
            checkbox.stateChanged.connect(lambda state, sys_id=system_id: 
                                        self.koncentryczne_okregi.toggle_system(sys_id, state == Qt.Checked))
            layers_layout.addWidget(checkbox)
            self.system_checkboxes[system_id] = checkbox
        
        # Dodanie przycisków "Wszystkie" i "Żadne"
        buttons_layout = QHBoxLayout()
        
        all_button = QPushButton("Wszystkie")
        all_button.clicked.connect(self.select_all_systems)
        buttons_layout.addWidget(all_button)
        
        none_button = QPushButton("Żadne")
        none_button.clicked.connect(self.deselect_all_systems)
        buttons_layout.addWidget(none_button)
        
        layers_layout.addLayout(buttons_layout)
        
        # Ustawienie layoutu dla grupy
        layers_group.setLayout(layers_layout)
        
        # Dodanie grupy do głównego layoutu
        self.main_layout.addWidget(layers_group)
    
    def add_animation_controls(self):
        """Dodanie kontrolek animacji"""
        # Utworzenie grupy dla kontrolek animacji
        animation_group = QGroupBox("Animacja")
        animation_layout = QVBoxLayout()
        
        # Przycisk pauzy/wznowienia
        self.pause_button = QPushButton("Pauza")
        self.pause_button.setCheckable(True)
        animation_layout.addWidget(self.pause_button)
        
        # Suwak prędkości animacji (opcjonalnie)
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Prędkość:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(1)
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        animation_layout.addLayout(speed_layout)
        
        # Ustawienie layoutu dla grupy
        animation_group.setLayout(animation_layout)
        
        # Dodanie grupy do głównego layoutu
        self.main_layout.addWidget(animation_group)
    
    def add_display_options(self):
        """Dodanie opcji wyświetlania"""
        # Utworzenie grupy dla opcji wyświetlania
        display_group = QGroupBox("Opcje wyświetlania")
        display_layout = QVBoxLayout()
        
        # Checkbox "Pokaż etykiety"
        self.labels_checkbox = QCheckBox("Pokaż etykiety")
        self.labels_checkbox.setChecked(True)
        display_layout.addWidget(self.labels_checkbox)
        
        # Checkbox "Pokaż szczegóły"
        self.details_checkbox = QCheckBox("Pokaż szczegóły")
        self.details_checkbox.setChecked(True)
        display_layout.addWidget(self.details_checkbox)
        
        # Wybór stylu wyświetlania
        style_layout = QHBoxLayout()
        style_label = QLabel("Styl:")
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Klasyczny", "Minimalistyczny", "Szczegółowy"])
        
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combo)
        display_layout.addLayout(style_layout)
        
        # Ustawienie layoutu dla grupy
        display_group.setLayout(display_layout)
        
        # Dodanie grupy do głównego layoutu
        self.main_layout.addWidget(display_group)
    
    def connect_signals(self):
        """Połączenie sygnałów z akcjami"""
        # Połączenie kontrolek animacji
        self.pause_button.toggled.connect(self.toggle_animation)
        
        # Połączenie opcji wyświetlania
        self.labels_checkbox.stateChanged.connect(self.update_display_options)
        self.details_checkbox.stateChanged.connect(self.update_display_options)
        self.style_combo.currentTextChanged.connect(self.update_display_options)
    
    def toggle_animation(self, paused):
        """Włączanie/wyłączanie animacji"""
        # Zmiana etykiety przycisku
        if paused:
            self.pause_button.setText("Wznów")
        else:
            self.pause_button.setText("Pauza")
        
        # Przekazanie informacji do widoku
        self.koncentryczne_okregi.animation_paused = paused
    
    def update_display_options(self):
        """Aktualizacja opcji wyświetlania"""
        # Pobranie wartości z kontrolek
        show_labels = self.labels_checkbox.isChecked()
        show_details = self.details_checkbox.isChecked()
        style = self.style_combo.currentText()
        
        # Aktualizacja opcji w widoku
        self.koncentryczne_okregi.show_labels = show_labels
        self.koncentryczne_okregi.show_details = show_details
        self.koncentryczne_okregi.style = style
        
        # Aktualizacja dla wszystkich systemów
        for system_id, system_data in self.koncentryczne_okregi.systems.items():
            system_data['instance'].set_display_options(show_labels, show_details, style)
        
        # Wymuszenie odświeżenia widoku
        self.koncentryczne_okregi.update_visualization()
    
    def select_all_systems(self):
        """Zaznaczenie wszystkich systemów"""
        for checkbox in self.system_checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all_systems(self):
        """Odznaczenie wszystkich systemów"""
        for checkbox in self.system_checkboxes.values():
            checkbox.setChecked(False)
    
    def update_checkbox(self, system_id, visible):
        """Aktualizacja stanu checkboxa po zmianie z zewnątrz"""
        if system_id in self.system_checkboxes:
            # Blokujemy sygnały, aby nie wywołać rekurencji
            self.system_checkboxes[system_id].blockSignals(True)
            self.system_checkboxes[system_id].setChecked(visible)
            self.system_checkboxes[system_id].blockSignals(False)