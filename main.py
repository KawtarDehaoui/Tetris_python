import pygame
import ftandclass as f

# Initialisation de Pygame
pygame.init()

# Chargement de la musique
pygame.mixer.music.load('Original Tetris theme (Tetris Soundtrack).mp3')  
pygame.mixer.music.play(-1)

# Lancer le jeu
pygame.display.set_caption('Tetris')
f.game_loop()

# Quitter le jeu
pygame.mixer.music.stop()
pygame.quit()
