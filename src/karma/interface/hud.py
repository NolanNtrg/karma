import pygame
from karma.enums import RessourceType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from karma.resources.ressourceManager import RessourceManager

class HUD:
    def __init__(self) -> None:
        self.fontDay = pygame.font.Font(None, 40)
        self.fontTimer = pygame.font.Font(None, 30)

        # Icônes Soleil / Lune
        self.sunImg = pygame.transform.scale_by(pygame.image.load(ASSETS_DIR / "soleil.png").convert_alpha(), 2)
        self.moonImg = pygame.transform.scale_by(pygame.image.load(ASSETS_DIR / "eclipseTotale.png").convert_alpha(), 2)

        self.fontRessourceKarma = pygame.font.Font(None, 30)
        self.fontRessourceEnergy = pygame.font.Font(None, 30)
        self.fontRessourceRawMaterial = pygame.font.Font(None, 30)

        self.karmaIcon = pygame.image.load(ASSETS_DIR / "hud" / "karma.png").convert_alpha()
        self.energyIcon = pygame.image.load(ASSETS_DIR / "hud" / "energy.png").convert_alpha()
        self.rawMaterialIcon = pygame.image.load(ASSETS_DIR / "hud" / "rawMaterials.png").convert_alpha()

    def draw(self,screen: pygame.Surface,currentDay: int,isDay: bool,cycleTimer: float,totalDuration: float) -> None:
        # 1. Icône Jour / Nuit en haut à gauche
        icon = self.sunImg if isDay else self.moonImg
        screen.blit(icon, (20, 20))

        # 2. Textes Jour et Compteur en bas à droite
        remainingMs = max(0.0, totalDuration - cycleTimer)
        remainingSeconds = int(remainingMs // 1000)
        mins = remainingSeconds // 60
        secs = remainingSeconds % 60
        timeText = f"{mins:02d}:{secs:02d}"

        dayStr = f"Day {currentDay}"
        phaseStr = f"{timeText} remaining • Day" if isDay else f"{timeText} remaining • Night"

        daySurf = self.fontDay.render(dayStr, False, "white")
        timerSurf = self.fontTimer.render(phaseStr, False, "white")

        timerRect = timerSurf.get_rect(bottomright=(SCREEN_WIDTH - 25, SCREEN_HEIGHT - 20))
        dayRect = daySurf.get_rect(bottomright=(SCREEN_WIDTH - 25, timerRect.top - 5))

        screen.blit(daySurf, dayRect)
        screen.blit(timerSurf, timerRect)

        # 3. Badges ressources en haut à droite
        resources = [
            (self.karmaIcon, str(RessourceManager().getStock(RessourceType.Karma)), self.fontRessourceKarma),
            (self.energyIcon, str(RessourceManager().getStock(RessourceType.Energy)), self.fontRessourceEnergy),
            (self.rawMaterialIcon, str(RessourceManager().getStock(RessourceType.RawMaterial)), self.fontRessourceRawMaterial),
        ]

        rendered_resources = []
        max_text_width = 0
        for icon, val_str, font in resources:
            text_surf = font.render(val_str, False, "white")
            max_text_width = max(max_text_width, text_surf.get_width())
            rendered_resources.append((icon, text_surf))

        badge_height = 38
        badge_width = max(130, max_text_width + 32 + 30)
        border_radius = badge_height // 2

        # Surface semi-transparente pour le fond noir
        bg_surf = pygame.Surface((badge_width, badge_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 0, 0, 160), bg_surf.get_rect(), border_radius=border_radius)
        pygame.draw.rect(bg_surf, (255, 255, 255, 35), bg_surf.get_rect(), width=1, border_radius=border_radius)

        top_y = 20
        for icon, text_surf in rendered_resources:
            badge_rect = pygame.Rect(0, 0, badge_width, badge_height)
            badge_rect.topright = (SCREEN_WIDTH - 20, top_y)

            # Fond noir transparent
            screen.blit(bg_surf, badge_rect)

            # Icône à droite
            icon_rect = icon.get_rect(midright=(badge_rect.right - 4, badge_rect.centery))
            screen.blit(icon, icon_rect)

            # Texte
            text_rect = text_surf.get_rect(midright=(icon_rect.left - 8, badge_rect.centery))
            screen.blit(text_surf, text_rect)

            top_y += badge_height + 8
