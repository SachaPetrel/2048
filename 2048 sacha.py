import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
LARGEUR, HAUTEUR = 400, 400
TAILLE_GRILLE = 4
TAILLE_CELLULE = LARGEUR // TAILLE_GRILLE

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)

# Palette de couleurs pour chaque chiffre
COULEURS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Initialisation de la grille
grille = [[0] * TAILLE_GRILLE for _ in range(TAILLE_GRILLE)]

# Score initial
score = 0

# Nouvelle variable pour gérer l'état de pause
en_pause = False

# Ajouter deux cases 2 ou 4 au début du jeu
def ajouter_case():
    cellules_vides = [(i, j) for i in range(TAILLE_GRILLE) for j in range(TAILLE_GRILLE) if grille[i][j] == 0]
    if cellules_vides:
        i, j = random.choice(cellules_vides)
        grille[i][j] = random.choice([2, 4])

# Fonction pour animer le déplacement d'une case vers une nouvelle position
def animer_deplacement(x_debut, y_debut, x_fin, y_fin):
    vitesse_animation = 1000  # Ajustez la vitesse d'animation selon votre préférence
    delta_x = (x_fin - x_debut) / vitesse_animation
    delta_y = (y_fin - y_debut) / vitesse_animation

    for _ in range(vitesse_animation):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()
            pygame.time.delay(10)
            x_debut += delta_x
            y_debut += delta_y
            afficher_grille(écran, x_debut, y_debut)

# Fonction pour afficher la grille avec l'animation du déplacement
def afficher_grille(écran, x_debut=0, y_debut=0):
    écran.fill(BLANC)
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            pygame.draw.rect(écran, GRIS, (j * TAILLE_CELLULE, i * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE), 2)
            valeur = grille[i][j]
            couleur = COULEURS.get(valeur, (255, 255, 255))
            pygame.draw.rect(écran, couleur, (j * TAILLE_CELLULE + 3 + x_debut, i * TAILLE_CELLULE + 3 + y_debut, TAILLE_CELLULE - 6, TAILLE_CELLULE - 6))
            if valeur != 0:
                police = pygame.font.Font(None, 36)
                texte = police.render(str(valeur), True, NOIR)
                rect_texte = texte.get_rect(center=(j * TAILLE_CELLULE + TAILLE_CELLULE / 2 + x_debut, i * TAILLE_CELLULE + TAILLE_CELLULE / 2 + y_debut))
                écran.blit(texte, rect_texte)

    # Affichage du score en bas
    police = pygame.font.Font(None, 36)
    texte_score = police.render(f"Score : {score}", True, NOIR)
    écran.blit(texte_score, (10, HAUTEUR - 40))

# Fonction pour déplacer les cases avec animation
def déplacer_cases_animation(direction):
    global score
    for _ in range(TAILLE_GRILLE):  # Répéter le déplacement pour chaque ligne ou colonne
        for i in range(TAILLE_GRILLE):
            if direction == 'gauche':
                ligne = [cellule for cellule in grille[i] if cellule != 0]
                ligne += [0] * (TAILLE_GRILLE - len(ligne))
                for j in range(TAILLE_GRILLE - 1):
                    if ligne[j] == ligne[j + 1]:
                        ligne[j], ligne[j + 1] = 2 * ligne[j], 0
                        score += ligne[j]
                        animer_deplacement(j * TAILLE_CELLULE, i * TAILLE_CELLULE, (j + 1) * TAILLE_CELLULE, i * TAILLE_CELLULE)
                ligne = [cellule for cellule in ligne if cellule != 0]
                ligne += [0] * (TAILLE_GRILLE - len(ligne))
                grille[i] = ligne
            elif direction == 'droite':
                ligne = [cellule for cellule in grille[i] if cellule != 0]
                ligne = [0] * (TAILLE_GRILLE - len(ligne)) + ligne
                for j in range(TAILLE_GRILLE - 1, 0, -1):
                    if ligne[j] == ligne[j - 1]:
                        ligne[j], ligne[j - 1] = 2 * ligne[j], 0
                        score += ligne[j]
                        animer_deplacement(j * TAILLE_CELLULE, i * TAILLE_CELLULE, (j - 1) * TAILLE_CELLULE, i * TAILLE_CELLULE)
                ligne = [cellule for cellule in ligne if cellule != 0]
                ligne = [0] * (TAILLE_GRILLE - len(ligne)) + ligne
                grille[i] = ligne
            elif direction == 'haut':
                colonne = [grille[j][i] for j in range(TAILLE_GRILLE) if grille[j][i] != 0]
                colonne += [0] * (TAILLE_GRILLE - len(colonne))
                for j in range(TAILLE_GRILLE - 1):
                    if colonne[j] == colonne[j + 1]:
                        colonne[j], colonne[j + 1] = 2 * colonne[j], 0
                        score += colonne[j]
                        animer_deplacement(i * TAILLE_CELLULE, j * TAILLE_CELLULE, i * TAILLE_CELLULE, (j + 1) * TAILLE_CELLULE)
                colonne = [cellule for cellule in colonne if cellule != 0]
                colonne += [0] * (TAILLE_GRILLE - len(colonne))
                for j in range(TAILLE_GRILLE):
                    grille[j][i] = colonne[j]
            elif direction == 'bas':
                colonne = [grille[j][i] for j in range(TAILLE_GRILLE) if grille[j][i] != 0]
                colonne = [0] * (TAILLE_GRILLE - len(colonne)) + colonne
                for j in range(TAILLE_GRILLE - 1, 0, -1):
                    if colonne[j] == colonne[j - 1]:
                        colonne[j], colonne[j - 1] = 2 * colonne[j], 0
                        score += colonne[j]
                        animer_deplacement(i * TAILLE_CELLULE, j * TAILLE_CELLULE, i * TAILLE_CELLULE, (j - 1) * TAILLE_CELLULE)
                colonne = [cellule for cellule in colonne if cellule != 0]
                colonne = [0] * (TAILLE_GRILLE - len(colonne)) + colonne
                for j in range(TAILLE_GRILLE):
                    grille[j][i] = colonne[j]



# Fonction principale
def principal():
    global score, en_pause
    # Initialisation de l'écran
    écran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu 2048")

    # Boucle de jeu
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    déplacer_cases_animation('gauche')
                elif event.key == pygame.K_RIGHT:
                    déplacer_cases_animation('droite')
                elif event.key == pygame.K_UP:
                    déplacer_cases_animation('haut')
                elif event.key == pygame.K_DOWN:
                    déplacer_cases_animation('bas')
                elif event.key == pygame.K_p:  # Touche 'P' pour mettre en pause/reprendre
                    basculer_pause()
                ajouter_case()

        if not en_pause:  # Mettre à jour la grille uniquement si le jeu n'est pas en pause
            # Affichage de la grille
            afficher_grille(écran)

            # Affichage du score
            police = pygame.font.Font(None, 36)
            texte_score = police.render(f"Score : {score}", True, NOIR)
            écran.blit(texte_score, (10, HAUTEUR - 40))

            # Rafraîchissement de l'écran
            pygame.display.flip()

    # Fermeture de Pygame
    pygame.quit()

# Lancement du jeu
if __name__ == "__main__":
    ajouter_case()  # Ajouter les deux premières cases au début
    principal()  # Lancer le jeu




