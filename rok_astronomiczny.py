#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moduł odpowiedzialny za wizualizację roku astronomicznego
Prezentuje orbitę Ziemi, fazy księżyca, pory roku i znaki zodiaku
"""

import math
import datetime
import calendar
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPathItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainterPath, QRadialGradient

class RokAstronomiczny:
    """
    Klasa implementująca wizualizację roku astronomicznego
    Pokazuje orbitę Ziemi, fazy księżyca, pory roku oraz znaki zodiaku
    """
    
    def __init__(self):
        """Inicjalizacja roku astronomicznego"""
        self.timezone = "Lokalna"  # Domyślnie strefa lokalna
        
        # Opcje wyświetlania
        self.show_labels = True
        self.show_details = False
        self.style = "Klasyczny"
        
        # Inicjalizacja dat równonocy i przesileń (przybliżone wartości)
        # W rzeczywistości należałoby je obliczać w zależności od roku
        self.vernal_equinox = datetime.datetime(datetime.datetime.now().year, 3, 20)  # Równonoc wiosenna (ok. 20 marca)
        self.summer_solstice = datetime.datetime(datetime.datetime.now().year, 6, 21)  # Przesilenie letnie (ok. 21 czerwca)
        self.autumn_equinox = datetime.datetime(datetime.datetime.now().year, 9, 23)  # Równonoc jesienna (ok. 23 września)
        self.winter_solstice = datetime.datetime(datetime.datetime.now().year, 12, 21)  # Przesilenie zimowe (ok. 21 grudnia)
        
        # Znaki zodiaku z datami (przybliżone, w rzeczywistości zmieniają się co roku)
        self.zodiac_signs = [
            {"name": "Baran", "start_date": (3, 21), "end_date": (4, 19), "color": QColor(255, 0, 0, 100)},
            {"name": "Byk", "start_date": (4, 20), "end_date": (5, 20), "color": QColor(0, 255, 0, 100)},
            {"name": "Bliźnięta", "start_date": (5, 21), "end_date": (6, 20), "color": QColor(255, 255, 0, 100)},
            {"name": "Rak", "start_date": (6, 21), "end_date": (7, 22), "color": QColor(0, 0, 255, 100)},
            {"name": "Lew", "start_date": (7, 23), "end_date": (8, 22), "color": QColor(255, 0, 255, 100)},
            {"name": "Panna", "start_date": (8, 23), "end_date": (9, 22), "color": QColor(0, 255, 255, 100)},
            {"name": "Waga", "start_date": (9, 23), "end_date": (10, 22), "color": QColor(128, 0, 128, 100)},
            {"name": "Skorpion", "start_date": (10, 23), "end_date": (11, 21), "color": QColor(128, 0, 0, 100)},
            {"name": "Strzelec", "start_date": (11, 22), "end_date": (12, 21), "color": QColor(0, 128, 0, 100)},
            {"name": "Koziorożec", "start_date": (12, 22), "end_date": (1, 19), "color": QColor(0, 0, 128, 100)},
            {"name": "Wodnik", "start_date": (1, 20), "end_date": (2, 18), "color": QColor(128, 128, 0, 100)},
            {"name": "Ryby", "start_date": (2, 19), "end_date": (3, 20), "color": QColor(0, 128, 128, 100)}
        ]
        
        # Pory roku
        self.seasons = [
            {"name": "Wiosna", "start_date": self.vernal_equinox, "color": QColor(124, 252, 0, 150)},
            {"name": "Lato", "start_date": self.summer_solstice, "color": QColor(255, 165, 0, 150)},
            {"name": "Jesień", "start_date": self.autumn_equinox, "color": QColor(165, 42, 42, 150)},
            {"name": "Zima", "start_date": self.winter_solstice, "color": QColor(135, 206, 250, 150)}
        ]
    
    def get_current_position(self):
        """Obliczenie aktualnej pozycji w roku astronomicznym"""
        now = datetime.datetime.now()
        
        # Dzień roku (1-366)
        day_of_year = now.timetuple().tm_yday
        
        # Konwersja na kąt (0-360 stopni)
        # Zakładamy, że rok zaczyna się w punkcie orbity odpowiadającym przesileniu zimowemu (ziemia jest najbliżej Słońca)
        angle = (day_of_year / 365.25) * 360
        
        # Obliczenie aktualnej pory roku
        current_season = None
        for i, season in enumerate(self.seasons):
            next_i = (i + 1) % len(self.seasons)
            next_season = self.seasons[next_i]
            
            # Sprawdzenie czy aktualna data jest pomiędzy początkiem bieżącej pory roku a początkiem następnej
            # (z uwzględnieniem przejścia roku)
            if i == len(self.seasons) - 1:  # Zima
                if now >= season["start_date"] or now < next_season["start_date"]:
                    current_season = season
                    break
            else:
                if season["start_date"] <= now < next_season["start_date"]:
                    current_season = season
                    break
        
        # Jeśli nie udało się określić pory roku, przyjmujemy zimę
        if not current_season:
            current_season = self.seasons[3]  # Zima
        
        # Obliczenie aktualnego znaku zodiaku
        current_zodiac = None
        for sign in self.zodiac_signs:
            start_month, start_day = sign["start_date"]
            end_month, end_day = sign["end_date"]
            
            # Sprawdzenie czy aktualna data mieści się w zakresie znaku
            # (z uwzględnieniem przejścia roku dla Koziorożca)
            if start_month > end_month:  # Przejście przez koniec roku (Koziorożec)
                if (now.month == start_month and now.day >= start_day) or \
                   (now.month == end_month and now.day <= end_day) or \
                   (start_month < now.month <= 12) or \
                   (1 <= now.month < end_month):
                    current_zodiac = sign
                    break
            else:
                if (now.month == start_month and now.day >= start_day) or \
                   (now.month == end_month and now.day <= end_day) or \
                   (start_month < now.month < end_month):
                    current_zodiac = sign
                    break
        
        # Jeśli nie udało się określić znaku zodiaku, przyjmujemy Barana
        if not current_zodiac:
            current_zodiac = self.zodiac_signs[0]  # Baran
            
        return {
            "day_of_year": day_of_year,
            "angle": angle,
            "current_season": current_season,
            "current_zodiac": current_zodiac
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
        """Rysowanie wizualizacji roku astronomicznego"""
        # Obliczenie środka sceny
        center_x = 0
        center_y = 0
        
        # Pobranie aktualnej pozycji astronomicznej
        position = self.get_current_position()
        
        # Rysowanie tła (ciemny kosmos)
        self.draw_background(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie Słońca w środku
        self.draw_sun(scene, center_x, center_y, inner_radius)
        
        # Rysowanie orbity Ziemi
        self.draw_earth_orbit(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie podziałki roku (miesiące)
        if self.show_labels:
            self.draw_month_markers(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie oznaczeń pór roku
        self.draw_seasons(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie znaków zodiaku
        if self.show_details:
            self.draw_zodiac(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie aktualnej pozycji Ziemi na orbicie
        self.draw_earth_position(scene, center_x, center_y, inner_radius, outer_radius, position)
        
        # Rysowanie informacji o aktualnej porze roku i znaku zodiaku
        if self.show_details:
            self.draw_current_info(scene, center_x, center_y, inner_radius, outer_radius, position)
    
    def draw_background(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie tła - kosmicznej przestrzeni"""
        # Promień zewnętrznego koła
        radius = outer_radius
        
        # Rysowanie tła jako koła wypełnionego gradientem
        background = QGraphicsEllipseItem(
            center_x - radius, center_y - radius,
            radius * 2, radius * 2
        )
        
        # Brak wypełnienia tła - tylko kontur
        background.setBrush(QBrush(Qt.NoBrush))
        
        # Brak obramowania
        background.setPen(QPen(Qt.NoPen))
        
        # Dodanie do sceny
        scene.addItem(background)
        background.setZValue(10)  # Z-index dla tła
        
        # Dodanie wewnętrznego kręgu
        inner_circle = QGraphicsEllipseItem(
            center_x - inner_radius, center_y - inner_radius,
            inner_radius * 2, inner_radius * 2
        )
        inner_circle.setPen(QPen(QColor(50, 50, 80), 1))
        inner_circle.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie do sceny
        scene.addItem(inner_circle)
        inner_circle.setZValue(11)
    
    def draw_sun(self, scene, center_x, center_y, inner_radius):
        """Rysowanie Słońca w środku układu"""
        # Promień Słońca (mniejszy niż wewnętrzny promień pierścienia)
        sun_radius = inner_radius * 0.7
        
        # Rysowanie Słońca jako koła z gradientem
        sun = QGraphicsEllipseItem(
            center_x - sun_radius, center_y - sun_radius,
            sun_radius * 2, sun_radius * 2
        )
        
        # Gradient dla Słońca - od żółtego do pomarańczowego
        gradient = QRadialGradient(center_x, center_y, sun_radius)
        gradient.setColorAt(0, QColor(255, 255, 200))  # Jasny żółty w środku
        gradient.setColorAt(0.7, QColor(255, 200, 50))  # Żółty
        gradient.setColorAt(1, QColor(255, 140, 0))    # Pomarańczowy na krawędzi
        
        sun.setBrush(QBrush(Qt.NoBrush))
        sun.setPen(QPen(QColor(255, 140, 0, 150), 1))
        
        # Dodanie do sceny
        scene.addItem(sun)
        sun.setZValue(15)  # Z-index dla Słońca (wyższy niż tło)
    
    def draw_earth_orbit(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie orbity Ziemi"""
        # Średni promień pierścienia - to będzie promień orbity
        orbit_radius = (inner_radius + outer_radius) / 2
        
        # Rysowanie orbity jako okręgu
        orbit = QGraphicsEllipseItem(
            center_x - orbit_radius, center_y - orbit_radius,
            orbit_radius * 2, orbit_radius * 2
        )
        
        # Ustawienie stylu orbity
        orbit.setPen(QPen(QColor(100, 100, 150), 1, Qt.DashLine))
        orbit.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie do sceny
        scene.addItem(orbit)
        orbit.setZValue(12)  # Z-index dla orbity (nad tłem, pod Ziemią)
    
    def draw_month_markers(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie znaczników miesięcy"""
        # Średni promień pierścienia
        orbit_radius = (inner_radius + outer_radius) / 2
        
        # Nazwy miesięcy
        month_names = [
            "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
            "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
        ]
        
        # Rysowanie znaczników dla każdego miesiąca
        for i, month_name in enumerate(month_names):
            # Kąt dla danego miesiąca (0 stopni = początek stycznia)
            angle = math.radians(i * 30)  # 360 / 12 = 30 stopni na miesiąc
            
            # Obliczenie pozycji znacznika
            marker_x = center_x + orbit_radius * math.cos(angle)
            marker_y = center_y + orbit_radius * math.sin(angle)
            
            # Rysowanie znacznika jako małego punktu
            marker = QGraphicsEllipseItem(
                marker_x - 2, marker_y - 2, 4, 4
            )
            marker.setBrush(QBrush(QColor(200, 200, 255)))
            marker.setPen(QPen(Qt.NoPen))
            
            # Dodanie do sceny
            scene.addItem(marker)
            marker.setZValue(13)
            
            # Dodanie etykiety z nazwą miesiąca
            if self.show_labels:
                # Pozycja etykiety (nieco dalej od znacznika)
                label_radius = orbit_radius * 1.1
                label_x = center_x + label_radius * math.cos(angle)
                label_y = center_y + label_radius * math.sin(angle)
                
                # Utworzenie etykiety
                label = QGraphicsTextItem(month_name)
                
                # Ustawienie czcionki i koloru
                font = QFont("Arial", 6)
                label.setFont(font)
                label.setDefaultTextColor(QColor(200, 200, 255))
                
                # Obliczenie szerokości tekstu dla właściwego wyśrodkowania
                text_width = label.boundingRect().width()
                text_height = label.boundingRect().height()
                
                # Ustawienie pozycji z uwzględnieniem szerokości tekstu
                label.setPos(label_x - text_width / 2, label_y - text_height / 2)
                
                # Dodanie do sceny
                scene.addItem(label)
                label.setZValue(13)
    
    def draw_seasons(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie oznaczeń pór roku"""
        # Średni promień pierścienia
        orbit_radius = (inner_radius + outer_radius) / 2
        
        # Pozycje równonocy i przesileń (kąty w stopniach)
        # Zakładamy, że rok zaczyna się od przesilenia zimowego (ok. 21 grudnia)
        vernal_equinox_angle = math.radians(90)    # Równonoc wiosenna (ok. 20 marca)
        summer_solstice_angle = math.radians(180)  # Przesilenie letnie (ok. 21 czerwca)
        autumn_equinox_angle = math.radians(270)   # Równonoc jesienna (ok. 23 września)
        winter_solstice_angle = math.radians(0)    # Przesilenie zimowe (ok. 21 grudnia)
        
        # Rysowanie znaczników dla punktów równonocy i przesileń
        solstice_points = [
            {"name": "Przesilenie zimowe", "angle": winter_solstice_angle, "color": QColor(135, 206, 250)},  # Jasny niebieski
            {"name": "Równonoc wiosenna", "angle": vernal_equinox_angle, "color": QColor(124, 252, 0)},      # Jasny zielony
            {"name": "Przesilenie letnie", "angle": summer_solstice_angle, "color": QColor(255, 165, 0)},    # Pomarańczowy
            {"name": "Równonoc jesienna", "angle": autumn_equinox_angle, "color": QColor(165, 42, 42)}       # Brązowy
        ]
        
        for point in solstice_points:
            # Obliczenie pozycji znacznika
            marker_x = center_x + orbit_radius * math.cos(point["angle"])
            marker_y = center_y + orbit_radius * math.sin(point["angle"])
            
            # Rysowanie znacznika jako wyraźniejszego punktu
            marker = QGraphicsEllipseItem(
                marker_x - 3, marker_y - 3, 6, 6
            )
            marker.setBrush(QBrush(point["color"]))
            marker.setPen(QPen(QColor(255, 255, 255), 1))
            
            # Dodanie do sceny
            scene.addItem(marker)
            marker.setZValue(14)
            
            # Dodanie etykiety dla punktu
            if self.show_labels:
                # Pozycja etykiety (nieco dalej od znacznika)
                label_radius = orbit_radius * 0.85
                label_x = center_x + label_radius * math.cos(point["angle"])
                label_y = center_y + label_radius * math.sin(point["angle"])
                
                # Utworzenie etykiety
                label = QGraphicsTextItem(point["name"])
                
                # Ustawienie czcionki i koloru
                font = QFont("Arial", 6)
                font.setBold(True)
                label.setFont(font)
                label.setDefaultTextColor(point["color"])
                
                # Obliczenie szerokości tekstu dla właściwego wyśrodkowania
                text_width = label.boundingRect().width()
                text_height = label.boundingRect().height()
                
                # Ustawienie pozycji z uwzględnieniem szerokości tekstu
                label.setPos(label_x - text_width / 2, label_y - text_height / 2)
                
                # Dodanie do sceny
                scene.addItem(label)
                label.setZValue(14)
    
    def draw_zodiac(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie znaków zodiaku"""
        if not self.show_details:
            return
            
        # Różnica między promieniami
        radius_diff = outer_radius - inner_radius
        
        # Zewnętrzny promień dla segmentów zodiaku
        zodiac_radius = outer_radius - radius_diff * 0.1
        
        # Szerokość pierścienia zodiaku
        zodiac_width = radius_diff * 0.2
        
        # Rysowanie segmentów dla każdego znaku zodiaku
        for i, sign in enumerate(self.zodiac_signs):
            # Kąt początkowy i końcowy (każdy znak zajmuje 30 stopni)
            start_angle = i * 30
            span_angle = 30
            
            # Rysowanie segmentu dla znaku
            zodiac_segment = QGraphicsEllipseItem(
                center_x - zodiac_radius, center_y - zodiac_radius,
                zodiac_radius * 2, zodiac_radius * 2
            )
            
            # Ustawienie pióra i pędzla
            segment_pen = QPen(Qt.NoPen)
            zodiac_segment.setPen(segment_pen)
            
            # Tworzymy ścieżkę dla wypełnienia tylko części pierścienia
            path = QPainterPath()
            path.arcMoveTo(center_x - zodiac_radius, center_y - zodiac_radius,
                         zodiac_radius * 2, zodiac_radius * 2, start_angle)
            path.arcTo(center_x - zodiac_radius, center_y - zodiac_radius,
                      zodiac_radius * 2, zodiac_radius * 2, start_angle, span_angle)
            
            # Dodanie wewnętrznego łuku
            inner_zodiac_radius = zodiac_radius - zodiac_width
            path.arcTo(center_x - inner_zodiac_radius, center_y - inner_zodiac_radius,
                      inner_zodiac_radius * 2, inner_zodiac_radius * 2, 
                      start_angle + span_angle, -span_angle)
            
            path.closeSubpath()
            
            # Utworzenie elementu ścieżki
            segment_item = QGraphicsPathItem(path)
            segment_item.setPen(QPen(Qt.NoPen))
            segment_item.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny
            scene.addItem(segment_item)
            segment_item.setZValue(11)  # Pod orbitą ziemi
            
            # Dodanie etykiety znaku
            if self.show_labels:
                # Kąt środkowy znaku
                mid_angle = math.radians(start_angle + span_angle / 2)
                
                # Pozycja etykiety
                label_radius = zodiac_radius - zodiac_width / 2
                label_x = center_x + label_radius * math.cos(mid_angle)
                label_y = center_y + label_radius * math.sin(mid_angle)
                
                # Utworzenie etykiety
                label = QGraphicsTextItem(sign["name"])
                
                # Ustawienie czcionki i koloru
                font = QFont("Arial", 6)
                label.setFont(font)
                label.setDefaultTextColor(QColor(255, 255, 255))
                
                # Obliczenie szerokości tekstu dla właściwego wyśrodkowania
                text_width = label.boundingRect().width()
                text_height = label.boundingRect().height()
                
                # Ustawienie pozycji z uwzględnieniem szerokości tekstu
                label.setPos(label_x - text_width / 2, label_y - text_height / 2)
                
                # Dodanie do sceny
                scene.addItem(label)
                label.setZValue(12)
    
    def draw_earth_position(self, scene, center_x, center_y, inner_radius, outer_radius, position):
        """Rysowanie aktualnej pozycji Ziemi na orbicie"""
        # Średni promień pierścienia - to będzie promień orbity
        orbit_radius = (inner_radius + outer_radius) / 2
        
        # Kąt pozycji Ziemi (w radianach)
        angle = math.radians(position["angle"])
        
        # Obliczenie pozycji Ziemi na orbicie
        earth_x = center_x + orbit_radius * math.cos(angle)
        earth_y = center_y + orbit_radius * math.sin(angle)
        
        # Promień planety Ziemia
        earth_radius = (outer_radius - inner_radius) * 0.15
        
        # Rysowanie Ziemi jako koła
        earth = QGraphicsEllipseItem(
            earth_x - earth_radius, earth_y - earth_radius,
            earth_radius * 2, earth_radius * 2
        )
        
        # Gradient dla Ziemi - niebieski z zielonymi kontynentami
        gradient = QRadialGradient(earth_x, earth_y, earth_radius)
        gradient.setColorAt(0, QColor(0, 100, 255))  # Niebieski (oceany)
        gradient.setColorAt(0.5, QColor(0, 120, 255))
        gradient.setColorAt(0.8, QColor(0, 80, 200))
        
        earth.setBrush(QBrush(Qt.NoBrush))
        earth.setPen(QPen(QColor(255, 255, 255, 150), 1))
        
        # Dodanie do sceny
        scene.addItem(earth)
        earth.setZValue(20)  # Z-index dla Ziemi (wyższy niż wszystko inne)
    
    def draw_current_info(self, scene, center_x, center_y, inner_radius, outer_radius, position):
        """Rysowanie informacji o aktualnej porze roku i znaku zodiaku"""
        if not self.show_details:
            return
            
        # Pobranie aktualnych danych
        current_season = position["current_season"]
        current_zodiac = position["current_zodiac"]
        
        # Tekst do wyświetlenia
        info_text = f"Pora roku: {current_season['name']}\nZnak zodiaku: {current_zodiac['name']}"
        
        # Utworzenie pola tekstowego
        info_display = QGraphicsTextItem(info_text)
        
        # Ustawienie czcionki i koloru
        font = QFont("Arial", 8)
        info_display.setFont(font)
        info_display.setDefaultTextColor(QColor(255, 255, 255))
        
        # Pozycja tekstu - u dołu pierścienia
        info_y = center_y + outer_radius * 0.8
        
        # Obliczenie szerokości tekstu dla właściwego wyśrodkowania
        text_width = info_display.boundingRect().width()
        
        # Ustawienie pozycji
        info_display.setPos(center_x - text_width / 2, info_y)
        
        # Dodanie do sceny
        scene.addItem(info_display)
        info_display.setZValue(25)  # Na wierzchu
    
    def cleanup(self):
        """Czyszczenie zasobów"""
        # Brak zasobów do czyszczenia
        pass