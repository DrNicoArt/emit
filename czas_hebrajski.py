#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moduł odpowiedzialny za wizualizację czasu hebrajskiego
Prezentuje kalendarz hebrajski z właściwymi podziałami i świętami
"""

import math
from datetime import datetime, timezone, timedelta
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsPathItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainterPath

class CzasHebrajski:
    """
    Klasa implementująca wizualizację czasu hebrajskiego
    Wyświetla kalendarz hebrajski z podziałkami miesięcy i dni
    """
    
    def __init__(self):
        """Inicjalizacja czasu hebrajskiego"""
        # Aktualna strefa czasowa - domyślnie lokalna
        self.timezone = None
        
        # Opcje wyświetlania
        self.show_labels = True
        self.show_details = True
        self.style = "Klasyczny"
        
        # Base Z-index dla warstw tego systemu
        self.base_z_index = 0
        
        # Inicjalizacja danych kalendarza hebrajskiego
        self.init_hebrew_calendar_data()
    
    def init_hebrew_calendar_data(self):
        """Inicjalizacja danych kalendarza hebrajskiego"""
        # Nazwy miesięcy hebrajskich
        self.hebrew_months = [
            "Nisan", "Ijar", "Siwan", "Tamuz", "Aw", "Elul", 
            "Tiszri", "Cheszwan", "Kislew", "Tewet", "Szwat", "Adar"
        ]
        
        # Nazwy miesięcy po hebrajsku
        self.hebrew_month_names = [
            "ניסן", "אייר", "סיון", "תמוז", "אב", "אלול",
            "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר"
        ]
        
        # Liczba dni w miesiącach (uproszczone - w rzeczywistości zależy od roku)
        self.days_in_month = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        
        # Ważne święta hebrajskie
        self.hebrew_holidays = {
            "Pesach": {"month": 0, "day": 15},  # Nisan 15
            "Szawuot": {"month": 2, "day": 6},  # Siwan 6
            "Rosz ha-Szana": {"month": 6, "day": 1},  # Tiszri 1
            "Jom Kipur": {"month": 6, "day": 10},  # Tiszri 10
            "Sukot": {"month": 6, "day": 15},  # Tiszri 15
            "Chanuka": {"month": 8, "day": 25},  # Kislew 25
            "Purim": {"month": 11, "day": 14}  # Adar 14
        }
    
    def get_current_hebrew_date(self):
        """
        Obliczanie bieżącej daty w kalendarzu hebrajskim
        W rzeczywistej implementacji należałoby użyć biblioteki do konwersji kalendarzy
        """
        # Pobieramy aktualną datę
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
        
        # Uproszczona konwersja - w rzeczywistej aplikacji należałoby użyć
        # biblioteki do dokładnej konwersji dat między kalendarzami
        # To jest bardzo uproszczone przybliżenie
        
        # Przykładowe współczynniki przesunięcia - w rzeczywistości to znacznie bardziej skomplikowane
        # Zakładamy, że 1 stycznia 2023 to około 8 Tewet 5783
        
        # Obliczamy dzień roku
        day_of_year = now.timetuple().tm_yday
        
        # Przybliżony miesiąc hebrajski (bardzo uproszczone)
        # Zakładamy, że Nisan (pierwszy miesiąc) zaczyna się około 22 marca
        spring_equinox = 80  # ok. 21 marca to 80 dzień roku
        adjusted_day = (day_of_year - spring_equinox) % 365
        
        # Obliczamy przybliżony miesiąc
        month = 0
        days_passed = 0
        
        for i in range(len(self.days_in_month)):
            if days_passed + self.days_in_month[i] > adjusted_day:
                month = i
                break
            days_passed += self.days_in_month[i]
        
        # Obliczamy dzień miesiąca
        day = adjusted_day - days_passed + 1
        
        # Przybliżony rok hebrajski - w rzeczywistości zależy od daty
        # Dla uproszczenia zakładamy, że rok hebrajski to rok gregoriański + 3760
        year = now.year + 3760
        
        return {
            "year": year,
            "month": month,
            "month_name": self.hebrew_months[month],
            "hebrew_name": self.hebrew_month_names[month],
            "day": day,
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
        """Rysowanie kalendarza hebrajskiego"""
        # Obliczenie środka sceny
        center_x = 0
        center_y = 0
        
        # Pobranie aktualnej daty hebrajskiej
        hebrew_date = self.get_current_hebrew_date()
        
        # Rysowanie pierścienia kalendarza
        self.draw_calendar_ring(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie segmentów miesięcy
        self.draw_month_segments(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie etykiet miesięcy
        if self.show_labels:
            self.draw_month_labels(scene, center_x, center_y, inner_radius, outer_radius, 
                                 self.style == "Szczegółowy")
        
        # Rysowanie znacznika dla aktualnego dnia
        self.draw_current_day_marker(scene, center_x, center_y, inner_radius, outer_radius, hebrew_date)
        
        # Rysowanie szczegółowych informacji o dacie hebrajskiej
        if self.show_details:
            self.draw_detailed_info(scene, center_x, center_y, inner_radius, outer_radius, hebrew_date)
    
    def draw_calendar_ring(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie pierścienia kalendarza - tylko kontury, bez wypełnień"""
        # Rysowanie okręgów granicznych
        inner_circle = QGraphicsEllipseItem(center_x - inner_radius, center_y - inner_radius, 
                                          inner_radius * 2, inner_radius * 2)
        outer_circle = QGraphicsEllipseItem(center_x - outer_radius, center_y - outer_radius, 
                                          outer_radius * 2, outer_radius * 2)
        
        # Ustawienie stylu okręgów
        circle_pen = QPen(QColor(180, 160, 100))
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
    
    def draw_month_segments(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie segmentów miesięcy"""
        # Liczba miesięcy
        num_months = len(self.hebrew_months)
        
        # Kąt dla jednego miesiąca
        month_angle = 360 / num_months
        
        # Rysowanie segmentów dla każdego miesiąca
        for i in range(num_months):
            # Kąt początkowy i końcowy dla miesiąca
            start_angle = i * month_angle
            end_angle = (i + 1) * month_angle
            
            # Rysowanie linii granic miesięcy
            start_angle_rad = math.radians(start_angle)
            inner_x = center_x + inner_radius * math.cos(start_angle_rad)
            inner_y = center_y + inner_radius * math.sin(start_angle_rad)
            outer_x = center_x + outer_radius * math.cos(start_angle_rad)
            outer_y = center_y + outer_radius * math.sin(start_angle_rad)
            
            # Utworzenie linii
            month_line = QGraphicsLineItem(inner_x, inner_y, outer_x, outer_y)
            
            # Ustawienie stylu linii
            line_pen = QPen(QColor(180, 160, 100))
            line_pen.setWidth(1)
            month_line.setPen(line_pen)
            
            # Dodanie do sceny
            month_line.setZValue(self.base_z_index + 1)
            scene.addItem(month_line)
            
            # Tworzenie interaktywnego elementu dla miesiąca
            from widgets.koncentryczne_okregi import InteraktywnyElement
            
            # Obliczenie środka segmentu miesiąca
            mid_angle_rad = math.radians((start_angle + end_angle) / 2)
            mid_radius = (inner_radius + outer_radius) / 2
            mid_x = center_x + mid_radius * math.cos(mid_angle_rad)
            mid_y = center_y + mid_radius * math.sin(mid_angle_rad)
            
            # Rozmiar elementu interaktywnego
            element_size = (outer_radius - inner_radius) * 0.8
            
            # Tworzenie elementu interaktywnego
            month_element = InteraktywnyElement(
                mid_x - element_size/2, mid_y - element_size/2,
                element_size, element_size,
                self.hebrew_months[i],
                f"Miesiąc: {self.hebrew_months[i]} ({self.hebrew_month_names[i]})\n"
                f"Liczba dni: {self.days_in_month[i]}"
            )
            
            # Ukrycie wizualnej reprezentacji elementu interaktywnego
            month_element.setPen(QPen(Qt.NoPen))
            month_element.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny
            month_element.setZValue(self.base_z_index + 2)
            scene.addItem(month_element)
            
            # Rysowanie podziałek dni wewnątrz segmentu miesiąca
            if self.show_details:
                # Liczba dni w miesiącu
                days = self.days_in_month[i]
                
                # Rysowanie podziałek dla każdego dnia
                for day in range(1, days + 1):
                    # Kąt dla podziałki dnia
                    day_angle = start_angle + (day - 0.5) * month_angle / days
                    day_angle_rad = math.radians(day_angle)
                    
                    # Pozycja podziałki - przy zewnętrznym brzegu
                    day_marker_length = (outer_radius - inner_radius) * 0.1
                    start_x = center_x + (outer_radius - day_marker_length) * math.cos(day_angle_rad)
                    start_y = center_y + (outer_radius - day_marker_length) * math.sin(day_angle_rad)
                    end_x = center_x + outer_radius * math.cos(day_angle_rad)
                    end_y = center_y + outer_radius * math.sin(day_angle_rad)
                    
                    # Utworzenie linii podziałki
                    day_marker = QGraphicsLineItem(start_x, start_y, end_x, end_y)
                    
                    # Ustawienie stylu podziałki - cieńsza niż linia miesiąca
                    day_pen = QPen(QColor(160, 140, 80))
                    day_pen.setWidth(1)
                    day_marker.setPen(day_pen)
                    
                    # Dodanie do sceny
                    day_marker.setZValue(self.base_z_index + 2)
                    scene.addItem(day_marker)
                    
                    # Dodanie etykiety dnia dla wybranych dni (np. co 5 dni)
                    if day % 5 == 0 and self.show_labels:
                        # Pozycja etykiety
                        label_x = center_x + (outer_radius - day_marker_length * 1.5) * math.cos(day_angle_rad)
                        label_y = center_y + (outer_radius - day_marker_length * 1.5) * math.sin(day_angle_rad)
                        
                        # Utworzenie etykiety
                        day_label = QGraphicsTextItem(str(day))
                        
                        # Ustawienie czcionki
                        day_font = QFont("Arial", 6)
                        day_label.setFont(day_font)
                        day_label.setDefaultTextColor(QColor(180, 160, 100))
                        
                        # Wyśrodkowanie tekstu
                        br = day_label.boundingRect()
                        day_label.setPos(label_x - br.width()/2, label_y - br.height()/2)
                        
                        # Dodanie do sceny
                        day_label.setZValue(self.base_z_index + 3)
                        scene.addItem(day_label)
    
    def draw_month_labels(self, scene, center_x, center_y, inner_radius, outer_radius, show_hebrew=False):
        """Rysowanie etykiet miesięcy - zastąpione przez interaktywne elementy"""
        # Liczba miesięcy
        num_months = len(self.hebrew_months)
        
        # Kąt dla jednego miesiąca
        month_angle = 360 / num_months
        
        # Rysowanie etykiet dla każdego miesiąca
        for i in range(num_months):
            # Kąt środkowy dla miesiąca
            mid_angle = (i + 0.5) * month_angle
            mid_angle_rad = math.radians(mid_angle)
            
            # Pozycja etykiety - przy zewnętrznym brzegu
            label_radius = outer_radius * 1.05
            label_x = center_x + label_radius * math.cos(mid_angle_rad)
            label_y = center_y + label_radius * math.sin(mid_angle_rad)
            
            # Tekst etykiety
            if show_hebrew:
                label_text = f"{self.hebrew_months[i]} ({self.hebrew_month_names[i]})"
            else:
                label_text = self.hebrew_months[i]
            
            # Utworzenie etykiety
            month_label = QGraphicsTextItem(label_text)
            
            # Ustawienie czcionki
            month_font = QFont("Arial", 8)
            month_label.setFont(month_font)
            month_label.setDefaultTextColor(QColor(200, 180, 120))
            
            # Wyśrodkowanie tekstu
            br = month_label.boundingRect()
            month_label.setPos(label_x - br.width()/2, label_y - br.height()/2)
            
            # Dodanie do sceny
            month_label.setZValue(self.base_z_index + 5)
            scene.addItem(month_label)
            
            # Sprawdzenie, czy w tym miesiącu są święta
            has_holidays = any(holiday_data["month"] == i for holiday_data in self.hebrew_holidays.values())
            
            # Dodanie oznaczenia miesiąca ze świętami
            if has_holidays and self.show_details:
                holiday_marker_size = 5
                marker = QGraphicsEllipseItem(
                    label_x - holiday_marker_size/2, label_y - br.height()/2 - holiday_marker_size - 2,
                    holiday_marker_size, holiday_marker_size
                )
                
                marker.setPen(QPen(Qt.NoPen))
                marker.setBrush(QBrush(QColor(220, 180, 100)))
                
                marker.setZValue(self.base_z_index + 6)
                scene.addItem(marker)
    
    def draw_current_day_marker(self, scene, center_x, center_y, inner_radius, outer_radius, hebrew_date):
        """Rysowanie znacznika dla aktualnego dnia"""
        # Liczba miesięcy
        num_months = len(self.hebrew_months)
        
        # Kąt dla jednego miesiąca
        month_angle = 360 / num_months
        
        # Obliczenie kąta dla aktualnego dnia
        current_month = hebrew_date["month"]
        current_day = hebrew_date["day"]
        
        # Kąt początkowy miesiąca
        month_start_angle = current_month * month_angle
        
        # Kąt dla dnia w miesiącu
        day_angle = month_start_angle + (current_day - 0.5) * month_angle / self.days_in_month[current_month]
        day_angle_rad = math.radians(day_angle)
        
        # Rysowanie linii znacznika aktualnego dnia
        marker_start_x = center_x + inner_radius * math.cos(day_angle_rad)
        marker_start_y = center_y + inner_radius * math.sin(day_angle_rad)
        marker_end_x = center_x + outer_radius * math.cos(day_angle_rad)
        marker_end_y = center_y + outer_radius * math.sin(day_angle_rad)
        
        current_day_line = QGraphicsLineItem(marker_start_x, marker_start_y, marker_end_x, marker_end_y)
        
        # Ustawienie stylu znacznika - grubsza, wyróżniająca się linia
        marker_pen = QPen(QColor(220, 180, 100))
        marker_pen.setWidth(2)
        current_day_line.setPen(marker_pen)
        
        # Dodanie do sceny
        current_day_line.setZValue(self.base_z_index + 10)
        scene.addItem(current_day_line)
        
        # Dodanie punktu znacznika na końcu linii
        marker_size = 6
        current_day_marker = QGraphicsEllipseItem(
            marker_end_x - marker_size/2, marker_end_y - marker_size/2,
            marker_size, marker_size
        )
        
        # Ustawienie stylu punktu
        current_day_marker.setPen(QPen(Qt.NoPen))
        current_day_marker.setBrush(QBrush(QColor(220, 180, 100)))
        
        # Dodanie do sceny
        current_day_marker.setZValue(self.base_z_index + 11)
        scene.addItem(current_day_marker)
        
        # Sprawdzenie, czy aktualny dzień jest świętem
        current_holiday = None
        for holiday_name, holiday_data in self.hebrew_holidays.items():
            if holiday_data["month"] == current_month and holiday_data["day"] == current_day:
                current_holiday = holiday_name
                break
        
        # Jeśli aktualny dzień jest świętem, dodajemy specjalne oznaczenie
        if current_holiday and self.show_details:
            # Rysowanie oznaczenia święta
            holiday_marker_size = 10
            holiday_marker = QGraphicsEllipseItem(
                marker_end_x - holiday_marker_size/2, marker_end_y - holiday_marker_size/2,
                holiday_marker_size, holiday_marker_size
            )
            
            # Ustawienie stylu oznaczenia
            holiday_marker.setPen(QPen(QColor(240, 200, 120), 2))
            holiday_marker.setBrush(QBrush(Qt.NoBrush))
            
            # Dodanie do sceny
            holiday_marker.setZValue(self.base_z_index + 12)
            scene.addItem(holiday_marker)
            
            # Dodanie etykiety święta
            holiday_label = QGraphicsTextItem(current_holiday)
            
            # Pozycja etykiety - na zewnątrz znacznika
            label_x = marker_end_x + holiday_marker_size * 1.5 * math.cos(day_angle_rad)
            label_y = marker_end_y + holiday_marker_size * 1.5 * math.sin(day_angle_rad)
            
            # Ustawienie czcionki
            holiday_font = QFont("Arial", 8, QFont.Bold)
            holiday_label.setFont(holiday_font)
            holiday_label.setDefaultTextColor(QColor(240, 200, 120))
            
            # Wyśrodkowanie tekstu
            br = holiday_label.boundingRect()
            holiday_label.setPos(label_x - br.width()/2, label_y - br.height()/2)
            
            # Dodanie do sceny
            holiday_label.setZValue(self.base_z_index + 13)
            scene.addItem(holiday_label)
    
    def draw_detailed_info(self, scene, center_x, center_y, inner_radius, outer_radius, hebrew_date):
        """Rysowanie szczegółowych informacji o dacie hebrajskiej jako interaktywny element"""
        # Określenie położenia panelu informacyjnego
        info_x = center_x - inner_radius * 0.9
        info_y = center_y - inner_radius * 0.1
        info_width = inner_radius * 1.8
        info_height = inner_radius * 0.3
        
        # Formatowanie daty hebrajskiej
        month_name = hebrew_date["month_name"]
        hebrew_name = hebrew_date["hebrew_name"]
        day = hebrew_date["day"]
        year = hebrew_date["year"]
        
        # Formatowanie daty gregoriańskiej
        gregorian_date = hebrew_date["date"].strftime("%d.%m.%Y")
        
        # Tekst informacyjny
        info_text = f"Data hebrajska: {day} {month_name} {year}\n" + \
                   f"({day} {hebrew_name} {year})\n" + \
                   f"Data gregoriańska: {gregorian_date}"
        
        # Utworzenie interaktywnego elementu informacyjnego
        from widgets.koncentryczne_okregi import InteraktywnyElement
        info_element = InteraktywnyElement(
            info_x, info_y, info_width, info_height,
            "Kalendarz Hebrajski",
            info_text
        )
        
        # Ustawienie stylu elementu
        info_element.setPen(QPen(QColor(200, 180, 120), 1))
        info_element.setBrush(QBrush(Qt.NoBrush))  # Bez wypełnienia
        
        # Dodanie do sceny
        info_element.setZValue(self.base_z_index + 20)
        scene.addItem(info_element)
        
        # Dodanie tekstu bezpośrednio
        date_display = QGraphicsTextItem(info_text)
        date_display.setPos(info_x + 10, info_y + 10)
        date_display.setDefaultTextColor(QColor(220, 200, 140))
        
        # Ustawienie czcionki
        date_font = QFont("Arial", 8)
        date_display.setFont(date_font)
        
        # Dodanie do sceny
        date_display.setZValue(self.base_z_index + 21)
        scene.addItem(date_display)
    
    def cleanup(self):
        """Czyszczenie zasobów"""
        # W tej implementacji nie ma potrzeby czyszczenia zasobów
        pass