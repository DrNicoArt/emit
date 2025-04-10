#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moduł odpowiedzialny za wizualizację czasu pulsarowego
Symuluje pulsy pulsara na podstawie danych naukowych
"""

import time
import math
import random
from datetime import datetime, timezone, timedelta
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QRadialGradient, QLinearGradient

class CzasPulsarowy:
    """
    Klasa implementująca wizualizację czasu pulsarowego
    Symuluje pulsy pulsara i pokazuje odpowiadającą im skalę czasu
    """
    
    def __init__(self):
        """Inicjalizacja czasu pulsarowego"""
        # Aktualna strefa czasowa - domyślnie lokalna
        self.timezone = None
        
        # Opcje wyświetlania
        self.show_labels = True
        self.show_details = True
        self.style = "Klasyczny"
        
        # Base Z-index dla warstw tego systemu
        self.base_z_index = 0
        
        # Inicjalizacja danych o pulsarach
        self.init_pulsar_data()
        
        # Inicjalizacja historii pulsów
        self.init_pulse_history()
        
        # Wybrany pulsar (domyślnie pierwszy)
        self.selected_pulsar_index = 0
        
        # Aktualny stan pulsu
        self.current_pulse = 0.0  # Wartość od 0 do 1 (0 = pomiędzy pulsami, 1 = maksimum pulsu)
        self.pulse_timer = time.time()  # Czas ostatniej aktualizacji pulsu
    
    def init_pulsar_data(self):
        """Inicjalizacja danych o pulsarach"""
        # Dane pulsarów (okres obrotu w milisekundach, lokalizacja, odkrycie)
        self.pulsars = [
            {
                "name": "PSR B0531+21 (Krab)",
                "period": 33.0,  # milisekundy
                "location": "Gwiazdozbiór Byka",
                "discovery": "1968",
                "notes": "Pozostałość po supernowej z 1054 roku"
            },
            {
                "name": "PSR B1937+21",
                "period": 1.558,  # milisekundy
                "location": "Gwiazdozbiór Liska",
                "discovery": "1982",
                "notes": "Pierwszy odkryty pulsar milisekundowy"
            },
            {
                "name": "PSR J0737-3039",
                "period": 22.7,  # milisekundy
                "location": "Gwiazdozbiór Rufy",
                "discovery": "2003",
                "notes": "Podwójny pulsar - pierwszy odkryty układ tego typu"
            },
            {
                "name": "PSR B1919+21",
                "period": 1337.0,  # milisekundy
                "location": "Gwiazdozbiór Liska",
                "discovery": "1967",
                "notes": "Pierwszy odkryty pulsar"
            }
        ]
    
    def init_pulse_history(self):
        """Inicjalizacja historii pulsów"""
        # Inicjalizacja tablicy historii pulsów (ostatnie 20 pulsów)
        self.pulse_history = [0.0] * 20
        
        # Indeks aktualnego pulsu w historii
        self.history_index = 0
    
    def update_pulse_state(self):
        """Aktualizacja stanu pulsowania na podstawie aktualnego czasu"""
        # Pobieramy aktualny czas
        current_time = time.time()
        
        # Obliczamy czas, który minął od ostatniej aktualizacji
        elapsed_time = current_time - self.pulse_timer
        
        # Aktualizujemy timer
        self.pulse_timer = current_time
        
        # Pobieramy okres aktualnie wybranego pulsara (w milisekundach)
        pulsar_period = self.pulsars[self.selected_pulsar_index]["period"]
        
        # Konwersja okresu na sekundy
        period_seconds = pulsar_period / 1000.0
        
        # Aktualizujemy stan pulsu
        # Puls jest sinusoidą z okresem równym okresowi pulsara
        time_in_period = (current_time % period_seconds) / period_seconds
        
        # Pulsar świeci tylko przez krótki moment swojego okresu
        # Modelujemy to za pomocą funkcji Gaussa
        pulse_width = 0.1  # Szerokość pulsu jako ułamek okresu
        pulse_center = 0.5  # Centrum pulsu w okresie (0.5 = środek okresu)
        
        # Obliczenie odległości od centrum pulsu (z uwzględnieniem cykliczności)
        distance = min(abs(time_in_period - pulse_center), 
                      abs(time_in_period - pulse_center - 1), 
                      abs(time_in_period - pulse_center + 1))
        
        # Obliczenie wartości pulsu za pomocą funkcji Gaussa
        self.current_pulse = math.exp(-(distance ** 2) / (2 * pulse_width ** 2))
        
        # Aktualizacja historii pulsów
        if elapsed_time >= period_seconds:
            # Jeśli minął pełny okres, dodajemy nowy punkt do historii
            num_periods = int(elapsed_time / period_seconds)
            
            for _ in range(min(num_periods, 5)):  # Maksymalnie 5 punktów na raz, żeby nie zapełnić historii
                self.history_index = (self.history_index + 1) % len(self.pulse_history)
                
                # Dodanie losowego szumu do pulsu (symulacja zakłóceń)
                noise = random.uniform(0.8, 1.2)
                self.pulse_history[self.history_index] = min(1.0, self.current_pulse * noise)
    
    def set_timezone(self, timezone):
        """Ustawienie strefy czasowej"""
        self.timezone = timezone
    
    def set_display_options(self, show_labels=True, show_details=False, style="Klasyczny"):
        """Ustawienie opcji wyświetlania"""
        self.show_labels = show_labels
        self.show_details = show_details
        self.style = style
    
    def draw(self, scene, inner_radius, outer_radius):
        """Rysowanie wizualizacji czasu pulsarowego"""
        # Obliczenie środka sceny
        center_x = 0
        center_y = 0
        
        # Aktualizacja stanu pulsu
        self.update_pulse_state()
        
        # Rysowanie tła
        self.draw_background(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie informacji o pulsarze
        if self.show_labels:
            self.draw_pulsar_info(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie diagramu pulsu
        self.draw_pulse_diagram(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie historii pulsów
        if self.show_details:
            self.draw_pulse_history(scene, center_x, center_y, inner_radius, outer_radius)
    
    def draw_background(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie tła dla czasu pulsarowego - tylko kontury, bez wypełnień"""
        # Średni promień obszaru czasu pulsarowego
        mid_radius = (inner_radius + outer_radius) / 2
        
        # Rysowanie okręgów granicznych
        inner_circle = QGraphicsEllipseItem(
            int(center_x - inner_radius), int(center_y - inner_radius), 
            int(inner_radius * 2), int(inner_radius * 2)
        )
        outer_circle = QGraphicsEllipseItem(
            int(center_x - outer_radius), int(center_y - outer_radius), 
            int(outer_radius * 2), int(outer_radius * 2)
        )
        
        # Ustawienie stylu okręgów
        circle_pen = QPen(QColor(120, 80, 120))
        circle_pen.setWidth(1)
        inner_circle.setPen(circle_pen)
        outer_circle.setPen(circle_pen)
        
        # Bez wypełnienia
        inner_circle.setBrush(QBrush(Qt.NoBrush))
        outer_circle.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie do sceny
        inner_circle.setZValue(self.base_z_index)
        outer_circle.setZValue(self.base_z_index)
        scene.addItem(inner_circle)
        scene.addItem(outer_circle)
        
        # Rysowanie promieniowych linii podziału (opcjonalnie)
        if self.show_labels:
            # Rysowanie 8 linii podziału
            for i in range(8):
                angle = math.radians(i * 45)  # Podział co 45 stopni
                
                # Obliczenie współrzędnych początku i końca linii
                start_x = int(center_x + inner_radius * math.cos(angle))
                start_y = int(center_y + inner_radius * math.sin(angle))
                end_x = int(center_x + outer_radius * math.cos(angle))
                end_y = int(center_y + outer_radius * math.sin(angle))
                
                # Utworzenie linii podziału
                division_line = QGraphicsLineItem(start_x, start_y, end_x, end_y)
                
                # Ustawienie stylu linii
                line_pen = QPen(QColor(120, 80, 120, 80))  # Półprzezroczysta
                line_pen.setWidth(1)
                line_pen.setStyle(Qt.DotLine)
                division_line.setPen(line_pen)
                
                # Dodanie do sceny
                division_line.setZValue(self.base_z_index + 1)
                scene.addItem(division_line)
    
    def draw_pulsar_info(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie informacji o wybranym pulsarze"""
        # Aktualne dane pulsara
        pulsar = self.pulsars[self.selected_pulsar_index]
        
        # Określenie położenia panelu informacyjnego
        info_x = center_x - inner_radius * 0.9
        info_y = center_y - inner_radius * 0.5
        info_width = inner_radius * 1.8
        info_height = inner_radius * 0.3
        
        # Utworzenie interaktywnego elementu informacyjnego
        from widgets.koncentryczne_okregi import InteraktywnyElement
        info_element = InteraktywnyElement(
            int(info_x), int(info_y), int(info_width), int(info_height),
            pulsar["name"],
            f"Pulsar: {pulsar['name']}\n"
            f"Okres obrotu: {pulsar['period']} ms\n"
            f"Lokalizacja: {pulsar['location']}\n"
            f"Odkrycie: {pulsar['discovery']}\n"
            f"Informacje: {pulsar['notes']}"
        )
        
        # Ustawienie stylu elementu
        info_element.setPen(QPen(QColor(150, 100, 150), 1))
        info_element.setBrush(QBrush(Qt.NoBrush))  # Bez wypełnienia
        
        # Dodanie do sceny
        info_element.setZValue(self.base_z_index + 10)
        scene.addItem(info_element)
        
        # Dodanie tekstu bezpośrednio
        pulsar_text = QGraphicsTextItem(f"Pulsar: {pulsar['name']}\nOkres: {pulsar['period']} ms")
        pulsar_text.setPos(int(info_x + 10), int(info_y + 10))
        pulsar_text.setDefaultTextColor(QColor(200, 150, 200))
        
        # Ustawienie czcionki
        pulsar_font = QFont("Arial", 8)
        pulsar_text.setFont(pulsar_font)
        
        # Dodanie do sceny
        pulsar_text.setZValue(self.base_z_index + 11)
        scene.addItem(pulsar_text)
    
    def draw_pulse_diagram(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie diagramu pulsu"""
        # Średni promień obszaru czasu pulsarowego
        mid_radius = (inner_radius + outer_radius) / 2
        pulse_area_width = outer_radius - inner_radius
        
        # Rysowanie wskaźnika aktualnego pulsu
        pulse_radius = mid_radius * (0.8 + 0.2 * self.current_pulse)  # Pulsujący promień
        pulse_indicator = QGraphicsEllipseItem(
            int(center_x - pulse_radius), int(center_y - pulse_radius),
            int(pulse_radius * 2), int(pulse_radius * 2)
        )
        
        # Ustawienie stylu wskaźnika
        pulse_pen = QPen(QColor(200, 100, 200))
        pulse_pen.setWidth(1)
        pulse_indicator.setPen(pulse_pen)
        
        # Bez wypełnienia lub półprzezroczyste, zależnie od siły pulsu
        pulse_color = QColor(200, 100, 200, int(100 * self.current_pulse))
        pulse_indicator.setBrush(QBrush(pulse_color))
        
        # Dodanie do sceny
        pulse_indicator.setZValue(self.base_z_index + 5)
        scene.addItem(pulse_indicator)
        
        # Rysowanie centralnego punktu pulsu
        central_point_size = int(4 + 4 * self.current_pulse)  # Pulsujący rozmiar
        central_point = QGraphicsEllipseItem(
            int(center_x - central_point_size/2), int(center_y - central_point_size/2),
            central_point_size, central_point_size
        )
        
        # Ustawienie stylu centralnego punktu
        central_point.setPen(QPen(Qt.NoPen))
        
        # Kolor zależny od siły pulsu
        central_color = QColor(
            int(200 + 55 * self.current_pulse),  # R
            int(100 + 55 * self.current_pulse),  # G
            int(200 + 55 * self.current_pulse)   # B
        )
        central_point.setBrush(QBrush(central_color))
        
        # Dodanie do sceny
        central_point.setZValue(self.base_z_index + 15)
        scene.addItem(central_point)
        
        # Rysowanie promieni pulsu
        if self.current_pulse > 0.5:
            # Liczba promieni
            num_rays = 12
            
            # Długość promieni zależna od siły pulsu
            ray_length = pulse_area_width * 0.5 * ((self.current_pulse - 0.5) * 2)  # Od 0 do 1
            
            # Rysowanie promieni
            for i in range(num_rays):
                ray_angle = 2 * math.pi * i / num_rays
                
                # Współrzędne początku i końca promienia
                start_x = int(center_x + mid_radius * math.cos(ray_angle))
                start_y = int(center_y + mid_radius * math.sin(ray_angle))
                end_x = int(center_x + (mid_radius + ray_length) * math.cos(ray_angle))
                end_y = int(center_y + (mid_radius + ray_length) * math.sin(ray_angle))
                
                # Utworzenie linii promienia
                ray = QGraphicsLineItem(start_x, start_y, end_x, end_y)
                
                # Ustawienie stylu promienia
                ray_pen = QPen(central_color)
                ray_pen.setWidth(1)
                ray.setPen(ray_pen)
                
                # Dodanie do sceny
                ray.setZValue(self.base_z_index + 6)
                scene.addItem(ray)
    
    def draw_pulse_history(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie historii pulsów"""
        # Określenie obszaru wykresu historii
        history_x = center_x - inner_radius * 0.8
        history_y = center_y + inner_radius * 0.2
        history_width = inner_radius * 1.6
        history_height = inner_radius * 0.3
        
        # Rysowanie tła wykresu
        history_background = QGraphicsRectItem(
            int(history_x), int(history_y), 
            int(history_width), int(history_height)
        )
        
        # Ustawienie stylu tła
        history_background.setPen(QPen(QColor(120, 80, 120)))
        history_background.setBrush(QBrush(Qt.NoBrush))  # Bez wypełnienia
        
        # Dodanie do sceny
        history_background.setZValue(self.base_z_index + 20)
        scene.addItem(history_background)
        
        # Rysowanie wykresu historii pulsów
        # Szerokość i wysokość słupka
        bar_width = history_width / len(self.pulse_history)
        
        for i in range(len(self.pulse_history)):
            # Indeks w historii (od najstarszego do najnowszego)
            idx = (self.history_index - i) % len(self.pulse_history)
            pulse_value = self.pulse_history[idx]
            
            # Wysokość słupka proporcjonalna do wartości pulsu
            bar_height = history_height * pulse_value
            
            # Pozycja słupka
            bar_x = history_x + i * bar_width
            bar_y = history_y + history_height - bar_height
            
            # Utworzenie słupka
            bar = QGraphicsRectItem(
                int(bar_x), int(bar_y), 
                int(bar_width), int(bar_height)
            )
            
            # Ustawienie stylu słupka
            bar.setPen(QPen(Qt.NoPen))
            
            # Kolor zależny od wartości pulsu
            bar_color = QColor(
                200,                          # R
                int(100 + 100 * pulse_value), # G - konwersja float na int
                200                           # B
            )
            bar_color.setAlpha(150)  # Półprzezroczysty
            bar.setBrush(QBrush(bar_color))
            
            # Dodanie do sceny
            bar.setZValue(self.base_z_index + 21)
            scene.addItem(bar)
        
        # Dodanie etykiety wykresu
        history_label = QGraphicsTextItem("Historia pulsów")
        history_label.setPos(int(history_x + 5), int(history_y + 5))
        history_label.setDefaultTextColor(QColor(200, 150, 200))
        
        # Ustawienie czcionki
        label_font = QFont("Arial", 7)
        history_label.setFont(label_font)
        
        # Dodanie do sceny
        history_label.setZValue(self.base_z_index + 22)
        scene.addItem(history_label)
    
    def cleanup(self):
        """Czyszczenie zasobów"""
        # W tej implementacji nie ma potrzeby czyszczenia zasobów
        pass