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

    def draw(self,screen: pygame.Surface,currentDay: int,isDay: bool,cycleTimer: float,totalDuration: float,resourceManager: RessourceManager) -> None:
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

        # 3. Textes ressources en haut à droite

        strRessourceKarma = str(int(round(resourceManager.getStock(RessourceType.Karma))))
        strRessourceEnergy = str(int(resourceManager.getStock(RessourceType.Energy)))
        strRessourceRawMaterial = str(int(resourceManager.getStock(RessourceType.RawMaterial)))

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