import pygame

from karma.enums import RessourceType
from karma.resources.ressourceManager import RessourceManager
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH

class HUD:
    def __init__(self) -> None:
        self.fontDay = pygame.font.Font(None, 40)
        self.fontTimer = pygame.font.Font(None, 30)

        self.sunImg = pygame.transform.scale_by(pygame.image.load(ASSETS_DIR / "soleil.png").convert_alpha(), 2)
        self.moonImg = pygame.transform.scale_by(pygame.image.load(ASSETS_DIR / "eclipseTotale.png").convert_alpha(), 2)

        self.fontRessourceKarma = pygame.font.Font(None, 30)
        self.fontRessourceEnergy = pygame.font.Font(None, 30)
        self.fontRessourceRawMaterial = pygame.font.Font(None, 30)

        self.karmaIcon = pygame.image.load(ASSETS_DIR / "hud" / "karma.png").convert_alpha()
        self.energyIcon = pygame.image.load(ASSETS_DIR / "hud" / "energy.png").convert_alpha()
        self.rawMaterialIcon = pygame.image.load(ASSETS_DIR / "hud" / "rawMaterials.png").convert_alpha()

        ship_img = pygame.image.load(ASSETS_DIR / "base" / "day" / "idle_1.png").convert_alpha()
        self.shipIcon = pygame.transform.scale(ship_img, (40, 40))

    def draw(
        self,
        screen: pygame.Surface,
        currentDay: int,
        isDay: bool,
        cycleTimer: float,
        totalDuration: float,
        base_health: int,
        base_max_health: int,
    ) -> None:
        self.DrawCycleIcon(screen, isDay)
        self.DrawCycleTimer(screen, currentDay, isDay, cycleTimer, totalDuration)
        self.DrawRessources(screen)
        self.DrawBaseHealth(screen, base_health, base_max_health)

    def DrawCycleIcon(self, screen: pygame.Surface, isDay: bool) -> None:
        icon = self.sunImg if isDay else self.moonImg
        screen.blit(icon, (20, 20))

    def DrawCycleTimer(
        self,
        screen: pygame.Surface,
        currentDay: int,
        isDay: bool,
        cycleTimer: float,
        totalDuration: float,
    ) -> None:
        """2. Textes Jour et Compteur en bas à droite."""
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

    def DrawRessources(self, screen: pygame.Surface) -> None:
        strRessourceKarma = str(RessourceManager().getStock(RessourceType.Karma))
        strRessourceEnergy = str(RessourceManager().getStock(RessourceType.Energy))
        strRessourceRawMaterial = str(RessourceManager().getStock(RessourceType.RawMaterial))

        karmaSurf = self.fontRessourceKarma.render(strRessourceKarma, False, "white")
        energySurf = self.fontRessourceEnergy.render(strRessourceEnergy, False, "white")
        rawMaterialSurf = self.fontRessourceRawMaterial.render(strRessourceRawMaterial, False, "white")

        karmaIconRect = self.karmaIcon.get_rect(topright=(SCREEN_WIDTH - 25, 20))
        karmaRect = karmaSurf.get_rect(midright=(karmaIconRect.left - 8, karmaIconRect.centery))

        energyIconRect = self.energyIcon.get_rect(topright=(SCREEN_WIDTH - 25, max(karmaIconRect.bottom, karmaRect.bottom) + 8))
        energyRect = energySurf.get_rect(midright=(energyIconRect.left - 8, energyIconRect.centery))

        rawMaterialIconRect = self.rawMaterialIcon.get_rect(topright=(SCREEN_WIDTH - 25, max(energyIconRect.bottom, energyRect.bottom) + 8))
        rawMaterialRect = rawMaterialSurf.get_rect(midright=(rawMaterialIconRect.left - 8, rawMaterialIconRect.centery))

        screen.blit(karmaSurf, karmaRect)
        screen.blit(self.karmaIcon, karmaIconRect)

        screen.blit(energySurf, energyRect)
        screen.blit(self.energyIcon, energyIconRect)

        screen.blit(rawMaterialSurf, rawMaterialRect)
        screen.blit(self.rawMaterialIcon, rawMaterialIconRect)

    def DrawBaseHealth(self, screen: pygame.Surface, health: int, max_health: int) -> None:
        width, height = 220, 25
        ratio = max(0.0, min(1.0, health / max_health)) if max_health > 0 else 0.0

        x = 25
        y_center = SCREEN_HEIGHT - 35

        screen.blit(self.shipIcon, (x, y_center - 20))

        bar_x = x + 50
        bar_y = y_center - height // 2

        # Fond rouge (dégâts) + jauge verte (vie actuelle) + bordure blanche
        pygame.draw.rect(screen, (100, 20, 20), (bar_x, bar_y, width, height))
        pygame.draw.rect(screen, (35, 180, 50), (bar_x, bar_y, int(width * ratio), height))
        pygame.draw.rect(screen, "white", (bar_x, bar_y, width, height), 2)

        text = self.fontTimer.render(f"Vaisseau : {health}/{max_health}", False, "white")
        text_rect = text.get_rect(center=(bar_x + width // 2, bar_y + height // 2))
        screen.blit(text, text_rect)