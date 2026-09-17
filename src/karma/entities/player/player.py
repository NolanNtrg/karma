import pygame
from karma.settings import ASSETS_DIR

from typing import Any

from karma.entities.entity import Entity
from karma.entities.bullet import Bullet
from karma.entities.enemies.enemy import Enemy
from karma.entities.shooter import Shooter
from karma.entities.sprite import SpriteAnimator
from karma.environment.camera import Camera


class Player(Entity):
    instance = None

    # constantes pour le tir du joueur
    ATTACK_DAMAGE = 40
    ATTACK_INTERVAL = 300.0  # ms entre deux tirs
    BULLET_SPEED = 0.5  # pixels par ms

    BULLET_SIZE = (16, 16)
    MUZZLE_FLASH_DURATION = 100.0  # ms d'affichage de la case muzzle flash
    MUZZLE_FLASH_FRAME = (3, 0)  # case du tileset astronaute représentant le tir

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "Player":
        # Si l'instance n'existe pas encore, on la crée
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    # Constructeur
    def __init__(self, name: str, position: pygame.Vector2, speed: float, health: int = 100) -> None:
        if self._initialized :
            return
        self.instance = super().__init__(position, health)
        self.name: str = name
        self.speed: float = speed

        self.animator = SpriteAnimator(
            ASSETS_DIR / "Soldiers" / "MachineGunner-Class.png",
            idleFrameCoords=[(0, 0), (0, 1)],
            walkFrameCoords=[(1, 0), (1, 1)],
        )

        # initialisation des variables pour le tir
        self.timeSinceLastAttack: float = self.ATTACK_INTERVAL  # prêt à tirer dès le début
        self.muzzleFlashTimer: float = 0.0
        self.muzzleFlashImage = SpriteAnimator.getSprite(self.animator.spriteSheet, *self.MUZZLE_FLASH_FRAME)

        self.shooter = Shooter(Bullet.loadImage(self.BULLET_SIZE))
        self._initialized = True


    def getDirection(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        dx: float = (keys[pygame.K_d] - keys[pygame.K_q])
        dy: float = (keys[pygame.K_s] - keys[pygame.K_z])
        direction: pygame.Vector2 = pygame.Vector2(dx, dy)

        if direction.length_squared() == 0:
            return direction

        return direction.normalize()

    def update(
        self,
        dt: float,
        enemies: list[Enemy] | None = None,
        camera: Camera | None = None,
        map_size: tuple[float, float] | None = None,
    ) -> None:
        direction = self.getDirection()
        self.position += direction * self.speed * dt
        if map_size is not None:
            # on retire la taille du sprite de la borne max pour garder le sprite entier dans la carte
            # (position est le coin haut-gauche, donc sans ça le bord droit/bas pourrait dépasser)
            sprite_width, sprite_height = self.animator.image.get_size()
            max_x = max(0.0, map_size[0] - sprite_width)
            max_y = max(0.0, map_size[1] - sprite_height)
            self.position.x = max(0.0, min(self.position.x, max_x))
            self.position.y = max(0.0, min(self.position.y, max_y))
        self.animator.update(dt, direction.length_squared() > 0, direction)

        self.timeSinceLastAttack += dt
        self.shooter.updateBullets(dt, enemies or [], camera)

        self.muzzleFlashTimer = max(0.0, self.muzzleFlashTimer - dt)

    def shoot(self, targetPosition: pygame.Vector2) -> None:
        # Déclenché au clic, avec un délai de recharge entre deux tirs.
        if self.timeSinceLastAttack < self.ATTACK_INTERVAL:
            return

        direction = targetPosition - self.getCenter()
        if direction.length_squared() == 0:
            return

        self.timeSinceLastAttack = 0.0
        self.animator.flip = direction.x < 0
        self.shooter.spawnBullet(self.getCenter(), direction, self.ATTACK_DAMAGE, self.BULLET_SPEED)
        self.muzzleFlashTimer = self.MUZZLE_FLASH_DURATION

    def getCenter(self) -> pygame.Vector2:
        return self.position + pygame.Vector2(self.animator.image.get_size()) / 2

    def draw(self, screen: pygame.Surface, camera: Camera | None = None) -> None:
        position = camera.apply(self.position) if camera else self.position
        # affiche le muzzle flash si le joueur vient de tirer, sinon affiche l'image normale
        isFiring = self.muzzleFlashTimer > 0
        image = pygame.transform.flip(self.muzzleFlashImage, self.animator.flip, False) if isFiring else self.animator.image
        screen.blit(image, position)

        self.shooter.drawBullets(screen, camera)
