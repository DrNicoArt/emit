"""
Moduł odpowiedzialny za wizualizację czasu atomowego
Prezentuje precyzyjny czas pobrany z serwera NTP
"""

import threading
import math
import time
from datetime import datetime, timezone, timedelta
import socket

import ntplib
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QRadialGradient

class CzasAtomowy:
    """
    Klasa implementująca wizualizację czasu atomowego
    Synchronizuje się z serwerami czasu NTP i wyświetla precyzyjny czas
    """
    
    def __init__(self):
        """Inicjalizacja czasu atomowego"""
        # Ostatnia synchronizacja z serwerem NTP
        self.last_sync_time = None
        
        # Różnica między czasem lokalnym a NTP (offset)
        self.time_offset = 0
        
        # Status synchronizacji
        self.sync_status = "Niesynchronizowany"
        self.is_sync = False
        
        # Ustawienia kolorów
        self.colors = {
            "background": QColor(30, 30, 60),
            "time_display": QColor(200, 200, 255),
            "precision_indicator": QColor(0, 150, 255),
            "sync_status_ok": QColor(0, 200, 0),
            "sync_status_error": QColor(200, 0, 0),
            "text": QColor(255, 255, 255)
        }
        
        # Aktualna strefa czasowa - domyślnie lokalna
        self.timezone = None
        
        # Opcje wyświetlania
        self.show_labels = True
        self.show_details = True
        self.style = "Klasyczny"
        
        # Utworzenie wątku synchronizacji w tle
        self.sync_thread = threading.Thread(target=self.ntp_sync_loop, daemon=True)
        self.sync_thread.start()
    
    def ntp_sync_loop(self):
        """Wątek synchronizacji z serwerem NTP"""
        while True:
            # Próba synchronizacji z serwerem NTP
            self.sync_with_ntp()
            
            # Synchronizacja co 60 sekund
            time.sleep(60)
    
    def sync_with_ntp(self):
        """Synchronizacja z serwerem NTP"""
        try:
            # Utworzenie klienta NTP
            ntp_client = ntplib.NTPClient()
            
            # Lista serwerów NTP do próby
            ntp_servers = [
                'pool.ntp.org',
                'time.google.com',
                'time.windows.com',
                'time.nist.gov'
            ]
            
            # Próba każdego serwera po kolei
            for server in ntp_servers:
                try:
                    # Próba uzyskania czasu z serwera NTP
                    response = ntp_client.request(server, version=3, timeout=2)
                    
                    # Zapisanie różnicy czasu
                    self.time_offset = response.offset
                    
                    # Aktualizacja statusu synchronizacji
                    self.last_sync_time = datetime.now()
                    self.sync_status = f"Zsynchronizowano z {server}"
                    self.is_sync = True
                    
                    # Sukces - przerywamy pętlę
                    return
                except (ntplib.NTPException, socket.timeout, socket.gaierror):
                    # Próba następnego serwera
                    continue
            
            # Wszystkie serwery zawiodły
            self.sync_status = "Błąd synchronizacji - serwery niedostępne"
            self.is_sync = False
            
        except Exception as e:
            # Ogólny błąd synchronizacji
            self.sync_status = f"Błąd synchronizacji: {str(e)}"
            self.is_sync = False
    
    def get_atomic_time(self):
        """Pobieranie aktualnego czasu atomowego"""
        # Aktualny czas lokalny
        now = datetime.now()
        
        # Zastosowanie przesunięcia czasu z serwera NTP
        atomic_time = now + timedelta(seconds=self.time_offset)
        
        # Zastosowanie strefy czasowej, jeśli została ustawiona
        if self.timezone and self.timezone != "Lokalna":
            if self.timezone.startswith("UTC"):
                # Parsowanie przesunięcia UTC
                try:
                    if "+" in self.timezone:
                        offset = int(self.timezone.split("+")[1])
                        atomic_time = datetime.now(timezone.utc) + timedelta(hours=offset) + timedelta(seconds=self.time_offset)
                    elif "-" in self.timezone:
                        offset = int(self.timezone.split("-")[1])
                        atomic_time = datetime.now(timezone.utc) - timedelta(hours=offset) + timedelta(seconds=self.time_offset)
                    else:
                        atomic_time = datetime.now(timezone.utc) + timedelta(seconds=self.time_offset)
                except Exception:
                    # W przypadku błędu użyj czasu z przesunięciem NTP
                    pass
                    
        return atomic_time
    
    def is_synchronized(self):
        """Sprawdzenie czy czas jest zsynchronizowany"""
        return self.is_sync
    
    def get_sync_status(self):
        """Pobieranie statusu synchronizacji"""
        return self.sync_status
    
    def set_timezone(self, timezone):
        """Ustawienie strefy czasowej"""
        self.timezone = timezone
    
    def set_display_options(self, show_labels=True, show_details=False, style="Klasyczny"):
        """Ustawienie opcji wyświetlania"""
        self.show_labels = show_labels
        self.show_details = show_details
        self.style = style
    
    def draw(self, scene, inner_radius, outer_radius):
        """Rysowanie wizualizacji czasu atomowego"""
        # Obliczenie środka sceny
        center_x = 0
        center_y = 0
        
        # Pobranie aktualnego czasu atomowego
        atomic_time = self.get_atomic_time()
        
        # Rysowanie tła
        self.draw_background(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie wyświetlacza czasu
        self.draw_time_display(scene, center_x, center_y, inner_radius, outer_radius, atomic_time)
        
        # Rysowanie wskaźnika synchronizacji
        self.draw_sync_indicator(scene, center_x, center_y, inner_radius, outer_radius)
        
        # Rysowanie wskaźnika precyzji (milisekundy)
        self.draw_precision_indicator(scene, center_x, center_y, inner_radius, outer_radius, atomic_time)
    
    def draw_background(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie tła dla czasu atomowego - tylko kontury, bez wypełnień"""
        # Obliczenie szerokości pierścienia
        ring_width = outer_radius - inner_radius
        
        # Utworzenie pierścienia tła
        background = QGraphicsEllipseItem(
            center_x - outer_radius, center_y - outer_radius,
            outer_radius * 2, outer_radius * 2
        )
        
        # Wycięcie wewnętrznego koła
        inner_circle = QGraphicsEllipseItem(
            center_x - inner_radius, center_y - inner_radius,
            inner_radius * 2, inner_radius * 2
        )
        
        # Ustawienie pędzli i piór dla tła
        background.setPen(QPen(Qt.NoPen))
        inner_circle.setPen(QPen(Qt.NoPen))
        
        # Brak wypełnienia tła - tylko kontury
        background.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie konturu wewnętrznego
        inner_edge = QGraphicsEllipseItem(
            center_x - inner_radius, center_y - inner_radius,
            inner_radius * 2, inner_radius * 2
        )
        inner_edge.setPen(QPen(QColor(100, 150, 200), 1))
        inner_edge.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie konturu zewnętrznego
        outer_edge = QGraphicsEllipseItem(
            center_x - outer_radius, center_y - outer_radius,
            outer_radius * 2, outer_radius * 2
        )
        outer_edge.setPen(QPen(QColor(100, 150, 200), 1))
        outer_edge.setBrush(QBrush(Qt.NoBrush))
        
        # Dodanie elementów do sceny
        scene.addItem(background)
        scene.addItem(inner_edge)
        scene.addItem(outer_edge)
        
        # Z-index dla tła
        background.setZValue(30)
        inner_edge.setZValue(31)
        outer_edge.setZValue(31)
    
    def draw_time_display(self, scene, center_x, center_y, inner_radius, outer_radius, atomic_time):
        """Rysowanie wyświetlacza czasu atomowego"""
        if not self.show_labels:
            return
        
        # Obliczenie promienia środkowego
        middle_radius = (inner_radius + outer_radius) / 2
        
        # Formatowanie czasu atomowego
        time_text = atomic_time.strftime("%H:%M:%S")
        
        # Dodanie milisekund jeśli pokazujemy szczegóły
        if self.show_details:
            milliseconds = int(atomic_time.microsecond / 1000)
            time_text += f".{milliseconds:03d}"
        
        # Utworzenie pola tekstowego dla czasu
        time_display = QGraphicsTextItem(time_text)
        
        # Ustawienie czcionki i koloru
        font = QFont("Arial", 10)
        font.setBold(True)
        time_display.setFont(font)
        time_display.setDefaultTextColor(self.colors["time_display"])
        
        # Wyśrodkowanie tekstu
        text_width = time_display.boundingRect().width()
        text_height = time_display.boundingRect().height()
        
        # Ustawienie pozycji
        time_display.setPos(
            center_x - text_width / 2,
            center_y - text_height / 2
        )
        
        # Dodanie do sceny
        scene.addItem(time_display)
        time_display.setZValue(35)
        
        # Dla stylu zaawansowanego dodajemy cień pod tekstem
        if self.style == "Zaawansowany":
            # Prostokąt pod tekstem
            text_bg = QGraphicsRectItem(
                center_x - text_width / 1.8,
                center_y - text_height / 1.8,
                text_width * 1.1,
                text_height * 1.1
            )
            text_bg.setPen(QPen(Qt.NoPen))
            text_bg.setBrush(QBrush(QColor(0, 0, 0, 120)))
            scene.addItem(text_bg)
            text_bg.setZValue(34)
    
    def draw_sync_indicator(self, scene, center_x, center_y, inner_radius, outer_radius):
        """Rysowanie wskaźnika synchronizacji"""
        # Obliczenie promienia środkowego
        middle_radius = (inner_radius + outer_radius) / 2
        
        # Pozycja wskaźnika synchronizacji - u dołu pierścienia
        indicator_y = center_y + middle_radius * 0.6
        
        # Kolor wskaźnika zależy od statusu synchronizacji
        indicator_color = self.colors["sync_status_ok"] if self.is_synchronized() else self.colors["sync_status_error"]
        
        # Utworzenie wskaźnika jako kółka
        indicator = QGraphicsEllipseItem(
            center_x - 5, indicator_y - 5,
            10, 10
        )
        
        # Ustawienie koloru
        indicator.setPen(QPen(indicator_color, 1))
        indicator.setBrush(QBrush(indicator_color))
        
        # Dodanie do sceny
        scene.addItem(indicator)
        indicator.setZValue(36)
        
        # Dodanie tekstu statusu, jeśli wyświetlamy szczegóły
        if self.show_details:
            # Tekst statusu
            status_text = self.get_sync_status()
            
            # Utworzenie pola tekstowego
            status_display = QGraphicsTextItem(status_text)
            
            # Ustawienie czcionki i koloru
            font = QFont("Arial", 7)
            status_display.setFont(font)
            status_display.setDefaultTextColor(indicator_color)
            
            # Wyśrodkowanie tekstu
            text_width = status_display.boundingRect().width()
            text_height = status_display.boundingRect().height()
            
            # Ustawienie pozycji pod wskaźnikiem
            status_display.setPos(
                center_x - text_width / 2,
                indicator_y + 10
            )
            
            # Dodanie do sceny
            scene.addItem(status_display)
            status_display.setZValue(36)
    
    def draw_precision_indicator(self, scene, center_x, center_y, inner_radius, outer_radius, atomic_time):
        """Rysowanie wskaźnika precyzji (milisekundy)"""
        if not self.show_details:
            return
        
        # Pobranie części ułamkowej sekundy (milisekundy)
        milliseconds = atomic_time.microsecond / 1000
        
        # Określenie kąta wskazówki milisekundowej (1000ms = pełny obrót)
        angle = 2 * math.pi * milliseconds / 1000
        
        # Obliczenie pozycji końca wskazówki
        radius = (inner_radius + outer_radius) / 2 * 0.8
        tip_x = center_x + radius * math.sin(angle)
        tip_y = center_y - radius * math.cos(angle)
        
        # Rysowanie wskazówki milisekund
        ms_hand = scene.addLine(
            center_x, center_y, tip_x, tip_y,
            QPen(self.colors["precision_indicator"], 2)
        )
        ms_hand.setZValue(36)
        
        # Dodanie okręgu podziałki milisekund
        tick_radius = radius * 1.05
        ticks_circle = scene.addEllipse(
            center_x - tick_radius, center_y - tick_radius,
            tick_radius * 2, tick_radius * 2,
            QPen(self.colors["precision_indicator"], 1),
            QBrush(Qt.NoBrush)
        )
        ticks_circle.setZValue(37)
        
        # Dodanie znaczników co 100ms
        for i in range(10):
            tick_angle = 2 * math.pi * i / 10
            
            # Znacznik wewnętrzny
            inner_tick_radius = tick_radius * 0.95
            outer_tick_radius = tick_radius * 1.05
            
            inner_x = center_x + inner_tick_radius * math.sin(tick_angle)
            inner_y = center_y - inner_tick_radius * math.cos(tick_angle)
            
            outer_x = center_x + outer_tick_radius * math.sin(tick_angle)
            outer_y = center_y - outer_tick_radius * math.cos(tick_angle)
            
            # Używamy int() do konwersji float na int dla parametru width
            pen = QPen(self.colors["precision_indicator"])
            pen.setWidth(2)  # 2 zamiast zmiennoprzecinkowej szerokości
            
            tick = scene.addLine(
                inner_x, inner_y, outer_x, outer_y,
                pen
            )
            tick.setZValue(38)
    
    def cleanup(self):
        """Czyszczenie zasobów"""
        # Nic do czyszczenia, wątek jest daemon
        pass