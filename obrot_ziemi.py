#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moduł odpowiedzialny za wizualizację obrotu Ziemi
Prezentuje aktualną pozycję punktów na Ziemi względem Słońca
"""

import math
from datetime import datetime, timezone, timedelta
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsPathItem, QGraphicsPolygonItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPolygonF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainterPath, QRadialGradient

class ObrotZiemi:
    """
    Klasa implementująca wizualizację obrotu Ziemi
    Pokazuje dzień i noc na kuli ziemskiej oraz pozycje kontynentów
    """
    
    def __init__(self):
        """Inicjalizacja wizualizacji obrotu Ziemi"""
        # Aktualna strefa czasowa - domyślnie lokalna
        self.timezone = None
        
        # Opcje wyświetlania
        self.show_labels = True
        self.show_details = True
        self.style = "Klasyczny"
        
        # Base Z-index dla warstw tego systemu
        self.base_z_index = 0
        
        # Inicjalizacja danych o kontynentach i miastach
        self.init_continents_data()
        self.init_cities_data()
    
    def init_continents_data(self):
        """Inicjalizacja danych o kontynentach"""
        # Dla uproszczenia używamy uproszczonych danych o położeniu kontynentów
        # Każdy kontynent jest określony przez kąt (długość geograficzna) i rozpiętość
        self.continents = [
            {"name": "Europa", "longitude": 15, "span": 30, "color": QColor(100, 180, 100)},
            {"name": "Azja", "longitude": 90, "span": 80, "color": QColor(180, 160, 100)},
            {"name": "Afryka", "longitude": 20, "span": 60, "color": QColor(180, 140, 60)},
            {"name": "Ameryka Pn.", "longitude": -100, "span": 50, "color": QColor(160, 100, 100)},
            {"name": "Ameryka Pd.", "longitude": -60, "span": 40, "color": QColor(100, 160, 120)},
            {"name": "Australia", "longitude": 135, "span": 30, "color": QColor(180, 120, 60)},
            {"name": "Antarktyda", "longitude": 0, "span": 360, "color": QColor(200, 200, 220)}
        ]
    
    def init_cities_data(self):
        """Inicjalizacja danych o miastach"""
        # Dla uproszczenia używamy kilku największych miast
        self.cities = [
            {"name": "Londyn", "longitude": 0, "latitude": 51.5, "timezone": "Europe/London"},
            {"name": "Paryż", "longitude": 2.35, "latitude": 48.85, "timezone": "Europe/Paris"},
            {"name": "Nowy Jork", "longitude": -74, "latitude": 40.7, "timezone": "America/New_York"},
            {"name": "Tokio", "longitude": 139.7, "latitude": 35.7, "timezone": "Asia/Tokyo"},
            {"name": "Sydney", "longitude": 151.2, "latitude": -33.9, "timezone": "Australia/Sydney"},
            {"name": "Rio de Janeiro", "longitude": -43.2, "latitude": -22.9, "timezone": "America/Sao_Paulo"},
            {"name": "Kair", "longitude": 31.2, "latitude": 30.0, "timezone": "Africa/Cairo"},
            {"name": "Moskwa", "longitude": 37.6, "latitude": 55.75, "timezone": "Europe/Moscow"}
        ]
    
    def get_current_earth_rotation(self):
        """Obliczenie aktualnego obrotu Ziemi"""
        # Pobieramy aktualną datę i czas
        now = datetime.now()
        
        # Zastosowanie strefy czasowej, jeśli została ustawiona
        if self.timezone and self.timezone != "Lokalna":
            if self.timezone.startswith("UTC"):
                # Parsowanie przesunięcia UTC
                try:
                    if "+" in self.timezone:
                        offset = int(self.timezone.split("+")[1])
                        now = datetime.now(timezone.utc) + timedelta(hours=offset)
                    elif "-" in self.timezone:
                        offset = int(self.timezone.split("-")[1])
                        now = datetime.now(timezone.utc) - timedelta(hours=offset)
                    else:
                        now = datetime.now(timezone.utc)
                except Exception:
                    # W przypadku błędu użyj czasu lokalnego
                    pass
        
        # Obliczamy kąt obrotu Ziemi (południk Greenwich = 0 stopni)
        # Pełny obrót (360 stopni) zajmuje 24 godziny
        # Przeliczamy czas na kąt: godzina * 15 + minuty * 0.25 + sekundy * 0.004166...
        angle = (now.hour * 15) + (now.minute * 0.25) + (now.second * 0.00417)
        
        # Uwzględniamy datę (dzień w roku) dla kąta nachylenia osi Ziemi
        # Upraszaczamy, zakładając że maksymalne nachylenie to 23.5 stopnia
        day_of_year = now.timetuple().tm_yday  # Dzień roku (1-366)
        
        # Obliczenie nachylenia osi (zależy od dnia w roku)
        # Maksymalne nachylenie w przesilenia (21 czerwca i 21 grudnia)
        # Dzień 172 to mniej więcej 21 czerwca, dzień 355 to mniej więcej 21 grudnia
        days_from_spring = (day_of_year - 80) % 365  # 80 to mniej więcej 21 marca (równonoc wiosenna)
        tilt_angle = 23.5 * math.sin(2 * math.pi * days_from_spring / 365)
        
        return {
            "rotation_angle": angle,
            "tilt_angle": tilt_angle,
            "date": now
        }
    
    def set_timezone(self, timezone):
        """Ustawienie strefy czasowej"""
        self.timezone = timezone
    
    def set_display_options(self, show_labels=True, show_details=False, style="Klasyczny"):
        """Ustawienie opcji wyświetlania"""
        self.show_labels = show_labels
        self.show_details = show_details
        self.style = style
    
    def draw(self, scene, inner_radius, outer_radius):
        """Rysowanie wizualizacji obrotu Ziemi"""
        # Obliczenie środka sceny
        center_x = 0
        center_y = 0
        
        # Pobranie aktualnego obrotu Ziemi
        earth_rotation = self.get_current_earth_rotation()
        
        # Rysowanie tła (kula ziemska)
        self.draw_earth_globe(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie linii terminatora (granica dnia i nocy)
        self.draw_day_night_terminator(scene, center_x, center_y, inner_radius, outer_radius, earth_rotation)
        
        # Rysowanie kontynentów
        self.draw_continents(scene, center_x, center_y, inner_radius, outer_radius, earth_rotation)
        
        # Rysowanie siatki geograficznej (południki i równoleżniki)
        if self.show_labels:
            self.draw_geographic_grid(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie miast
        if self.show_details:
            self.draw_cities(scene, center_x, center_y, inner_radius, outer_radius, earth_rotation)
        
        # Rysowanie informacji o aktualnym czasie
        self.draw_time_info(scene, center_x, center_y, inner_radius, outer_radius, earth_rotation)
    
    def draw_earth_globe(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie kuli ziemskiej"""
        # Średni promień kuli ziemskiej
        globe_radius = (inner_radius + outer_radius) / 2
        
        # Rysowanie kuli jako okręgu
        globe = QGraphicsEllipseItem(center_x - globe_radius, center_y - globe_radius, 
                                   globe_radius * 2, globe_radius * 2)
        
        # Ustawienie stylu kuli
        globe_pen = QPen(QColor(100, 150, 200))
        globe_pen.setWidth(1)
        globe.setPen(globe_pen)
        
        # Brak wypełnienia globu - tylko kontur
        globe.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie do sceny
        globe.setZValue(self.base_z_index + 1)
        scene.addItem(globe)
        
        # Rysowanie osi obrotu (opcjonalnie)
        if self.show_details:
            # Oś od bieguna północnego do południowego
            axis_length = globe_radius * 1.2
            axis = QGraphicsLineItem(center_x, center_y - axis_length, center_x, center_y + axis_length)
            
            # Ustawienie stylu osi
            axis_pen = QPen(QColor(200, 200, 220))
            axis_pen.setWidth(1)
            axis_pen.setStyle(Qt.DashLine)
            axis.setPen(axis_pen)
            
            # Dodanie do sceny
            axis.setZValue(self.base_z_index)  # Pod kulą ziemską
            scene.addItem(axis)
    
    def draw_day_night_terminator(self, scene, center_x, center_y, inner_radius, outer_radius, earth_rotation):
        """Rysowanie linii terminatora (granica dnia i nocy)"""
        # Średni promień kuli ziemskiej
        globe_radius = (inner_radius + outer_radius) / 2
        
        # Kąt obrotu Ziemi w radianach (konwersja ze stopni)
        rotation_angle = math.radians(earth_rotation["rotation_angle"])
        
        # Rysowanie półkola dla nocy
        # Noc jest po przeciwnej stronie Słońca
        night_start_angle = rotation_angle - math.pi/2
        night_span_angle = math.pi  # 180 stopni
        
        # Rysowanie obszaru nocy
        night_path = QPainterPath()
        night_path.arcMoveTo(center_x - globe_radius, center_y - globe_radius, 
                            globe_radius * 2, globe_radius * 2, 
                            math.degrees(night_start_angle))
        night_path.arcTo(center_x - globe_radius, center_y - globe_radius, 
                        globe_radius * 2, globe_radius * 2, 
                        math.degrees(night_start_angle), math.degrees(night_span_angle))
        
        # Utworzenie półkola nocy
        night = QGraphicsPathItem(night_path)
        
        # Ustawienie stylu obszaru nocy
        night_pen = QPen(QColor(50, 50, 100))
        night_pen.setWidth(1)
        night.setPen(night_pen)
        
        # Bez wypełnienia dla obszaru nocy
        night.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie do sceny
        night.setZValue(self.base_z_index + 5)  # Nad kulą ziemską, pod kontynentami
        scene.addItem(night)
        
        # Rysowanie linii terminatora (granica dnia i nocy)
        terminator_start_x = center_x + globe_radius * math.cos(night_start_angle)
        terminator_start_y = center_y + globe_radius * math.sin(night_start_angle)
        terminator_end_x = center_x + globe_radius * math.cos(night_start_angle + night_span_angle)
        terminator_end_y = center_y + globe_radius * math.sin(night_start_angle + night_span_angle)
        
        terminator = QGraphicsLineItem(terminator_start_x, terminator_start_y, terminator_end_x, terminator_end_y)
        
        # Ustawienie stylu linii terminatora
        terminator_pen = QPen(QColor(100, 100, 180))
        terminator_pen.setWidth(2)
        terminator_pen.setStyle(Qt.DashLine)
        terminator.setPen(terminator_pen)
        
        # Dodanie do sceny
        terminator.setZValue(self.base_z_index + 6)
        scene.addItem(terminator)
        
        # Dodanie etykiet "Dzień" i "Noc"
        if self.show_labels:
            # Pozycja etykiety "Dzień" (środek dnia)
            day_label_angle = rotation_angle + math.pi/2
            day_label_x = center_x + globe_radius * 0.7 * math.cos(day_label_angle)
            day_label_y = center_y + globe_radius * 0.7 * math.sin(day_label_angle)
            
            # Utworzenie interaktywnego elementu dla dnia
            from widgets.koncentryczne_okregi import InteraktywnyElement
            day_label = InteraktywnyElement(
                day_label_x - 20, day_label_y - 10, 40, 20,
                "DZIEŃ",
                "Obszar Ziemi oświetlony przez Słońce.\nW tej części świata jest teraz dzień."
            )
            
            # Ukrycie tła elementu interaktywnego
            day_label.setPen(QPen(Qt.NoPen))
            day_label.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny
            day_label.setZValue(self.base_z_index + 10)
            scene.addItem(day_label)
            
            # Pozycja etykiety "Noc" (środek nocy)
            night_label_angle = rotation_angle - math.pi/2
            night_label_x = center_x + globe_radius * 0.7 * math.cos(night_label_angle)
            night_label_y = center_y + globe_radius * 0.7 * math.sin(night_label_angle)
            
            # Utworzenie interaktywnego elementu dla nocy
            night_label = InteraktywnyElement(
                night_label_x - 20, night_label_y - 10, 40, 20,
                "NOC",
                "Obszar Ziemi nieoświetlony przez Słońce.\nW tej części świata jest teraz noc."
            )
            
            # Ukrycie tła elementu interaktywnego
            night_label.setPen(QPen(Qt.NoPen))
            night_label.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny
            night_label.setZValue(self.base_z_index + 10)
            scene.addItem(night_label)
    
    def draw_continents(self, scene, center_x, center_y, inner_radius, outer_radius, earth_rotation):
        """Rysowanie kontynentów"""
        # Średni promień kuli ziemskiej
        globe_radius = (inner_radius + outer_radius) / 2
        
        # Kąt obrotu Ziemi w radianach (konwersja ze stopni)
        rotation_angle = math.radians(earth_rotation["rotation_angle"])
        
        # Rysowanie każdego kontynentu
        for continent in self.continents:
            # Kąt kontynentu (uwzględniając obrót Ziemi)
            continent_angle = math.radians(continent["longitude"]) - rotation_angle
            
            # Określenie rozpiętości kątowej kontynentu
            span_angle = math.radians(continent["span"])
            
            # Czy to Antarktyda (specjalny przypadek)
            is_antarctica = continent["name"] == "Antarktyda"
            
            if is_antarctica:
                # Antarktyda jest na biegunie południowym - rysujemy jako czapę polarną
                cap_radius = globe_radius * 0.3  # Mniejszy rozmiar
                antarctica = QGraphicsEllipseItem(
                    center_x - cap_radius, center_y + globe_radius * 0.7 - cap_radius,
                    cap_radius * 2, cap_radius * 2
                )
                
                # Ustawienie stylu - tylko kontur bez wypełnienia
                continent_pen = QPen(QColor(continent["color"]))
                continent_pen.setWidth(1)
                antarctica.setPen(continent_pen)
                antarctica.setBrush(QBrush(Qt.NoBrush))
                
                # Dodanie do sceny
                antarctica.setZValue(self.base_z_index + 8)
                scene.addItem(antarctica)
            else:
                # Rysowanie pozostałych kontynentów jako sektorów koła
                # Tworzymy wielokąt reprezentujący kontynent
                continent_polygon = QPolygonF()
                
                # Dodanie punktu środkowego
                continent_polygon.append(QPointF(center_x, center_y))
                
                # Określenie liczby punktów do narysowania łuku kontynentu
                num_points = 20
                
                # Dodanie punktów łuku
                for i in range(num_points + 1):
                    point_angle = continent_angle - span_angle/2 + i * span_angle / num_points
                    x = center_x + globe_radius * math.cos(point_angle)
                    y = center_y + globe_radius * math.sin(point_angle)
                    continent_polygon.append(QPointF(x, y))
                
                # Utworzenie elementu wielokąta
                continent_item = QGraphicsPolygonItem(continent_polygon)
                
                # Ustawienie stylu - tylko kontur bez wypełnienia
                continent_pen = QPen(QColor(continent["color"]))
                continent_pen.setWidth(1)
                continent_item.setPen(continent_pen)
                continent_item.setBrush(QBrush(Qt.NoBrush))
                
                # Dodanie do sceny
                continent_item.setZValue(self.base_z_index + 7)
                scene.addItem(continent_item)
            
            # Dodanie etykiety kontynentu (opcjonalnie)
            if self.show_labels and not is_antarctica:
                # Środek kontynentu
                label_angle = continent_angle
                label_radius = globe_radius * 0.7  # Nieco bliżej środka
                label_x = center_x + label_radius * math.cos(label_angle)
                label_y = center_y + label_radius * math.sin(label_angle)
                
                # Utworzenie interaktywnego elementu etykiety
                from widgets.koncentryczne_okregi import InteraktywnyElement
                continent_label = InteraktywnyElement(
                    label_x - 30, label_y - 10, 60, 20,
                    continent["name"],
                    f"Kontynent: {continent['name']}\nPołożenie: {continent['longitude']}° długości geograficznej"
                )
                
                # Ukrycie tła elementu interaktywnego
                continent_label.setPen(QPen(Qt.NoPen))
                continent_label.setBrush(QBrush(Qt.NoBrush))
                
                # Dodanie do sceny
                continent_label.setZValue(self.base_z_index + 10)
                scene.addItem(continent_label)
    
    def draw_geographic_grid(self, scene, center_x, center_y, inner_radius, outer_radius, num_meridians=12, num_parallels=6):
        """Rysowanie siatki geograficznej (południki i równoleżniki)"""
        # Średni promień kuli ziemskiej
        globe_radius = (inner_radius + outer_radius) / 2
        
        # Rysowanie południków
        for i in range(num_meridians):
            meridian_angle = 2 * math.pi * i / num_meridians
            
            # Rysowanie linii południka
            meridian = QGraphicsLineItem(
                center_x, center_y - globe_radius,
                center_x, center_y + globe_radius
            )
            
            # Obrót linii południka
            from PyQt5.QtGui import QTransform
            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.rotate(math.degrees(meridian_angle))
            transform.translate(-center_x, -center_y)
            meridian.setTransform(transform)
            
            # Ustawienie stylu południka
            meridian_pen = QPen(QColor(100, 100, 150, 80))  # Półprzezroczysty
            meridian_pen.setWidth(1)
            meridian_pen.setStyle(Qt.DotLine)
            meridian.setPen(meridian_pen)
            
            # Dodanie do sceny
            meridian.setZValue(self.base_z_index + 2)  # Pod kontynentami
            scene.addItem(meridian)
        
        # Rysowanie równoleżników
        for i in range(1, num_parallels):
            # Obliczenie promienia równoleżnika
            parallel_radius = globe_radius * i / num_parallels
            
            # Rysowanie okręgu równoleżnika
            parallel = QGraphicsEllipseItem(
                center_x - parallel_radius, center_y - parallel_radius,
                parallel_radius * 2, parallel_radius * 2
            )
            
            # Ustawienie stylu równoleżnika
            parallel_pen = QPen(QColor(100, 100, 150, 80))  # Półprzezroczysty
            parallel_pen.setWidth(1)
            parallel_pen.setStyle(Qt.DotLine)
            parallel.setPen(parallel_pen)
            parallel.setBrush(QBrush(Qt.NoBrush))  # Bez wypełnienia
            
            # Dodanie do sceny
            parallel.setZValue(self.base_z_index + 2)  # Pod kontynentami
            scene.addItem(parallel)
    
    def draw_cities(self, scene, center_x, center_y, inner_radius, outer_radius, earth_rotation):
        """Rysowanie miast"""
        # Średni promień kuli ziemskiej
        globe_radius = (inner_radius + outer_radius) / 2
        
        # Kąt obrotu Ziemi w radianach (konwersja ze stopni)
        rotation_angle = math.radians(earth_rotation["rotation_angle"])
        
        # Rysowanie każdego miasta
        for city in self.cities:
            # Kąt miasta (uwzględniając obrót Ziemi)
            city_longitude_angle = math.radians(city["longitude"]) - rotation_angle
            
            # Kąt szerokości geograficznej (od równika)
            city_latitude_angle = math.radians(city["latitude"])
            
            # Obliczenie pozycji miasta na kuli ziemskiej
            # Uwzględniamy szerokość geograficzną - miasta na równiku są najdalej od środka
            latitude_factor = math.cos(city_latitude_angle)  # 1 dla równika, 0 dla biegunów
            city_radius = globe_radius * latitude_factor
            
            # Współrzędne miasta
            city_x = center_x + city_radius * math.cos(city_longitude_angle)
            city_y = center_y + city_radius * math.sin(city_longitude_angle)
            
            # Rysowanie punktu miasta
            city_size = 4
            city_point = QGraphicsEllipseItem(
                city_x - city_size/2, city_y - city_size/2,
                city_size, city_size
            )
            
            # Ustawienie stylu punktu miasta
            city_point.setPen(QPen(Qt.NoPen))
            city_point.setBrush(QBrush(QColor(255, 200, 0)))  # Żółty punkt
            
            # Dodanie do sceny
            city_point.setZValue(self.base_z_index + 15)  # Nad wszystkim
            scene.addItem(city_point)
            
            # Dodanie etykiety miasta
            # Utworzenie interaktywnego elementu etykiety
            from widgets.koncentryczne_okregi import InteraktywnyElement
            city_label = InteraktywnyElement(
                city_x - 25, city_y - 10, 50, 20,
                city["name"],
                f"Miasto: {city['name']}\n"
                f"Współrzędne: {city['longitude']}°E, {city['latitude']}°N\n"
                f"Strefa czasowa: {city['timezone']}"
            )
            
            # Ukrycie tła elementu interaktywnego
            city_label.setPen(QPen(Qt.NoPen))
            city_label.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny
            city_label.setZValue(self.base_z_index + 16)
            scene.addItem(city_label)
    
    def draw_time_info(self, scene, center_x, center_y, inner_radius, outer_radius, earth_rotation):
        """Rysowanie informacji o aktualnym czasie"""
        # Określenie położenia panelu informacyjnego
        info_x = center_x - inner_radius * 0.9
        info_y = center_y + inner_radius * 0.5
        info_width = inner_radius * 1.8
        info_height = inner_radius * 0.3
        
        # Formatowanie czasu
        time_str = earth_rotation["date"].strftime("%H:%M:%S")
        
        # Tekst informacyjny
        info_text = f"Czas lokalny: {time_str}\nKąt obrotu: {earth_rotation['rotation_angle']:.1f}°\nNachylenie osi: {earth_rotation['tilt_angle']:.1f}°"
        
        # Utworzenie interaktywnego elementu informacyjnego
        from widgets.koncentryczne_okregi import InteraktywnyElement
        info_element = InteraktywnyElement(
            info_x, info_y, info_width, info_height,
            "Informacje o obrocie Ziemi",
            info_text
        )
        
        # Ustawienie stylu elementu
        info_element.setPen(QPen(QColor(150, 150, 200), 1))
        info_element.setBrush(QBrush(Qt.NoBrush))  # Bez wypełnienia
        
        # Dodanie do sceny
        info_element.setZValue(self.base_z_index + 30)
        scene.addItem(info_element)
        
        # Dodanie tekstu bezpośrednio
        time_display = QGraphicsTextItem(info_text)
        time_display.setPos(info_x + 10, info_y + 10)
        time_display.setDefaultTextColor(QColor(200, 200, 220))
        
        # Ustawienie czcionki
        time_font = QFont("Arial", 8)
        time_display.setFont(time_font)
        
        # Dodanie do sceny
        time_display.setZValue(self.base_z_index + 31)
        scene.addItem(time_display)
    
    def cleanup(self):
        """Czyszczenie zasobów"""
        # W tej implementacji nie ma potrzeby czyszczenia zasobów
        pass