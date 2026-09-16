# Bâtiments et score

## Ressources

Au début : Karma = 0, Énergie = 100, Matière première = 500.

La Matière première n'a pas de bâtiment producteur : c'est une réserve fixe pour toute la partie, à dépenser avec soin.

Le Karma va de -1000 à +1000. Chaque bâtiment "propre" donne +100 karma/minute tant qu'il est actif, chaque bâtiment "sale" retire 100 karma/minute — ce taux est le même pour tous les bâtiments propres/sales (valeur fixée dans le code, pas ajustable par bâtiment). Le vrai choix se joue sur le coût et la production, pas sur le karma lui-même.

## Producteurs d'énergie (tier 1, dispo dès le début)

| **Bâtiment** | **Coût (Énergie)** | **Point de vie** | **Karma** | **Énergie / seconde** |
| --- | --- | --- | --- | --- |
| Panneau solaire | 80 | 250 | +100/min | 15 |
| Centrale à charbon | 150 | 600 | -100/min | 35 |

Avec seulement 100 énergie au départ, la centrale à charbon n'est pas finançable au tour 1 : on commence forcément propre, et la tentation du charbon n'arrive qu'une fois qu'on a économisé. Le charbon est strictement meilleur en jeu (2,3x la production, PV largement supérieurs) pour le même coût en karma — tout le prix est moral, pas mécanique.

## Transformateurs (tier 2, Matière première → Énergie)

| **Bâtiment** | **Coût (Énergie)** | **Point de vie** | **Karma** | **Matière première / cycle** | **Énergie / cycle** | **Cadence** | **Efficacité** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Transformateur lent | 250 | 400 | +100/min | 20 | 150 | 4000 ms | 7,5 énergie/matière |
| Transformateur rapide | 300 | 500 | -100/min | 20 | 220 | 2000 ms | 11 énergie/matière |

Le transformateur rapide tire 47% d'énergie en plus de la même réserve finie de matière première, et deux fois plus vite. Même logique de tentation que les producteurs, mais au moment où les réserves commencent à manquer.

## Défenses

| **Bâtiment** | **Coût (Énergie)** | **Point de vie** | **Dégâts / tir** | **Cadence** | **Portée** |
| --- | --- | --- | --- | --- | --- |
| Mur | 40 | 800 | — | — | — |
| Tourelle | 200 | 350 | 90 | 700 ms | 150 px |

Tourelle ≈ 128,6 DPS. Un mur seul encaisse 2 coups de Blindé, 4 coups de Rôdeur, ou 12 coups de Coureur avant de tomber.

## Base

Point de vie : 1000.

## Ennemis

| **Ennemi** | **Point de vie** | **Dégâts** | **Cadence** | **DPS** | **Vitesse** |
| --- | --- | --- | --- | --- | --- |
| Coureur | 110 | 65 | 700 ms | 92,9 | 34 px/s |
| Rôdeur | 260 | 240 | 900 ms | 266,7 | 24 px/s |
| Blindé | 7000 | 650 | 1200 ms | 541,7 | 15 px/s |

Ratio DPS/vitesse (force relative à la lenteur) : Coureur 2,7 — Rôdeur 11,1 — Blindé 36,1. Plus un ennemi est lent, plus il punit disproportionnellement — ce n'est pas juste une éponge à PV.

Face à une tourelle seule : le Coureur meurt en 0,86 s, le Rôdeur en 2 s, le Blindé survit 54 s et ne peut pas être géré par une seule tourelle — il faut plusieurs défenses en place avant son arrivée.
