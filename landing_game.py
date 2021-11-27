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
screen = None
raumschiff = pygame.image.load('raumschiff.png')
mond = pygame.image.load('mondoberflaeche.png')
uhr = pygame.time.Clock()
meinGashebel = None
boden = 540   # Landeplatz ist auf y = 540
start = 90
gravitaet = 10
raumschiff_masse = 5000.0
# Diese Globals werden verändert, wenn das Spiel läuft
geschwindigkeit = -100.0
schub = 0
delta_v = 0
y_pos = 90
fps = 30
meinGashebel_ypos = 500

class GameState:
    def __init__(self):
        self.hoehe = 2000
        self.fuel = 5000.0
        self.velocity = -100.0
        self.game_ended = False
        self.success = False

game_state = GameState()

def reset_globals():
    global geschwindigkeit, schub, delta_v, y_pos, fps, meinGashebel_ypos, game_state
    geschwindigkeit = -100.0
    schub = 0
    delta_v = 0
    y_pos = 90
    fps = 30
    meinGashebel_ypos = 500
    game_state.hoehe = 2000
    game_state.fuel = 5000.0
    game_state.velocity = -100.0
    game_state.game_ended = False
    game_state.success = False


# der Gashebel
class GashebelKlasse(pygame.sprite.Sprite):
    def __init__(self, ort = [0,0]):
        pygame.sprite.Sprite.__init__(self)  # ruft Sprite-Initialisierer auf
        image_surface = pygame.surface.Surface([30, 10])
        image_surface.fill([128,128,128])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = ort

# berechnet Position, Bewegung, Beschleunigung, Treibstoff
def berechne_geschwindigkeit():
    global schub, geschwindigkeit, delta_v, y_pos
    delta_t = 1/fps
    schub = (500 - meinGashebel_ypos) * 5.0  # Position des Gashebels in Schub umwandeln                                                  
    game_state.fuel -= schub /(10 * fps)              # Treibstoff verbrauchen
    if game_state.fuel < 0:  game_state.fuel = 0.0
    if game_state.fuel < 0.1:  schub = 0.0
    delta_v = delta_t * (-gravitaet + 200 * schub / (raumschiff_masse + game_state.fuel))
    geschwindigkeit = geschwindigkeit + delta_v
    game_state.velocity = geschwindigkeit
    delta_h = geschwindigkeit * delta_t
    game_state.hoehe = game_state.hoehe + delta_h
    y_pos = boden - (game_state.hoehe * (boden - start) / 2000) - 90

# gib den aktuellen Status als Text aus 
def gib_statistik_aus():
    v_str = "Geschwindigkeit: %i m/s" % geschwindigkeit
    h_str = "Höhe:   %.1f" % game_state.hoehe
    t_str = "Schub:   %i" % schub
    a_str = "Beschleunigung: %.1f" % (delta_v * fps)
    f_str = "Treibstoff:  %i" % game_state.fuel  
    v_font = pygame.font.Font(None, 26)
    v_surf = v_font.render(v_str, 1, (255, 255, 255))
    screen.blit(v_surf, [10, 50])
    a_font = pygame.font.Font(None, 26)
    a_surf = a_font.render(a_str, 1, (255, 255, 255))
    screen.blit(a_surf, [10, 100])
    h_font = pygame.font.Font(None, 26)
    h_surf = h_font.render(h_str, 1, (255, 255, 255))
    screen.blit(h_surf, [10, 150])
    t_font = pygame.font.Font(None, 26)
    t_surf = t_font.render(t_str, 1, (255, 255, 255))
    screen.blit(t_surf, [10, 200])  
    f_font = pygame.font.Font(None, 26)
    f_surf = f_font.render(f_str, 1, (255, 255, 255))
    screen.blit(f_surf, [60, 300])

# Die Flammen des Raumschiffs zeigen. Deren Größe ist abhaengig vom Schub.   
def zeige_flammen():
    flammen_groesse = schub / 15
    for i in range (2):
        startx = 252 - 10 + i * 19
        starty = y_pos + 83
        pygame.draw.polygon(screen, [255, 109, 14], [(startx, starty), 
                                 (startx + 4, starty + flammen_groesse), 
                                 (startx + 8, starty)], 0)

# Endstand ausgeben wenn das Spiel vorbei ist
def gib_endstand_aus(draw: bool):
    final1 = "Spiel vorbei!"
    final2 = "Geschwindigkeit war %.1f m/s" % geschwindigkeit
    if game_state.fuel == 0:
        final3 = "Tank leer!"
        final4 = "Ohne Treibstoff geht nichts mehr."
        game_state.success = False
    elif geschwindigkeit > -5:
        final3 = "Gute Landung!"
        final4 = "Die NASA braucht noch Astronauten!"
        game_state.success = True
    elif geschwindigkeit > -15:
        final3 = "Aua!  Etwas rau, aber du hast überlebt."
        final4 = "Nächstes Mal machst du es besser."
        game_state.success = True
    else:
        final3 = "Eijei! Das 30-Milliarden-Euro-Schiff ist kaputt!"
        final4 = "Wie kommst du jetzt nach Hause?"
        game_state.success = False
    game_state.game_ended = True
    if draw:
        pygame.draw.rect(screen, [0, 0, 0], [5, 5, 350, 280],0)  
        f1_font = pygame.font.Font(None, 60)
        f1_surf = f1_font.render(final1, 1, (255, 255, 255))
        screen.blit(f1_surf, [20, 50])   
        f2_font = pygame.font.Font(None, 30)
        f2_surf = f2_font.render(final2, 1, (255, 255, 255))
        screen.blit(f2_surf, [20, 110]) 
        f3_font = pygame.font.Font(None, 24)
        f3_surf = f3_font.render(final3, 1, (255, 255, 255))
        screen.blit(f3_surf, [20, 150]) 
        f4_font = pygame.font.Font(None, 24)
        f4_surf = f4_font.render(final4, 1, (255, 255, 255))
        screen.blit(f4_surf, [20, 180]) 
        pygame.display.flip()

# Setzt den Gashebel in die prozentuale Position
def set_lever(gas_percent: float) -> None:
    global meinGashebel_ypos
    meinGashebel_ypos = 500 - 200 * gas_percent
    if meinGashebel:
        meinGashebel.rect.centery = meinGashebel_ypos
        if meinGashebel.rect.centery < 300:
            meinGashebel.rect.centery = 300
        if meinGashebel.rect.centery > 500:
            meinGashebel.rect.centery = 500

def init(draw=True):
    global screen, meinGashebel
    pygame.init()
    screen = pygame.display.set_mode([400,600])
    screen.fill([0, 0, 0])
    meinGashebel = GashebelKlasse([15, 500])

def game_tick(draw=True):
    global fps
    fps = uhr.get_fps()
    if fps < 1: fps = 30
    if game_state.hoehe > 0.01 and game_state.fuel > 0:
        game_state.game_ended = False
        berechne_geschwindigkeit()
        if draw:
            screen.fill([0, 0, 0])
            gib_statistik_aus()
            pygame.draw.rect(screen, [0, 0, 255], [80, 350, 24, 100], 2)
            treibstoffhebel = 96 * game_state.fuel / 5000 
            pygame.draw.rect(screen, [0,255,0], [84,448-treibstoffhebel,18, treibstoffhebel], 0) 
            pygame.draw.rect(screen, [255, 0, 0], [25, 300, 10, 200],0)  # Gashebel-Slider
            screen.blit(mond, [0, 500, 400, 100])                        # Mond
            pygame.draw.rect(screen, [60, 60, 60], [220, 535, 70, 5],0)  # Landeplatz
            screen.blit(meinGashebel.image, meinGashebel.rect)           # Schubgriff
            zeige_flammen()                                              # Flammen
            screen.blit(raumschiff, [230, y_pos, 50, 90])                # Raumschiff
            anweisung1 = "Lande weich, ohne dass der Treibstoff ausgeht!"
            anweisung2 = "Gute Landung: < 15m/s   Tolle Landung: < 5m/s"
            anweisung1_font = pygame.font.Font(None, 24)
            anweisung1_surf = anweisung1_font.render(anweisung1, 1, (255, 255, 255))
            screen.blit(anweisung1_surf, [20, 550])
            anweisung2_font = pygame.font.Font(None, 24)
            anweisung2_surf = anweisung1_font.render(anweisung2, 1, (255, 255, 255))
            screen.blit(anweisung2_surf, [20, 575])
            pygame.display.flip()  
    
    else:  # Spiel vorbei, gib den Endstand aus
        gib_endstand_aus(draw)