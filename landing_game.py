# -*- coding: utf-8 -*-
# Listing_24-1.py
# Copyright Warren Sande, 2009
# Released under MIT license   http://www.opensource.org/licenses/mit-license.php
# Version 61  ----------------------------

# (Modifiziert von Tim Poerschke, zur Modularisierung)

########################################################################################
#
# direkt so aus dem Netz uebernommen
#
# Author: siehe oben
#
# Ziel soll es sein, fuer die Steuerung Fuzzyregeln zu entwerfen und zu implementieren
#
########################################################################################

import pygame

class GameState:
    def __init__(self):
        self.hoehe = 2000
        self.fuel = 5000.0
        self.velocity = -100.0
        self.game_ended = False
        self.success = False

# der Gashebel
class GashebelKlasse(pygame.sprite.Sprite):
    def __init__(self, ort = [0,0]):
        pygame.sprite.Sprite.__init__(self)  # ruft Sprite-Initialisierer auf
        image_surface = pygame.surface.Surface([30, 10])
        image_surface.fill([128,128,128])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = ort

class LandingGame:
    raumschiff = pygame.image.load('raumschiff.png')
    mond = pygame.image.load('mondoberflaeche.png')
    boden = 540   # Landeplatz ist auf y = 540
    start = 90
    gravitaet = 10
    raumschiff_masse = 5000.0
   
    def __init__(self):
        self.game_state = GameState()
        self.reset_globals()

    def reset_globals(self):
        self.uhr = pygame.time.Clock()
        self.screen = None
        self.meinGashebel = None
        self.schub = 0
        self.delta_v = 0
        self.y_pos = 90
        self.fps = 30
        self.meinGashebel_ypos = 500
        self.game_state.hoehe = 2000
        self.game_state.fuel = 5000.0
        self.game_state.velocity = -100.0
        self.game_state.game_ended = False
        self.game_state.success = False

    # berechnet Position, Bewegung, Beschleunigung, Treibstoff
    def berechne_geschwindigkeit(self):
        delta_t = 1 / self.fps
        self.schub = (500 - self.meinGashebel_ypos) * 5.0   # Position des Gashebels in Schub umwandeln                                                  
        self.game_state.fuel -= self.schub /(10 * self.fps) # Treibstoff verbrauchen
        if self.game_state.fuel < 0: 
            self.game_state.fuel = 0.0
        if self.game_state.fuel < 0.1:  
            self.schub = 0.0
        self.delta_v = delta_t * (-self.gravitaet + 200 * self.schub / (self.raumschiff_masse + self.game_state.fuel))
        self.game_state.velocity = self.game_state.velocity + self.delta_v
        delta_h = self.game_state.velocity * delta_t
        self.game_state.hoehe = self.game_state.hoehe + delta_h
        self.y_pos = self.boden - (self.game_state.hoehe * (self.boden - self.start) / 2000) - 90

    # gib den aktuellen Status als Text aus 
    def gib_statistik_aus(self):
        v_str = "Geschwindigkeit: %i m/s" % self.game_state.velocity
        h_str = "Höhe:   %.1f" % self.game_state.hoehe
        t_str = "Schub:   %i" % self.schub
        a_str = "Beschleunigung: %.1f" % (self.delta_v * self.fps)
        f_str = "Treibstoff:  %i" % self.game_state.fuel  
        v_font = pygame.font.Font(None, 26)
        v_surf = v_font.render(v_str, 1, (255, 255, 255))
        self.screen.blit(v_surf, [10, 50])
        a_font = pygame.font.Font(None, 26)
        a_surf = a_font.render(a_str, 1, (255, 255, 255))
        self.screen.blit(a_surf, [10, 100])
        h_font = pygame.font.Font(None, 26)
        h_surf = h_font.render(h_str, 1, (255, 255, 255))
        self.screen.blit(h_surf, [10, 150])
        t_font = pygame.font.Font(None, 26)
        t_surf = t_font.render(t_str, 1, (255, 255, 255))
        self.screen.blit(t_surf, [10, 200])  
        f_font = pygame.font.Font(None, 26)
        f_surf = f_font.render(f_str, 1, (255, 255, 255))
        self.screen.blit(f_surf, [60, 300])

    # Die Flammen des Raumschiffs zeigen. Deren Größe ist abhaengig vom Schub.   
    def zeige_flammen(self):
        flammen_groesse = self.schub / 15
        for i in range(2):
            startx = 252 - 10 + i * 19
            starty = self.y_pos + 83
            pygame.draw.polygon(self.screen, [255, 109, 14], [(startx, starty), 
                                    (startx + 4, starty + flammen_groesse), 
                                    (startx + 8, starty)], 0)

    # Endstand ausgeben wenn das Spiel vorbei ist
    def gib_endstand_aus(self, draw: bool):
        final1 = "Spiel vorbei!"
        final2 = "Geschwindigkeit war %.1f m/s" % self.game_state.velocity
        if self.game_state.fuel == 0:
            final3 = "Tank leer!"
            final4 = "Ohne Treibstoff geht nichts mehr."
            self.game_state.success = False
        elif self.game_state.velocity > -5:
            final3 = "Gute Landung!"
            final4 = "Die NASA braucht noch Astronauten!"
            self.game_state.success = True
        elif self.game_state.velocity > -15:
            final3 = "Aua!  Etwas rau, aber du hast überlebt."
            final4 = "Nächstes Mal machst du es besser."
            self.game_state.success = True
        else:
            final3 = "Eijei! Das 30-Milliarden-Euro-Schiff ist kaputt!"
            final4 = "Wie kommst du jetzt nach Hause?"
            self.game_state.success = False
        self.game_state.game_ended = True

        if draw:
            pygame.draw.rect(self.screen, [0, 0, 0], [5, 5, 350, 280],0)  
            f1_font = pygame.font.Font(None, 60)
            f1_surf = f1_font.render(final1, 1, (255, 255, 255))
            self.screen.blit(f1_surf, [20, 50])   
            f2_font = pygame.font.Font(None, 30)
            f2_surf = f2_font.render(final2, 1, (255, 255, 255))
            self.screen.blit(f2_surf, [20, 110]) 
            f3_font = pygame.font.Font(None, 24)
            f3_surf = f3_font.render(final3, 1, (255, 255, 255))
            self.screen.blit(f3_surf, [20, 150]) 
            f4_font = pygame.font.Font(None, 24)
            f4_surf = f4_font.render(final4, 1, (255, 255, 255))
            self.screen.blit(f4_surf, [20, 180]) 
            pygame.display.flip()

    # Setzt den Gashebel in die prozentuale Position
    def set_lever(self, gas_percent: float) -> None:
        self.meinGashebel_ypos = 500 - 200 * gas_percent
        if self.meinGashebel:
            self.meinGashebel.rect.centery = self.meinGashebel_ypos
            if self.meinGashebel.rect.centery < 300:
                self.meinGashebel.rect.centery = 300
            if self.meinGashebel.rect.centery > 500:
                self.meinGashebel.rect.centery = 500

    def init(self, draw=True):
        pygame.init()
        self.screen = pygame.display.set_mode([400,600])
        self.screen.fill([0, 0, 0])
        self.meinGashebel = GashebelKlasse([15, 500])

    def game_tick(self, draw=True):
        self.fps = self.uhr.get_fps()
        if self.fps < 1: self.fps = 30
        if self.game_state.hoehe > 0.01 and self.game_state.fuel > 0:
            self.game_state.game_ended = False
            self.berechne_geschwindigkeit()
            if draw:
                self.screen.fill([0, 0, 0])
                self.gib_statistik_aus()
                pygame.draw.rect(self.screen, [0, 0, 255], [80, 350, 24, 100], 2)
                treibstoffhebel = 96 * self.game_state.fuel / 5000 
                pygame.draw.rect(self.screen, [0,255,0], [84,448-treibstoffhebel,18, treibstoffhebel], 0) 
                pygame.draw.rect(self.screen, [255, 0, 0], [25, 300, 10, 200],0)  # Gashebel-Slider
                self.screen.blit(self.mond, [0, 500, 400, 100])                   # Mond
                pygame.draw.rect(self.screen, [60, 60, 60], [220, 535, 70, 5],0)  # Landeplatz
                self.screen.blit(self.meinGashebel.image, self.meinGashebel.rect) # Schubgriff
                self.zeige_flammen()                                              # Flammen
                self.screen.blit(self.raumschiff, [230, self.y_pos, 50, 90])      # Raumschiff
                anweisung1 = "Lande weich, ohne dass der Treibstoff ausgeht!"
                anweisung2 = "Gute Landung: < 15m/s   Tolle Landung: < 5m/s"
                anweisung1_font = pygame.font.Font(None, 24)
                anweisung1_surf = anweisung1_font.render(anweisung1, 1, (255, 255, 255))
                self.screen.blit(anweisung1_surf, [20, 550])
                anweisung2_font = pygame.font.Font(None, 24)
                anweisung2_surf = anweisung1_font.render(anweisung2, 1, (255, 255, 255))
                self.screen.blit(anweisung2_surf, [20, 575])
                pygame.display.flip()  
        
        else:  # Spiel vorbei, gib den Endstand aus
            self.gib_endstand_aus(draw)