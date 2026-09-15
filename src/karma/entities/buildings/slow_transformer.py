import pygame

from karma.entities.buildings.transformer import Transformer


class SlowTransformer(Transformer):
    # Transformateur lent qui augmente le karma quand actif

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        rawMaterialCost: int,
        energyOutput: int,
        transformInterval: float,
    ) -> None:
        super().__init__(
            position, health, energyCost, 100.0, rawMaterialCost, energyOutput, transformInterval
        )
