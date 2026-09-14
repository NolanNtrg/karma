# Example file showing a circle moving on screen
import pygame

# Programme principal du jeux
def main():
    # Démmarre le module 
    pygame.init()
    # définit l'écran et sa taille, retourne la surface pour le dessin
    screen = pygame.display.set_mode((1280, 720))
    # Définit l'horloge pour connaitre le temps qui a passé
    clock = pygame.time.Clock()
    # Pour savoir quand la boucle du jeu se termine
    running = True
    # Le temps passé entre deux rafraichissement de l'écran en millisecondes
    dt = 0
    # La position du joueur : au milieu de l'écran
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    # Boucle de l'animation
    while running:
        # Limite le frame rate à 60 images par secondes et retourne le temps réel passé
        dt = clock.tick(60) 
        # Parcourt tous les évenements pour les traiter
        for event in pygame.event.get():
            # QUIT signifie que l'utilisateur a fermé la fenêtre
            if event.type == pygame.QUIT:
                running = False
        # Efface l'écran précédent en remplissant l'écran 
        screen.fill("green")
        # Examine les touches pressées, possiblement plusieurs
        keys = pygame.key.get_pressed()
        # Action de modification pour chaque touche
        if keys[pygame.K_s]:
            player_pos.x -= 0.3 * dt
        if keys[pygame.K_d]:
            player_pos.x += 0.3 * dt
        if keys[pygame.K_a]:
            player_pos.y -= 0.3 * dt
        if keys[pygame.K_q]:
            player_pos.y += 0.3 * dt
        # Dessin d'un cercle à la position du joueur
        pygame.draw.circle(screen, "red", player_pos, 40)
        # Comme les dessins sont fait dans un buffer, permute le buffer
        pygame.display.flip()

    # Termine proprement le module
    pygame.quit()

# Appel au programme principal
main()