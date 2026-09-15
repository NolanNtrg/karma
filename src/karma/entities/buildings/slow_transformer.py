import pygame

from karma.entities.buildings.transformer import Transformer


class SlowTransformer(Transformer):
    # Variante propre et lente de la transformation : fait monter le karma tant qu'active

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
            position, health, energyCost, 1.0, rawMaterialCost, energyOutput, transformInterval
        )
