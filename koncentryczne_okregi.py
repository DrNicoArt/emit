#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget głównej wizualizacji koncentrycznych okręgów
Odpowiada za rysowanie wszystkich systemów czasowych
"""

import math
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QFont, QPainterPath

# Klasa interaktywnego elementu
class InteraktywnyElement(QGraphicsEllipseItem):
    """
    Klasa reprezentująca interaktywny element okręgu, który reaguje na najechanie myszą i kliknięcie
    """
    def __init__(self, x, y, width, height, text, details, parent=None):
        super().__init__(x, y, width, height, parent)
        self.text = text
        self.details = details
        self.setCursor(Qt.PointingHandCursor)
        self.setAcceptHoverEvents(True)
        self.info_text = None
        
    def hoverEnterEvent(self, event):
        """Obsługa najechania myszą na element"""
        # Tworzenie tekstu informacyjnego
        if not self.info_text:
            # Tworzymy prostokąt z informacją po prawej stronie całego widoku
            scene = self.scene()
            if scene:
                scene_width = scene.width()
                scene_height = scene.height()
                
                info_font = QFont("Arial", 12)
                self.info_text = QGraphicsTextItem(self.text)
                self.info_text.setFont(info_font)
                self.info_text.setDefaultTextColor(QColor(255, 255, 255))
                
                # Pozycja w prawym górnym rogu
                text_width = self.info_text.boundingRect().width()
                self.info_text.setPos(scene_width/4 - text_width/2, -scene_height/3)
                self.info_text.setZValue(1000)  # Zawsze na wierzchu
                scene.addItem(self.info_text)
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        """Obsługa opuszczenia elementu przez mysz"""
        if self.info_text:
            scene = self.scene()
            if scene:
                scene.removeItem(self.info_text)
                self.info_text = None
        super().hoverLeaveEvent(event)
        
    def mousePressEvent(self, event):
        """Obsługa kliknięcia na element"""
        scene = self.scene()
        if scene:
            # Usunięcie istniejących szczegółowych informacji
            if hasattr(scene, 'detail_text') and scene.detail_text:
                scene.removeItem(scene.detail_text)
                
            # Dodanie szczegółowych informacji
            detail_font = QFont("Arial", 10)
            scene.detail_text = QGraphicsTextItem(self.details)
            scene.detail_text.setFont(detail_font)
            scene.detail_text.setDefaultTextColor(QColor(220, 220, 255))
            
            # Pozycja w prawej dolnej części
            scene_width = scene.width()
            scene_height = scene.height()
            text_width = scene.detail_text.boundingRect().width()
            scene.detail_text.setPos(scene_width/4 - text_width/2, scene_height/3)
            scene.detail_text.setZValue(1000)  # Zawsze na wierzchu
            scene.addItem(scene.detail_text)
        super().mousePressEvent(event)

# Import systemów czasowych
from systemy_czasowe.czas_lokalny import CzasLokalny
from systemy_czasowe.czas_hebrajski import CzasHebrajski
from systemy_czasowe.czas_atomowy import CzasAtomowy
from systemy_czasowe.czas_pulsarowy import CzasPulsarowy
from systemy_czasowe.obrot_ziemi import ObrotZiemi
from systemy_czasowe.rok_astronomiczny import RokAstronomiczny

class KoncentryczneOkregi(QGraphicsView):
    """
    Główny widget wizualizacji koncentrycznych okręgów czasu
    """
    
    # Sygnał informujący o zmianie stanu systemu
    system_toggled = pyqtSignal(str, bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Konfiguracja widoku
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        # Utworzenie sceny
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # Inicjalizacja systemów czasowych
        self.init_systems()
        
        # Konfiguracja timera dla aktualizacji - zwiększona częstotliwość
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_visualization)
        self.update_timer.start(100)  # Aktualizacja 10 razy na sekundę dla płynności
        
        # Śledzenie pozycji kliknięcia do interakcji
        self.last_click_pos = None
        
        # Zmienne kontrolujące zoom
        self.zoom_factor = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        
        # Stan widoczności systemów
        self.visible_systems = {
            'local_time': True,
            'hebrew_time': True,
            'atomic_time': True,
            'pulsar_time': True,
            'earth_rotation': True,
            'astronomical_year': True
        }
        
        # Opcje wyświetlania
        self.show_details = True
        self.show_labels = True
        self.style = "Klasyczny"  # Klasyczny, Minimalistyczny, Szczegółowy
        
        # Aktualna strefa czasowa
        self.timezone = "Lokalna"
        
        # Stan animacji
        self.animation_paused = False
    
    def init_systems(self):
        """Inicjalizacja wszystkich systemów czasowych"""
        # Utworzenie instancji systemów czasowych
        self.systems = {
            'local_time': {'instance': CzasLokalny(), 'z_index': 100, 'name': 'Czas Lokalny'},
            'hebrew_time': {'instance': CzasHebrajski(), 'z_index': 200, 'name': 'Czas Hebrajski'},
            'atomic_time': {'instance': CzasAtomowy(), 'z_index': 300, 'name': 'Czas Atomowy'},
            'pulsar_time': {'instance': CzasPulsarowy(), 'z_index': 400, 'name': 'Czas Pulsarowy'},
            'earth_rotation': {'instance': ObrotZiemi(), 'z_index': 500, 'name': 'Obrót Ziemi'},
            'astronomical_year': {'instance': RokAstronomiczny(), 'z_index': 600, 'name': 'Rok Astronomiczny'}
        }
        
        # Inicjalizacja bazowych Z-indeksów dla każdego systemu
        for system_id, system_data in self.systems.items():
            system_data['instance'].base_z_index = system_data['z_index']
    
    def update_visualization(self):
        """Aktualizacja wizualizacji - odświeżenie sceny"""
        if not self.animation_paused:
            # Czyszczenie sceny przed ponownym rysowaniem
            self.scene.clear()
            
            # Pobranie aktualnego rozmiaru widoku
            size = min(self.width(), self.height()) * 0.9 * self.zoom_factor
            
            # Rysowanie tła
            self.draw_background(size)
            
            # Rysowanie siatki pomocniczej (opcjonalnie)
            if self.show_labels:
                self.draw_grid(size)
            
            # Rysowanie separatorów między systemami
            self.draw_separators(size)
            
            # Rysowanie systemów czasowych w odpowiedniej kolejności
            # Kolejność: czas lokalny (wewnętrzny) -> rok astronomiczny (zewnętrzny)
            system_order = ['local_time', 'hebrew_time', 'atomic_time', 'pulsar_time', 'earth_rotation', 'astronomical_year']
            
            inner_radius = size * 0.1  # Początkowy promień wewnętrzny
            
            for system_id in system_order:
                if self.visible_systems[system_id]:
                    # Dla każdego systemu zwiększamy promień
                    outer_radius = inner_radius + size * 0.1
                    self.draw_system(system_id, inner_radius, outer_radius, size)
                    inner_radius = outer_radius  # Kolejny system zaczyna się tam, gdzie kończy się poprzedni
    
    def draw_background(self, size):
        """Rysowanie tła sceny"""
        # Główne tło - ciemny gradient radialny
        gradient = QRadialGradient(0, 0, size)
        gradient.setColorAt(0, QColor(35, 35, 50))
        gradient.setColorAt(1, QColor(20, 20, 30))
        
        # Rysowanie tła jako dużego prostokąta
        self.scene.setBackgroundBrush(QBrush(gradient))
        self.scene.setSceneRect(-size, -size, size * 2, size * 2)
    
    def draw_separators(self, size):
        """Rysowanie linii separujących między systemami czasowymi"""
        # Promienie dla poszczególnych systemów
        radii = [size * 0.1, size * 0.2, size * 0.3, size * 0.4, size * 0.5, size * 0.6]
        
        # Rysowanie okręgów separujących
        for i, radius in enumerate(radii):
            if i < len(radii) - 1:  # Nie rysujemy separatora po ostatnim systemie
                separator = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
                separator.setPen(QPen(QColor(50, 50, 70), 1))
                separator.setBrush(QBrush(Qt.NoBrush))
                separator.setZValue(50)  # Z-index dla separatorów
                self.scene.addItem(separator)
    
    def draw_grid(self, size):
        """Rysowanie subtelnej siatki pomocniczej"""
        # Rysowanie linii siatki
        grid_color = QColor(40, 40, 60)
        grid_pen = QPen(grid_color, 0.5, Qt.DotLine)
        
        # Linie poziome i pionowe
        for i in range(-5, 6):
            # Linie poziome
            line = self.scene.addLine(-size, i * size / 5, size, i * size / 5, grid_pen)
            line.setZValue(10)
            
            # Linie pionowe
            line = self.scene.addLine(i * size / 5, -size, i * size / 5, size, grid_pen)
            line.setZValue(10)
    
    def draw_system(self, system_id, inner_radius, outer_radius, size):
        """Rysowanie konkretnego systemu czasowego"""
        if system_id in self.systems and self.visible_systems[system_id]:
            system = self.systems[system_id]['instance']
            
            # Ustawienie opcji wyświetlania
            system.set_display_options(self.show_labels, self.show_details, self.style)
            
            # Ustawienie strefy czasowej
            system.set_timezone(self.timezone)
            
            # Wywołanie metody draw konkretnego systemu
            system.draw(self.scene, inner_radius, outer_radius)
    
    def toggle_system(self, system_id, visible):
        """Włączanie/wyłączanie widoczności danego systemu czasowego"""
        if system_id in self.visible_systems:
            self.visible_systems[system_id] = visible
            
            # Emisja sygnału o zmianie stanu systemu
            self.system_toggled.emit(system_id, visible)
            
            # Odświeżenie wizualizacji
            self.update_visualization()
    
    def update_timezone(self, timezone):
        """Aktualizacja strefy czasowej we wszystkich systemach"""
        self.timezone = timezone
        
        # Przekazanie nowej strefy czasowej do wszystkich systemów
        for system_id, system_data in self.systems.items():
            system_data['instance'].set_timezone(timezone)
        
        # Odświeżenie wizualizacji
        self.update_visualization()
    
    def reset_view(self):
        """Przywrócenie domyślnego widoku"""
        self.resetTransform()
        self.zoom_factor = 1.0
        
        # Reset widoczności systemów
        for system_id in self.visible_systems:
            self.visible_systems[system_id] = True
            self.system_toggled.emit(system_id, True)
        
        # Reset opcji wyświetlania
        self.show_details = True
        self.show_labels = True
        self.style = "Klasyczny"
        
        # Aktualizacja wszystkich systemów
        for system_id, system_data in self.systems.items():
            system_data['instance'].set_display_options(self.show_labels, self.show_details, self.style)
        
        # Odświeżenie wizualizacji
        self.update_visualization()
    
    def zoom_in(self):
        """Przybliżenie widoku"""
        if self.zoom_factor < self.max_zoom:
            scale_factor = 1.2
            self.zoom_factor *= scale_factor
            self.scale(scale_factor, scale_factor)
            self.update_visualization()
    
    def zoom_out(self):
        """Oddalenie widoku"""
        if self.zoom_factor > self.min_zoom:
            scale_factor = 1 / 1.2
            self.zoom_factor *= scale_factor
            self.scale(scale_factor, scale_factor)
            self.update_visualization()
    
    def wheelEvent(self, event):
        """Obsługa zdarzenia przewijania kółkiem myszy (zoom)"""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        # Zoom in/out zależnie od kierunku przewijania
        if event.angleDelta().y() > 0 and self.zoom_factor < self.max_zoom:
            self.zoom_factor *= zoom_in_factor
            self.scale(zoom_in_factor, zoom_in_factor)
        elif event.angleDelta().y() < 0 and self.zoom_factor > self.min_zoom:
            self.zoom_factor *= zoom_out_factor
            self.scale(zoom_out_factor, zoom_out_factor)
        
        self.update_visualization()
    
    def mousePressEvent(self, event):
        """Obsługa kliknięcia myszy - interakcja z wizualizacją"""
        # Zapisanie pozycji kliknięcia do dalszego wykorzystania
        self.last_click_pos = self.mapToScene(event.pos())
        
        # Standardowa obsługa zdarzenia (przesuwanie widoku)
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        """Obsługa zdarzenia zmiany rozmiaru widgetu"""
        # Dopasowanie sceny do nowego rozmiaru
        self.update_visualization()
        super().resizeEvent(event)
    
    def cleanup(self):
        """Czyszczenie zasobów przy zamknięciu"""
        # Zatrzymanie timera
        self.update_timer.stop()
        
        # Wywołanie metody cleanup dla każdego systemu
        for system_id, system_data in self.systems.items():
            if hasattr(system_data['instance'], 'cleanup'):
                system_data['instance'].cleanup()