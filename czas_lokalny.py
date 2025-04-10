#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moduł odpowiedzialny za wizualizację czasu lokalnego
Prezentuje klasyczny zegar analogowy i cyfrowy
"""

import math
from datetime import datetime, timezone, timedelta
import pytz
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainterPath

class CzasLokalny:
    """
    Klasa implementująca wizualizację czasu lokalnego
    Wyświetla analogowy zegar z cyfrowym wskaźnikiem czasu
    """
    
    def __init__(self):
        """Inicjalizacja czasu lokalnego"""
        # Aktualna strefa czasowa - domyślnie lokalna
        self.timezone = None
        
        # Opcje wyświetlania
        self.show_labels = True
        self.show_details = True
        self.style = "Klasyczny"
        
        # Base Z-index dla warstw tego systemu
        self.base_z_index = 0
    
    def get_current_time(self):
        """Pobieranie aktualnego czasu"""
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
            else:
                # Dla konkretnych nazw stref czasowych (np. 'Europe/Warsaw')
                try:
                    now = datetime.now(pytz.timezone(self.timezone))
                except:
                    # W przypadku błędu użyj czasu lokalnego
                    pass
        
        return now
    
    def set_timezone(self, timezone):
        """Ustawienie strefy czasowej"""
        self.timezone = timezone
    
    def set_display_options(self, show_labels=True, show_details=False, style="Klasyczny"):
        """Ustawienie opcji wyświetlania"""
        self.show_labels = show_labels
        self.show_details = show_details
        self.style = style
    
    def draw(self, scene, inner_radius, outer_radius):
        """Rysowanie zegara analogowego i cyfrowego"""
        # Pobranie aktualnego czasu
        now = self.get_current_time()
        
        # Rysowanie tła zegara
        self.draw_background(scene, 0, 0, outer_radius - inner_radius)
        
        # Rysowanie podziałki zegara i oznaczenia godzin
        if self.show_labels:
            self.draw_ticks(scene, 0, 0, outer_radius - inner_radius)
            self.draw_hour_numbers(scene, 0, 0, outer_radius - inner_radius)
        
        # Rysowanie wskazówek
        self.draw_hands(scene, 0, 0, outer_radius - inner_radius, now.hour, now.minute, now.second)
        
        # Rysowanie cyfrowego wyświetlacza czasu
        if self.show_details:
            self.draw_digital_display(scene, 0, 0, outer_radius - inner_radius, now)
    
    def draw_background(self, scene, center_x, center_y, radius):
        """Rysowanie tła zegara - tylko kontury, bez wypełnień"""
        # Rysowanie okręgu zegara
        clock_circle = QGraphicsEllipseItem(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Ustawienie stylu - tylko cienki kontur
        pen = QPen(QColor(180, 180, 200))
        pen.setWidth(1)
        clock_circle.setPen(pen)
        clock_circle.setBrush(QBrush(Qt.NoBrush))  # Bez wypełnienia
        
        # Dodanie do sceny z odpowiednim z-indeksem
        clock_circle.setZValue(self.base_z_index)
        scene.addItem(clock_circle)
        
        # Dodanie środkowego punktu (opcjonalnie)
        center_dot = QGraphicsEllipseItem(center_x - 4, center_y - 4, 8, 8)
        center_dot.setPen(QPen(Qt.NoPen))
        center_dot.setBrush(QBrush(QColor(220, 220, 240)))
        center_dot.setZValue(self.base_z_index + 10)  # Wyżej niż tarcza
        scene.addItem(center_dot)
    
    def draw_ticks(self, scene, center_x, center_y, radius):
        """Rysowanie podziałki zegara"""
        # Rysowanie znaczników godzin i minut
        for i in range(60):
            angle = math.radians(i * 6 - 90)  # Kąt w radianach (0 stopni to 3:00)
            
            # Długość i grubość znacznika zależą od tego, czy to znacznik godziny czy minuty
            if i % 5 == 0:  # Znaczniki godzin
                # Dłuższe i grubsze znaczniki dla godzin
                inner_radius = radius * 0.8
                pen_width = 2
                pen_color = QColor(220, 220, 240)
            else:  # Znaczniki minut
                # Krótsze i cieńsze znaczniki dla minut
                inner_radius = radius * 0.85
                pen_width = 1
                pen_color = QColor(150, 150, 170)
            
            # Obliczenie współrzędnych początku i końca linii znacznika
            start_x = center_x + inner_radius * math.cos(angle)
            start_y = center_y + inner_radius * math.sin(angle)
            end_x = center_x + radius * 0.9 * math.cos(angle)
            end_y = center_y + radius * 0.9 * math.sin(angle)
            
            # Utworzenie linii znacznika
            tick = QGraphicsLineItem(start_x, start_y, end_x, end_y)
            
            # Ustawienie stylu
            pen = QPen(pen_color)
            pen.setWidth(pen_width)
            tick.setPen(pen)
            
            # Dodanie do sceny z odpowiednim z-indeksem
            tick.setZValue(self.base_z_index + 1)  # Nad tarczą, pod wskazówkami
            scene.addItem(tick)
    
    def draw_hour_numbers(self, scene, center_x, center_y, radius):
        """Rysowanie znaczników godzinowych bez cyfr - tylko kreski i interaktywne pola"""
        # W miejsce cyfr godzinowych dodajemy interaktywne pola
        for hour in range(1, 13):
            angle = math.radians(hour * 30 - 90)  # Kąt w radianach (0 stopni to 3:00)
            
            # Obliczenie pozycji znacznika godziny
            x = center_x + radius * 0.7 * math.cos(angle)
            y = center_y + radius * 0.7 * math.sin(angle)
            
            # Utworzenie interaktywnego elementu
            from widgets.koncentryczne_okregi import InteraktywnyElement
            hour_marker = InteraktywnyElement(
                x - 10, y - 10, 20, 20,
                f"Godzina {hour}",
                f"Jest to godzina {hour} na zegarze analogowym.\nW tym systemie zegar podzielony jest na 12 godzin."
            )
            
            # Ukrycie kolorowania tła elementu interaktywnego
            hour_marker.setPen(QPen(Qt.NoPen))
            hour_marker.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny z odpowiednim z-indeksem
            hour_marker.setZValue(self.base_z_index + 5)
            scene.addItem(hour_marker)
    
    def draw_hands(self, scene, center_x, center_y, radius, hours, minutes, seconds):
        """Rysowanie wskazówek zegara - znacznie grubszych i dłuższych"""
        # Obliczanie kątów dla wskazówek
        hour_angle = math.radians((hours % 12 + minutes / 60) * 30 - 90)
        minute_angle = math.radians(minutes * 6 - 90)
        second_angle = math.radians(seconds * 6 - 90)
        
        # Rysowanie wskazówki godzinowej (krótsza)
        hour_length = radius * 0.45
        hour_width = 8
        self.draw_hand(
            scene, center_x, center_y, hour_angle, hour_length, 
            hour_width, QColor(220, 220, 250), self.base_z_index + 20, 2
        )
        
        # Rysowanie wskazówki minutowej (dłuższa)
        minute_length = radius * 0.65
        minute_width = 6
        self.draw_hand(
            scene, center_x, center_y, minute_angle, minute_length, 
            minute_width, QColor(200, 200, 250), self.base_z_index + 21, 2
        )
        
        # Rysowanie wskazówki sekundowej (cienka, ale wyraźna)
        second_length = radius * 0.75
        self.draw_second_hand(
            scene, center_x, center_y, second_angle, second_length, 
            QColor(200, 100, 100), self.base_z_index + 22
        )
    
    def draw_hand(self, scene, center_x, center_y, angle, length, width, color, z_value, line_width=2):
        """Rysowanie wskazówki zegara - tylko kontur bez wypełnienia, z opcjonalną grubością"""
        # Obliczenie współrzędnych końca wskazówki
        end_x = center_x + length * math.cos(angle)
        end_y = center_y + length * math.sin(angle)
        
        # Punkty kształtu wskazówki - tworzymy kształt piórkowy zamiast prostej linii
        points = []
        
        # Punkt początkowy (lekko cofnięty za środek)
        back_length = width * 0.5
        back_x = center_x - back_length * math.cos(angle)
        back_y = center_y - back_length * math.sin(angle)
        
        # Obliczanie punktów bocznych (dla grubości)
        side_angle = angle + math.pi/2  # Prostopadle do wskazówki
        side_x = math.cos(side_angle)
        side_y = math.sin(side_angle)
        
        # Dodanie punktów kształtu wskazówki
        points.append(QPointF(back_x + side_x * width/2, back_y + side_y * width/2))
        points.append(QPointF(end_x + side_x * width/6, end_y + side_y * width/6))  # Zwężenie na końcu
        points.append(QPointF(end_x - side_x * width/6, end_y - side_y * width/6))  # Zwężenie na końcu
        points.append(QPointF(back_x - side_x * width/2, back_y - side_y * width/2))
        
        # Utworzenie ścieżki dla wskazówki
        path = QPainterPath()
        path.moveTo(points[0])
        for p in points[1:]:
            path.lineTo(p)
        path.closeSubpath()
        
        # Utworzenie elementu graficznego dla ścieżki
        from PyQt5.QtWidgets import QGraphicsPathItem
        hand = QGraphicsPathItem(path)
        
        # Ustawienie stylu - tylko kontur
        pen = QPen(color)
        pen.setWidth(line_width)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        hand.setPen(pen)
        
        # Bez wypełnienia lub z lekkim wypełnieniem
        if self.style == "Klasyczny":
            hand.setBrush(QBrush(Qt.NoBrush))  # Brak wypełnienia
        else:
            # Lekkie wypełnienie dla innych stylów
            fill_color = QColor(color)
            fill_color.setAlpha(80)  # Półprzezroczyste
            hand.setBrush(QBrush(fill_color))
        
        # Dodanie do sceny z odpowiednim z-indeksem
        hand.setZValue(z_value)
        scene.addItem(hand)
    
    def draw_second_hand(self, scene, center_x, center_y, angle, length, color, z_value):
        """Rysowanie wskazówki sekundowej - znacznie grubszej dla lepszej widoczności"""
        # Obliczenie współrzędnych końca wskazówki
        end_x = center_x + length * math.cos(angle)
        end_y = center_y + length * math.sin(angle)
        
        # Rysowanie linii wskazówki sekundowej
        second_hand = QGraphicsLineItem(center_x, center_y, end_x, end_y)
        
        # Ustawienie stylu - zauważalna czerwona wskazówka
        pen = QPen(color)
        pen.setWidth(2)  # Grubość linii
        pen.setCapStyle(Qt.RoundCap)
        second_hand.setPen(pen)
        
        # Dodanie do sceny z odpowiednim z-indeksem
        second_hand.setZValue(z_value)
        scene.addItem(second_hand)
        
        # Dodanie małego okręgu na końcu wskazówki sekundowej
        tip_size = 4
        tip = QGraphicsEllipseItem(end_x - tip_size/2, end_y - tip_size/2, tip_size, tip_size)
        tip.setPen(QPen(Qt.NoPen))
        tip.setBrush(QBrush(color))
        tip.setZValue(z_value)
        scene.addItem(tip)
    
    def draw_digital_display(self, scene, center_x, center_y, radius, now):
        """Dodanie interaktywnego elementu zamiast cyfrowego wyświetlacza czasu"""
        # Przygotowanie tekstu z aktualnym czasem
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d.%m.%Y")
        time_text = f"{time_str}"
        
        # Utworzenie interaktywnego elementu
        from widgets.koncentryczne_okregi import InteraktywnyElement
        display_width = radius * 0.7
        display_height = 30
        digital_display = InteraktywnyElement(
            center_x - display_width/2, center_y + radius * 0.4 - display_height/2,
            display_width, display_height,
            f"Czas: {time_str}",
            f"Data: {date_str}\nCzas: {time_str}\nStrefa czasowa: {self.timezone or 'Lokalna'}"
        )
        
        # Ustawienie stylu
        pen = QPen(QColor(150, 150, 200))
        pen.setWidth(1)
        digital_display.setPen(pen)
        
        # Bez wypełnienia dla lepszej integracji z interfejsem
        digital_display.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie do sceny z odpowiednim z-indeksem
        digital_display.setZValue(self.base_z_index + 30)
        scene.addItem(digital_display)
        
        # Dodanie tekstu czasu wewnątrz elementu interaktywnego
        time_label = QGraphicsTextItem(time_text)
        time_label.setPos(center_x - time_label.boundingRect().width()/2, 
                         center_y + radius * 0.4 - time_label.boundingRect().height()/2)
        
        font = QFont("Arial", 10)
        time_label.setFont(font)
        time_label.setDefaultTextColor(QColor(220, 220, 240))
        
        time_label.setZValue(self.base_z_index + 31)
        scene.addItem(time_label)
    
    def cleanup(self):
        """Czyszczenie zasobów"""
        # W tej implementacji nie ma potrzeby czyszczenia zasobów
        pass